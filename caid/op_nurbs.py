# -*- coding: utf-8 -*-

from igakit.nurbs import NURBS
from numpy import sqrt, zeros

class opNURBS(object):
    """
    this class implements a generic differential operator applied to a NURBS
    object.
    """
    def __init__(self, nrb):
        """
        creates a gradiant map from a NURBS object
        """

        self._nrb = nrb

    @property
    def dim(self):
        """
        Parametric dimension of the opNURBS object {1,2,3}.
        """
        return self._nrb.dim

    @property
    def shape(self):
        """
        Shape of the control point net. Also the number of
        basis functions in each parametric direction.
        """
        return self._nrb.shape

    @property
    def degree(self):
        """
        Polynomial degrees for each parametric direction.
        """
        return self._nrb.degree

    @property
    def knots(self):
        """
        Knot vectors for each parametric dimension.
        """
        return self._nrb.knots

    @property
    def array(self):
        """
        Container for control points, weights, and fields.
        """
        return self._nrb.array

    @property
    def control(self):
        """
        Control point grid in homogeneous 4D space.
        """
        return self._nrb.control

    @property
    def weights(self):
        """
        Rational weight grid.
        """
        return self._nrb.weights

    @property
    def points(self):
        """
        Control point grid projected into Cartesian 3D space.
        """
        return self._nrb.points

    def set_points(self, pts):
        """
        Sets the Control point grid projected into Cartesian 3D space.
        """
        self._nrb.set_points(pts)

    @property
    def fields(self):
        """
        Control variables.
        """
        return self._nrb.fields

    def spans(self, axis=None):
        """
        Non-empty span indices.
        """
        return self._nrb.spans(axis=axis)


    def breaks(self, axis=None):
        """
        Breaks (unique knot values).
        """
        return self._nrb.breaks(axis=axis)

    def copy(self):
        """
        Copy a opNURBS object.

        Returns a new instace of the NURBS objects with copies of the
        control points and knot vectors. Modifying the knot vector or
        control points of the returned object WILL NOT affect this
        object.

        Examples
        --------

        Create a random curve, copy the curve, change the control points,
        demonstrate that now c1 and c2 are different.

        >>> C = np.random.rand(5,3)
        >>> U = [0,0,1,2,3,4,4]
        >>> nrb = NURBS([U], C)
        >>> c1 = grad(nrb)
        >>> c2 = c1.copy()
        >>> c2.control[2,:] = [1.0,1.0,0.0,1.0]
        >>> print np.allclose(c1.control, c2.control, rtol=0, atol=1e-15)

        """
        gnrb = opNURBS.__new__(type(self))
        gnrb._nrb = self._nrb.copy()
        return gnrb

    def clone(self):
        """
        Clone a opNURBS object.

        Returns a new instace of the opNURBS objects with references to
        the control points and knot vectors of this opNURBS
        object. Modifying the knot vector or control points of the
        returned object WILL affect this object.

        Examples
        --------

        Create a random curve, copy the curve, change the control points,
        demonstrate that changing c2 changes c1.

        >>> C = np.random.rand(5,3)
        >>> U = [0,0,1,2,3,4,4]
        >>> nrb = NURBS([U], C)
        >>> c1 = grad(nrb)
        >>> c2 = c1.clone()
        >>> c2.control[2,:] = [1.0,1.0,0.0,1.0]
        >>> print np.allclose(c1.control, c2.control, rtol=0, atol=1e-15)

        """
        gnrb = opNURBS.__new__(type(self))
        gnrb._nrb = self._nrb.clone()
        return gnrb

    def transform(self, trans):
        """
        Apply a scaling, rotation, or a translation to a opNURBS object.

        A opNURBS object can be scaled, rotated, or translated by
        applying the tranformation to the control points. To contruct
        composite transformations, consult the docstrings in
        :mod:`igakit.transform`.

        Parameters
        ----------
        trans : array_like
            a matrix or transformation which scales, rotates,
            and/or translates a NURBS object.

        """
        self._nrb.transform(trans)
        return self

    def translate(self, displ, axis=None):
        self._nrb.translate(displ, axis=axis)
        return self

    def move(self, displ, axis=None):
        self._nrb.move(displ, axis=axis)
        return self

    def scale(self, scale, axis=None):
        self._nrb.translate(scale, axis=axis)
        return self

    def rotate(self, angle, axis=2):
        self._nrb.translate(angle, axis=axis)
        return self

    def transpose(self, axes=None):
        """
        Permute the axes of a NURBS object.

        Permute parametric axes with the given ordering and adjust the
        control points accordingly.

        Parameters
        ----------
        axes : sequence of ints, optional
            By default, reverse order of the axes, otherwise permute
            the axes according to the values given.

        Examples
        --------

        Create a random B-spline volume, swap the 2nd and 3rd axes,
        evaluate and check.

        >>> C = np.random.rand(4,3,3)
        >>> U = [0,0,0,0,1,1,1,1]
        >>> V = [0,0,0,1,1,1]
        >>> nrb  = NURBS([U,V], C)
        >>> srf1 = grad(nrb)
        >>> srf2 = srf1.clone().transpose([1,0])
        >>> u = 0.25; v = 0.50
        >>> xyz1 = srf1(u,v)
        >>> xyz2 = srf2(v,u)
        >>> print [np.allclose(xyz1[i], xyz2[i], rtol=0, atol=1e-12) for i in range(0, len(xyz1))]

        """
        self._nrb.transpose(axes=axes)
        return self

    def swap(self, axis1, axis2):
        """
        Interchange two parametric axes of NURBS object.

        Parameters
        ----------
        axis1 : int
            First axis.
        axis2 : int
            Second axis.

        Examples
        --------

        Create a random B-spline surface,
        swap the first and last axes, evaluate and check.

        >>> C = np.random.rand(4,3,3)
        >>> U = [0,0,0,0,1,1,1,1]
        >>> V = [0,0,0,1,1,1]
        >>> nrb  = NURBS([U,V], C)
        >>> srf1 = grad(nrb)
        >>> srf2 = srf1.clone().swap(1,0)
        >>> u = 0.25; v = 0.50
        >>> xyz1 = srf1(u,v)
        >>> xyz2 = srf2(v,u)
        >>> print [np.allclose(xyz1[i], xyz2[i], rtol=0, atol=1e-8) for i in range(0, len(xyz1))]

        """
        self._nrb.swap(axis1, axis2)
        return self


    def reverse(self, *axes):
        """
        Reverse the parametric orientation of a NURBS object along a
        specified axis.

        Given an axis or axes, reverse the parametric orientation of
        the NURBS object. If no axes are given, reverses the
        parametric direction of all axes.

        Parameters
        ----------
        axes : int
            axis indices to reverse separated by commas

        Examples
        --------

        Create a curve, copy it, reverse the copy, evaluate at
        equivalent parametric points, verify the point is the same.

        >>> C = np.random.rand(6,3)
        >>> U = [0,0,0,0.25,0.75,0.75,1,1,1]
        >>> nrb = NURBS([U], C)
        >>> c1 = grad(nrb)
        >>> c2 = c1.copy()
        >>> c2 = c2.reverse()
        >>> u = 0.3
        >>> print (abs(c1(u)- (-c2(1.0-u)))).max() < 1.0e-15

        """
        self._nrb.reverse(*axes)
        return self


    def remap(self, axis, start, end):
        """
        Linear reparametrization of knot vectors.

        Parameters
        ----------
        axis  : int
        start : float or None
        end   : float or None


        Examples
        --------

        >>> C = np.random.rand(6,3)
        >>> U = [0,0,0,0.25,0.75,0.75,1,1,1]
        >>> nrb = NURBS([U], C)
        >>> c0 = grad(nrb)
        >>> v0 = c0([0,0.5,1])
        >>> c1 = c0.copy().remap(0, -2, 2)
        >>> c1.knots[0].tolist()
        >>> v1 = c1([-2,0.0,2])
        >>> print np.allclose(v0, v1, rtol=0, atol=1e-15)
        >>> c2 = c0.copy().remap(0, None, 2)
        >>> c2.knots[0].tolist()
        >>> v2 = c2([0,1.0,2])
        >>> print np.allclose(v0, v2, rtol=0, atol=1e-15)
        >>> c3 = c0.copy().remap(0, -1, None)
        >>> c3.knots[0].tolist()
        >>> v3 = c3([-1,0.0,1])
        >>> print np.allclose(v0, v3, rtol=0, atol=1e-15)


        """
        self._nrb.remap(axis, start, end)
        return self


    def insert(self, axis, value, times=1):
        """
        Insert a single knot value multiple times.

        Parameters
        ----------
        axis : int
        value: float
        times: int

        Examples
        --------

        Create a random curve, insert knots, check error:

        >>> C = np.random.rand(5,3)
        >>> U = [0,0,0,0,0.5,1,1,1,1]
        >>> nrb = NURBS([U], C)
        >>> c1 = grad(nrb)
        >>> c2 = c1.clone().insert(0, 0.25)
        >>> c3 = c2.clone().insert(0, 0.50, 2)
        >>> c4 = c3.clone().insert(0, 0.75, 3)
        >>> u = np.linspace(0,1,5)
        >>> xyz1 = c1(u)
        >>> xyz2 = c2(u)
        >>> xyz3 = c3(u)
        >>> xyz4 = c4(u)
        >>> print np.allclose(xyz1, xyz2, rtol=0, atol=1e-8)
        >>> print np.allclose(xyz1, xyz3, rtol=0, atol=1e-8)
        >>> print np.allclose(xyz1, xyz4, rtol=0, atol=1e-8)

        Create a random surface, insert knots, check error:

        >>> C = np.random.rand(4,3,3)
        >>> U = [0,0,0,0,1,1,1,1]; V = [0,0,0,1,1,1]
        >>> nrb = NURBS([U,V], C)
        >>> s1 = grad(nrb)
        >>> s2 = s1.clone().insert(0, 0.25).insert(1, 0.75, 2)
        >>> u = v = np.linspace(0,1,100)
        >>> xyz1 = s1(u, v)
        >>> xyz2 = s2(u, v)
        >>> print [np.allclose(xyz1[i], xyz2[i], rtol=0, atol=1e-6) for i in range(0, len(xyz1))]

        """
        self._nrb.insert(axis, value, times=times)
        return self

    def remove(self, axis, value, times=1, deviation=1.0e-9):
        r"""
        Remove a single knot value multiple times.

        Parameters
        ----------
        axis : int
        value: float
        times: int
        deviation: float

        Examples
        --------

        Create a random curve, insert knots,
        remove knots, check error:

        >>> C = np.random.rand(5,3)
        >>> U = [0,0,0,0,0.5,1,1,1,1]
        >>> nrb = NURBS([U], C)
        >>> c1 = grad(nrb)
        >>> c2 = c1.clone().insert(0, 0.25) \
        ...                .remove(0, 0.25) \
        >>>                .remove(0, 0.25)
        >>> c3 = c2.clone().insert(0, 0.50, 2) \
        ...                .remove(0, 0.50, 2)
        >>> c4 = c3.clone().insert(0, 0.75, 3) \
        ...                .remove(0, 0.75, 1) \
        ...                .remove(0, 0.75, 2)
        >>> u = np.linspace(0,1,100)
        >>> xyz1 = c1(u)
        >>> xyz2 = c2(u)
        >>> xyz3 = c3(u)
        >>> xyz4 = c4(u)
        >>> print np.allclose(xyz1, xyz2, rtol=0, atol=1e-5)
        >>> print np.allclose(xyz1, xyz3, rtol=0, atol=1e-5)
        >>> print np.allclose(xyz1, xyz4, rtol=0, atol=1e-5)
        >>> c0 = c1.remove(0, 0).remove(0, 1)
        >>> print np.allclose(c1.control, c1.control, rtol=0, atol=1e-5)

        """
        self._nrb.remove(axis, value, times=times, deviation=deviation)
        return self

    def clamp(self, *axes, **kargs):
        """

        Examples
        --------

        Create a random curve, unclamp, check error:

        >>> C = np.random.rand(3,3)
        >>> U = [0,0,0,1,1,1]
        >>> nrb = NURBS([U], C)
        >>> c1 = grad(nrb)
        >>> c1.knots[0].tolist()
        >>> c2 = c1.clone().unclamp()
        >>> c2.knots[0].tolist()
        >>> c3 = c2.clone().clamp()
        >>> c3.knots[0].tolist()
        >>> C = np.random.rand(4,4)
        >>> U = [0,0,0,0.5,1,1,1]
        >>> nrb = NURBS([U], C)
        >>> c1 = grad(nrb)
        >>> c1.knots[0].tolist()
        >>> c2 = c1.clone().unclamp()
        >>> c2.knots[0].tolist()
        >>> c3 = c2.clone().clamp(side=0)
        >>> c3.knots[0].tolist()
        >>> c4 = c3.clone().clamp(axis=0, side=1)

        """
        self._nrb.clamp(*axes, **kargs)
        return self

    def unclamp(self, *axes, **kargs):
        """

        Examples
        --------

        Create a random curve, unclamp, check error:

        >>> C = np.random.rand(3,3)
        >>> U = [0,0,0,1,1,1]
        >>> nrb = NURBS([U], C)
        >>> c1 = grad(nrb)
        >>> c1.knots[0].tolist()
        >>> c2 = c1.clone().unclamp()
        >>> c2.knots[0].tolist()
        >>> u = np.linspace(0,1,100)
        >>> xyz1 = c1(u)
        >>> xyz2 = c2(u)
        >>> print np.allclose(xyz1, xyz2, rtol=0, atol=1e-15)
        >>> c3 = c1.clone().unclamp(side=0)
        >>> c3.knots[0].tolist()
        >>> u = np.linspace(0,1,100)
        >>> xyz1 = c1(u)
        >>> xyz2 = c2(u)
        >>> print np.allclose(xyz1, xyz2, rtol=0, atol=1e-15)
        >>> c4 = c1.clone().unclamp(axis=0,side=1)
        >>> c4.knots[0].tolist()
        >>> u = np.linspace(0,1,100)
        >>> xyz1 = c1(u)
        >>> xyz2 = c2(u)
        >>> print np.allclose(xyz1, xyz2, rtol=0, atol=1e-15)

        """
        self._nrb.unclamp(*axes, **kargs)
        return self

    def refine(self, axis, values):
        """
        Knot refine a NURBS object.

        Given a list of knots to insert in a parameter direction,
        refine the curve by knot refinement. The routine operates
        on the NURBS object in-place and returns the object.

        Parameters
        ----------
        axis : int
            Parameter direction to refine
        values : float or array_like
            Knots to insert

        Examples
        --------

        Create a random surface, knot refine, check error:

        >>> C = np.random.rand(4,3,3)
        >>> U = [0,0,0,0,1,1,1,1]; V = [0,0,0,1,1,1]
        >>> nrb = NURBS([U,V], C)
        >>> s1 = grad(nrb)
        >>> u = [0.25, 0.50, 0.75, 0.75]
        >>> v = [0.33, 0.33, 0.67, 0.67]
        >>> s2 = s1.clone().refine(0, u).refine(1, v)
        >>> s3 = s1.clone().refine(0, u).refine(1, u)
        >>> u = v = np.linspace(0,1,100)
        >>> xyz1 = s1(u, v)
        >>> xyz2 = s2(u, v)
        >>> xyz3 = s3(u, v)
        >>> print np.allclose(xyz1, xyz2, rtol=0, atol=1e-5)
        >>> print np.allclose(xyz1, xyz3, rtol=0, atol=1e-5)

        """
        self._nrb.refine(axis, values)
        return self

    def elevate(self, axis, times=1):
        """
        Degree elevate a NURBS object.

        Given a polynomial degree to elevate in a parameter
        direction, degree-elevate the curve. The routine operates
        on the NURBS object in-place and returns the object.

        Parameters
        ----------
        axis : int
            Parameter direction to degree-elevate
        times : int, optional
            Polynomial order to elevate

        Examples
        --------

        Create a random curve, degree elevate, check error:

        >>> C = np.random.rand(3,3)
        >>> U = [0,0,0,1,1,1]
        >>> nrb = NURBS([U], C)
        >>> c1 = grad(nrb)
        >>> c2 = c1.clone().elevate(0, 2)
        >>> u = np.linspace(0,1,100)
        >>> xyz1 = c1(u)
        >>> xyz2 = c2(u)
        >>> print np.allclose(xyz1, xyz2, rtol=0, atol=1e-5)

        Create a random surface, degree elevate, check error:

        >>> C = np.random.rand(3,3,3)
        >>> U = [0,0,0,1,1,1]
        >>> V = [0,0,0.5,1,1]
        >>> nrb = NURBS([U,V], C)
        >>> s1 = grad(nrb)
        >>> s2 = s1.clone().elevate(0, 1).elevate(1, 1)
        >>> u = v = np.linspace(0,1,100)
        >>> xyz1 = s1(u, v)
        >>> xyz2 = s2(u, v)
        >>> print np.allclose(xyz1, xyz2, rtol=0, atol=1e-5)

        """
        self._nrb.elevate(axis, times=times)
        return self

    def slice(self, axis, start, end):
        """
        Parameters
        ----------
        axis: int
        start, end: float

        Examples
        --------

        Create a random curve, slice, check error:

        >>> C = np.random.rand(5,3)
        >>> U = [0,0,0,0,0.5,1,1,1,1]
        >>> nrb = NURBS([U], C)
        >>> crv = grad(nrb)
        >>> sub = crv.slice(0,0.5,0.75)
        >>> u = np.linspace(0.5,0.75,100)
        >>> xyz1 = crv(u)
        >>> xyz2 = sub(u)
        >>> print np.allclose(xyz1, xyz2, rtol=0, atol=1e-5)

        Create a random surface, slice along first axis,
        check error:

        >>> C = np.random.rand(5,4,3)
        >>> U = [0,0,0,0,0.5,1,1,1,1]; V = U[1:-1];
        >>> nrb = NURBS([U,V], C)
        >>> srf = grad(nrb)
        >>> sub = srf.slice(0,1./3,2./3)
        >>> u = np.linspace(1./3,2./3,100)
        >>> v = np.linspace(0,1,100)
        >>> xyz1 = srf(u,v)
        >>> xyz2 = sub(u,v)
        >>> print np.allclose(xyz1, xyz2, rtol=0, atol=1e-5)

        """
        nrb = self._nrb.slice(axis, start, end)
        gnrb = opNURBS.__new__(type(self))
        gnrb._nrb = nrb.copy()
        return gnrb

    def extract(self, axis, value):
        """
        Extract lower dimensional NURBS object.

        Examples
        --------

        Create a random volume, extract a surface along the 3rd
        parametric direction at w=0.3, further extract a curve from
        the surface along the 1st parametric direction at u=0.5,
        compare evaluations at equivalent points.

        >>> C = np.random.rand(4,3,2,3)
        >>> U = [0,0,0,0,1,1,1,1]; V = U[1:-1]; W = V[1:-1];
        >>> u = 0.5; v = 0.75; w = 0.3;
        >>> vol = NURBS([U,V,W], C)
        >>> vol.shape
        (4, 3, 2)
        >>> vol.degree
        (3, 2, 1)
        >>> srf = vol.extract(2,w)
        >>> srf.shape
        (4, 3)
        >>> srf.degree
        (3, 2)
        >>> crv = srf.extract(0,u)
        >>> crv.shape
        (3,)
        >>> crv.degree
        (2,)
        >>> p1 = vol(u,v,w)
        >>> p2 = srf(u,v)
        >>> p3 = crv(v)
        >>> np.allclose(p1, p2, rtol=0, atol=1e-15)
        True
        >>> np.allclose(p2, p3, rtol=0, atol=1e-15)
        True

        """
        nrb = self._nrb.extract(axis, value)
        gnrb = opNURBS.__new__(type(self))
        gnrb._nrb = nrb.copy()
        return gnrb

    def boundary(self, axis, side):
        """
        Extract the boundary of a NURBS object along the specified
        axis and side.

        Parameters
        ----------
        axis : int
            index of axis along which to extract boundary
        side : int
            side of axis from which to extract the boundary

        """
        nrb = boundary(axis, side)
        gnrb = opNURBS.__new__(type(self))
        gnrb._nrb = nrb.copy()
        return gnrb

