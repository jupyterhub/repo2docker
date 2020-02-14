"""
Docker container engine for repo2docker
"""

import docker
from .engine import Container, ContainerEngine, ContainerEngineException, Image


class DockerContainer(Container):
    def __init__(self, container):
        self._c = container

    def reload(self):
        return self._c.reload()

    def logs(self, *, stream=False):
        return self._c.logs(stream=stream)

    def kill(self, *, signal="KILL"):
        return self._c.kill(signal=signal)

    def remove(self):
        return self._c.remove()

    def stop(self, *, timeout=10):
        return self._c.stop(timeout=timeout)

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

    def __init__(self, *, parent):
        super().__init__(parent=parent)
        try:
            self._apiclient = docker.APIClient(
                version="auto", **docker.utils.kwargs_from_env()
            )
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
        # fmt: off
        # black adds a trailing , but this is invalid in Python 3.5
        **kwargs
        # fmt: on
    ):
        return self._apiclient.build(
            buildargs=buildargs,
            cache_from=cache_from,
            container_limits=container_limits,
            forcerm=True,
            rm=True,
            tag=tag,
            custom_context=custom_context,
            decode=True,
            dockerfile=dockerfile,
            fileobj=fileobj,
            path=path,
            **kwargs,
        )

    def images(self):
        images = self._apiclient.images()
        return [Image(tags=image["RepoTags"]) for image in images]

    def inspect_image(self, image):
        return self._apiclient.inspect_image(image)

    def push(self, image_spec):
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
        # fmt: off
        # black adds a trailing , but this is invalid in Python 3.5
        **kwargs
        # fmt: on
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
