import pypolyclip
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def test_multi_numpy(plot=False):
    """A module to test clipping multiple polygons in a single pass."""

    # define the size of the pixel grid
    # naxis=np.array((100,100),dtype=int)
    naxis = (100, 100)

    # create 6 polygons to clip... here they're an irregular quadralateral, but
    # this isn't a requirement
    px = np.array(
        [
            [3.4, 3.4, 4.4, 4.4],
            [3.5, 3.5, 4.3, 4.3],
            [3.1, 3.1, 3.9, 3.9],
            [8.0, 8.0, 9.0, 9.0],
            [5.8, 6.2, 6.3, 5.6],
            [5.8, 5.8, 7.2, 7.2],
        ]
    )

    py = np.array(
        [
            [1.4, 1.9, 1.9, 1.4],
            [3.7, 4.4, 4.4, 3.7],
            [2.1, 2.9, 2.9, 2.1],
            [8.0, 8.0, 9.0, 9.0],
            [1.5, 1.8, 2.4, 1.9],
            [3.8, 5.2, 5.2, 3.8],
        ]
    )

    # compare the area expected by the shoelace algorithm
    A = _area(px, py, axis=1)

    # call the clipping
    # xc,yc are the coordinates in the grid
    # area is the relative pixel area in that grid cell
    # slices is a list of slice objects to apply to the xc,yc,area arrays
    xc, yc, area, slices = pypolyclip.multi(px, py, naxis)

    # compute the total area by summing over all the pixels for each polygon
    A0 = np.asarray([np.sum(area[s]) for s in slices], dtype=float)

    # these are the correct values
    xc0 = np.array(
        [3, 4, 3, 3, 4, 4, 3, 5, 5, 6, 6, 5, 5, 5, 6, 6, 6, 7, 7, 7], dtype=np.uint32
    )
    yc0 = np.array(
        [1, 1, 3, 4, 3, 4, 2, 1, 2, 1, 2, 3, 4, 5, 3, 4, 5, 3, 4, 5], dtype=np.uint32
    )
    area0 = np.array([0.3, 0.2, 0.15, 0.2, 0.09, 0.12, 0.64, 0.138,
                      0.02414287, 0.0583333, 0.07452378, 0.04, 0.2, 0.04,
                      0.2, 1., 0.2, 0.04, 0.2, 0.04], dtype=np.float32)
    slices0 = [
        slice(0, 2, 1),
        slice(2, 6, 1),
        slice(6, 7, 1),
        slice(7, 7, 1),
        slice(7, 11, 1),
        slice(11, 20, 1),
    ]

    # show how one can use the slices
    lam = np.empty_like(xc, dtype=np.uint16)
    for i, s in enumerate(slices):
        lam[s] = i
    # apply assertion tests
    assert np.allclose(xc, xc0), "X-positions are not equal"
    assert np.allclose(yc, yc0), "Y-positions are not equal"
    assert np.allclose(area, area0), "Areas are not equal"
    assert slices == slices0, "Slices are not equal"
    assert np.allclose(A, A0), "Sum of areas are not equal"

    if plot:
        _plot(px, py, xc, yc, area, slices, filename="quadrilaterals.png")


