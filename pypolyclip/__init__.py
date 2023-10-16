try:
    from .version import version as __version__
except ImportError:
    __version__ = ''

from .pypolyclip import clip_single, clip_multi  # noqa: F401
