"""repo2docker: convert git repositories into jupyter-suitable docker images

Images produced by repo2docker can be used with Jupyter notebooks standalone
or with BinderHub.

Usage:

    python -m repo2docker https://github.com/you/your-repo
"""
import getpass
import json
import logging
import os
import shutil
import sys
import tempfile
import time
import warnings
from urllib.parse import urlparse

import entrypoints
import escapism
from pythonjsonlogger import jsonlogger
from traitlets import Any, Bool, Dict, Int, List, Unicode, default, observe
from traitlets.config import Application

from . import __version__, contentproviders
from .buildpacks import (
    CondaBuildPack,
    DockerBuildPack,
    JuliaProjectTomlBuildPack,
    JuliaRequireBuildPack,
    LegacyBinderDockerBuildPack,
    NixBuildPack,
    PipfileBuildPack,
    PythonBuildPack,
    RBuildPack,
)
from .engine import BuildError, ContainerEngineException, ImageLoadError
from .utils import ByteSpecification, R2dState, chdir, get_platform


class Repo2Docker(Application):
    """An application for converting git repositories to docker images"""

    name = "jupyter-repo2docker"
    version = __version__
    description = __doc__
    # disable aliases/flags because we don't use the traitlets for CLI parsing
    # other than --Class.trait=value
    aliases = {}
    flags = {}

    @default("log_level")
    def _default_log_level(self):
        """The application's default log level"""
        return logging.INFO

    git_workdir = Unicode(
        None,
        config=True,
        allow_none=True,
        help="""
        Working directory to use for check out of git repositories.

        The default is to use the system's temporary directory. Should be
        somewhere ephemeral, such as /tmp.
        """,
    )

    subdir = Unicode(
        "",
        config=True,
        help="""
        Subdirectory of the git repository to examine.

        Defaults to ''.
        """,
    )

    cache_from = List(
        [],
        config=True,
        help="""
        List of images to try & re-use cached image layers from.

        Docker only tries to re-use image layers from images built locally,
        not pulled from a registry. We can ask it to explicitly re-use layers
        from non-locally built images by through the 'cache_from' parameter.
        """,
    )

    buildpacks = List(
        [
            LegacyBinderDockerBuildPack,
            DockerBuildPack,
            JuliaProjectTomlBuildPack,
            JuliaRequireBuildPack,
            NixBuildPack,
            RBuildPack,
            CondaBuildPack,
            PipfileBuildPack,
            PythonBuildPack,
        ],
        config=True,
        help="""
        Ordered list of BuildPacks to try when building a git repository.
        """,
    )

    extra_build_kwargs = Dict(
        {},
        help="""
        extra kwargs to limit CPU quota when building a docker image.
        Dictionary that allows the user to set the desired runtime flag
        to configure the amount of access to CPU resources your container has.
        Reference https://docs.docker.com/config/containers/resource_constraints/#cpu
        """,
        config=True,
    )

    extra_run_kwargs = Dict(
        {},
        help="""
        extra kwargs to limit CPU quota when running a docker image.
        Dictionary that allows the user to set the desired runtime flag
        to configure the amount of access to CPU resources your container has.
        Reference https://docs.docker.com/config/containers/resource_constraints/#cpu
        """,
        config=True,
    )

    default_buildpack = Any(
        PythonBuildPack,
        config=True,
        help="""
        The default build pack to use when no other buildpacks are found.
        """,
    )

    # Git is our content provider of last resort. This is to maintain the
    # old behaviour when git and local directories were the only supported
    # content providers. We can detect local directories from the path, but
    # detecting if something will successfully `git clone` is very hard if all
    # you can do is look at the path/URL to it.
    content_providers = List(
        [
            contentproviders.Local,
            contentproviders.Zenodo,
            contentproviders.Figshare,
            contentproviders.Dataverse,
            contentproviders.Hydroshare,
            contentproviders.Swhid,
            contentproviders.Mercurial,
            contentproviders.Git,
        ],
        config=True,
        help="""
        Ordered list by priority of ContentProviders to try in turn to fetch
        the contents specified by the user.
        """,
    )

    build_memory_limit = ByteSpecification(
        0,
        help="""
        Total memory that can be used by the docker image building process.

        Set to 0 for no limits.
        """,
        config=True,
    )

    volumes = Dict(
        {},
        help="""
        Volumes to mount when running the container.

        Only used when running, not during build process!

        Use a key-value pair, with the key being the volume source &
        value being the destination volume.

        Both source and destination can be relative. Source is resolved
        relative to the current working directory on the host, and
        destination is resolved relative to the working directory of the
        image - ($HOME by default)
        """,
        config=True,
    )

    user_id = Int(
        help="""
        UID of the user to create inside the built image.

        Should be a uid that is not currently used by anything in the image.
        Defaults to uid of currently running user, since that is the most
        common case when running r2d manually.

        Might not affect Dockerfile builds.
        """,
        config=True,
    )

    @default("user_id")
    def _user_id_default(self):
        """
        Default user_id to current running user.
        """
        return os.geteuid()

    user_name = Unicode(
        "jovyan",
        help="""
        Username of the user to create inside the built image.

        Should be a username that is not currently used by anything in the
        image, and should conform to the restrictions on user names for Linux.

        Defaults to username of currently running user, since that is the most
        common case when running repo2docker manually.
        """,
        config=True,
    )

    @default("user_name")
    def _user_name_default(self):
        """
        Default user_name to current running user.
        """
        return getpass.getuser()

    appendix = Unicode(
        config=True,
        help="""
        Appendix of Dockerfile commands to run at the end of the build.

        Can be used to customize the resulting image after all
        standard build steps finish.
        """,
    )

    labels = Dict(
        {},
        help="""
        Extra labels to set on the final image.

        Each Label is a key-value pair, with the key being the name of the label
        and the value its value.
        """,
        config=True,
    )

    platform = Unicode(
        config=True,
        help="""
        Platform to build for, linux/amd64 (recommended) or linux/arm64 (experimental).
        """,
    )

    @default("platform")
    def _platform_default(self):
        """
        Default platform
        """
        p = get_platform()
        if p == "linux/arm64":
            warnings.warn(
                "Building for linux/arm64 is experimental. "
                "To use the recommended platform set --Repo2Docker.platform=linux/amd64. "
                "To silence this warning set --Repo2Docker.platform=linux/arm64."
            )
        return p

    extra_build_args = Dict(
        {},
        help="""
        Extra build args to pass to the image build process.
        This is pretty much only useful for custom Dockerfile based builds.
        """,
        config=True,
    )

    json_logs = Bool(
        False,
        help="""
        Log output in structured JSON format.

        Useful when stdout is consumed by other tools
        """,
        config=True,
    )

    repo = Unicode(
        ".",
        help="""
        Specification of repository to build image for.

        Could be local path or git URL.
        """,
        config=True,
    )

    ref = Unicode(
        None,
        help="""
        Git ref that should be built.

        If repo is a git repository, this ref is checked out
        in a local clone before repository is built.
        """,
        config=True,
        allow_none=True,
    )

    swh_token = Unicode(
        None,
        help="""
        Token to use authenticated SWH API access.

        If unset, default to unauthenticated (limited) usage of the Software
        Heritage API.
        """,
        config=True,
        allow_none=True,
    )

    cleanup_checkout = Bool(
        True,
        help="""
        Delete source repository after building is done.

        Useful when repo2docker is doing the git cloning
        """,
        config=True,
    )

    @default("cleanup_checkout")
    def _defaut_cleanup_checkout(self):
        # if the source exists locally we don't want to delete it at the end
        # FIXME: Find a better way to figure out if repo is 'local'. Push this into ContentProvider?
        return not os.path.exists(self.repo)

    output_image_spec = Unicode(
        "",
        help="""
        Docker Image name:tag to tag the built image with.

        Required parameter.
        """,
        config=True,
    )

    push = Bool(
        False,
        help="""
        Set to true to push docker image after building
        """,
        config=True,
    )

    run = Bool(
        True,
        help="""
        Run docker image after building
        """,
        config=True,
    )

    # FIXME: Refactor class to be able to do --no-build without needing
    #        deep support for it inside other code
    dry_run = Bool(
        False,
        help="""
        Do not actually build the docker image, just simulate it.
        """,
        config=True,
    )

    @observe("dry_run")
    def _dry_run_changed(self, change):
        if change.new:
            # dry_run forces run and push to be False
            self.push = self.run = False

    # FIXME: Refactor classes to separate build & run steps
    run_cmd = List(
        [],
        help="""
        Command to run when running the container

        When left empty, a jupyter notebook is run.
        """,
        config=True,
    )

    all_ports = Bool(
        False,
        help="""
        Publish all declared ports from container whiel running.

        Equivalent to -P option to docker run
        """,
        config=True,
    )

    ports = Dict(
        {},
        help="""
        Port mappings to establish when running the container.

        Equivalent to -p {key}:{value} options to docker run.
        {key} refers to port inside container, and {value}
        refers to port / host:port in the host
        """,
        config=True,
    )

    environment = List(
        [],
        help="""
        Environment variables to set when running the built image.

        Each item must be a string formatted as KEY=VALUE
        """,
        config=True,
    )

    target_repo_dir = Unicode(
        "",
        help="""
        Path inside the image where contents of the repositories are copied to,
        and where all the build operations (such as postBuild) happen.

        Defaults to ${HOME} if not set
        """,
        config=True,
    )

    engine = Unicode(
        "docker",
        config=True,
        help="""
        Name of the container engine.

        Defaults to 'docker'.
        """,
    )

    def get_engine(self):
        """Return an instance of the container engine.

        Currently no arguments are passed to the engine constructor.
        """
        engines = entrypoints.get_group_named("repo2docker.engines")
        try:
            entry = engines[self.engine]
        except KeyError:
            raise ContainerEngineException(
                f"Container engine '{self.engine}' not found. Available engines: {','.join(engines.keys())}"
            )
        engine_class = entry.load()
        return engine_class(parent=self)

    def fetch(self, url, ref, checkout_path):
        """Fetch the contents of `url` and place it in `checkout_path`.

        The `ref` parameter specifies what "version" of the contents should be
        fetched. In the case of a git repository `ref` is the SHA-1 of a commit.

        Iterate through possible content providers until a valid provider,
        based on URL, is found.
        """
        picked_content_provider = None
        for ContentProvider in self.content_providers:
            cp = ContentProvider()
            spec = cp.detect(url, ref=ref)
            if spec is not None:
                picked_content_provider = cp
                self.log.info(f"Picked {cp.__class__.__name__} content provider.\n")
                break

        if picked_content_provider is None:
            self.log.error(f"No matching content provider found for {url}.")

        swh_token = self.config.get("swh_token", self.swh_token)
        if swh_token and isinstance(picked_content_provider, contentproviders.Swhid):
            picked_content_provider.set_auth_token(swh_token)

        for log_line in picked_content_provider.fetch(
            spec, checkout_path, yield_output=self.json_logs
        ):
            self.log.info(log_line, extra=dict(phase=R2dState.FETCHING))

        if not self.output_image_spec:
            image_spec = "r2d" + self.repo
            # if we are building from a subdirectory include that in the
            # image name so we can tell builds from different sub-directories
            # apart.
            if self.subdir:
                image_spec += self.subdir
            if picked_content_provider.content_id is not None:
                image_spec += picked_content_provider.content_id
            else:
                image_spec += str(int(time.time()))
            self.output_image_spec = escapism.escape(
                image_spec, escape_char="-"
            ).lower()

    def json_excepthook(self, etype, evalue, traceback):
        """Called on an uncaught exception when using json logging

        Avoids non-JSON output on errors when using --json-logs
        """
        self.log.error(
            f"Error during build: {evalue}",
            exc_info=(etype, evalue, traceback),
            extra=dict(phase=R2dState.FAILED),
        )

    def initialize(self, *args, **kwargs):
        """Init repo2docker configuration before start"""
        # FIXME: Remove this function, move it to setters / traitlet reactors
        self.log = logging.getLogger("repo2docker")
        self.log.setLevel(self.log_level)
        logHandler = logging.StreamHandler()
        self.log.handlers = []
        self.log.addHandler(logHandler)
        if self.json_logs:
            # register JSON excepthook to avoid non-JSON output on errors
            sys.excepthook = self.json_excepthook
            # Need to reset existing handlers, or we repeat messages
            formatter = jsonlogger.JsonFormatter()
            logHandler.setFormatter(formatter)
        else:
            # due to json logger stuff above,
            # our log messages include carriage returns, newlines, etc.
            # remove the additional newline from the stream handler
            self.log.handlers[0].terminator = ""
            # We don't want a [Repo2Docker] on all messages
            self.log.handlers[0].formatter = logging.Formatter(fmt="%(message)s")

        if self.dry_run and (self.run or self.push):
            raise ValueError("Cannot push or run image if we are not building it")

        if self.volumes and not self.run:
            raise ValueError("Cannot mount volumes if container is not run")

    def push_image(self):
        """Push docker image to registry"""
        client = self.get_engine()
        # Build a progress setup for each layer, and only emit per-layer
        # info every 1.5s
        progress_layers = {}
        layers = {}
        last_emit_time = time.time()
        for chunk in client.push(self.output_image_spec):
            if client.string_output:
                self.log.info(chunk, extra=dict(phase=R2dState.PUSHING))
                continue
            # else this is Docker output

            # each chunk can be one or more lines of json events
            # split lines here in case multiple are delivered at once
            for line in chunk.splitlines():
                line = line.decode("utf-8", errors="replace")
                try:
                    progress = json.loads(line)
                except Exception as e:
                    self.log.warning("Not a JSON progress line: %r", line)
                    continue
                if "error" in progress:
                    self.log.error(progress["error"], extra=dict(phase=R2dState.FAILED))
                    raise ImageLoadError(progress["error"])
                if "id" not in progress:
                    continue
                # deprecated truncated-progress data
                if "progressDetail" in progress and progress["progressDetail"]:
                    progress_layers[progress["id"]] = progress["progressDetail"]
                else:
                    progress_layers[progress["id"]] = progress["status"]
                # include full progress data for each layer in 'layers' data
                layers[progress["id"]] = progress
                if time.time() - last_emit_time > 1.5:
                    self.log.info(
                        "Pushing image\n",
                        extra=dict(
                            progress=progress_layers,
                            layers=layers,
                            phase=R2dState.PUSHING,
                        ),
                    )
                    last_emit_time = time.time()
        self.log.info(
            f"Successfully pushed {self.output_image_spec}",
            extra=dict(phase=R2dState.PUSHING),
        )

    def run_image(self):
        """Run docker container from built image

        and wait for it to finish.
        """
        container = self.start_container()
        self.wait_for_container(container)

    def start_container(self):
        """Start docker container from built image

        Returns running container
        """
        client = self.get_engine()

        docker_host = os.environ.get("DOCKER_HOST")
        if docker_host:
            host_name = urlparse(docker_host).hostname
        else:
            host_name = "127.0.0.1"
        self.hostname = host_name

        if not self.run_cmd:
            if len(self.ports) == 1:
                # single port mapping specified
                # retrieve container and host port from dict
                # {'8888/tcp': ('hostname', 'port')}
                # or
                # {'8888/tcp': 'port'}
                container_port_proto, host_port = next(iter(self.ports.items()))
                if isinstance(host_port, tuple):
                    # (hostname, port) tuple or string port
                    host_name, host_port = host_port
                    self.hostname = host_name
                host_port = int(host_port)
                container_port = int(container_port_proto.split("/", 1)[0])
            else:
                # no port specified, pick a random one
                container_port = host_port = str(self._get_free_port())
                self.ports = {f"{container_port}/tcp": host_port}
            self.port = host_port
            # To use the option --NotebookApp.custom_display_url
            # make sure the base-notebook image is updated:
            # docker pull jupyter/base-notebook
            run_cmd = [
                "jupyter",
                "notebook",
                "--ip=0.0.0.0",
                f"--port={container_port}",
                f"--NotebookApp.custom_display_url=http://{host_name}:{host_port}",
                "--NotebookApp.default_url=/lab",
            ]
        else:
            # run_cmd given by user, if port is also given then pass it on
            run_cmd = self.run_cmd

        container_volumes = {}
        if self.volumes:
            image = client.inspect_image(self.output_image_spec)
            image_workdir = image.config["WorkingDir"]

            for k, v in self.volumes.items():
                container_volumes[os.path.abspath(k)] = {
                    "bind": v if v.startswith("/") else os.path.join(image_workdir, v),
                    "mode": "rw",
                }

        run_kwargs = dict(
            publish_all_ports=self.all_ports,
            ports=self.ports,
            command=run_cmd,
            volumes=container_volumes,
            environment=self.environment,
        )

        run_kwargs.update(self.extra_run_kwargs)

        container = client.run(self.output_image_spec, **run_kwargs)

        while container.status == "created":
            time.sleep(0.5)
            container.reload()

        return container

    def wait_for_container(self, container):
        """Wait for a container to finish

        Displaying logs while it's running
        """

        last_timestamp = None
        try:
            for line in container.logs(stream=True, timestamps=True):
                line = line.decode("utf-8")
                last_timestamp, line = line.split(" ", maxsplit=1)
                self.log.info(line, extra=dict(phase=R2dState.RUNNING))

        finally:
            container.reload()
            if container.status == "running":
                self.log.info(
                    "Stopping container...\n", extra=dict(phase=R2dState.RUNNING)
                )
                container.kill()
            exit_code = container.exitcode

            container.wait()

            self.log.info(
                "Container finished running.\n".upper(),
                extra=dict(phase=R2dState.RUNNING),
            )
            # are there more logs? Let's send them back too
            late_logs = container.logs(since=last_timestamp).decode("utf-8")
            for line in late_logs.split("\n"):
                self.log.debug(line + "\n", extra=dict(phase=R2dState.RUNNING))

            container.remove()
            if exit_code:
                sys.exit(exit_code)

    def _get_free_port(self):
        """
        Hacky method to get a free random port on local host
        """
        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        port = s.getsockname()[1]
        s.close()
        return port

    def find_image(self):
        # if this is a dry run it is Ok for dockerd to be unreachable so we
        # always return False for dry runs.
        if self.dry_run:
            return False
        # check if we already have an image for this content
        client = self.get_engine()
        for image in client.images():
            for tag in image.tags:
                if tag == self.output_image_spec + ":latest":
                    return True
        return False

    def build(self):
        """
        Build docker image
        """
        # Check if r2d can connect to docker daemon
        if not self.dry_run:
            try:
                docker_client = self.get_engine()
            except ContainerEngineException as e:
                self.log.error(f"\nContainer engine initialization error: {e}\n")
                self.exit(1)

        # If the source to be executed is a directory, continue using the
        # directory. In the case of a local directory, it is used as both the
        # source and target. Reusing a local directory seems better than
        # making a copy of it as it might contain large files that would be
        # expensive to copy.
        if os.path.isdir(self.repo):
            # never cleanup when we are working in a local repo
            self.cleanup_checkout = False
            checkout_path = self.repo
        else:
            if self.git_workdir is None:
                checkout_path = tempfile.mkdtemp(prefix="repo2docker")
            else:
                checkout_path = self.git_workdir

        try:
            self.fetch(self.repo, self.ref, checkout_path)

            if self.find_image():
                self.log.info(
                    f"Reusing existing image ({self.output_image_spec}), not building."
                )
                # no need to build, so skip to the end by `return`ing here
                # this will still execute the finally clause and let's us
                # avoid having to indent the build code by an extra level
                return

            if self.subdir:
                checkout_path = os.path.join(checkout_path, self.subdir)
                if not os.path.isdir(checkout_path):
                    self.log.error(
                        f"Subdirectory {self.subdir} does not exist",
                        extra=dict(phase=R2dState.FAILED),
                    )
                    raise FileNotFoundError(f"Could not find {checkout_path}")

            with chdir(checkout_path):
                for BP in self.buildpacks:
                    bp = BP()
                    if bp.detect():
                        picked_buildpack = bp
                        break
                else:
                    picked_buildpack = self.default_buildpack()

                picked_buildpack.platform = self.platform
                picked_buildpack.appendix = self.appendix
                # Add metadata labels
                picked_buildpack.labels["repo2docker.version"] = self.version
                repo_label = "local" if os.path.isdir(self.repo) else self.repo
                picked_buildpack.labels["repo2docker.repo"] = repo_label
                picked_buildpack.labels["repo2docker.ref"] = self.ref

                picked_buildpack.labels.update(self.labels)

                build_args = {
                    "NB_USER": self.user_name,
                    "NB_UID": str(self.user_id),
                }
                if self.target_repo_dir:
                    build_args["REPO_DIR"] = self.target_repo_dir
                build_args.update(self.extra_build_args)

                if self.dry_run:
                    print(picked_buildpack.render(build_args))
                else:
                    self.log.debug(
                        picked_buildpack.render(build_args),
                        extra=dict(phase=R2dState.BUILDING),
                    )
                    if self.user_id == 0:
                        raise ValueError(
                            "Root as the primary user in the image is not permitted."
                        )

                    self.log.info(
                        f"Using {bp.__class__.__name__} builder\n",
                        extra=dict(phase=R2dState.BUILDING),
                    )

                    for l in picked_buildpack.build(
                        docker_client,
                        self.output_image_spec,
                        self.build_memory_limit,
                        build_args,
                        self.cache_from,
                        self.extra_build_kwargs,
                        platform=self.platform,
                    ):
                        if docker_client.string_output:
                            self.log.info(l, extra=dict(phase=R2dState.BUILDING))
                        # else this is Docker output
                        elif "stream" in l:
                            self.log.info(
                                l["stream"], extra=dict(phase=R2dState.BUILDING)
                            )
                        elif "error" in l:
                            self.log.info(l["error"], extra=dict(phase=R2dState.FAILED))
                            raise BuildError(l["error"])
                        elif "status" in l:
                            self.log.info(
                                "Fetching base image...\r",
                                extra=dict(phase=R2dState.BUILDING),
                            )
                        else:
                            self.log.info(
                                json.dumps(l), extra=dict(phase=R2dState.BUILDING)
                            )

        finally:
            # Cleanup checkout if necessary
            # never cleanup when checking out a local repo
            if self.cleanup_checkout:
                shutil.rmtree(checkout_path, ignore_errors=True)

    def start(self):
        self.build()

        if self.push:
            self.push_image()

        if self.run:
            self.run_image()
