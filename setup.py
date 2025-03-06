"""
Setup script for pypolyclip.
"""
import os
from glob import glob

import numpy as np
from setuptools import Extension, setup

package = 'pypolyclip'
ext = Extension(f'{package}.polyclip',
                glob(os.path.join(package, 'src', '*.c')),
                include_dirs=[os.path.join(package, 'include'),
                              np.get_include()])

setup(ext_modules=[ext])
