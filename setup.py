from glob import glob
import numpy as np
import os
from setuptools import setup,Extension


def main():
    path=('pypolyclip',)

    
    ext=Extension('.'.join(path)+'.polyclip',
                  glob(os.path.join(*path,'src','*.c')),
                  include_dirs=[os.path.join(*path,'include'),
                                np.get_include()])
    
    setup(ext_modules=[ext])


if __name__=='__main__':
    main()
