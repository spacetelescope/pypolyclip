import os
from glob import glob

import numpy as np
from setuptools import Extension, setup


path = ('pypolyclip',)
ext = Extension('.'.join(path) + '.polyclip',
                glob(os.path.join(*path, 'src', '*.c')),
                include_dirs=[os.path.join(*path, 'include'),
                              np.get_include()])

setup(ext_modules=[ext])
