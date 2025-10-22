try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"

from .app import Repo2Docker

# You can add this if you want an __all__ variable to control imports
__all__ = ["__version__", "Repo2Docker"]
