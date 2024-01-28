from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

from . import _version
from .app import Repo2Docker

__version__ = _version.get_versions()["version"]
