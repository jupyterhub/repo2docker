"""
Docker container engine for repo2docker
"""

import shutil
import tarfile
import tempfile

from iso8601 import parse_date
from traitlets import Dict, List, Unicode

import docker

from .engine import Container, ContainerEngine, ContainerEngineException, Image
from .utils import execute_cmd


class DockerContainer(Container):
    def __init__(self, container):
        self._c = container

    def reload(self):
        return self._c.reload()

    def logs(self, *, stream=False, timestamps=False, since=None):
        if since:
            # docker only accepts integer timestamps
            # this means we will usually replay logs from the last second
            # of the container
            # we should check if this ever returns anything new,
            # since we know it ~always returns something redundant
            since = int(parse_date(since).timestamp())
        return self._c.logs(stream=stream, timestamps=timestamps, since=since)

    def kill(self, *, signal="KILL"):
        return self._c.kill(signal=signal)

    def remove(self):
        return self._c.remove()

    def stop(self, *, timeout=10):
        return self._c.stop(timeout=timeout)

    def wait(self):
        return self._c.wait()

    @property
    def exitcode(self):
        return self._c.attrs["State"]["ExitCode"]

    @property
    def status(self):
        return self._c.status


class DockerEngine(ContainerEngine):
    """
    https://docker-py.readthedocs.io/en/4.2.0/api.html#module-docker.api.build
    """

    string_output = False

    extra_init_args = Dict(
        {},
        help="""
        Extra kwargs to pass to docker client when initializing it.

        Dictionary that allows users to specify extra parameters to pass
        to APIClient, parameters listed in https://docker-py.readthedocs.io/en/stable/api.html#docker.api.client.APIClient.

        Parameters here are merged with whatever is picked up from the
        environment.
        """,
        config=True,
    )

    extra_buildx_build_args = List(
        Unicode(),
        help="""
        Extra commandline arguments to pass to `docker buildx build` when building the image.
        """,
        config=True,
    )

    def __init__(self, *, parent):
        super().__init__(parent=parent)
        try:
            kwargs = docker.utils.kwargs_from_env()
            kwargs.update(self.extra_init_args)
            kwargs.setdefault("version", "auto")
            self._apiclient = docker.APIClient(**kwargs)
        except docker.errors.DockerException as e:
            raise ContainerEngineException("Check if docker is running on the host.", e)

    def build(
        self,
        *,
        buildargs=None,
        cache_from=None,
        container_limits=None,
        tag="",
        custom_context=False,
        dockerfile="",
        fileobj=None,
        path="",
        labels=None,
        platform=None,
        **kwargs,
    ):
        if not shutil.which("docker"):
            raise RuntimeError("The docker commandline client must be installed")
        args = ["docker", "buildx", "build", "--progress", "plain", "--load"]
        if buildargs:
            for k, v in buildargs.items():
                args += ["--build-arg", f"{k}={v}"]

        if cache_from:
            for cf in cache_from:
                args += ["--cache-from", cf]

        if dockerfile:
            args += ["--file", dockerfile]

        if tag:
            args += ["--tag", tag]

        if labels:
            for k, v in labels.items():
                args += ["--label", f"{k}={v}"]

        if platform:
            args += ["--platform", platform]

        # place extra args right *before* the path
        args += self.extra_buildx_build_args

        if fileobj:
            with tempfile.TemporaryDirectory() as d:
                tarf = tarfile.open(fileobj=fileobj)
                tarf.extractall(d)

                args += [d]

                for line in execute_cmd(args, True):
                    # Simulate structured JSON output from buildx build, since we
                    # do get structured json output from pushing and running
                    yield {"stream": line}
        else:
            # Assume 'path' is passed in
            args += [path]

            for line in execute_cmd(args, True):
                # Simulate structured JSON output from buildx build, since we
                # do get structured json output from pushing and running
                yield {"stream": line}

    def images(self):
        images = self._apiclient.images()
        return [Image(tags=image["RepoTags"]) for image in images]

    def inspect_image(self, image):
        image = self._apiclient.inspect_image(image)
        return Image(tags=image["RepoTags"], config=image["Config"])

    def push(self, image_spec):
        if self.registry_credentials:
            self._apiclient.login(**self.registry_credentials)
        return self._apiclient.push(image_spec, stream=True)

    def run(
        self,
        image_spec,
        *,
        command=None,
        environment=None,
        ports=None,
        publish_all_ports=False,
        remove=False,
        volumes=None,
        **kwargs,
    ):
        client = docker.from_env(version="auto")
        container = client.containers.run(
            image_spec,
            command=command,
            environment=(environment or []),
            detach=True,
            ports=(ports or {}),
            publish_all_ports=publish_all_ports,
            remove=remove,
            volumes=(volumes or {}),
            **kwargs,
        )
        return DockerContainer(container)
