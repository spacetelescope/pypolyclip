# pypolyclip

[![CI Tests](https://github.com/spacetelescope/pypolyclip/actions/workflows/ci_tests.yml/badge.svg?branch=main)](https://github.com/spacetelescope/pypolyclip/actions/workflows/ci_tests.yml) [![coverage](https://codecov.io/github/spacetelescope/pypolyclip/branch/main/graph/badge.svg?token=8xpNHaI9wD)](https://codecov.io/github/spacetelescope/pypolyclip)

A Python package to clip polygons against a pixel grid.

The polyclip functions were originally developed for the CUBISM
project [Smith et al. 2007 (PASP 119, 1133)](https://ui.adsabs.harvard.edu/abs/2007PASP..119.1133S/).

## Installation

The package can be installed using pip from the command line:
```
pip install pypolyclip
```

## Description
The [polyclip](http://tir.astro.utoledo.edu/jdsmith/code/idl.php)
code employs the [Sutherland-Hodgman
algorithm](https://en.wikipedia.org/wiki/Sutherland–Hodgman_algorithm)
to clip simple polygons against a tessellated grid of square pixels.
Therefore, this differs from similar packages, which often clip between
two arbitrary polygons.

The testing function `test/test_pypolyclip.py` can be invoked to produce
the following example figures:

<img src="docs/_static/polygons.png"  width="350" height="350">
<img src="docs/_static/quadrilaterals.png"  width="350" height="350">

In each figure, the Cartesian coordinates for each pixel that overlaps
with a given polygon are labeled with the area of that pixel that is
covered (the area of a pixel is defined as 1). Therefore, the sum of the
areas of the individual pixels for each polygon should be the total area
of the polygon.

The first figure shows clipping of polygons with differing numbers of
vertices, which internally requires the use of "for loops". However, if
the number of vertices is the same for all polygons (such as the second
figure), then [NumPy](https://numpy.org/) is used internally to improve
performance by several percent.


## Example usage
This first example demonstrates polygons with the same number of
vertices:

```
import numpy as np
from pypolyclip import clip_multi

# define the size of the pixel grid
naxis = (100, 100)

# create 3 polygons to clip

# the x-vertices of the polygon
px = np.array([[3.4, 3.4, 4.4, 4.4],
               [3.5, 3.5, 4.3, 4.3],
               [3.1, 3.1, 3.9, 3.9]])

# the y-vertices of the polygon
py = np.array([[1.4, 1.9, 1.9, 1.4],
               [3.7, 4.4, 4.4, 3.7],
               [2.1, 2.9, 2.9, 2.1]])

# call the clipper
xc, yc, area, slices = clip_multi(px, py, naxis)

# xc, yc are the grid indices with overlapping pixels.
# area is the overlapping area on a given pixel.
# slices is a list of slice objects to link between the input polygons
# and the clipped pixel grid.

# the slices object can be used to get the area of each polygon
for i, s in enumerate(slices):
    print(f'total area for polygon {i}={np.sum(area[s])}')
```

This second example demonstrates clipping polygons that have a different
number of vertices.  Note that `px` and `py` are lists of lists instead
of NumPy arrays as in the first example.

```
import numpy as np
from pypolyclip import clip_multi

# define the size of the pixel grid
naxis = (100, 100)

# create 3 polygons to clip

# the x-vertices of the polygon
px = [[3.4, 3.4, 4.4, 4.8, 4.4],
      [3.5, 3.5, 4.3, 4.3],
      [3.1, 3.8, 3.1]]

# the y-vertices of the polygon
py = [[1.4, 1.9, 1.9, 1.65, 1.4],
      [3.7, 4.4, 4.4, 3.7],
      [2.1, 2.1, 3.4]]

# call the clipper
xc, yc, area, slices = clip_multi(px, py, naxis)

# xc, yc are the grid indices with overlapping pixels.
# area is the overlapping area on a given pixel.
# slices is a list of slice objects to link between the input polygons
# and the clipped pixel grid.

# the slices object can be used to get the area of each polygon
for i, s in enumerate(slices):
    print(f'total area for polygon {i}={np.sum(area[s])}')
```

See also `test/test_pypolyclip.py` for examples.