def test_multi_list(plot=False):
    """A module to test clipping multiple polygons in a single pass."""

    # define the size of the pixel grid
    naxis = (100, 100)

    # create a bunch of polygons, these will hold the vertices and areas
    px = []
    py = []
    A = []

    # create a square
    xx, yy = _polygon(4, radius=1, x0=4.6, y0=3, theta0=76.0)
    px.append(xx)
    py.append(yy)
    A.append(_area(xx, yy))

    # create a pentagon
    xx, yy = _polygon(5, radius=1, x0=4.8, y0=5.6, theta0=31.0)
    px.append(xx)
    py.append(yy)
    A.append(_area(xx, yy))

    # create a star
    xx, yy = _polygon(-5, radius=2, x0=8.4, y0=2.6, theta0=23.0)
    px.append(xx)
    py.append(yy)
    A.append(_area(xx, yy))

    # create a "circle"
    xx, yy = _polygon(1000, radius=1, x0=7.9, y0=6.8, theta0=23.0)
    px.append(xx)
    py.append(yy)
    A.append(_area(xx, yy))

    # create a right triangle
    xx, yy = [3.5, 4.6, 3.5], [0.4, 0.4, 1.8]
    px.append(xx)
    py.append(yy)
    A.append(_area(xx, yy))

    # clip against the pixel grid
    xc, yc, area, slices = pypolyclip.multi(px, py, naxis)

    # compute the total area by summing over all the pixels for each polygon
    A0 = np.asarray([np.sum(area[s]) for s in slices], dtype=float)

    # the correct values
    xc0 = [3, 3, 4, 4, 5, 5, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 7, 7, 7, 8, 8,
           8, 8, 8, 9, 9, 9, 9, 10, 6, 6, 7, 7, 7, 8, 8, 8, 3, 3, 4, 4]

    yc0 = [2, 3, 2, 3, 2, 3, 5, 4, 5, 6, 4, 5, 6, 1, 2, 1, 2, 3, 4, 0, 1, 2,
           3, 4, 1, 2, 3, 4, 2, 6, 7, 5, 6, 7, 5, 6, 7, 0, 1, 0, 1]
    area0 = [0.04210257, 0.11319429, 0.73980240, 0.7365468, 0.21809514,
             0.15025878, 0.05417120, 0.17991099, 0.9576262, 0.34914187,
             0.06675320, 0.60335850, 0.16667908, 0.07140104, 0.04707969,
             0.2457072,  0.8243331,  0.6631042, 0.012714,   0.07671321,
             0.8113126,  1.00000000, 0.7673367,  0.0011166, 0.06346372,
             0.79520196, 0.36266422, 0.07165156, 0.06405382, 0.0478719,
             0.01064858, 0.10141449, 0.95417684, 0.655588, 0.06179164,
             0.80204993, 0.50661606, 0.3, 0.24090907, 0.21857142, 0.01051948]
    slices0 = [
        slice(0, 6, 1),
        slice(6, 13, 1),
        slice(13, 29, 1),
        slice(29, 37, 1),
        slice(37, 41, 1),
    ]

    # apply assertion tests
    assert np.allclose(xc, xc0), "X-positions are not equal"
    assert np.allclose(yc, yc0), "Y-positions are not equal"
    assert np.allclose(area, area0, atol=1e-3), "Areas are not equal"
    assert slices == slices0, "Slices are not equal"
    assert np.allclose(A, A0), "Sum of areas are not equal"

    if plot:
        _plot(px, py, xc, yc, area, slices, filename="polygons.png")


