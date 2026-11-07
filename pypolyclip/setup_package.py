# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Extension module definitions for pypolyclip.

The limited API (stable ABI) settings are applied by extension-helpers
from the ``py-limited-api`` option in pyproject.toml.
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
