# pypolyclip

A python driver for [polyclip](http://tir.astro.utoledo.edu/jdsmith/code/idl.php) written in C by JD Smith.

## Installation
```
linux> pip install .
```

## Description
There are two functions that have the same outputs and only similar inputs



## Example usage
```

# import relevant modules
import pypolyclip
import numpy as np

# define the size of the pixel grid
naxis=np.array([100,100],dtype=np.uint16)


# create 3 polygons to clip... here they're quadrilaterals, but that is not a requirement

# the x-vertices of the polygon
px=np.array([[3.4,3.4,4.4,4.4],
             [3.5,3.5,4.3,4.3],
             [3.1,3.1,3.9,3.9]],dtype=float)

# the y-vertices of the polygon
py=np.array([[1.4,1.9,1.9,1.4],
             [3.7,4.4,4.4,3.7],
             [2.1,2.9,2.9,2.1]],dtype=float)


# call the clipper
xc,yc,area,slices=pypolyclip.multi(px,py,naxis)

# xc,yc are the coordinates in the grid
# area is the relative pixel area in that grid cell
# slices is a list of slice objects to link between the polygons and clipped pixel grid

# use these things like
for i,s in enumerate(slices):
	A=np.sum(areas[s])
	print(f'total area for polygon {i}={A}')

```

But see also the `test/test_pypolyclip.py` for examples.