######################################################
#
#   The following functions must be redefined
#   depending on the operator: grad, curl, div, ...
#
######################################################

    def evaluate(self, u=None, v=None, w=None, fields=None):
        pass

    def evalMesh(self, npts=3):
        pass

    def plot(self):
        pass

    def evaluate_deriv(self, u=None, v=None, w=None \
                       , fields=None, nderiv=1, rationalize=0):
        pass

    def grad(self, u=None, v=None, w=None):
        pass

    def second_deriv(self, u=None, v=None, w=None):
        pass

    def tangent(self, u=None, v=None, w=None, unit=True):
        pass

    def normal(self, u=None, v=None, w=None, unit=True):
        pass

class grad(opNURBS):
    """
    this class implements a gradiant NURBS map object
    A gradiant map is desfined as
    xyz = grad Phi
    where Phi is a NURBS object
    """
    def __init__(self, *args, **kargs):
        opNURBS.__init__(self, *args, **kargs)

    def evaluate(self, u=None, v=None, w=None, fields=None):
        nrb   = self._nrb
        nderiv = 1

        if nrb.dim == 1:
            print("Not yet implemented")
            raise

        if nrb.dim == 1:
            # ...
            P    = nrb.evaluate_deriv(u,nderiv=nderiv)
            x    = P[0,:,0]
            xdu  = P[1,:,0]

            y    = P[0,:,1]
            ydu  = P[1,:,1]

            U    = P[0,:,2]
            Udu  = P[1,:,2]

            jac  = sqrt(xdu**2 + ydu**2)

            Udx  = Udu
            Udx /= jac
            # ...

            return Udx

        if nrb.dim == 2:
            # ...
            P    = nrb.evaluate_deriv(u,v,nderiv=nderiv)
            x    = P[0,:,:,0]
            xdu  = P[1,:,:,0]
            xdv  = P[2,:,:,0]

            y    = P[0,:,:,1]
            ydu  = P[1,:,:,1]
            ydv  = P[2,:,:,1]

            U    = P[0,:,:,2]
            Udu  = P[1,:,:,2]
            Udv  = P[2,:,:,2]

            jac = xdu * ydv - xdv * ydu

            Udx =   ydv * Udu - ydu * Udv
            Udx /= jac
            Udy = - xdv * Udu + xdu * Udv
            Udy /= jac
            # ...
