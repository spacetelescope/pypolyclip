# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Setup script for pypolyclip.
"""
import os
from glob import glob

import numpy as np
from setuptools import Extension, setup

package = 'pypolyclip'

# Build against the Python limited API (stable ABI) for Python 3.12+
# so that a single abi3 wheel works on all supported Python versions.
# The wheel tag is set by "py-limited-api" in pyproject.toml.
ext = Extension(f'{package}.polyclip',
                glob(os.path.join(package, 'src', '*.c')),
                include_dirs=[os.path.join(package, 'include'),
                              np.get_include()],
                define_macros=[('Py_LIMITED_API', '0x030C0000')],
                py_limited_api=True)

setup(ext_modules=[ext])
