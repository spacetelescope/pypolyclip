# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Extension module definitions for pypolyclip.

Building against the limited API (stable ABI) is opt-in. When the
``EXTENSION_HELPERS_PY_LIMITED_API`` environment variable is set (e.g.,
to ``cp312``), extension-helpers applies the limited API settings to
these extensions. The cibuildwheel configuration in pyproject.toml sets
this variable, so release wheels target the limited API.
"""

import os
from glob import glob

import numpy as np
from setuptools import Extension

PKG_DIR = os.path.relpath(os.path.dirname(__file__))


def get_extensions():
    """
    Return the C extensions for pypolyclip.

    Returns
    -------
    extensions : list of `~setuptools.Extension`
        The extension modules to build.
    """
    sources = sorted(glob(os.path.join(PKG_DIR, 'src', '*.c')))
    include_dirs = [os.path.join(PKG_DIR, 'include'), np.get_include()]

    return [Extension('pypolyclip.polyclip', sources,
                      include_dirs=include_dirs)]
