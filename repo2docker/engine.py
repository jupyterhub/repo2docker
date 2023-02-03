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
    def logs(self, *, stream=False, timestamps=False, since=None):
        """
        Get the container logs.

        Parameters
        ----------
        stream : bool
            If `True` return an iterator over the log lines, otherwise return all logs
        timestamps : bool
            If `True` log lines will be prefixed with iso8601 timestamps followed by space
        since : str
            A timestamp string
            Should be in the same format as the timestamp prefix given
            when `timestamps=True`

            If given, start logs from this point,
            instead of from container start.

        Returns
        -------
        str or generator of log strings
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

    @abstractmethod
    def wait(self):
        """
        Wait for the container to stop
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

        Full list of statuses:
        https://github.com/moby/moby/blob/v19.03.5/api/swagger.yaml#L4832
        """


class Image:
    """
    Information about a container image
    """

    def __init__(self, *, tags, config=None):
        self._tags = tags or []
        self._config = config

    @property
    def tags(self):
        """
        A list of tags associated with an image.

        If locally built images have a localhost prefix this prefix should be removed or the image may not be recognised.
        If there are no tags [] will be returned.
        """
        return self._tags

    @property
    def config(self):
        """
        A dictionary of image configuration information

        If this is `None` the information has not been loaded.
        If not `None` this must include the following fields:
        - WorkingDir: The default working directory
        """
        return self._config

    def __repr__(self):
        return f"Image(tags={self.tags},config={self.config})"


class ContainerEngine(LoggingConfigurable):
    """
    Abstract container engine.

    Inherits from LoggingConfigurable, which means it has a log property.
    Initialised with a reference to the parent so can also be configured using traitlets.
    """

    string_output = True
    """
    Whether progress events should be strings or an object.

    Originally Docker was the only container engine supported by repo2docker.
    Some operations including build() and push() would return generators of events in a Docker specific format.
    This format of events is not easily constructable with other engines so the default is to return strings and raise an exception if an error occurs.
    If an engine returns docker style events set this variable to False.
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
        path="",
        labels=None,
        platform=None,
        **kwargs,
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
        dockerfile : str
            Path to Dockerfile within the build context
        fileobj : tarfile
            A tar file-like object containing the build context
        path : str
            path to the Dockerfile
        labels : dict
            Dictionary of labels to set on the image
        platform: str
            Platform to build for

        Returns
        -------
        A generator of strings. If an error occurs an exception must be thrown.

        If `string_output=True` this should instead be whatever Docker returns:
        https://github.com/jupyter/repo2docker/blob/0.11.0/repo2docker/app.py#L725-L735
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
        Image object with .config dict.
        """
        raise NotImplementedError("inspect_image not implemented")

    def push(self, image_spec):
        """
        Push image to a registry

        Parameters
        ----------
        image_spec : str
            The repository spec to push to

        Returns
        -------
        A generator of strings. If an error occurs an exception must be thrown.

        If `string_output=True` this should instead be whatever Docker returns:
        https://github.com/jupyter/repo2docker/blob/0.11.0/repo2docker/app.py#L469-L495
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
        volumes={},
        **kwargs,
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
            Container port bindings in the form generated by `repo2docker.utils.validate_and_generate_port_mapping`
            https://github.com/jupyter/repo2docker/blob/0.11.0/repo2docker/utils.py#L95
        publish_all_ports : bool
            If `True` publish all ports to host
        remove : bool
            If `True` delete container when it completes
        volumes : dict
            Volume bindings in the form `{src : dest}`

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
