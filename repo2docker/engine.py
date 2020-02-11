"""
Interface for a repo2docker container engine
"""

from abc import ABC, abstractmethod


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


class ContainerEngine(ABC):
    """
    Abstract container engine
    """

    # containers = Container

    # Based on https://docker-py.readthedocs.io/en/4.2.0/api.html#module-docker.api.build

    @abstractmethod
    def build(
        self,
        *,
        buildargs={},
        cache_from=[],
        container_limits={},
        forcerm=False,
        rm=False,
        tag="",
        custom_context=False,
        decode=False,
        dockerfile="",
        fileobj=None,
        path="",
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
        forcerm : bool
            Always remove containers including unsuccessful builds
        rm : bool
            Remove intermediate containers
        tag : str
            Tag to add to the image

        custom_context : bool
            If `True` fileobj is a Tar file object containing the build context
            TODO: Specific to Docker
        decode : bool
            If `True` decode responses into dicts
            TODO: repo2docker sets this to True but it's not clear what other clients should return
        dockerfile : str
            Path to Dockerfile within the build context
        fileobj : tarfile
            A tar file-like object containing the build context
            TODO: Specific to Docker, other clients can untar this to a tempdir
        path : str
            path to the Dockerfile
        """

    @abstractmethod
    def images(self):
        """
        List images

        Returns
        -------
        list[str] : List of images
        """

    @abstractmethod
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

    @abstractmethod
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

    # Note this is different from the Docker client which has Client.containers.run
    def run(
        image_spec,
        *,
        command=[],
        environment=[],
        detach=False,
        ports={},
        publish_all_ports=False,
        remove=False,
        volumes={},
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
        detach : bool
            If `True` run container in background
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
