# -*- coding: UTF-8 -*-

"""
TODO still under dev
"""

import numpy as np
from numpy import array, asarray
from caid.cad_geometry import cad_geometry
from igakit.nurbs import NURBS

# ..........................................
class Bezier(NURBS):
    """
    this class implements a bezier patch
    a bezier patch is defined by giving a list of control points and weights

    Parameters
    ----------
    control : array_like or 2-tuple of array_like
        Control points and optional rational weights.
    fields : array_like, optional
       Additional fields.
    weights : array_like, optional
       Rational weights. If weights are omitted, the object will be
       non-rational (B-spline).

    Attributes
    ----------
    dim : int
        Parametric dimension of the NURBS object {1,2,3}
    shape : tuple of ints
        Number of control points in each parametric dimension.
    degree : tuple of ints
        Polynomial degrees in each parametric dimension.
    knots : tuple of numpy.ndarray
        Knot vectors in each parametric dimension.
    array: numpy.ndarray
        Container for control points, weights, and fields.
    control : numpy.ndarray
        Control points in homogeneous 4D space (includes rational weights).
    weigths : numpy.ndarray
        Rational weigths.
    points : numpy.ndarray
        Control points projected into Cartesian 3D space.
    fields : numpy.ndarray or None
        Additional fields.
    """
    def __init__(self, control=None, fields=None, weights=None):
        if control is not None:
            shape = control.shape
            degree = shape[:-1]
        knots = []
        for p in degree:
            u = [-1.]*p+[1.]*p
            knots.append(u)
        NURBS.__init__(self, knots, control)
# ..........................................

# ..........................................
class Beziers(object):
    """

    Parameters
    ----------


    Attributes
    ----------

    """
    def __init__(self, nrb):
        geometry = cad_geometry()
        geometry.append(nrb)
        geo_ref, list_lmatrices = geometry.bezier_extract()
        nrb_ref = geo_ref[0]
        list_lmatrices = list_lmatrices[0]
        npatchs = len(list_lmatrices)
        shape = list(list_lmatrices[0].shape)
        print(npatchs)
        print(shape)
        shape = [npatchs] + [3+1+1] + shape
        self._array = np.zeros(shape)
        for patch_id in range(0, npatchs):
            self._array[patch_id, 3, ...] = list_lmatrices[patch_id]
# ..........................................

# ..........................................
class Bezier_Patchs(object):
    """
    an abstract class that implements a container for bezier patchs

    Parameters
    ----------


    Attributes
    ----------


    """

#    def __new__(typ, *args, **kwargs):
#        obj = object.__new__(typ)
#        obj._list           = []
#        obj._currentElt     = -1

    def __init__(self, geometry=None):
        self._list = []
        self._currentElt = -1
        if geometry is not None:
            geo_ref, list_lmatrices = geometry.bezier_extract()
            for nrb in geo_ref:
                self._list.append(nrb)
#            for nrb in geometry:
#                nrb_new = nrb.clone()
#                for axis in range(0, nrb.dim):
#                    degree = nrb.degree[axis]
#                    list_t, list_m = nrb.breaks(axis=axis, mults=True)
#                    # ... remove boundaries
#                    list_t = list_t[1:-1]
#                    list_m = list_m[1:-1]
#                    for t,m in zip(list_t, list_m):
#                        times = degree - m
#                        nrb_new = nrb_new.clone().insert(axis, t, times=times)

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return self

    def __getitem__(self, key):
        return self._list[key]

    def __next__(self):
        if len(self) == 0:
            raise StopIteration
        self._currentElt += 1
        if self._currentElt >= len(self):
            self._currentElt = -1
            raise StopIteration
        return self._list[self._currentElt]

    def index(self, bezier):
        return self._list.index(bezier)

    def append(self, bezier):
        """
        append a bezier patch object in the current bezier container object.

        Args:
            bezier: a Bezier object

        Examples
        --------

        """
        self._list.append(bezier)

    def remove(self, bezier):
        """
        remove a cad_nurbs object in the current cad_geometry object. After
        removing a cad_nurbs, please do not forget to specify
        internal/external faces and the global connectivity.

        Args:
            bezier: a cad_nurbs object

        Examples
        --------


        """
        self._list.remove(bezier)
# ..........................................

if __name__ == "__main__":
    from caid.cad_geometry import line, square, trilinear
#    print (">>>>>>>>>>>>> line")
#    bezier = line(p=[2])[0]
#    bez = Bezier(control=bezier.points)
##    print bez.knots
#    print bez.shape
#    print bez.degree
#
#    print (">>>>>>>>>>>>> square")
#    bezier = square(p=[4,4])[0]
#    bez = Bezier(control=bezier.points)
##    print bez.knots
#    print bez.shape
#    print bez.degree
#
#    print (">>>>>>>>>>>>> trilinear")
#    bezier = trilinear(p=[3,3,3])[0]
#    bez = Bezier(control=bezier.points)
##    print bez.knots
#    print bez.shape
#    print bez.degree

    print (">>>>>>>>>>>>> square extraction")
    geo = square(n=[3,3], p=[2,2])
    nrb = geo[0]
#    geo_ref, list_lmatrices = geo.bezier_extract()
#    print len(list_lmatrices)
#    print geo_ref[0].shape
#
#    geo_f = geo.toBezier(0)
#    print len(geo_f)

#    bb = Bezier_Patchs(geometry=geo)
    bb = Beziers(nrb)


    print ("done")
