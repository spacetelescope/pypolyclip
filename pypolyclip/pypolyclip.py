import numpy as np

from . import polyclip

# NEVER CHANGE THESE WITHOUT ADDRESSING DATATYPES INSIDE THE C CODE
INT = np.int32
FLT = np.float32


def clip_multi(x, y, nxy):
    """
    Clip multiple polygons against a tessellated grid of square pixels.

    Parameters
    ----------
    x : 2D array-like of float
        The x coordinates of the polygon corners as a 2D array. Each row
        represents a separate polygon.

    y : 2D array-like of float
        The y coordinates of the polygon corners as a 2D array. Each row
        represents a separate polygon.

    nxy : list, tuple, or `np.ndarray` of 2 int
        The size of the pixel grid.

    Returns
    -------
    xx : 2D `np.ndarray` of int
        The x-pixel indices that have overlapping area. Each row
        represents a separate polygon

    yy : 2D `np.ndarray` of int
        The y-pixel indices that have overlapping area. Each row
        represents a separate polygon.

    areas : 1D `np.ndarray` of float
        The overlapping area on a given pixel.

    slices : list of slice objects
        A list of slice objects that maps between the input and output
        coordinates. The length of the list is equal to the number of
        input polygons.

    Notes
    -----
    This is a Python driver to call JD Smith's polyclip.c code.

    This function does not validate that the input polygons are
    valid. One way to check for valid polygons is to use the `Shapely
    <https://shapely.readthedocs.io/en/stable/>`_ package::

        >>> from shapely.geometry import Polygon
        >>> print(Polygon(zip(xv, yv)).is_valid)

    where ``xv`` and ``yv`` are the x and y vertices of a single
    polygon.

    The ``xx``, ``yy``, and ``areas`` output arrays will always have the
    same length. However, ``slices`` will have the same length as the
    number of input polygons.

    If ``x`` and ``y`` are input as a list or tuple, then they are
    assumed to be a list of polygons, which can have an arbitrary number
    of vertices. If ``x`` and ``y`` are input as `~np.array` objects,
    then it is assumed that all of the polygons have the same number of
    vertices. In that case, NumPy vectorization can be used to improve
    performance.
    """
    # must find the bounding boxes for each pixel
    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        # if here, then the inputs are numpy arrays, and so the polygons
        # all have the same number of vertices.  Therefore, we can use
        # numpy operations to do many calculations
        l = np.clip(np.floor(np.amin(x, axis=1)), 0, nxy[0]).astype(INT)  # noqa: E741
        r = np.clip(np.floor(np.amax(x, axis=1)), 0, nxy[0]).astype(INT)
        b = np.clip(np.floor(np.amin(y, axis=1)), 0, nxy[1]).astype(INT)
        t = np.clip(np.floor(np.amax(y, axis=1)), 0, nxy[1]).astype(INT)

        # make some polygon indices
        npoly = x.shape[0]
        indices = np.linspace(0, x.size, npoly + 1, dtype=INT)
    elif isinstance(x, (tuple, list)) and isinstance(y, (tuple, list)):
        # if here, then the inputs are a list, which can permit polygons
        # to have differing number of vertices (such as a triangle and a
        # quadrilateral).  Therefore, we must explicitly loop over the
        # polygons --- which is more costly, but more general.
        npoly = len(x)
        l = np.empty(npoly, dtype=INT)  # noqa: E741
        r = np.empty(npoly, dtype=INT)
        b = np.empty(npoly, dtype=INT)
        t = np.empty(npoly, dtype=INT)
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
    polyclip.multi(l, r, b, t,
                   np.hstack(x).astype(FLT),
                   np.hstack(y).astype(FLT),
                   npoly, indices, xx, yy, nclip, areas)

    # create a list of slices objects from returned indices
    slices = [slice(indices[i], indices[i + 1], 1) for i in range(npoly)]

    # trim the results
    nclip = nclip[0]  # undo that C-gotcha above :(
    areas = areas[:nclip]
    xx = xx[:nclip]
    yy = yy[:nclip]

    return xx, yy, areas, slices


def clip_single(x, y, nxy, return_polygons=False):
    """
    Clip a single polygon against a tessellated grid of square pixels.

    Parameters
    ----------
    x : 1D array-like of float
        The x coordinates of the polygon corners.

    y : 1D array-like of float
        The y coordinates of the polygon corners.

    nxy : list, tuple, or `np.ndarray` of 2 int
        The size of the pixel grid.

    return_polygons : bool, optional
        If `True`, then the ``px`` and ``py`` arrays that describe the
        coordinates of the clipped polygons will also be returned.
        Default = False

    Returns
    -------
    xx : 1D `np.ndarray` of int
        The x-pixel indices that have overlapping area.

    yy : 1D `np.ndarray` of int
        The x-pixel indices that have overlapping area.

    areas : 1D `np.ndarray` of float
        The overlapping area on a given pixel.

    slices : list of slice objects
        A list of slice objects that maps between the input and output
        coordinates.

    px : list of 1D float `np.ndarray`
        The x-pixel coordinates of the clipped polygons. Each element of
        the list contains a 1D `np.array` that represents the polygon
        vertices. Only returned if ``return_polygons=True``.

    py : list of 1D float `np.ndarray`
        The y-pixel coordinates of the clipped polygons. Each element of
        the list contains a 1D `np.array` that represents the polygon
        vertices. Only returned if ``return_polygons=True``.

    Notes
    -----
    This is a Python driver to call JD Smith's polyclip.c code.

    This function does not validate that the input polygons are
    valid. One way to check for valid polygons is to use the `Shapely
    <https://shapely.readthedocs.io/en/stable/>`_ package::

        >>> from shapely.geometry import Polygon
        >>> print(Polygon(zip(xv, yv)).is_valid)

    where ``xv`` and ``yv`` are the x and y vertices of a single
    polygon.

    The ``xx``, ``yy``, and ``areas`` output arrays will always have the
    same length. However, ``slices`` will have the same length as the
    number of input polygons.
    """
    # compute bounding box for the pixel
    l = np.asarray(np.clip(np.floor(np.amin(x)), 0, nxy[0]), dtype=INT)  # noqa: E741
    r = np.asarray(np.clip(np.floor(np.amax(x)), 0, nxy[0]), dtype=INT)
    b = np.asarray(np.clip(np.floor(np.amin(y)), 0, nxy[1]), dtype=INT)
    t = np.asarray(np.clip(np.floor(np.amax(y)), 0, nxy[1]), dtype=INT)

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

    # call the polygon clipper
    polyclip.single(l, r, b, t,
                    np.asarray(x, dtype=FLT),
                    np.asarray(y, dtype=FLT),
                    nverts, px_out, py_out, inds, nclip, areas, ri_out)

    # extract data
    nclip = nclip[0]
    xx = inds[:nclip, 0]
    yy = inds[:nclip, 1]
    areas = areas[:nclip]

    # return a dummy set of indices, so that this output looks like
    # the output for the clip_multi function
    slices = [slice(0, len(xx), 1)]

    if return_polygons:
        px = []
        py = []
        pmax = ri_out[nclip]
        pind = ri_out[:pmax]
        for i in range(len(pind) - 1):
            s = slice(pind[i], pind[i + 1], 1)

            px.append(px_out[s])
            py.append(py_out[s])

        return xx, yy, areas, slices, px, py
    else:
        return xx, yy, areas, slices