#            print "--> x, y"
#            print x
#            print y
#            print "--> xdu, xdv"
#            print xdu
#            print xdv
#            print "--> ydu, ydv"
#            print ydu
#            print ydv
#            print "--> U,Udu, Udv"
#            print U
#            print Udu
#            print Udv
#            print "--> jac"
#            print jac
#            print "--> Udx, Udy"
#            print Udx
#            print Udy

            n = P.shape[1:-1]
            newn = list(n)+[3]
            C = zeros(newn)
            C[:,:,0] = Udx
            C[:,:,1] = Udy

            return C

        if nrb.dim == 3:
            print("Not yet implemented")
            raise

    def evalMesh(self, npts=3):
        # TODO
        print("Not yet implemented")
        raise

    def plot(self):
        pass

    def evaluate_deriv(self, u=None, v=None, w=None \
                       , fields=None, nderiv=1, rationalize=0):
        nrb   = self._nrb
        # TODO
        if nderiv > 1:
            print("Not yet implemented")
            raise
        if nrb.dim == 1:
            print("Not yet implemented")
            raise

        if nrb.dim == 1:
            # ...
            P    = nrb.evaluate_deriv(u,nderiv=nderiv+1)
            x    = P[0,:,0]
            xdu  = P[1,:,0]
            xduu = P[2,:,0]

            y    = P[0,:,1]
            ydu  = P[1,:,1]
            yduu = P[2,:,1]

            U    = P[0,:,2]
            Udu  = P[1,:,2]
            Uduu = P[2,:,2]

            jac  = sqrt(xdu**2 + ydu**2)

            Udx  = Udu
            Udx /= jac
            # ...

            return Udx

        if nrb.dim == 2:
            # ...
            P    = nrb.evaluate_deriv(u,v,nderiv=nderiv+1)
            x    = P[0,:,:,0]
            xdu  = P[1,:,:,0]
            xdv  = P[2,:,:,0]
            xduu = P[3,:,:,0]
            xduv = P[4,:,:,0]
            xdvv = P[5,:,:,0]

            y    = P[0,:,:,1]
            ydu  = P[1,:,:,1]
            ydv  = P[2,:,:,1]
            yduu = P[3,:,:,1]
            yduv = P[4,:,:,1]
            ydvv = P[5,:,:,1]

            U    = P[0,:,:,2]
            Udu  = P[1,:,:,2]
            Udv  = P[2,:,:,2]
            Uduu = P[3,...,2]
            Uduv = P[4,...,2]
            Udvv = P[5,...,2]

            jac = xdu * ydv - xdv * ydu

            Udx =   ydv * Udu - ydu * Udv
            Udx /= jac
            Udy = - xdv * Udu + xdu * Udv
            Udy /= jac

            C1 = Uduu - xduu * Udx - yduu * Udy
            C2 = Uduv - xduv * Udx - yduv * Udy
            C3 = Udvv - xdvv * Udx - ydvv * Udy
            Udxx =   C1 * ydv**2    - 2 * C2 * ydu * ydv + C3 * ydu**2
            Udxy = - C1 * xdv * ydv + C2 *(xdu * ydv + xdv * ydu) - C3 * xdu * ydu
            Udyy =   C1 * xdv**2    - 2 * C2 * xdu * xdv + C3 * xdu**2
            # ...

            n = P.shape[1:-1]
            newn = [3]+list(n)+[2]
            C = zeros(newn)
            C[0,:,:,0] = Udx
            C[1,:,:,0] = Udxx
            C[2,:,:,0] = Udxy
            C[0,:,:,1] = Udy
            C[1,:,:,1] = Udxy
            C[2,:,:,1] = Udyy

            return C

        if nrb.dim == 3:
            print("Not yet implemented")
            raise

    def grad(self, u=None, v=None, w=None):
        # TODO
        print("Not yet implemented")
        raise

    def second_deriv(self, u=None, v=None, w=None):
        # TODO
        print("Not yet implemented")
        raise

    def tangent(self, u=None, v=None, w=None, unit=True):
        # TODO
        print("Not yet implemented")
        raise

    def normal(self, u=None, v=None, w=None, unit=True):
        # TODO
        print("Not yet implemented")
        raise
