"""
Pypolyclip is a Python library for clipping polygons against a pixel
grid.
"""
try:
    from pypolyclip.version import version as __version__
except ImportError:
    __version__ = ''

from pypolyclip.pypolyclip import clip_multi, clip_single  # noqa: F401