def test_single(plot=False):
    """A module to test clipping a single polygon."""

    # define the size of the pixel grid
    naxis = np.array((100, 100), dtype=int)

    # create a polygon
    px = np.array([8.5, 10.5, 10.5, 11.5, 12.0, 12.5, 13.5, 14.5, 15.0,
                   14.0, 13.5, 13.0, 13.0, 12.0, 9.5, 4.5, 2.5, 1.0, 0.75,
                   1.5, 1.75, 1.5, 2.0, 3.5, 3.0, 3.5, 3.5, 4.0, 5.5, 5.0,
                   5.5, 8.5])
    py = np.array([1.0, 1.0, 4.5, 6.0, 5.5, 3.5, 2.5, 3.0, 4.0, 4.0, 3.75,
                   4.5, 8.0, 10.0, 10.0, 10.5, 10.0, 8.5, 3.0, 6.0, 4.5,
                   2.5, 1.0, 1.0, 2.5, 3.5, 2.0, 1.0, 1.0, 2.5, 4.0, 4.0])

    # call the clipping
    xc, yc, area, slices = pypolyclip.single(px, py, naxis)

    # these are the expected values
    xc0 = np.array([0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  1,
                    1,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  3,  3,  3,
                    3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  4,  4,
                    4,  4,  4,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  6,
                    6,  6,  6,  6,  6,  6,  7,  7,  7,  7,  7,  7,  7,  8,
                    8,  8,  8,  8,  8,  8,  8,  8,  8,  9,  9,  9,  9,  9,
                    9,  9,  9,  9,  9, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                    11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 13, 13,
                    13, 14, 14], dtype=np.int32)
    yc0 = np.array([3,  4,  5,  6,  7,  8,  1,  2,  3,  4,  5,  6,  7,  8,
                    9,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10,  1,  2,  3,
                    4,  5,  6,  7,  8,  9, 10,  1,  2,  3,  4,  5,  6,  7,
                    8,  9, 10,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10,  4,
                    5,  6,  7,  8,  9, 10,  4,  5,  6,  7,  8,  9, 10,  1,
                    2,  3,  4,  5,  6,  7,  8,  9, 10,  1,  2,  3,  4,  5,
                    6,  7,  8,  9, 10,  1,  2,  3,  4,  5,  6,  7,  8,  9,
                    5,  6,  7,  8,  9,  3,  4,  5,  6,  7,  8,  9,  2,  3,
                    4,  2,  3], dtype=np.int32)
    A0 = np.array([0.10227275, 0.18181816, 0.13636366, 0.09090909, 0.04545453,
                   0.00568181, 0.16666669, 0.44270834, 0.375, 0.41145834,
                   0.7916667, 1., 1., 0.875, 0.125,
                   1., 1., 1., 1., 1.,
                   1., 1., 1., 0.875, 0.03125,
                   0.5833334, 0.6041667, 0.9375, 1., 1.,
                   1., 1., 1., 1., 0.25,
                   1., 1., 1., 1., 1.,
                   1., 1., 1., 1., 0.45624995,
                   0.33333325, 0.08333325, 0.33333325, 1., 1.,
                   1., 1., 1., 1., 0.39999962,
                   1., 1., 1., 1., 1.,
                   1., 0.3000002, 1., 1., 1.,
                   1., 1., 1., 0.19999981, 0.5,
                   0.5, 0.5, 1., 1., 1.,
                   1., 1., 1., 0.0999999, 1.,
                   1., 1., 1., 1., 1.,
                   1., 1., 1., 0.01250005, 0.5,
                   0.5, 0.5, 0.58333325, 0.9791666, 1.,
                   1., 1., 1., 0.3125, 1.,
                   1., 1., 1., 0.40625, 0.75,
                   0.96875, 1., 1., 0.75, 0.25,
                   0.3125, 0.9166666, 0.08333325, 0.0625, 0.75],
                  dtype=np.float32)
    slices0 = [slice(0, 115, 1)]

    # xc,yc are the coordinates in the grid
    # area is the relative pixel area in that grid cell
    # for the single, there is no notion of the polyindices

    # apply assertion tests
    assert np.allclose(xc, xc0), "X-positions are not equal"
    assert np.allclose(yc, yc0), "Y-positions are not equal"
    assert np.allclose(area, A0), "Areas are not equal"
    assert slices == slices0, "Slices are not equal"

    if plot:
        _plot(px[np.newaxis, ...], py[np.newaxis, ...], xc, yc, area, slices)


def _area(px, py, axis=None):
    """
    Implement the shoelace formula for area of a simple polygon

    Parameters
    ----------
    px : `np.ndarray`
       the x-positions of the vertices

    py : `np.ndarray`
       the y-positions of the vertices

    axis : int, optional
       the axis over the indices to sum over.  See `np.sum()` for more info.
       Default is None.

    Returns
    -------
    A : `np.ndarray`
       The areas based on shoelace algorithm

    Notes
    -----
    https://en.wikipedia.org/wiki/Shoelace_formula

    """
    A = 0.5 * np.abs(
        np.sum(px * np.roll(py, 1, axis=axis), axis=axis)
        - np.sum(py * np.roll(px, 1, axis=axis), axis=axis)
    )
    return A


