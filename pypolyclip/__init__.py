try:
    from .version import version as __version__
except ImportError:
    __version__ = ''

from .pypolyclip import multi, single  # noqa: F401
