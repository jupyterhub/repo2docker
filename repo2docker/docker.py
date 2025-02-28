"""
Docker container engine for repo2docker
"""

import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from argparse import ArgumentError
from contextlib import ExitStack, contextmanager
from pathlib import Path

from iso8601 import parse_date
from traitlets import Dict, List, Unicode

import docker

from .engine import Container, ContainerEngine, Image
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

    string_output = True

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

    def build(
        self,
        push=False,
        load=False,
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
        args = ["docker", "buildx", "build", "--progress", "plain"]
        if load:
            if push:
                raise ValueError(
                    "Setting push=True and load=True is currently not supported"
                )
            args.append("--load")

        if push:
            args.append("--push")

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

        with ExitStack() as stack:
            if self.registry_credentials:
                stack.enter_context(self.docker_login(**self.registry_credentials))
            if fileobj:
                with tempfile.TemporaryDirectory() as d:
                    tarf = tarfile.open(fileobj=fileobj)
                    tarf.extractall(d)

                    args += [d]

                    yield from execute_cmd(args, True)
            else:
                # Assume 'path' is passed in
                args += [path]

                yield from execute_cmd(args, True)

    def inspect_image(self, image):
        """
        Return image configuration if it exists, otherwise None
        """
        proc = subprocess.run(
            ["docker", "image", "inspect", image], capture_output=True
        )

        if proc.returncode != 0:
            return None

        config = json.loads(proc.stdout.decode())[0]
        return Image(tags=config["RepoTags"], config=config["Config"])

    @contextmanager
    def docker_login(self, username, password, registry):
        # Determine existing DOCKER_CONFIG
        old_dc_path = os.environ.get("DOCKER_CONFIG")
        if old_dc_path is None:
            dc_path = Path("~/.docker/config.json").expanduser()
        else:
            dc_path = Path(old_dc_path)

        with tempfile.TemporaryDirectory() as d:
            new_dc_path = Path(d) / "config.json"
            if dc_path.exists():
                # If there is an existing DOCKER_CONFIG, copy it to new location so we inherit
                # whatever configuration the user has already set
                shutil.copy2(dc_path, new_dc_path)

            os.environ["DOCKER_CONFIG"] = d
            proc = subprocess.run(
                [
                    "docker",
                    "login",
                    "--username",
                    username,
                    "--password-stdin",
                    registry,
                ],
                input=password.encode(),
                check=True,
            )
            try:
                yield
            finally:
                if old_dc_path:
                    os.environ["DOCKER_CONFIG"] = old_dc_path
                else:
                    del os.environ["DOCKER_CONFIG"]

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
