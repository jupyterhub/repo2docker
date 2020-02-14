"""
Interface for a repo2docker container engine
"""

from abc import ABC, abstractmethod
from traitlets.config import LoggingConfigurable


# Based on https://docker-py.readthedocs.io/en/4.2.0/containers.html


class Container(ABC):
    """
    Abstract container returned by repo2docker engines
    """

    @abstractmethod
    def reload(self):
        """
        Refresh container attributes
        """

    @abstractmethod
    def logs(self, stream=False):
        """
        Get the container logs.

        Parameters
        ----------
        stream : bool
            If `True` return an iterator over the log lines, otherwise return all
            logs

        Returns
        -------
        str or iterator
        """

    @abstractmethod
    def kill(self, *, signal="KILL"):
        """
        Send a signal to the container

        Parameters
        ----------
        signal : str
            The signal, default `KILL`
        """

    @abstractmethod
    def remove(self):
        """
        Remove the container
        """

    @abstractmethod
    def stop(self, *, timeout=10):
        """
        Stop the container

        Parameters
        ----------
        timeout : If the container doesn't gracefully stop after this timeout kill it
        """

    @property
    @abstractmethod
    def exitcode(self):
        """
        The container exit code if exited
        """

    @property
    @abstractmethod
    def status(self):
        """
        The status of the container

        Returns
        -------
        str : The status of the container.
            Values include `created` `running` `exited`.

        TODO: Does Docker have a fixed list of these?
        """


class Image:
    """
    Information about a container image
    """

    def __init__(self, *, tags):
        self._tags = tags or []

    @property
    def tags(self):
        """
        A list of tags associated with an image.

        If locally built images have a localhost prefix this prefix should be removed or the image may not be recognised.
        If there are no tags [] will be returned.
        """
        return self._tags

    def __repr__(self):
        return "Image(tags={})".format(self.tags)


class ContainerEngine(LoggingConfigurable):
    """
    Abstract container engine.

    Inherits from LoggingConfigurable, which means it has a log property.
    Initialised with a reference to the parent so can also be configured using traitlets.
    """

    def __init__(self, *, parent):
        """
        Initialise the container engine

        Parameters
        ----------
        parent: Application
            Reference to the parent application so that its configuration file can be used in this plugin.
        """
        super().__init__(parent=parent)

    # Based on https://docker-py.readthedocs.io/en/4.2.0/api.html#module-docker.api.build

    def build(
        self,
        *,
        buildargs={},
        cache_from=[],
        container_limits={},
        tag="",
        custom_context=False,
        dockerfile="",
        fileobj=None,
        path=""
    ):
        """
        Build a container

        Parameters
        ----------
        buildargs : dict
            Dictionary of build arguments
        cache_from : list[str]
            List of images to chech for caching
        container_limits : dict
            Dictionary of resources limits. These keys are supported:
              - `cpusetcpus`
              - `cpushares`
              - `memory`
              - `memswap`
        tag : str
            Tag to add to the image

        custom_context : bool
            If `True` fileobj is a Tar file object containing the build context
            TODO: Specific to Docker
        dockerfile : str
            Path to Dockerfile within the build context
        fileobj : tarfile
            A tar file-like object containing the build context
            TODO: Specific to Docker, other clients can untar this to a tempdir
        path : str
            path to the Dockerfile
        """
        raise NotImplementedError("build not implemented")

    def images(self):
        """
        List images

        Returns
        -------
        list[Image] : List of Image objects.
        """
        raise NotImplementedError("images not implemented")

    def inspect_image(self, image):
        """
        Get information about an image

        TODO: This is specific to the engine, can we convert it to a standard format?

        Parameters
        ----------
        image : str
            The image

        Returns
        -------
        dict
        """
        raise NotImplementedError("inspect_image not implemented")

    def push(self, image_spec, *, stream=True):
        """
        Push image to a registry

        Parameters
        ----------
        image_spec : str
            The repository spec to push to
        stream : bool
            If `True` return output logs as a generator
        """
        raise NotImplementedError("push not implemented")

    # Note this is different from the Docker client which has Client.containers.run
    def run(
        self,
        image_spec,
        *,
        command=[],
        environment=[],
        ports={},
        publish_all_ports=False,
        remove=False,
        volumes={}
    ):
        """
        Run a container

        Parameters
        ----------
        image_spec : str
            The image to run
        command : list[str]
            The command to run
        environment : list[str]
            List of environment variables in the form `ENVVAR=value`
        ports : dict
            Container port bindings in the format expected by the engine
            TODO: Should we use a fixed format and convert to whatever's required by the engine?
        publish_all_ports : bool
            If `True` publish all ports to host
        remove : bool
            If `True` delete container when it completes
        volumes : dict
            Volume bindings in the format expected by the engine
            TODO: Should we use a fixed format and convert to whatever's required by the engine?

        Returns
        -------
        Container : the running container

        Raises
        ------
        NotImplementedError
            This engine does not support running containers
        """
        raise NotImplementedError("Running containers not supported")


class ContainerEngineException(Exception):
    """
    Base class for exceptions in the container engine
    """


class BuildError(ContainerEngineException):
    """
    Container build error
    """


class ImageLoadError(ContainerEngineException):
    """
    Container load/push error
    """