def _polygon(nvert, radius=1, factor=2, theta0=0.0, x0=0.0, y0=0.0):
    """
    Module to make polygon vertices

    Parameters
    ----------
    nvert : int
        The number of vertices to have.  If negative, then will create a
        star-polygon.  Must have: abs(nvert) >= 3.

    radius : float, optional
        The size of the polygon.  Default is 1

    factor : float, optional
        The factor to reduce the radius for alternating points in the star
        polygons.  default is 2

    theta0 : float, optional
        The rotation of the polygon in degrees.  Default is 0.

    x0 : float, optional
        The x-center of the polygon.  Default is 0.

    y0 : float, optional
        The y-center of the polygon.  Default is 0.

    Returns
    -------
    x : list
        The x-coordinates of the vertices

    y : list
        The y-coordinates of the vertices

    Notes
    -----
    https://en.wikipedia.org/wiki/Star_polygon

    """

    if nvert < -2:
        # make a star polygon
        nvert = 2 * np.abs(nvert)
        i = np.arange(0, nvert, 2, dtype=int)

        theta = np.arange(0, 2 * np.pi, 2 * np.pi / nvert) + theta0 * np.pi / 180.0
        radius = np.full_like(theta, radius)
        radius[i] /= factor
    elif nvert > 2:
        # make a simple convex polygon
        theta = np.arange(0, 2 * np.pi, 2 * np.pi / nvert) + theta0 * np.pi / 180.0
    else:
        raise ValueError("Cannot make polygon with fewer than 2 vertices.")
    # compute the coordinates
    x = radius * np.cos(theta) + x0
    y = radius * np.sin(theta) + y0

    # return as lists
    return list(x), list(y)


def _plot(px, py, xc, yc, areas, slices, seed=1618033988, alpha=0.2, filename=None, show=True):
    """
    Helper function to plot the results from pypolyclip

    Parameters
    ----------
    px : `np.ndarray'
       x-vertices of polygons

    py : `np.ndarray'
       y-vertices of polygons

    xc : `np.ndarray'
       x pixels in the clipped space

    yc : `np.ndarray'
       y pixels in the clipped space

    areas : `np.ndarray`
       pixel areas in the clipped space

    slices : list
       a list of slice objects to link the clipped space to the polygon

    seed : int, optional
       seed to set the random colors, default is 1618033988

    alpha : float, optional
       the alpha graphics setting, default is 0.2

    show : bool, optional
       flag to show the plot to the screen.  Default is True

    filename : str, optional
       a name to output a file.  Default is None (ie no file written)

    """

    # initialize the Random seed
    np.random.seed(seed)

    # make a canvas of a certain size
    figsize = (
        np.ceil(np.amax(xc)) - np.floor(np.amin(xc)),
        np.ceil(np.amax(yc)) - np.floor(np.amin(yc)),
    )

    # deal with really oblique figures
    if np.amin(figsize) <= 5:
        figsize = (figsize[0] * 2, figsize[1] * 2)
    # make some plots and get some numbers
    _, ax = plt.subplots(figsize=figsize)

    # set initial values of plot ranges
    xmin, xmax = np.inf, 0
    ymin, ymax = np.inf, 0

    # plot each region
    for xx, yy, ss in zip(px, py, slices):
        # get the random color, area, and vertices for each region
        color = np.random.rand(3)
        A = np.sum(areas[ss])
        xy = np.column_stack((xx, yy))

        # draw the region as a Patch
        patch = Polygon(xy, color=color, alpha=alpha, label=f"{A:.2f}")
        ax.add_patch(patch)

        # plot the vertices
        for x, y, a in zip(xc[ss], yc[ss], areas[ss]):
            plt.text(
                x + 0.5,
                y + 0.5,
                f"({x},{y})\n{a:.2f}",
                color=color,
                ha="center",
                va="center",
            )

            # update the plot ranges
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)
    # put a legend in the figure
    ax.legend(title=r"Areas", loc="upper left")

    # relabel the tick marks
    xticks = np.arange(xmin, xmax + 1, dtype=int)
    ax.xaxis.set_ticks(xticks)

    yticks = np.arange(ymin, ymax + 1, dtype=int)
    ax.yaxis.set_ticks(yticks)

    # put on a grid
    ax.grid(which="major")

    # label axes
    ax.set_xlabel("X (pixels)")
    ax.set_ylabel("Y (pixels)")

    # set the ranges
    ax.set_xlim(np.amin(xc) - 0.5, np.amax(xc) + 1)
    ax.set_ylim(np.amin(yc) - 0.5, np.amax(yc) + 1)

    # write file if requested
    if filename is not None:
        plt.savefig(filename)
    # ok... show the plot
    if show:
        plt.show()


if __name__ == "__main__":
    test_multi_list(plot=True)
    test_multi_numpy(plot=True)
    test_single(plot=True)
