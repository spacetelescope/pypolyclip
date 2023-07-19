import numpy as np

from . import polyclip


# NEVER CHANGE THESE WITHOUT ADDRESSING DATATYPES INSIDE THE C CODE
INT = np.int32
FLT = np.float32


def multi(x, y, nxy):
    """
    Function to call the multi-polygon clipping of JD Smith

    Parameters
    ----------
    x : `np.ndarray` or list of lists
        The x coordinates of the polygon corners (dtype of int or float)

    y : `np.ndarray` or list of lists
        The y coordinates of the polygon corners (dtype of int or float)

    nxy : list, tuple, or `np.ndarray`
        The size of the pixel grid.

    Returns
    -------
    xx : `np.ndarray`
        The x-pixel coordinates that have area (will be `int` dtype)

    yy : `np.ndarray`
        The y-pixel coordinates that have area (will be `int` dtype)

    areas : `np.ndarray`
        The area projected onto a given pixel (will be `float` dtype)

    slices : list
        a list of slice objects that will map between the input and
        output coordinates.

    Notes
    -----
    1) This is a Python driver to call JD Smith's polyclip.c code.
    2) Definitionally, there will be an equal number of elements to the
       output arrays xx, yy, and areas.  However, slices will have the
       same length as the number of input polygons, which is in general,
       different than the number of elements of xx (or yy or areas).
    3) If x/y are passed as a list or tuple, then they are assumed to a
       list of polygons, which can have an arbitrary number of vertices.
       If x/y are passed as a np.arrays, then it is assumed that all of
       the polygons have the same number of vertices.  In which case,
       np functions and explicit loops are avoided, so this will be slightly
       faster (at loss of generality).
    """

    # must find the bounding boxes for each pixel
    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        # if here, then the inputs are numpy arrays, and so the polygons
        # all have the same number of vertices.  Therefore, we can use
        # numpy operations to do many calculations
        l = np.clip(np.floor(np.amin(x, axis=1)), 0, nxy[0]).astype(INT)  # noqa
        r = np.clip(np.floor(np.amax(x, axis=1)), 0, nxy[0]).astype(INT)  # noqa
        b = np.clip(np.floor(np.amin(y, axis=1)), 0, nxy[1]).astype(INT)  # noqa
        t = np.clip(np.floor(np.amax(y, axis=1)), 0, nxy[1]).astype(INT)  # noqa

        # make some polygon indices
        npoly = x.shape[0]
        indices = np.linspace(0, x.size, npoly + 1, dtype=INT)
    elif isinstance(x, (tuple, list)) and isinstance(y, (tuple, list)):
        # if here, then the inputs are a list, which can permit polygons
        # to have differing number of vertices (such as a triangle and a
        # quadrilateral).  Therefore, we must explicitly loop over the
        # polygons --- which is more costly, but more general.
        npoly = len(x)
        l = np.empty(npoly, dtype=INT)  # noqa
        r = np.empty(npoly, dtype=INT)  # noqa
        b = np.empty(npoly, dtype=INT)  # noqa
        t = np.empty(npoly, dtype=INT)  # noqa
        indices = np.empty(npoly + 1, dtype=INT)
        indices[0] = 0
        for i, (_x, _y) in enumerate(zip(x, y)):
            l[i] = np.clip(np.floor(np.amin(_x)), 0, nxy[0])
            r[i] = np.clip(np.floor(np.amax(_x)), 0, nxy[0])
            b[i] = np.clip(np.floor(np.amin(_y)), 0, nxy[1])
            t[i] = np.clip(np.floor(np.amax(_y)), 0, nxy[1])
            indices[i + 1] = indices[i] + len(_x)
    else:
        raise TypeError("Invalid types for the input polygons.")

    # maximum number of pixels that could be affected
    npix = sum((r - l + 1) * (t - b + 1))

    # the number of output pixels must be an array (this is a C-gotcha)
    nclip = np.zeros(1, dtype=INT)

    # output arrays
    areas = np.empty(npix, dtype=FLT)
    xx = np.empty(npix, dtype=INT)
    yy = np.empty(npix, dtype=INT)

    # call the compiled C-code
    polyclip.multi(
        l,
        r,
        b,
        t,
        np.hstack(x).astype(FLT),
        np.hstack(y).astype(FLT),
        npoly,
        indices,
        xx,
        yy,
        nclip,
        areas,
    )

    # make the polyinds a python slice objects
    slices = [slice(indices[i], indices[i + 1], 1) for i in range(npoly)]

    # trim the results
    nclip = nclip[0]  # undo that C-gotcha above :(
    areas = areas[:nclip]
    xx = xx[:nclip]
    yy = yy[:nclip]

    return xx, yy, areas, slices


def single(x, y, nxy):
    """
    Function to call the multi-polygon clipping of JD Smith

    Parameters
    ----------
    x : int or float
        The x coordinates of the polygon corners

    y : int or float
        The y coordinates of the polygon corners

    nxy : list, tuple, or `np.ndarray`
           The size of the pixel grid.

    Returns
    -------
    xx : `np.ndarray`
        The x-pixel coordinates that have area (will be `int` dtype)

    yy : `np.ndarray`
        The y-pixel coordinates that have area (will be `int` dtype)

    areas : `np.ndarray`
        The area projected onto a given pixel (will be `float` dtype)

    slice : list
        a slice object that will map between the input and output
        coordinates. This is *ONLY* returned for consistency between
        the companion function `multi()`.

    Notes
    -----
    This is a Python driver to call JD Smith's polyclip.c code.

    """

    # compute bounding box for the pixel
    l = np.asarray(np.clip(np.floor(np.amin(x)), 0, nxy[0]), dtype=INT)  # noqa
    r = np.asarray(np.clip(np.floor(np.amax(x)), 0, nxy[0]), dtype=INT)  # noqa
    b = np.asarray(np.clip(np.floor(np.amin(y)), 0, nxy[1]), dtype=INT)  # noqa
    t = np.asarray(np.clip(np.floor(np.amax(y)), 0, nxy[1]), dtype=INT)  # noqa

    # get number of vertices for the polygon.  The C-code is expecting
    # this to be an array
    nverts = np.full(1, len(x), dtype=INT)  # np.array([len(x)], dtype=INT)

    # number of pixels that might be affected
    npix = (r - l + 1) * (t - b + 1)

    # recast some things for C
    nclip = np.zeros(1, dtype=INT)

    # output polygon indices
    px_out = np.empty((nverts[0] + 24) * npix, dtype=FLT)
    py_out = np.empty((nverts[0] + 24) * npix, dtype=FLT)

    # main outputs (area, pixel coords and reverse indices)
    areas = np.empty(npix, dtype=FLT)
    inds = np.empty((npix, 2), dtype=INT)
    ri_out = np.empty(npix + 1, dtype=INT)

    # call the pologyon clipper
    polyclip.single(
        l,
        r,
        b,
        t,
        np.asarray(x, dtype=FLT),
        np.asarray(y, dtype=FLT),
        nverts,
        px_out,
        py_out,
        inds,
        nclip,
        areas,
        ri_out,
    )

    # extract data
    nclip = nclip[0]
    # px_out = px_out[:nclip]
    # py_out = py_out[:nclip]
    # ri_out = ri_out[:nclip]

    # main outputs
    xx = inds[:nclip, 0]
    yy = inds[:nclip, 1]
    areas = areas[:nclip]

    # return a dummy set of indices, so that this output looks like
    # the output for the multi function
    slices = [slice(0, len(xx), 1)]

    return xx, yy, areas, slices
