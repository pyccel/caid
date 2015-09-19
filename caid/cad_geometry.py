# -*- coding: UTF-8 -*-
import numpy as np
from numpy import linspace
from igakit.nurbs import NURBS
from .op_nurbs import opNURBS
from .io import XML, TXT
import sys
from caid.core import bspline as bsplinelib

_bsp = bsplinelib.bsp

from numpy import pi, sqrt, array, zeros

def line(n=None, p=None, periodic=None):
    """Creates a unit line cad_geometry object.

    Kwargs:
        n (list int): This is a list containing the number of interior knots to insert. default None

        p (list int): This is a list containing the spline degree of the line. default None

    Returns:
       A cad_geometry object.
    """
    points = np.asarray([[0.,0.],[1.,0.]])
    return linear(points=points, n=n, p=p, periodic=periodic)

def square(n=None, p=None):
    """Creates a unit square cad_geometry object.

    Kwargs:
        n (list int): This is a list containing the number of interior knots to insert. default None

        p (list int): This is a list containing the spline degree of the line. default None

    Returns:
       A cad_geometry object.
    """
    points = np.asarray([[[0.,0.],[0.,1.]],[[1.,0.],[1.,1.]]])
    return bilinear(points=points, n=n, p=p)

def triangle(n=None, p=None, points=None, profile=0):
    """Creates a degenerated triangle cad_geometry object.

    Kwargs:
        n (list int): This is a list containing the number of interior knots to insert. default None

        p (list int): This is a list containing the spline degree of the line. default None

        profile (int): is the triangle type. The redandant Control Points
        depends on the profile value.

    Returns:
       A cad_geometry object.

    """
    if points is None:
        A = [0.,0.]
        B = [0.,1.]
        C = [1.,0.]
    else:
        A = points[0]
        B = points[1]
        C = points[2]


    if profile == 0:
        points = np.asarray([[A,A],[B,C]])
    if profile == 1:
        points = np.asarray([[A,B],[C,C]])
    if profile == 2:
        points = np.asarray([[A,B],[C,B]])
    if profile == 3:
        D = [.5*(b+c) for (b,c) in zip(B,C)]
        points = np.asarray([[A,B],[C,D]])
    return bilinear(points=points, n=n, p=p)

def linear(points=None, n=None, p=None, periodic=None):
    from igakit.cad import linear as nrb_linear
    """Creates a linear cad_geometry object.

    Kwargs:
        points (float array): The extremeties of the linear

        n (list int): This is a list containing the number of interior knots to insert. default None

        p (list int): This is a list containing the spline degree of the line. default None

    Returns:
       A cad_geometry object.

    p[0]         p[1]
    o------------o
       +----> u

    """
    nrb = nrb_linear(points)
    cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)
    cad_nrb.rational = False
    cad_nrb.orientation = [-1,1]

    geo = cad_geometry()
    geo.append(cad_nrb)

    # ... refinement
    list_t = None
    if n is not None:
        list_t = []
        for axis in range(0,cad_nrb.dim):
            ub = cad_nrb.knots[axis][0]
            ue = cad_nrb.knots[axis][-1]
            list_t.append(np.linspace(ub,ue,n[axis]+2)[1:-1])

    list_p = None
    if p is not None:
        list_p = []
        for axis in range(0,cad_nrb.dim):
            list_p.append(p[axis] - cad_nrb.degree[axis])

    geo.refine(list_t=list_t, list_p=list_p)
    # ...

    geo._internal_faces = []
    geo._external_faces = [[0,0],[0,1]]
    geo._connectivity   = []
    if periodic is not None:
        if periodic:
            geo[0].unclamp(0)

            list_connectivity   = []
            dict_con = {}
            dict_con['original']    = [0,0]
            dict_con['clone']       = [0,1]
            dict_con['periodic']    = True
            list_connectivity.append(dict_con)

            geo._connectivity = list_connectivity

            geo._internal_faces = [[0,0],[0,1]]
            geo._external_faces = []

    return geo

def arc(radius=1, center=None, angle=pi/2, n=None, p=None):
    from igakit.cad import circle
    """Creates a linear cad_geometry object.

    Kwargs:
        points (float array): The extremeties of the linear

        n (list int): This is a list containing the number of interior knots to insert. default None

        p (list int): This is a list containing the spline degree of the line. default None

    Returns:
       A cad_geometry object.

    p[0]         p[1]
    o------------o
       +----> u

    """
    nrb = circle(radius=radius, center=center, angle=angle)
    cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)
    cad_nrb.rational = False
    cad_nrb.orientation = [-1,1]

    geo = cad_geometry()
    geo.append(cad_nrb)

    # ... refinement
    list_t = None
    if n is not None:
        list_t = []
        for axis in range(0,cad_nrb.dim):
            ub = cad_nrb.knots[axis][0]
            ue = cad_nrb.knots[axis][-1]
            list_t.append(np.linspace(ub,ue,n[axis]+2)[1:-1])

    list_p = None
    if p is not None:
        list_p = []
        for axis in range(0,cad_nrb.dim):
            list_p.append(p[axis] - cad_nrb.degree[axis])

    geo.refine(list_t=list_t, list_p=list_p)
    # ...

    geo._connectivity   = []
    if angle % 2*np.pi:
        geo._internal_faces = []
        geo._external_faces = [[0,0],[0,1]]
    else:
        geo._internal_faces = [[0,0],[0,1]]
        geo._external_faces = []
        dict_con = {}; dict_con['original'] = [0,0]; dict_con['clone'] = [0,1]; geo._connectivity.append(dict_con)

    return geo

def bilinear(points=None, n=None, p=None):
    from igakit.cad import bilinear as nrb_bilinear
    """Creates a bilinear cad_geometry object.

    Kwargs:
        points (array): The summits of the quadrangle.

        n (list int): This is a list containing the number of interior knots to insert. default None

        p (list int): This is a list containing the spline degree of the line. default None

    Returns:
       A cad_geometry object.

    p[0,1]       p[1,1]
    o------------o
    |  v         |
    |  ^         |
    |  |         |
    |  +----> u  |
    o------------o
    p[0,0]       p[1,0]

    """
    nrb = nrb_bilinear(points)
    cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)
    cad_nrb.rational = False
    cad_nrb.orientation = [1,-1,-1,1]

    geo = cad_geometry()
    geo.append(cad_nrb)

    # ... refinement
    list_t = None
    if n is not None:
        list_t = []
        for axis in range(0,cad_nrb.dim):
            ub = cad_nrb.knots[axis][0]
            ue = cad_nrb.knots[axis][-1]
            list_t.append(np.linspace(ub,ue,n[axis]+2)[1:-1])

    list_p = None
    if p is not None:
        list_p = []
        for axis in range(0,cad_nrb.dim):
            list_p.append(p[axis] - cad_nrb.degree[axis])

    geo.refine(list_t=list_t, list_p=list_p)
    # ...

    geo._internal_faces = []
    geo._external_faces = [[0,0],[0,1],[0,2],[0,3]]
    geo._connectivity   = []


    return geo

def circle(radius=1.0, center=None, n=None, p=None):
    """Creates a 2D circle with 1 patch as cad_geometry object.

    Kwargs:
        radius (float): The radius of the circle. default 1.

        n (list int): This is a list containing the number of interior knots to insert. default None

        p (list int): This is a list containing the spline degree of the line. default None

    Returns:
       A cad_geometry object.

    """
    s = 1./np.sqrt(2)
    knots = [  [0.0 , 0.0 , 0.0 , 1.0 , 1.0 , 1.0] \
             , [0.0 , 0.0 , 0.0 , 1.0 , 1.0 , 1.0] ]

    points          = np.zeros((3,3,3))
    points[0,0,:]   = np.asarray([-s   , -s   , 0.])
    points[1,0,:]   = np.asarray([-2*s , 0.   , 0.])
    points[2,0,:]   = np.asarray([-s   , s    , 0.])
    points[0,1,:]   = np.asarray([0.   , -2*s , 0.])
    points[1,1,:]   = np.asarray([0.   , 0.0  , 0.])
    points[2,1,:]   = np.asarray([0.   , 2*s  , 0.])
    points[0,2,:]   = np.asarray([s    , -s   , 0.])
    points[1,2,:]   = np.asarray([2*s  , 0.   , 0.])
    points[2,2,:]   = np.asarray([s    , s    , 0.])
    points         *= radius

    if center is not None:
        points[...,0] += center[0]
        points[...,1] += center[1]
        try:
            points[...,2] += center[2]
        except:
            pass

    weights         = np.zeros((3,3))
    weights[0,0]    = 1.
    weights[1,0]    = s
    weights[2,0]    = 1.
    weights[0,1]    = s
    weights[1,1]    = 1.
    weights[2,1]    = s
    weights[0,2]    = 1.
    weights[1,2]    = s
    weights[2,2]    = 1.

    cad_nrb = cad_nurbs(knots, points, weights=weights)
    cad_nrb.rational = True
    cad_nrb.orientation = [-1,1,1,-1]

    geo = cad_geometry()
    geo.append(cad_nrb)

    # ... refinement
    list_t = None
    if n is not None:
        list_t = []
        for axis in range(0,cad_nrb.dim):
            ub = cad_nrb.knots[axis][0]
            ue = cad_nrb.knots[axis][-1]
            list_t.append(np.linspace(ub,ue,n[axis]+2)[1:-1])

    list_p = None
    if p is not None:
        list_p = []
        for axis in range(0,cad_nrb.dim):
            list_p.append(p[axis] - cad_nrb.degree[axis])

    geo.refine(list_t=list_t, list_p=list_p)
    # ...

    geo._internal_faces = []
    geo._external_faces = [[0,0],[0,1],[0,2],[0,3]]
    geo._connectivity   = []

    return geo

def quart_circle(rmin=0.5, rmax=1.0, center=None, n=None, p=None):
    """Creates a 2D quarter circle with 1 patch as cad_geometry object.

    Kwargs:
        rmin (float): Minimal radius of the quart-circle. default 0.5

        rmax (float): Maximal radius of the quart-circle. default 1.0

        n (list int): This is a list containing the number of interior knots to insert. default None

        p (list int): This is a list containing the spline degree of the line. default None

    Returns:
       A cad_geometry object.

    """
    knots = [  [0.0 , 0.0 , 0.0 , 1.0 , 1.0 , 1.0] \
             , [0.0 , 0.0 , 1.0 , 1.0] ]

    points          = np.zeros((3,2,3))
    j = 0
    points[0,j,:]   = np.asarray([0.0   , -rmin , 0.0])
    points[1,j,:]   = np.asarray([-rmin , -rmin , 0.0])
    points[2,j,:]   = np.asarray([-rmin , 0.0   , 0.0])
    j = 1
    points[0,j,:]   = np.asarray([0.0   , -rmax , 0.0])
    points[1,j,:]   = np.asarray([-rmax , -rmax , 0.0])
    points[2,j,:]   = np.asarray([-rmax , 0.0   , 0.0])

    if center is not None:
        points[...,0] += center[0]
        points[...,1] += center[1]
        try:
            points[...,2] += center[2]
        except:
            pass

    weights         = np.zeros((3,2))
    j = 0
    weights[0,j]   = 1.0
    weights[1,j]   = 0.707106781187
    weights[2,j]   = 1.0
    j = 1
    weights[0,j]   = 1.0
    weights[1,j]   = 0.707106781187
    weights[2,j]   = 1.0

    cad_nrb = cad_nurbs(knots, points, weights=weights)
    cad_nrb.rational = True
    cad_nrb.orientation = [1,-1,-1,1]

    geo = cad_geometry()
    geo.append(cad_nrb)

    # ... refinement
    list_t = None
    if n is not None:
        list_t = []
        for axis in range(0,cad_nrb.dim):
            ub = cad_nrb.knots[axis][0]
            ue = cad_nrb.knots[axis][-1]
            list_t.append(np.linspace(ub,ue,n[axis]+2)[1:-1])

    list_p = None
    if p is not None:
        list_p = []
        for axis in range(0,cad_nrb.dim):
            list_p.append(p[axis] - cad_nrb.degree[axis])

    geo.refine(list_t=list_t, list_p=list_p)
    # ...

    geo._internal_faces = []
    geo._external_faces = [[0,0],[0,1],[0,2],[0,3]]
    geo._connectivity   = []

    return geo

def annulus(rmin=0.5, rmax=1.0, center=None, n=None, p=None):
    """Creates a 2D annulus with 1 patch as cad_geometry object.

    Kwargs:
        rmin (float): Minimal radius of the annulus. default 0.5

        rmax (float): Maximal radius of the annulus. default 1.0

        n (list int): This is a list containing the number of interior knots to insert. default None

        p (list int): This is a list containing the spline degree of the line. default None

    Returns:
       A cad_geometry object.

    """
    knots = [  [0.0 , 0.0 , 1.0 , 1.0] \
             , [0.0 , 0.0 , 0.0 , 0.25 , 0.25 , 0.5 , 0.5 , 0.75 , 0.75 , 1.0 , 1.0 , 1.0] ]

    points          = np.zeros((2,9,3))
    j = 0
    points[j,0,:]   = np.asarray([0.0   , -rmin , 0.0])
    points[j,1,:]   = np.asarray([-rmin , -rmin , 0.0])
    points[j,2,:]   = np.asarray([-rmin , 0.0   , 0.0])
    points[j,3,:]   = np.asarray([-rmin , rmin  , 0.0])
    points[j,4,:]   = np.asarray([0.0   , rmin  , 0.0])
    points[j,5,:]   = np.asarray([rmin  , rmin  , 0.0])
    points[j,6,:]   = np.asarray([rmin  , 0.0   , 0.0])
    points[j,7,:]   = np.asarray([rmin  , -rmin , 0.0])
    points[j,8,:]   = np.asarray([0.0   , -rmin , 0.0])
    j = 1
    points[j,0,:]   = np.asarray([0.0   , -rmax , 0.0])
    points[j,1,:]   = np.asarray([-rmax , -rmax , 0.0])
    points[j,2,:]   = np.asarray([-rmax , 0.0   , 0.0])
    points[j,3,:]   = np.asarray([-rmax , rmax  , 0.0])
    points[j,4,:]   = np.asarray([0.0   , rmax  , 0.0])
    points[j,5,:]   = np.asarray([rmax  , rmax  , 0.0])
    points[j,6,:]   = np.asarray([rmax  , 0.0   , 0.0])
    points[j,7,:]   = np.asarray([rmax  , -rmax , 0.0])
    points[j,8,:]   = np.asarray([0.0   , -rmax , 0.0])

    if center is not None:
        points[...,0] += center[0]
        points[...,1] += center[1]
        try:
            points[...,2] += center[2]
        except:
            pass

    weights         = np.zeros((2,9))
    j = 0
    weights[j,0]   = 1.0
    weights[j,1]   = 0.707106781187
    weights[j,2]   = 1.0
    weights[j,3]   = 0.707106781187
    weights[j,4]   = 1.0
    weights[j,5]   = 0.707106781187
    weights[j,6]   = 1.0
    weights[j,7]   = 0.707106781187
    weights[j,8]   = 1.0
    j = 1
    weights[j,0]   = 1.0
    weights[j,1]   = 0.707106781187
    weights[j,2]   = 1.0
    weights[j,3]   = 0.707106781187
    weights[j,4]   = 1.0
    weights[j,5]   = 0.707106781187
    weights[j,6]   = 1.0
    weights[j,7]   = 0.707106781187
    weights[j,8]   = 1.0

    cad_nrb = cad_nurbs(knots, points, weights=weights)
    cad_nrb.rational = True
    cad_nrb.orientation = [-1,1,1,-1]

    geo = cad_geometry()
    geo.append(cad_nrb)

    # ... refinement
    list_t = None
    if n is not None:
        list_t = []
        for axis in range(0,cad_nrb.dim):
            ub = cad_nrb.knots[axis][0]
            ue = cad_nrb.knots[axis][-1]
            list_t.append(np.linspace(ub,ue,n[axis]+2)[1:-1])

    list_p = None
    if p is not None:
        list_p = []
        for axis in range(0,cad_nrb.dim):
            list_p.append(p[axis] - cad_nrb.degree[axis])

    geo.refine(list_t=list_t, list_p=list_p)
    # ...

    if rmin > 0.:
        geo._internal_faces = [[0,0],[0,2]]
        geo._external_faces = [[0,1],[0,3]]
    if rmin == 0.:
        geo._internal_faces = [[0,0],[0,1],[0,2]]
        geo._external_faces = [[0,3]]
    geo._connectivity   = []
    dict_con = {}; dict_con['original'] = [0,0]; dict_con['clone'] = [0,2]; geo._connectivity.append(dict_con)

    return geo

def circle_5mp(rmin=0.5, rmax=1.0, center=None, n=None, p=None):
    """Creates a 2D description of the circle using 5 patchs.

    Kwargs:
        rmin (float): Minimal radius of the annulus. default 0.5

        rmax (float): Maximal radius of the circle. default 1.0

        n (list int): This is a list containing the number of interior knots to insert. default None

        p (list int): This is a list containing the spline degree of the line. default None

    Returns:
       A cad_geometry object.

    """
    # ... Import the quart_circle domain
    geo_1 = quart_circle(rmin=rmin, rmax=rmax, center=center, n=n,p=p)
    geo_1[0].transpose()

    # ... Import the quart_circle domain
    geo_2 = quart_circle(rmin=rmin, rmax=rmax, center=center, n=n,p=p)
    geo_2[0].rotate(0.5*np.pi)
    geo_2[0].transpose()

    # ... Import the quart_circle domain
    geo_3 = quart_circle(rmin=rmin, rmax=rmax, center=center, n=n,p=p)
    geo_3[0].rotate(np.pi)
    geo_3[0].reverse(0)

    # ... Import the quart_circle domain
    geo_4 = quart_circle(rmin=rmin, rmax=rmax, center=center, n=n,p=p)
    geo_4[0].rotate(1.5*np.pi)
    geo_4[0].reverse(0)

    # ... Import the circle domain
    geo_5 = circle(radius=rmin, center=center,n=n,p=p)
    geo_5[0].rotate(0.25*np.pi)
    geo_5[0].rotate(0.5*np.pi)

    geo_12   = geo_1.merge(geo_2)
    geo_34   = geo_3.merge(geo_4)
    geo_1234 = geo_12.merge(geo_34)
    geo      = geo_1234.merge(geo_5)

    return geo

def pinched_quart_circle(rmin=0.5, rmax=1.0, epsilon=0.5, center=None, degree=0.0):
    """Creates a 2D pinched quarter circle with 1 patch as cad_geometry object.

    Kwargs:
        rmin (float): Minimal radius of the quart-circle. default 0.5

        rmax (float): Maximal radius of the quart-circle. default 1.0

        epsilon (float): Factor of deformation of the quart-circle. default 0.5

        degree (float): rotation degree. default 0.0

    Returns:
       A cad_geometry object.

    """

    # ... Import the quart_circle domain
    geo = quart_circle(rmin=rmin, rmax=rmax, center=center)
    #getting the patch:
    cad_nrb = geo[0]

    # Refining...
    list_t = None
    n = 4
    p = 3
    if n is not None:
        list_t = []
        for axis in range(0,geo.dim):
            ub = cad_nrb.knots[axis][0]
            ue = cad_nrb.knots[axis][-1]
            list_t.append(np.linspace(ub,ue,n+2)[1:-1])
        list_p = None
        if p is not None:
            list_p = []
            for axis in range(0,cad_nrb.dim):
                list_p.append(p - cad_nrb.degree[axis])
        geo.refine(list_t=list_t, list_p=list_p, list_m=[1,1])

    # "Pinching" the geometry
    cad_nrb = geo[0]
    if ((epsilon<=1.)and(epsilon>=0)) :
        epsilon = epsilon/10.
        # first corner
        cad_nrb.control[0,0,1] -= epsilon
        cad_nrb.control[1,0,1] -= epsilon/2.
        cad_nrb.control[0,1,1] -= epsilon
        cad_nrb.control[1,1,1] -= epsilon/2.
        # second corner
        cad_nrb.control[7,0,0] -= epsilon
        cad_nrb.control[6,0,0] -= epsilon/2.
        cad_nrb.control[7,1,0] -= epsilon
        cad_nrb.control[6,1,0] -= epsilon/2.

        cad_nrb.rotate(degree)
    else:
        print " ERROR  in pinched_quart_circle : epsilon should be in between 0 and 1"
        STOP
    return geo

def pinched_circle(radius=0.5, epsilon=0.5, center=None, n=None, p=None):
    geo = circle(radius=radius, center=center, n=n, p=p)
    geo[0].rotate(0.25*np.pi)
    cad_nrb = geo[0]

    # Refining...
    list_t = None
    n = 4
    p = 3
    if n is not None:
        list_t = []
        for axis in range(0,geo.dim):
            ub = cad_nrb.knots[axis][0]
            ue = cad_nrb.knots[axis][-1]
            list_t.append(np.linspace(ub,ue,n+2)[1:-1])
        list_p = None
        if p is not None:
            list_p = []
            for axis in range(0,cad_nrb.dim):
                list_p.append(p - cad_nrb.degree[axis])
        geo.refine(list_t=list_t, list_p=list_p, list_m=[1,1])

    # "Pinching" the geometry
    cad_nrb = geo[0]
    if ((epsilon<=1.)and(epsilon>=0)) :
        epsilon = epsilon/10.
        # first corner
        cad_nrb.control[0,0,1] -= epsilon
        cad_nrb.control[1,0,1] -= epsilon/2.
        cad_nrb.control[1,1,1] -= epsilon
        cad_nrb.control[0,1,1] -= epsilon/2.
        # second corner
        cad_nrb.control[7,0,0] -= epsilon
        cad_nrb.control[6,0,0] -= epsilon/2.
        cad_nrb.control[6,1,0] -= epsilon
        cad_nrb.control[7,1,0] -= epsilon/2.
        # third corner
        cad_nrb.control[1,6,0] += epsilon
        cad_nrb.control[0,6,0] += epsilon/2.
        cad_nrb.control[0,7,0] += epsilon
        cad_nrb.control[1,7,0] += epsilon/2.
        # second corner
        cad_nrb.control[6,6,1] += epsilon
        cad_nrb.control[7,6,1] += epsilon/2.
        cad_nrb.control[7,7,1] += epsilon
        cad_nrb.control[6,7,1] += epsilon/2.
    else:
        print " ERROR  in pinched_circle : epsilon should be in between 0 and 1"
        STOP
    return geo

def pinched_circle_5mp(rmin=0.5, rmax=1.0, epsilon=0.5, center=None, n=None, p=None):
    """Creates a 2D description of a pinched circle using 5 patchs.
       This geometry is supposed to avoid any singular points on the disk.

    Kwargs:
        rmin (float): Minimal radius of the annulus. default 0.5

        rmax (float): Maximal radius of the circle. default 1.0

        epsilon (float): Parameter that mesures the level of deformation of the internal interface. default 0.5

        n (list int): This is a list containing the number of interior knots to insert. default None

        p (list int): This is a list containing the spline degree of the line. default None

    Returns:
       A cad_geometry object.

    """
    # ... Import the quart_circle domain
    geo_1 = pinched_quart_circle(rmin=rmin, rmax=rmax, epsilon=epsilon, center=center)
    geo_1[0].transpose()

    # ... Import the quart_circle domain
    geo_2 = pinched_quart_circle(rmin=rmin, rmax=rmax, epsilon=epsilon, center=center, degree=0.5*np.pi)
    geo_2[0].reverse(0)

    # ... Import the quart_circle domain
    geo_3 = pinched_quart_circle(rmin=rmin, rmax=rmax, epsilon=epsilon, center=center, degree=np.pi)
    geo_3[0].reverse(0)

    # ... Import the quart_circle domain
    geo_4 = pinched_quart_circle(rmin=rmin, rmax=rmax, epsilon=epsilon, degree=1.5*np.pi)
#    geo_4[0].reverse(0)
    geo_4[0].transpose()

    # ... Import the pinched_circle domain
    geo_5 = pinched_circle(radius=rmin, epsilon=epsilon, center=center,n=n,p=p)

    geo_12   = geo_1.merge(geo_2)
    geo_34   = geo_3.merge(geo_4)
    geo_1234 = geo_12.merge(geo_34)
    geo      = geo_1234.merge(geo_5)

    return geo


def trilinear(points=None, n=None, p=None):
    from igakit.cad import trilinear as nrb_trilinear
    """Creates a bilinear cad_geometry object. TODO: needs to be updated

    Kwargs:
        points (array): The summits of the cube.

        n (list int): This is a list containing the number of interior knots to insert. default None

        p (list int): This is a list containing the spline degree of the line. default None

    Returns:
       A cad_geometry object.

       p[0,1,1]     p[1,1,1]
       o------------o
      /|           /|
     / |          / |          w
    o------------o  |          ^  v
    | p[0,0,1]   | p[1,0,1]    | /
    |  |         |  |          |/
    |  o-------- | -o          +----> u
    | / p[0,1,0] | / p[1,1,0]
    |/           |/
    o------------o
    p[0,0,0]     p[1,0,0]

    """
    nrb = nrb_trilinear(points)
    cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)
    cad_nrb.rational = False

    geo = cad_geometry()
    geo.append(cad_nrb)

    # ... refinement
    list_t = None
    if n is not None:
        list_t = []
        for axis in range(0,cad_nrb.dim):
            ub = cad_nrb.knots[axis][0]
            ue = cad_nrb.knots[axis][-1]
            list_t.append(np.linspace(ub,ue,n[axis]+2)[1:-1])

    list_p = None
    if p is not None:
        list_p = []
        for axis in range(0,cad_nrb.dim):
            list_p.append(p[axis] - cad_nrb.degree[axis])

    geo.refine(list_t=list_t, list_p=list_p)
    # ...

    geo._internal_faces = []
    geo._external_faces = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5]]
    geo._connectivity   = []

    return geo

def merge(list_geo, npts=5):
    """
    merge a list of cad_geometries and update internal/external faces and connectivities

    Args:
        list_geo: a list of cad_geometries

    Returns:
        a cad_geometries
    """
    geo_f = list_geo[0]
    for geo in list_geo[1:]:
        geo_f = geo_f.merge(geo, npts=npts)
    return geo_f

def tcoons(curves, profile=0):
    """
    creates a 2D geometry (for the moment) using 3 curves. the profile is given
    as for the construction of Triangle.
    TODO: profile > 0

    Args:
        curves: list of curves
        profile: the profile of the triangle

    Returns:
        a NURBS
    """

    from igakit.cad import coons

    [c1, c2, c3] = curves

    if np.allclose(c2.points[-1,:],c1.points[0,:]):
        c2 = c2.reverse()

    if np.allclose(c3.points[-1,:],c1.points[-1,:]):
        c3 = c3.reverse()

    # ...
    if profile==0:
        A = c1.points[0,:]

        P = np.zeros_like(c3.points)
        for i in range(0,P.shape[0]):
            P[i,:] = A[:]

        c = cad_nurbs(c3.knots, P, weights=c3.weights)
        nrb = coons([[c1,c2],[c,c3]])
    # ...

    # ...
    if profile==1:
        raise("TCoons with profile 1 Not yet implemented")
#        A = c2.points[0,:]
#
#        P = np.zeros_like(c3.points)
#        for i in range(0,P.shape[0]):
#            P[i,:] = A[:]
#
#        c = cad_nurbs(c3.knots, P, weights=c3.weights)
#        nrb = coons([[c1,c2],[c,c3]])
    # ...

    # ...
    if profile==2:
        raise("TCoons with profile 2 Not yet implemented")
#        A = c1.points[0,:]
#
#        P = np.zeros_like(c3.points)
#        for i in range(0,P.shape[0]):
#            P[i,:] = A[:]
#
#        c = cad_nurbs(c3.knots, P, weights=c3.weights)
#        nrb = coons([[c1,c2],[c,c3]])
    # ...

    # ...
    if profile==3:
        raise("TCoons with profile 3 Not yet implemented")
#        A = c1.points[0,:]
#
#        P = np.zeros_like(c3.points)
#        for i in range(0,P.shape[0]):
#            P[i,:] = A[:]
#
#        c = cad_nurbs(c3.knots, P, weights=c3.weights)
#        nrb = coons([[c1,c2],[c,c3]])
    # ...

    # ...

    return nrb


class cad_io:
    def __init__(self, file, mode="r"):
        """Open file and return a corresponding stream. If the file cannot be opened, an IOError is raised.
        file must be in ['xml', 'txt', 'zip']
        TODO : add hdf5 format

        Args:
            file: file name.
            mode: is an optional string that specifies the mode in which the file is opened. It defaults to 'r' which means open for reading in text mode. Other common values are 'w' for writing (truncating the file if it already exists)

        Returns:
            A file stream

        Raises:
            IOError: An error occurred accessing the bigtable.Table object.
        """
        self.__filename__ = file
        self.__format__ = str(file.split('.')[-1]).lower()

        self.mode = mode
        if self.mode not in ["r","w"]:
            print("cad_io : mode must be r or w")
            raise

        if self.__format__ not in ["xml","zip","txt"]:
            print("cad_io : format must be xml, zip or txt")
            raise

    def read(self, geo):
        """
        Write the given cad_geometry to the underlying stream
        """
        if self.mode != "r":
            print("mode file must be set to r ")
            raise

        if self.__format__=="vtk":
            print("VTK import Not yet implemented")
            raise

        if self.__format__=="hdf5":
            print("DHF5 import Not yet implemented")
            raise

        if self.__format__=="xml":
            try:
                rw = XML()
                return rw.read(self.__filename__, geo)
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

    def write(self, geo):
        """
        Write the given cad_geometry geo
        """
        if self.mode != "w":
            print("mode file must be set to w ")
            raise

        if self.__format__=="hdf5":
            print("Not yet implemented")
            raise

        if self.__format__=="xml":
            try:
                rw = XML()
                rw.write(self.__filename__, geo)
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

        if self.__format__=="zip":
            try:
                rw = TXT()
                rw.write(self.__filename__, geo, fmt="zip")
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

        if self.__format__=="txt":
            try:
                rw = TXT()
                rw.write(self.__filename__, geo, fmt="txt")
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

class cad_object(object):
    def __new__(typ, *args, **kwargs):
        obj = object.__new__(typ)
        obj._attributs = {}
        obj.rational = False
        obj.orientation = None
        obj.face = None
        return obj

    def __init__(self):
        self._attributs = {}
        self.rational = False
        self.orientation = None
        self.face = None

    def _clone_data(self, other):
        try:
            self.rational       = other.rational
            self.orientation    = other.orientation
            self._attributs     = other._attributs
        except:
            pass

    def _copy_data(self, other):
        try:
            self.rational       = other.rational
            self.orientation    = other.orientation.copy()
            self._attributs     = other._attributs.copy()
        except:
            pass

    def set_attributs(self, attributs):
        """
        sets attributs for the current cad_nurbs object. Needed when
        constructing the geometry by *hand*
        """
        self._attributs = attributs

    def set_attribut(self, attribut, value):
        """
        sets attribut to the value value for the current cad_nurbs object. Needed when
        constructing the geometry by *hand*
        """
        self._attributs[attribut] = value

    def get_attribut(self, name):
        """
        returns attributs for the current cad_nurbs object.
        """
        try:
            return self._attributs[name]
        except:
            return None

    @property
    def attributs(self):
        return self._attributs

    def set_orientation(self, list_sgn):
        """
        sets the orientation of the boundary for the current cad_nurbs object.

        Parameters
        ----------
        list_sgn : list of floats
            list_sgn is a list of signs for each face. the length of list_sgn is equal to the number of faces; 2 in 1D, 4 in 2D and 6 in 3D.
            a sign is either +1 or -1.
        """
        self.orientation = list_sgn

    def set_rational(self, value):
        """
        make the current cad_nurbs object rational.

        Parameters
        ----------
        value : int
            if equal to 1: the cad_nurbs is rational, and we use weights each
            time we evaluate it at given sites.
            if equal to 0: the cad_nubrs is simply a spline object, no need to
            use weights.
        """
        self.rational = value

    @property
    def nFaces(self):
        if self.dim == 1:
            nfaces = 2
        if self.dim == 2:
            nfaces = 4
        if self.dim == 3:
            nfaces = 6
        return nfaces

    def metric(self, u=None, v=None, w=None):
        """
        compute and return the metric at the parametric 1D sites u, v, w
        """
        xyz = []
        Dw = self.evaluate_deriv(u=u,v=v,w=w,nderiv=1)
        if self.dim == 1:
            x    = Dw[0,:,:,0]
            xdu  = Dw[1,:,:,0]
            y    = Dw[0,:,:,1]
            ydu  = Dw[1,:,:,1]
            jac  = 1. / np.sqrt(xdu**2 + ydu**2)
            xyz = [x,y]
        if self.dim == 2:
            x    = Dw[0,:,:,0]
            xdu  = Dw[1,:,:,0]
            xdv  = Dw[2,:,:,0]
            y    = Dw[0,:,:,1]
            ydu  = Dw[1,:,:,1]
            ydv  = Dw[2,:,:,1]
            jac = xdu * ydv - xdv * ydu
            xyz = [x,y]
        if self.dim == 3:
            print("Not yet implemented")
            raise
        return xyz, jac

class cad_nurbs(cad_object, NURBS):
#class cad_nurbs(NURBS, cad_object):
#    def __new__(typ, *args, **kwargs):
#        obj = NURBS.__new__(typ)
#        obj._attributs = {}
#        obj.rational = False
#        obj.orientation = None
#        obj.face = None
#        return obj

    def __init__(self, *args, **kwargs):
        """
        creates a cad_nurbs object. arguments are the same as for a cad_nurbs object.
        rational, orientation and face are set to None. The user must specify
        them in order to finalize the construction of the cad_nurbs object.

        An abstract cad_nurbs object class.

        This cad_nurbs class allows for the definition of B-spline or cad_nurbs
        curves/surfaces/volumes by specifying a control point array, a
        sequence of knot vectors and optional rational weights.

        Parameters
        ----------
        control : array_like or 2-tuple of array_like
            Control points and optional rational weights.
        knots : sequence of array_like
            Knot vectors. The number of knot vectors will define what kind
            of cad_nurbs object is created (1=curve, 2=surface, 3=volume).
        weights : array_like, optional
           Rational weights. If weights are omitted, the object will be
           non-rational (B-spline).
        fields : array_like, optional
           Additional fields.

        Attributes
        ----------
        dim : int
            Parametric dimension of the cad_nurbs object {1,2,3}
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

        Examples
        --------

        Create a quarter circle cad_nurbs curve with 2D control points and
        rational weigths and check error:

        >>> C = [[0, 1], [1, 1], [1, 0]] # 3x2 grid of 2D control points
        >>> w = [1, np.sqrt(2)/2, 1]     # rational weigths
        >>> U = [0,0,0, 1,1,1]           # knot vector
        >>> crv = cad_nurbs([U], C, weights=w)
        >>> u = np.linspace(0,1,1000)
        >>> xyz = crv(u)
        >>> x, y, z = xyz.T
        >>> r = np.sqrt(x**2+y**2)
        >>> np.allclose(r, 1, rtol=0, atol=1e-15)
        True
        >>> np.allclose(z, 0, rtol=0, atol=1e-15)
        True

        Create a quarter circle cad_nurbs curve with homogeneous 4D control
        points and check error:

        >>> wgt = np.sqrt(2)/2
        >>> Cw = np.zeros((3,4))
        >>> Cw[0,:] = [0.0, 1.0, 0.0, 1.0]
        >>> Cw[1,:] = [wgt, wgt, 0.0, wgt]
        >>> Cw[2,:] = [1.0, 0.0, 0.0, 1.0]
        >>> crv = cad_nurbs([U], Cw)
        >>> u = np.linspace(0,1,1000)
        >>> xyz = crv(u)
        >>> x, y, z = xyz.T
        >>> r = np.sqrt(x**2+y**2)
        >>> np.allclose(r, 1, rtol=0, atol=1e-15)
        True
        >>> np.allclose(z, 0, rtol=0, atol=1e-15)
        True

        Create a random B-spline curve:

        >>> C = np.random.rand(3,3) # 3D control points
        >>> U = [0,0,0, 1,1,1]      # knot vector
        >>> crv = cad_nurbs([U], C)
        >>> crv.dim
        1
        >>> crv.shape
        (3,)
        >>> crv.degree
        (2,)
        >>> np.allclose(crv.knots[0], U, rtol=0, atol=1e-15)
        True
        >>> np.allclose(crv.points,   C, rtol=0, atol=1e-15)
        True
        >>> np.allclose(crv.weights,  1, rtol=0, atol=1e-15)
        True

        Create a random B-spline surface:

        >>> C = np.random.rand(3,2,3) # 3x2 grid of 3D control points
        >>> U = [0,0,0, 1,1,1]        # knot vector
        >>> V = [0,0, 1,1]            # knot vector
        >>> srf = cad_nurbs([U,V], C)
        >>> srf.dim
        2
        >>> srf.shape
        (3, 2)
        >>> srf.degree
        (2, 1)
        >>> np.allclose(srf.knots[0], U, rtol=0, atol=1e-15)
        True
        >>> np.allclose(srf.knots[1], V, rtol=0, atol=1e-15)
        True
        >>> np.allclose(srf.points,   C, rtol=0, atol=1e-15)
        True
        >>> np.allclose(srf.weights,  1, rtol=0, atol=1e-15)
        True

        Create a random B-spline volume:

        >>> C = np.random.rand(3,2,7,3) # 3x2x7 grid of 3D control points
        >>> U = [0,0,0, 1,1,1]          # knot vector
        >>> V = [0,0, 1,1]              # knot vector
        >>> W = [0]*4+[0.25, 0.5, 0.5]+[1]*4
        >>> vol = cad_nurbs([U,V,W], C)
        >>> vol.dim
        3
        >>> vol.shape
        (3, 2, 7)
        >>> vol.degree
        (2, 1, 3)
        >>> np.allclose(vol.knots[0], U, rtol=0, atol=1e-15)
        True
        >>> np.allclose(vol.knots[1], V, rtol=0, atol=1e-15)
        True
        >>> np.allclose(vol.knots[2], W, rtol=0, atol=1e-15)
        True
        >>> np.allclose(vol.points,   C, rtol=0, atol=1e-15)
        True
        >>> np.allclose(vol.weights,  1, rtol=0, atol=1e-15)
        True
        """
        NURBS.__init__(self, *args, **kwargs)
        cad_object.__init__(self)
        self._attributs = {}
        self.rational = False
        self.orientation = None
        self.face = None
        self.set_attribut("type",self.__class__.__name__ )

    def set_points(self, pts):
        """
        Sets the Control point grid projected into Cartesian 3D space.
        """
        self.array[...,:3] = pts * self.weights[...,np.newaxis]

    def _clone_data(self, nrb):
        # nrb can be NURBS or cad_nurbs
        self._array = nrb.array
        self._knots = nrb.knots
        cad_object._clone_data(self, nrb)

    def _copy_data(self, nrb):
        # nrb can be NURBS or cad_nurbs
        self._array = self.array.copy()
        self._knots = tuple(k.copy() for k in self.knots)

        cad_object._copy_data(self, nrb)

    def clone(self):
        """
        Clone a cad_nurbs object.

        Returns a new instace of the cad_nurbs objects with references to
        the control points and knot vectors of this cad_nurbs
        object. Modifying the knot vector or control points of the
        returned object WILL affect this object.

        Examples
        --------

        Create a random curve, copy the curve, change the control points,
        demonstrate that changing c2 changes c1.

        >>> C = np.random.rand(5,2)
        >>> U = [0,0,1,2,3,4,4]
        >>> c1 = cad_nurbs([U], C)
        >>> c2 = c1.clone()
        >>> c2.control[2,:] = [1.0,1.0,0.0,1.0]
        >>> (abs(c2.control-c1.control)).max() < 1.0e-15
        True
        """
        cad_nrb = cad_nurbs.__new__(type(self))
        cad_nrb._clone_data(self)
        return cad_nrb

    def copy(self):
        """
        Copy a cad_nurbs object.

        Returns a new instace of the cad_nurbs objects with copies to
        the control points and knot vectors of this cad_nurbs
        object.

        Examples
        --------

        Create a random curve, copy the curve, change the control points,
        demonstrate that changing c2 changes c1.

        >>> C = np.random.rand(5,2)
        >>> U = [0,0,1,2,3,4,4]
        >>> c1 = cad_nurbs([U], C)
        >>> c2 = c1.copy()
        >>> c2.control[2,:] = [1.0,1.0,0.0,1.0]
        >>> (abs(c2.control-c1.control)).max() < 1.0e-15
        True
        """
        cad_nrb = cad_nurbs.__new__(type(self))
        cad_nrb._array = self.array.copy()
        cad_nrb._knots = tuple(k.copy() for k in self.knots)
        cad_nrb._attributs = {}
        cad_nrb.rational = self.rational
        cad_nrb.orientation = self.orientation
        cad_nrb.face = self.face
        return cad_nrb

    def elevate(self, *args, **kwargs):
        """
        Degree elevate a cad_nurbs object.

        Given a polynomial degree to elevate in a parameter
        direction, degree-elevate the curve. The routine operates
        on the cad_nurbs object in-place and returns the object.

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
        >>> c1 = cad_nurbs([U], C)
        >>> c1.degree
        (2,)
        >>> c2 = c1.clone().elevate(0, 2)
        >>> c2.degree
        (4,)
        >>> u = np.linspace(0,1,100)
        >>> xyz1 = c1(u)
        >>> xyz2 = c2(u)
        >>> np.allclose(xyz1, xyz2, rtol=0, atol=1e-15)
        True

        Create a random surface, degree elevate, check error:

        >>> C = np.random.rand(3,3,3)
        >>> U = [0,0,0,1,1,1]
        >>> V = [0,0,0.5,1,1]
        >>> s1 = cad_nurbs([U,V], C)
        >>> s1.degree
        (2, 1)
        >>> s2 = s1.clone().elevate(0, 1).elevate(1, 1)
        >>> s2.degree
        (3, 2)
        >>> u = v = np.linspace(0,1,100)
        >>> xyz1 = s1(u, v)
        >>> xyz2 = s2(u, v)
        >>> np.allclose(xyz1, xyz2, rtol=0, atol=1e-15)
        True
        """
        nrb = NURBS.elevate(self, *args, **kwargs)
        cad_nrb = cad_nurbs.__new__(type(self))
        cad_nrb._clone_data(nrb)
        cad_nrb.rational = self.rational
        cad_nrb.orientation = self.orientation
        cad_nrb._attributs = self._attributs
        return cad_nrb

    #
    def evalMesh(self, npts=3):
        # ...
        def _refine_array(x, nref):
            u0 = x[0] ; u1 = x[-1]
            nx = len(x)
            ne = nx - 1
            xref = np.zeros((ne, nref))

            for i,(a,b) in enumerate(zip(x[:-1], x[1:])):
                xref[i,:] = np.linspace(a,b,nref+1)[0:-1]

            xref = xref.reshape(ne*nref)
            xref = np.concatenate((xref,np.asarray([u1])))

            return xref
        # ...
        breaks = self.breaks()

        if self.dim == 1:
            list_xref = []
            for u in breaks:
                list_xref.append(_refine_array(np.asarray(u), npts))
            return [self(list_xref)]
        if self.dim == 2:
            list_lines = []
            for i in range(0,2):
                xref = _refine_array(breaks[self.dim-i-1], npts)
                for brk in breaks[i]:
                    crv = self.extract(i, brk)
                    list_lines.append(crv(xref))
            return list_lines
        if self.dim == 3:
            print("Not yet implemented")

    def evaluate_deriv(self, *args, **kwargs):
        """
        evaluates a cad_nurbs object (and its derivatives) at the given parametric values.
        Degree elevate a cad_nurbs object.

        Parameters
        ----------
        u : float or array_like
            The first logical direction
        v : float or array_like
            The second logical direction
        w : float or array_like
            The third logical direction
        nderiv : int, optional
            Derivative order (Default=1)
        rationalize : int, optional
            Put to 1 if the cad_nurbs is a NURBS (need to use weights for evaluation)
        fields : bool or array_like, optional
            TODO

        Examples
        --------

        Import the circle curve, compute points position and their derivatives:

        >>> from caid.cad_geometry import circle
        >>> geo = circle()
        >>> nrb = geo[0].extract(1,0.)

        >>> n = 10
        >>> t = np.linspace(0,1,n)
        >>> Dw = nrb.evaluate_deriv(t)
        >>> x  = Dw[0,:,0]
        >>> y  = Dw[0,:,1]
        >>> dx = Dw[1,:,0]
        >>> dy = Dw[1,:,1]
        >>> plt.figure()
        >>> t = np.linspace(0,1,100)
        >>> D = nrb(t)
        >>> xc = D[:,0]
        >>> yc = D[:,1]
        >>> plt.plot(x,y, 'ob')
        >>> plt.plot(xc,yc, '-r')
        >>> plt.show()

        The following example, shows the import of the 2D circle description,
        the computation of points and their derivatives. Finally, we plot the
        jacobian of the mapping:

        >>> from caid.cad_geometry import circle as domain
        >>> nrb = domain()[0]

        >>> nx = 100
        >>> tx = np.linspace(0,1,nx)
        >>> ny = 100
        >>> ty = np.linspace(0,1,ny)
        >>> Dw = nrb.evaluate_deriv(tx,ty,nderiv=1)
        >>> x    = Dw[0,:,:,0]
        >>> xdu  = Dw[1,:,:,0]
        >>> xdv  = Dw[2,:,:,0]
        >>> y    = Dw[0,:,:,1]
        >>> ydu  = Dw[1,:,:,1]
        >>> ydv  = Dw[2,:,:,1]

        >>> plt.figure()
        >>> jac = xdu * ydv - xdv * ydu
        >>> plt.contourf(x,y,jac) ; plt.colorbar() ; plt.title("Jacobian of the mapping")
        >>> plt.show()

        see also :class:`cad_geometry.plotJacobians`

        """
        rationalize = 0
        if self.rational:
            rationalize = 1
        kwargs['rationalize'] = rationalize
        return NURBS.evaluate_deriv(self, *args, **kwargs)

    def extract_face(self, face):
        """
        Extracts a face from the current cad_nurbs object.

        Parameters
        ----------
        face : int
            the ID of the boundary when want to extract

        Returns
        -------
            a cad_nurbs object
        """
        dim = self.dim
        if dim > 2:
            print("extract_face : not yet implemeted")
            raise

        # ...
        nfaces =  4
        list_sgn = [1]*4

        if face == 0:
            axis = 1
            ubound = self.knots[axis][0]
        if face == 1:
            axis = 0
            ubound = self.knots[axis][0]
        if face == 2:
            axis = 1
            ubound = self.knots[axis][-1]
        if face == 3:
            axis = 0
            ubound = self.knots[axis][-1]

        nrb_bnd = self.extract(axis,ubound)
        cad_nrb = cad_nurbs.__new__(type(self))
        cad_nrb._array = nrb_bnd.array
        cad_nrb._knots = nrb_bnd.knots
        cad_nrb.rational = self.rational
        try:
            cad_nrb.orientation = [self.orientation[face]]
        except:
            pass
        cad_nrb._attributs = self._attributs
        cad_nrb.face = face

        return cad_nrb

    def plotBoundariesInfo(self):
        """
        plots some informations about the current cad_nurbs object, including
        the orientation of boundary.
        """
        from matplotlib import pyplot as plt
        nrb = self

        if nrb.dim == 2:
            # ...
            def plot_crv(  nrb, t1, t2, tangent=True, normal=False, color='b' \
                         , label=None,scale=1.e-1, width='0.00001'):
                Dw = nrb.evaluate_deriv(t1)

                x  = Dw[0,:,0]
                y  = Dw[0,:,1]
                dx = Dw[1,:,0]
                dy = Dw[1,:,1]

                D = nrb(t2)
                xc = D[:,0]
                yc = D[:,1]

                d = np.sqrt(dx**2 + dy**2)
                dx = scale * dx/d
                dy = scale * dy/d
                n = len(x)
                for i in range(0,n):
                    if tangent:
                        arr = plt.Arrow(x[i], y[i], dx[i],  dy[i], width=width)
                    if normal:
                        arr = plt.Arrow(x[i], y[i], dy[i], -dx[i], width=width)
                    arr.set_facecolor('g')
                    ax = plt.gca()
                    ax.add_patch(arr)
                plt.plot(x,y, 'o'+color)
                if label is not None:
                    plt.plot(xc,yc, '-'+color, label=label)
                else:
                    plt.plot(xc,yc, '-'+color)
            # ...

            plt.figure()
            list_faces  = [0, 1, 2, 3]
            list_colors = ['r', 'g', 'b', 'k']
            for (face, color) in zip(list_faces, list_colors):
                if face in [0,2]:
                    axis = 0
                else:
                    axis = 1

                t1b = nrb.knots[axis][0] ; t1e = nrb.knots[axis][-1]
                t2b = nrb.knots[axis][0] ; t2e = nrb.knots[axis][-1]
                t1 = np.linspace(t1b,t1e,10)
                t2 = np.linspace(t2b,t2e,100)
                nrb_bnd = nrb.extract_face(face)
                plot_crv(nrb_bnd, t1, t2, tangent=False, normal=True, color=color,
                         label='Face '+str(face),scale=1.e-1, width='0.00001')
            plt.legend()

    def evaluate_deriv(self, u=None, v=None, w=None \
                       , fields=None, nderiv=1, rationalize=0):
        """
        Evaluate the NURBS object at the given parametric values.

        Parameters
        ----------
        u, v, w : float or array_like
        fields : bool or array_like, optional

        Examples
        --------

        >>> C = [[-1,0],[0,1],[1,0]]
        >>> U = [0,0,0,1,1,1]
        >>> crv = NURBS([U], C)
        >>> crv.evaluate(0.5).tolist()
        [0.0, 0.5, 0.0]
        >>> crv.evaluate([0.5]).tolist()
        [[0.0, 0.5, 0.0]]
        >>> crv.evaluate([0,1]).tolist()
        [[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]

        """
        def Arg(p, U, u):
            u = np.asarray(u, dtype='d')
            assert u.min() >= U[p]
            assert u.max() <= U[-p-1]
            return u
        #
        dim = self.dim
        nderivatives = nderiv
        if dim == 1:
            if nderiv == 1:
                nderivatives = 1
            if nderiv == 2:
                nderivatives = 1+1
        if dim == 2:
            if nderiv == 1:
                nderivatives = 2
            if nderiv == 2:
                nderivatives = 2+3
        if dim == 3:
            if nderiv == 1:
                nderivatives = 3
            if nderiv == 2:
                nderivatives = 3+6

        uvw = [u,v,w][:dim]
        for i, a in enumerate(uvw):
            if a is None:
                uvw[i] = self.breaks(i)
            else:
                U = self.knots[i]
                p = self.degree[i]
                uvw[i] = Arg(p, U, a)
        #

        #
        if fields is None or isinstance(fields, bool):
            F = None
        else:
            F = np.asarray(fields, dtype='d')
            shape = self.shape
            if F.shape == shape:
                F = F[...,np.newaxis]
            else:
                assert F.ndim-1 == len(shape)
                assert F.shape[:-1] == shape
            fields = True
        #
        if F is not None:
            Cw = self.control
            w = Cw[...,3,np.newaxis]
            CwF = np.concatenate([Cw, F*w], axis=-1)
            array = np.ascontiguousarray(CwF)
        else:
            array = self.array
        arglist = [nderiv, nderivatives, rationalize]
        for p, U in zip(self.degree, self.knots):
            arglist.extend([p, U])
        arglist.append(array)
        arglist.extend(uvw)
        #
        Evaluate = getattr(_bsp, 'EvaluateDeriv%d' % self.dim)
        CwF = Evaluate(*arglist)
        return CwF[...,:3]

    def grad(self, u=None, v=None, w=None):
        ndim = len(self.shape)
        Dw = self.evaluate_deriv(u=u, v=v, w=w)

        xyz_arrays = []
        du  = Dw[1,...,:]
        xyz_arrays.append(du)

        if ndim > 1:
            dv  = Dw[2,...,:]
            xyz_arrays.append(dv)

        if ndim > 2:
            dt  = Dw[3,...,:]
            xyz_arrays.append(dt)

        return xyz_arrays

    def second_deriv(self, u=None, v=None, w=None):
        ndim = len(self.shape)
        Dw = self.evaluate_deriv(u=u, v=v, w=w, nderiv=2)

        if ndim == 1:
            nb = 2
            ne = 3
        if ndim == 2:
            nb = 3
            ne = 6
        if ndim == 3:
            nb = 4
            ne = 10

        xyz_arrays = []
        for i in range(nb,ne):
            du = Dw[i,...,:]
            xyz_arrays.append(du)

        return xyz_arrays

    def tangent(self, u=None, v=None, w=None, unit=True):
        Dw = self.evaluate_deriv(u=u, v=v, w=w)

        dx = Dw[1,:,0]
        dy = Dw[1,:,1]
        if unit:
            d = np.sqrt(dx**2 + dy**2)
            dx = dx/d
            dy = dy/d
        return dx, dy

    def normal(self, u=None, v=None, w=None, unit=True):
        Dw = self.evaluate_deriv(u=u, v=v, w=w)

        dx = Dw[1,:,0]
        dy = Dw[1,:,1]
        if unit:
            d = np.sqrt(dx**2 + dy**2)
            dx = dx/d
            dy = dy/d
        return -dy, dx
    #


class cad_op_nurbs(opNURBS, cad_object):
    def __new__(typ, *args, **kwargs):
        obj = object.__new__(typ)
        obj._attributs = {}
        obj.rational = False
        obj.orientation = None
        obj.face = None
        obj._nrb = None
        return obj

    def __init__(self, op_nrb):
        self._nrb = op_nrb
        cad_object.__init__(self)
        self.set_attribut("type",self.__class__.__name__ )
        self.set_attribut("operator",op_nrb.__class__.__name__ )

    @property
    def array(self):
        return self._nrb.array

    @property
    def knots(self):
        return self._nrb.knots

    def _clone_data(self, op_nrb):
        # nrb can be opNURBS or cad_op_nurbs
        self._array = op_nrb.array
        self._knots = op_nrb.knots
        cad_object._clone_data(self, op_nrb)
        self._nrb = op_nrb._nrb

    def clone(self):
        """
        Clone a cad_op_nurbs object.

        Returns a new instace of the cad_nurbs objects with references to
        the control points and knot vectors of this cad_nurbs
        object. Modifying the knot vector or control points of the
        returned object WILL affect this object.

        Examples
        --------

        Create a random curve, copy the curve, change the control points,
        demonstrate that changing c2 changes c1.

        >>> C = np.random.rand(5,2)
        >>> U = [0,0,1,2,3,4,4]
        >>> nrb = NURBS([U], C)
        >>> gnrb = grad(nrb)
        >>> c1 = cad_op_nurbs(gnrb)
        >>> c2 = c1.clone()
        >>> c2.control[2,:] = [1.0,1.0,0.0,1.0]
        >>> (abs(c2.control-c1.control)).max() < 1.0e-15
        True
        """
        cad_nrb = cad_op_nurbs.__new__(type(self))
        cad_nrb._clone_data(self)
        return cad_nrb

    def elevate(self, *args, **kwargs):
        """
        Degree elevate a cad_nurbs object.

        Given a polynomial degree to elevate in a parameter
        direction, degree-elevate the curve. The routine operates
        on the cad_nurbs object in-place and returns the object.

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
        >>> c1 = cad_nurbs([U], C)
        >>> c1.degree
        (2,)
        >>> c2 = c1.clone().elevate(0, 2)
        >>> c2.degree
        (4,)
        >>> u = np.linspace(0,1,100)
        >>> xyz1 = c1(u)
        >>> xyz2 = c2(u)
        >>> np.allclose(xyz1, xyz2, rtol=0, atol=1e-15)
        True

        Create a random surface, degree elevate, check error:

        >>> C = np.random.rand(3,3,3)
        >>> U = [0,0,0,1,1,1]
        >>> V = [0,0,0.5,1,1]
        >>> s1 = cad_nurbs([U,V], C)
        >>> s1.degree
        (2, 1)
        >>> s2 = s1.clone().elevate(0, 1).elevate(1, 1)
        >>> s2.degree
        (3, 2)
        >>> u = v = np.linspace(0,1,100)
        >>> xyz1 = s1(u, v)
        >>> xyz2 = s2(u, v)
        >>> np.allclose(xyz1, xyz2, rtol=0, atol=1e-15)
        True
        """
        nrb = NURBS.elevate(self, *args, **kwargs)
        cad_nrb = cad_nurbs.__new__(type(self))
        cad_nrb._clone_data(nrb)
        cad_nrb.rational = self.rational
        cad_nrb.orientation = self.orientation
        cad_nrb._attributs = self._attributs
        return cad_nrb

    def evaluate(self, *args, **kwargs):
        return self._nrb.evaluate(*args, **kwargs)

    def evaluate_deriv(self, *args, **kwargs):
        """
        evaluates a cad_nurbs object (and its derivatives) at the given parametric values.
        Degree elevate a cad_nurbs object.

        Parameters
        ----------
        u : float or array_like
            The first logical direction
        v : float or array_like
            The second logical direction
        w : float or array_like
            The third logical direction
        nderiv : int, optional
            Derivative order (Default=1)
        rationalize : int, optional
            Put to 1 if the cad_nurbs is a NURBS (need to use weights for evaluation)
        fields : bool or array_like, optional
            TODO

        Examples
        --------

        Import the circle curve, compute points position and their derivatives:

        >>> from caid.cad_geometry import circle
        >>> geo = circle()
        >>> nrb = geo[0].extract(1,0.)

        >>> n = 10
        >>> t = np.linspace(0,1,n)
        >>> Dw = nrb.evaluate_deriv(t)
        >>> x  = Dw[0,:,0]
        >>> y  = Dw[0,:,1]
        >>> dx = Dw[1,:,0]
        >>> dy = Dw[1,:,1]
        >>> plt.figure()
        >>> t = np.linspace(0,1,100)
        >>> D = nrb(t)
        >>> xc = D[:,0]
        >>> yc = D[:,1]
        >>> plt.plot(x,y, 'ob')
        >>> plt.plot(xc,yc, '-r')
        >>> plt.show()

        The following example, shows the import of the 2D circle description,
        the computation of points and their derivatives. Finally, we plot the
        jacobian of the mapping:

        >>> from caid.cad_geometry import circle as domain
        >>> nrb = domain()[0]

        >>> nx = 100
        >>> tx = np.linspace(0,1,nx)
        >>> ny = 100
        >>> ty = np.linspace(0,1,ny)
        >>> Dw = nrb.evaluate_deriv(tx,ty,nderiv=1)
        >>> x    = Dw[0,:,:,0]
        >>> xdu  = Dw[1,:,:,0]
        >>> xdv  = Dw[2,:,:,0]
        >>> y    = Dw[0,:,:,1]
        >>> ydu  = Dw[1,:,:,1]
        >>> ydv  = Dw[2,:,:,1]

        >>> plt.figure()
        >>> jac = xdu * ydv - xdv * ydu
        >>> plt.contourf(x,y,jac) ; plt.colorbar() ; plt.title("Jacobian of the mapping")
        >>> plt.show()

        see also :class:`cad_geometry.plotJacobians`

        """
        rationalize = 0
        if self.rational:
            rationalize = 1
        kwargs['rationalize'] = rationalize
        return self._nrb.evaluate_deriv(*args, **kwargs)

    def extract_face(self, face):
        """
        Extracts a face from the current cad_nurbs object.

        Parameters
        ----------
        face : int
            the ID of the boundary when want to extract

        Returns
        -------
            a cad_nurbs object
        """
        dim = self.dim
        if dim > 2:
            print("extract_face : not yet implemeted")
            raise

        # ...
        nfaces =  4
        list_sgn = [1]*4

        if face == 0:
            axis = 1
            ubound = self.knots[0][0]
        if face == 1:
            axis = 0
            ubound = self.knots[1][0]
        if face == 2:
            axis = 1
            ubound = self.knots[0][-1]
        if face == 3:
            axis = 0
            ubound = self.knots[1][-1]

        nrb_bnd = self.extract(axis,ubound)
        cad_nrb = cad_nurbs.__new__(type(self))
        cad_nrb._array = nrb_bnd.array
        cad_nrb._knots = nrb_bnd.knots
        cad_nrb.rational = self.rational
        cad_nrb.orientation = [self.orientation[face]]
        cad_nrb._attributs = self._attributs
        cad_nrb.face = face

        return cad_nrb

    def plotBoundariesInfo(self):
        """
        plots some informations about the current cad_nurbs object, including
        the orientation of boundary.
        """
        from matplotlib import pyplot as plt
        nrb = self

        if nrb.dim == 2:
            # ...
            def plot_crv(  nrb, t1, t2, tangent=True, normal=False, color='b' \
                         , label=None,scale=1.e-1, width='0.00001'):
                Dw = nrb.evaluate_deriv(t1)

                x  = Dw[0,:,0]
                y  = Dw[0,:,1]
                dx = Dw[1,:,0]
                dy = Dw[1,:,1]

                D = nrb(t2)
                xc = D[:,0]
                yc = D[:,1]

                d = np.sqrt(dx**2 + dy**2)
                dx = scale * dx/d
                dy = scale * dy/d
                n = len(x)
                for i in range(0,n):
                    if tangent:
                        arr = plt.Arrow(x[i], y[i], dx[i],  dy[i], width=width)
                    if normal:
                        arr = plt.Arrow(x[i], y[i], dy[i], -dx[i], width=width)
                    arr.set_facecolor('g')
                    ax = plt.gca()
                    ax.add_patch(arr)
                plt.plot(x,y, 'o'+color)
                if label is not None:
                    plt.plot(xc,yc, '-'+color, label=label)
                else:
                    plt.plot(xc,yc, '-'+color)
            # ...
            t1b = nrb.knots[0][0] ; t1e = nrb.knots[0][-1]
            t2b = nrb.knots[0][0] ; t2e = nrb.knots[0][-1]
            t1 = np.linspace(t1b,t1e,10)
            t2 = np.linspace(t2b,t2e,100)

            plt.figure()
            list_faces  = [0, 1, 2, 3]
            list_colors = ['r', 'g', 'b', 'k']
            for (face, color) in zip(list_faces, list_colors):
                nrb_bnd = nrb.extract_face(face)
                plot_crv(nrb_bnd, t1, t2, tangent=False, normal=True, color=color,
                         label='Face '+str(face),scale=1.e-1, width='0.00001')
            plt.legend()

class cad_grad_nurbs(cad_op_nurbs):
    def __init__(self, *args, **kwargs):
        cad_op_nurbs.__init__(self, *args, **kwargs)

class cad_geometry(object):
    def __new__(typ, *args, **kwargs):
        obj = object.__new__(typ)
        obj._list           = []
        obj._currentElt     = -1
        obj._internal_faces = []
        obj._external_faces = []
        obj._connectivity   = []
        obj._attributs      = {}

        return obj

    def __init__(self, file=None, geo=None):
        """
        Creates a cad_geometry object.

        Examples
        --------

        Import a predefined geometry

        >>> from caid.cad_geometry import circle
        >>> geo = circle(radius=2.)

        print the number of patchs

        >>> print geo.npatchs
        1

        even in 2D, a cad_geometry is a 3D surface

        >>> print geo.Rd
        3

        the dimension of the logical domain is

        >>> print geo.dim
        2

        Next, we print some information about the connectivity, internal and
        external faces. These informations are important for a FEM solver.

        >>> geo.connectivity
        []

        >>> geo.external_faces
        [[0, 0], [0, 1], [0, 2], [0, 3]]

        >>> geo.internal_faces
        []

        In the next example, we create a circle cad_geometry object, with a
        logical grid of 31x31 internal points, using cubic NURBS

        >>> geo = circle(radius=2., n=[31,31], p=[3,3])

        Read XML file describing the geometry

        >>> geo = cad_geometry("mydomain.xml")
        """
        self._list = []
        self._currentElt = -1
        self._internal_faces = []
        self._external_faces = []
        self._connectivity   = []
        self._attributs      = {}

        if file is not None:
            self.__filename__ = file
            geo_io = cad_io(self.__filename__, mode="r")
            self = geo_io.read(self)

        if geo is not None:
            # TODO : que faire pour les infos??
            self.append(geo)

    def save(self, file):
        """
        saves the current cad_geometry. The current formats are ['xml', 'txt', 'zip']
        see :class:cad_io for more details
        """
        geo_io = cad_io(file, mode="w")
        geo_io.write(self)

    @property
    def internal_faces(self):
        """
        returns the internal faces for the current cad_geometry object
        """
        return self._internal_faces

    @property
    def external_faces(self):
        """
        returns the external faces for the current cad_geometry object

        Examples
        --------
        This example is given from the annulus cad_geometry object

        >>> from caid.cad_geometry import annulus
        >>> geo.external_faces
        [[0, 0], [0, 2]]

        """
        return self._external_faces

    @property
    def connectivity(self):
        """
        returns the connectivity of the current cad_geometry object
        The connectivity is a list of dictionaries. Each dictionary contains two
        keys:
            original:
                a couple of master-patch and master-face as [patch_id, face_id]
            clone:
                a couple of slave-patch and slave-face as [patch_id, face_id]


        Examples
        --------
        This example is given from the annulus cad_geometry object

        >>> from caid.cad_geometry import annulus
        >>> geo.connectivity
        [{'clone': [0, 3], 'original': [0, 1]}]

        """
        return self._connectivity

    @property
    def list_all(self):
        return self._list

    @property
    def dim(self):
        """
        Parametric dimension of the geometry object {1,2,3}.
        """
        try:
            dim = self._list[0].dim
        except:
            dim = 0
        return dim

    @property
    def Rd(self):
        """
        Physical dimension of the geometry object {1,2,3}.
        """
        try:
            Rd = self._list[0].points.shape[-1]
        except:
            Rd = 0
        return Rd

    def __len__(self):
        return len(self._list)

    @property
    def npatchs(self):
        """
        number of patchs of the geometry
        """
        return len(self._list)

    def index(self, nrb):
        return self._list.index(nrb)

    def set_internal_faces(self, values):
        """
        Sets the list of internal faces

        Examples
        --------
        This example is given from the annulus cad_geometry object

        >>> geo.set_internal_faces([[0,1],[0,3]])

        """
        self._internal_faces = values

    def set_external_faces(self, values):
        """
        Sets the list of external faces

        Examples
        --------
        This example is given from the annulus cad_geometry object

        >>> geo.set_external_faces([[0,0],[0,2]])

        """
        self._external_faces = values

    def set_connectivity(self, values):
        """
        Sets the list of connectivities. Connectivities is a list of dictionaries.
        Each dictionary contains two keys 'original' the master-face and 'clone'
        the slave-face.
        Each connectivity is a couple [patch_id, face_id]

        Examples
        --------
        This example is given from the annulus cad_geometry object

        >>> list_connectivity = []
        >>> dict_con = {}
        >>> dict_con['original'] = [0,1]
        >>> dict_con['clone'] = [0,3]
        >>> list_connectivity.append(dict_con)
        >>> geo.set_connectivity(list_connectivity)

        """
        self._connectivity = values

    def add_internal_face(self, values):
        """
        add an external face.

        Args:
            values: is a couple [patch_id,face_id]

        Examples
        --------
        This example is given from the annulus cad_geometry object

        >>> geo.add_external_face([0,2])

        """
        self._internal_faces.append(values)

    def add_external_face(self, values):
        """
        add an internal face.

        Args:
            values: is a couple [patch_id,face_id]

        Examples
        --------
        This example is given from the annulus cad_geometry object

        >>> geo.add_internal_face([0,1])

        """
        self._external_faces.append(values)

    def add_connectivity(self, values):
        """
        Add a Connectivity.

        Args:
            values: is a dictionary that contains two keys 'original' the master-face and 'clone'
        the slave-face.
        Each connectivity is a couple [patch_id, face_id]

        Examples
        --------
        This example is given from the annulus cad_geometry object

        >>> dict_con = {}
        >>> dict_con['original'] = [0,1]
        >>> dict_con['clone'] = [0,3]
        >>> geo.add_connectivity(dict_con)

        """
        self._connectivity.append(values)

    def set_attributs(self, attributs):
        """
        sets attributs for the current cad_geometry object. Needed when
        constructing the geometry by *hand*
        """
        self._attributs = attributs

    def set_attribut(self, attribut, value):
        """
        sets attribut to the value value for the current cad_geometry object. Needed when
        constructing the geometry by *hand*
        """
        self._attributs[attribut] = value

    def get_attribut(self, name):
        """
        returns attributs for the current cad_geometry object.
        """
        try:
            return self._attributs[name]
        except:
            return None

    @property
    def attributs(self):
        return self._attributs

    def __next__(self):
        if self.npatchs == 0:
            raise StopIteration
        self._currentElt += 1
        if self._currentElt >= self.npatchs:
            self._currentElt = -1
            raise StopIteration
        return self._list[self._currentElt]

    def __iter__(self):
        for nrb in self._list:
            yield nrb

    def __getitem__(self, key):
        return self._list[key]

    def append(self, nrb):
        """
        append a cad_nurbs object in the current cad_geometry object. After
        appending all cad_nurbs, please do not forget to specify
        internal/external faces and the global connectivity.

        Args:
            nrb: a cad_nurbs object

        Examples
        --------

        >>> from caid.cad_geometry import quart_circle, cad_geometry
        >>> nrb = quart_circle()[0]
        >>> geo = cad_geometry()
        >>> geo.append(nrb)

        """
        list_objects = ["cad_nurbs", "cad_object", "cad_op_nurbs", "cad_grad_nurbs"]
        if nrb.__class__.__name__ in list_objects:
            self._list.append(nrb)
        else:
            print("Warning: inserted object is not in ", list_objects)
            print("the current object is ", nrb.__class__.__name__)
            cad_nrb = cad_nurbs.__new__(cad_nurbs)
            cad_nrb._array = nrb.array
            cad_nrb._knots = nrb.knots
            self._list.append(cad_nrb)
#            raise NameError("cad_geometry class only handles cad_nurbs objects")


    def remove(self, nrb):
        """
        remove a cad_nurbs object in the current cad_geometry object. After
        removing a cad_nurbs, please do not forget to specify
        internal/external faces and the global connectivity.

        Args:
            nrb: a cad_nurbs object

        Examples
        --------

        >>> from caid.cad_geometry import quart_circle, cad_geometry
        >>> nrb = quart_circle()[0]
        >>> geo = cad_geometry()
        >>> geo.append(nrb)
        >>> print geo.npatchs
        1
        >>> geo.remove(nrb)
        >>> print geo.npatchs
        0

        """
        self._list.remove(nrb)

    def initialize_info(self):
        self._internal_faces = []
        self._external_faces = []
        self._connectivity   = []

    def translate(self, displ, axis=None):
        for nrb in self:
            nrb.translate(displ, axis=axis)

    def move(self, displ, axis=None):
        for nrb in self:
            nrb.move(displ, axis=axis)

    def scale(self, scale, axis=None):
        for nrb in self:
            nrb.scale(scale, axis=axis)

    def rotate(self, angle, axis=2):
        for nrb in self:
            nrb.rotate(angle, axis=axis)

    def refine(self, id=None, list_t=None, list_p=None, list_m=None):
        """
        refine the current cad_geometry object. If id is not specified, the refinement will affect all patchs.
        Otherwise, it will refine the given patch.

        Args:
            list_t (list of 1D numpy array):
                these are the internal knots to insert. You can use duplicated
                knots for the k-refinement

            list_p (list of int):
                this is the list of the final B-spline degrees

            list_m (list of int):
                this is the list of multiplicities of inserted knots for each axis

        Examples
        --------

        This example is taken from a the construction of the unit square as a
        cad_geometry

        >>> list_t = None
        >>> if n is not None:
        >>>     list_t = []
        >>>     for axis in range(0,cad_nrb.dim):
        >>>         ub = cad_nrb.knots[axis][0]
        >>>         ue = cad_nrb.knots[axis][-1]
        >>>         list_t.append(np.linspace(ub,ue,n[axis]+2)[1:-1])
        >>> list_p = None
        >>> if p is not None:
        >>>     list_p = []
        >>>     for axis in range(0,cad_nrb.dim):
        >>>         list_p.append(p[axis] - cad_nrb.degree[axis])
        >>> geo.refine(list_t=list_t, list_p=list_p, list_m=[1,1])

        """

        if id is not None:
            list_id = [id]
        else:
            list_id = list(range(0, self.npatchs))

        ll_hrefine = False
        if list_t is not None:
            ll_hrefine = True

        ll_prefine = False
        if list_p is not None:
            ll_prefine = True

        if list_m is None:
            list_m = np.ones(self.dim, dtype=np.int)

        for id in list_id:
            patch = self._list[id]
            if ll_prefine:
                P_ = patch
                dim = P_.dim
                for i in range(0,dim):
                    if list_p[i] > 0:
                        P_ = P_.clone().elevate(i, times=list_p[i])
                self._list[id] = P_

            patch = self._list[id]
            if ll_hrefine:
                P_ = patch
                dim = P_.dim
                for i in range(0,dim):
                    if len(list_t[i]) > 0:
                        m = list_m[i]
                        for j in range(0,m):
                            P_ = P_.clone().refine(i, list_t[i])
                self._list[id] = P_

    def expand(self):
        """
        returns a list of cad_geometries for each patch
        the connectivity is then broken.
        .. todo: handle the internal/external faces automatically
        """
        list_cad_geo = []
        for i in range(0, self.npatchs):
            tmp = cad_geometry(geo=self._list[i])
            list_cad_geo.append(tmp)
        return list_cad_geo

    def evalMesh(self, id=None, npts=3):
        """
        Evaluate and return the mesh

        Kwargs:
            id:
                if None the evaluation will be done over all patchs. Otherwise,
                it will be done on the specified patch

        Returns:
            TODO

        """
        if id is None:
            list_id = list(range(0, self.npatchs))
        else:
            list_id = [id]

        list_Mesh = []
        for i in list_id:
            geo = self._list[i]
            type_geo = geo.__class__.__name__
            if type_geo == "cad_nurbs" :
                list_Mesh.append(geo.evalMesh(npts))

        return list_Mesh

    def copy(self):
        """
        copy the current cad_geometry object

        Returns:
            a cad_geometry
        """
        geo = cad_geometry.__new__(type(self))
        for i in range(0, self.npatchs):
            P = self[i]
            geo.append(P.copy())
        geo.set_internal_faces(self.internal_faces)
        geo.set_external_faces(self.external_faces)
        geo.set_connectivity(self.connectivity)
        return geo

    def clone(self):
        """
        clone the current cad_geometry object

        Returns:
            a cad_geometry
        """
        geo = cad_geometry.__new__(type(self))
        for i in range(0, self.npatchs):
            P = self[i]
            geo.append(P.clone())
        geo.set_internal_faces(self.internal_faces)
        geo.set_external_faces(self.external_faces)
        geo.set_connectivity(self.connectivity)
        geo.set_attributs(self.attributs)
        return geo


    def polarExtrude(self, t=0., xyzc=None):
        """
        this routine creates a 2D geometry from a 1D closed curve
        self must be a curve

        Kwargs:
            xyzc (array):
                the center of the domain. default value is the mean of each of
                the coordinates

            t (float):
                if t> 0. it constructs an internal curve using a homothetic with
                respect to xyzc

        Returns:
            a cad_geometry

        """
        crv = self[0]
        P = crv.points
        x = P[:,0] ; y = P[:,1]

        if xyzc is None:
            xc = x.mean() ; yc = y.mean()
        else:
            xc = xyzc[0] ; yc = xyzc[1]

        Qx = xc + t * (x-xc)
        Qy = yc + t * (y-yc)
        Q = np.zeros_like(P)
        Q[:,0] = Qx ; Q[:,1] = Qy

        n = P.shape[0]
        C = np.zeros((2,n,3))
        C[0,:,:] = Q
        C[1,:,:] = P

        W = np.zeros((2,n))
        W[0,:] = crv.weights
        W[1,:] = crv.weights

        knots = [np.asarray([0., 0., 1., 1.]), crv.knots[0]]
        srf = cad_nurbs(knots, C, weights=W)
        srf.rational = crv.rational
        srf.orientation = [1,-1,-1,1]

        geo = cad_geometry()
        geo.append(srf)

        if t > 0.:
            geo._internal_faces = [[0,0],[0,2]]
            geo._external_faces = [[0,1],[0,3]]
        if t == 0.:
            geo._internal_faces = [[0,0],[0,1],[0,2]]
            geo._external_faces = [[0,3]]

        geo._connectivity   = []
        dict_con = {}
        dict_con['original'] = [0,0]; dict_con['clone'] = [0,2]
        geo._connectivity.append(dict_con)

        return geo

    def merge(self, geo_s, npts=5, tol=1.e-3):
        """
        merge two cad_geometries and return a new cad_geometry including an
        update for internal/external faces and connectivity.
        TODO: treate the 1D and 3D cases

        Args:
            geos_s (cad_geometry):
                This is the slave cad_geometry

        Kwargs:
            npts (int):
                used to evaluate and check equality of the extracted boundaries.
                Default value is 5

        Returns:
            a cad_geometry

        Examples
        --------

        This example is taken from the circle_5mp

        >>> # ... Import the quart_circle domain
        >>> geo_1 = quart_circle(rmin=rmin, rmax=rmax, n=n,p=p)
        >>> # ... Import the quart_circle domain
        >>> geo_2 = quart_circle(rmin=rmin, rmax=rmax, n=n,p=p)
        >>> geo_2[0].rotate(0.5*np.pi)
        >>> # ... Import the quart_circle domain
        >>> geo_3 = quart_circle(rmin=rmin, rmax=rmax, n=n,p=p)
        >>> geo_3[0].rotate(np.pi)
        >>> geo_3[0].reverse(0)
        >>> # ... Import the quart_circle domain
        >>> geo_4 = quart_circle(rmin=rmin, rmax=rmax, n=n,p=p)
        >>> geo_4[0].rotate(1.5*np.pi)
        >>> geo_4[0].reverse(0)
        >>> # ... Import the circle domain
        >>> geo_5 = circle(radius=rmin,n=n,p=p)
        >>> geo_5[0].rotate(0.25*np.pi)
        >>> geo_5[0].rotate(0.5*np.pi)
        >>> geo_12   = geo_1.merge(geo_2)
        >>> geo_34   = geo_3.merge(geo_4)
        >>> geo_1234 = geo_12.merge(geo_34)
        >>> geo      = geo_1234.merge(geo_5)

        """
        geo_m = self
        geo = cad_geometry()
        # ... copy master patchs
        for i_m in range(0, geo_m.npatchs):
            geo.append(geo_m[i_m])
        # ... copy slave patchs
        for i_s in range(0, geo_s.npatchs):
            geo.append(geo_s[i_s])

        if geo_m.dim == 1:
            nfaces = 2
        if geo_m.dim == 2:
            nfaces = 4
        if geo_m.dim == 3:
            nfaces = 6

        connectivity   = []
        for dict_con in geo_m._connectivity:
            connectivity.append(dict_con)
        for dict_con in geo_s._connectivity:
            [i_m,f_m] = dict_con['original']
            [i_s,f_s] = dict_con['clone']
            _dict_con = {}
            _dict_con['original'] = [i_m+geo_m.npatchs,f_m]
            _dict_con['clone']    = [i_s+geo_m.npatchs,f_s]
            connectivity.append(_dict_con)

        intext_faces_m = np.zeros((geo_m.npatchs, nfaces), dtype=np.int)
        intext_faces_s = np.zeros((geo_s.npatchs, nfaces), dtype=np.int)
        for i_m in range(0, geo_m.npatchs):
            nrb_m = geo_m[i_m]
            for i_s in range(0, geo_s.npatchs):
                nrb_s = geo_s[i_s]

                for f_m in range(0, nfaces):
                    bnd_m = nrb_m.extract_face(f_m).clone()
                    u_m = np.linspace(bnd_m.knots[0][0],bnd_m.knots[0][-1],npts)
                    P_m = bnd_m(u_m)
                    for f_s in range(0, nfaces):
                        bnd_s = nrb_s.extract_face(f_s).clone()
                        u_s = np.linspace(bnd_s.knots[0][0],bnd_s.knots[0][-1],npts)
                        P_s = bnd_s(u_s)

                        isSameFace = np.allclose(P_m, P_s, rtol=0, atol=tol)
                        isInvertFace = np.allclose(P_m[::-1], P_s, rtol=0, atol=tol)
                        if isSameFace:
                            dict_con = {}
                            dict_con['original'] = [i_m,f_m]
                            dict_con['clone']    = [i_s+geo_m.npatchs,f_s]
                            connectivity.append(dict_con)
                            intext_faces_m[i_m, f_m] = 1
                            intext_faces_s[i_s, f_s] = 1
                        if isInvertFace:
                            print("Merging Error: Found uncorrect orientation. Please change the orientation of the patchs (master,slave): ("\
                                    ,i_m,",",i_s,").")

                            print("Occured on the faces (master, slave): (",f_m,",",f_s,").")


        for intFace in geo_m._internal_faces:
            [i, f] = intFace
            if intext_faces_m[i, f] == 0:
                intext_faces_m[i, f] = 1
        for intFace in geo_s._internal_faces:
            [i,f] = intFace
            if intext_faces_s[i, f] == 0:
                _intFace = [i+geo_m.npatchs,f]
                intext_faces_s[i, f] = 1

        internalFaces = []
        externalFaces = []
        for i_m in range(0, geo_m.npatchs):
            for f_m in range(0, nfaces):
                if intext_faces_m[i_m,f_m] == 1:
                    internalFaces.append([i_m, f_m])
                else:
                    externalFaces.append([i_m, f_m])
        for i_s in range(0, geo_s.npatchs):
            for f_s in range(0, nfaces):
                if intext_faces_s[i_s,f_s] == 1:
                    internalFaces.append([i_s+geo_m.npatchs, f_s])
                else:
                    externalFaces.append([i_s+geo_m.npatchs, f_s])

        geo._connectivity = connectivity
        geo._internal_faces = internalFaces
        geo._external_faces = externalFaces

        return geo

    def update(self, npts=5):
        list_geo = self.expand()
        if len(list_geo) == 1:
            self.update_patch(i_m=0, npts=npts)
        if len(list_geo) > 1:
            geo = merge(list_geo, npts=npts)
            self.set_internal_faces(geo.internal_faces)
            self.set_external_faces(geo.external_faces)
            self.set_connectivity(geo.connectivity)

    def update_patch(self, i_m=0, npts=50):
        """
        merge two cad_geometries and return a new cad_geometry including an
        update for internal/external faces and connectivity.
        TODO: treate the 1D and 3D cases

        Args:
            geos_s (cad_geometry):
                This is the slave cad_geometry

        Kwargs:
            npts (int):
                used to evaluate and check equality of the extracted boundaries.
                Default value is 50

        Returns:
            a cad_geometry

        Examples
        --------

        This example is taken from the circle_5mp

        >>> # ... Import the quart_circle domain
        >>> geo_1 = quart_circle(rmin=rmin, rmax=rmax, n=n,p=p)
        >>> # ... Import the quart_circle domain
        >>> geo_2 = quart_circle(rmin=rmin, rmax=rmax, n=n,p=p)
        >>> geo_2[0].rotate(0.5*np.pi)
        >>> # ... Import the quart_circle domain
        >>> geo_3 = quart_circle(rmin=rmin, rmax=rmax, n=n,p=p)
        >>> geo_3[0].rotate(np.pi)
        >>> geo_3[0].reverse(0)
        >>> # ... Import the quart_circle domain
        >>> geo_4 = quart_circle(rmin=rmin, rmax=rmax, n=n,p=p)
        >>> geo_4[0].rotate(1.5*np.pi)
        >>> geo_4[0].reverse(0)
        >>> # ... Import the circle domain
        >>> geo_5 = circle(radius=rmin,n=n,p=p)
        >>> geo_5[0].rotate(0.25*np.pi)
        >>> geo_5[0].rotate(0.5*np.pi)
        >>> geo_12   = geo_1.merge(geo_2)
        >>> geo_34   = geo_3.merge(geo_4)
        >>> geo_1234 = geo_12.merge(geo_34)
        >>> geo      = geo_1234.merge(geo_5)

        """
        geo_m = self

        if geo_m.dim == 1:
            nfaces = 2
        if geo_m.dim == 2:
            nfaces = 4
        if geo_m.dim == 3:
            nfaces = 6

        connectivity   = []

        intext_faces_m = np.zeros((geo_m.npatchs, nfaces), dtype=np.int)
        nrb_m = geo_m[i_m]

        for f_m in range(0, nfaces):
            bnd_m = nrb_m.extract_face(f_m).clone()
            u_m = np.linspace(bnd_m.knots[0][0],bnd_m.knots[0][-1],npts)
            P_m = bnd_m(u_m)
            for f_s in range(f_m+1, nfaces):
                bnd_s = nrb_m.extract_face(f_s).clone()
                u_s = np.linspace(bnd_s.knots[0][0],bnd_s.knots[0][-1],npts)
                P_s = bnd_s(u_s)

                isSameFace = np.allclose(P_m, P_s)
                isInvertFace = np.allclose(P_m[::-1], P_s)
                if isSameFace:
                    dict_con = {}
                    dict_con['original'] = [i_m,f_m]
                    dict_con['clone']    = [i_m,f_s]
                    connectivity.append(dict_con)
                    intext_faces_m[i_m, f_m] = 1
                    intext_faces_m[i_m, f_s] = 1
                if isInvertFace:
                    print("Merging Error: Found uncorrect orientation.")
                    print("Occured on the faces (master, slave): (",f_m,",",f_s,").")


        internalFaces = []
        externalFaces = []
        for i_m in range(0, geo_m.npatchs):
            for f_m in range(0, nfaces):
                if intext_faces_m[i_m,f_m] == 1:
                    internalFaces.append([i_m, f_m])
                else:
                    externalFaces.append([i_m, f_m])

        self.set_connectivity(connectivity)
        self.set_internal_faces(internalFaces)
        self.set_external_faces(externalFaces)

    def split(self,patch_id,t,axis,normalize=[True,False]):
        """
        split the patch with id patch_id of the current cad_geometry, with
        respect to the knot t in the direction axis
        """
        geo = self
        nrb = geo[patch_id]
        _nrb = nrb.clone()

        noccur = len([s for s in _nrb.knots[axis] if s == t])
        p = _nrb.degree[axis]
        if p > noccur:
            list_t = t * np.ones(p-noccur)
            nrb.refine(axis,list_t)
        # ...

        it = min ([i for (i,s) in enumerate(nrb.knots[axis]) if s==t])

        if nrb.dim == 1:
            axis = 0
            u_1 = [s for s in nrb.knots[0] if s <= t]
            u_1.append(u_1[-1])
            p = nrb.degree[axis]
            bezier = False
            if len(u_1) == 2*p+2:
                bezier = True
            if normalize[0] or bezier:
                _u = [ (u - u_1[0]) / (u_1[-1] - u_1[0]) for u in u_1 ]
                u_1 = _u
            P_1 = nrb.points[:it,:]
            W_1 = nrb.weights[:it]
            nrb_1 = cad_nurbs([u_1], P_1, weights=W_1)

            u_2 = [s for s in nrb.knots[0] if s >= t]
            u_2.insert(0,u_2[0])
            p = nrb.degree[axis]
            bezier = False
            if len(u_2) == 2*p+2:
                bezier = True
            if normalize[1] or bezier:
                _u = [ (u - u_2[0]) / (u_2[-1] - u_2[0]) for u in u_2 ]
                u_2 = _u
            P_2 = nrb.points[it-1:]
            W_2 = nrb.weights[it-1:]
            nrb_2 = cad_nurbs([u_2], P_2, weights=W_2)
        # ...
        if nrb.dim == 2:
            if axis == 0:
                u_1 = [s for s in nrb.knots[0] if s <= t]
                u_1.append(u_1[-1])
                p = nrb.degree[axis]
                bezier = False
                if len(u_1) == 2*p+2:
                    bezier = True
                if normalize[0] or bezier:
                    _u = [ (u - u_1[0]) / (u_1[-1] - u_1[0]) for u in u_1 ]
                    u_1 = _u
                v   = nrb.knots[1]
                P_1 = nrb.points[:it,:,:]
                W_1 = nrb.weights[:it,:]
                nrb_1 = cad_nurbs([u_1,v], P_1, weights=W_1)

                u_2 = [s for s in nrb.knots[0] if s >= t]
                u_2.insert(0,u_2[0])
                p = nrb.degree[axis]
                bezier = False
                if len(u_2) == 2*p+2:
                    bezier = True
                if normalize[1] or bezier:
                    _u = [ (u - u_2[0]) / (u_2[-1] - u_2[0]) for u in u_2 ]
                    u_2 = _u
                P_2 = nrb.points[it-1:,:,:]
                W_2 = nrb.weights[it-1:,:]
                nrb_2 = cad_nurbs([u_2,v], P_2, weights=W_2)
            if axis == 1:
                u   = nrb.knots[0]
                v_1 = [s for s in nrb.knots[1] if s <= t]
                v_1.append(v_1[-1])
                p = nrb.degree[axis]
                bezier = False
                if len(v_1) == 2*p+2:
                    bezier = True
                if normalize[0] or bezier:
                    _v = [ (v - v_1[0]) / (v_1[-1] - v_1[0]) for v in v_1 ]
                    v_1 =_v
                P_1 = nrb.points[:,:it,:]
                W_1 = nrb.weights[:,:it]
                nrb_1 = cad_nurbs([u,v_1], P_1, weights=W_1)

                u   = nrb.knots[0]
                v_2 = [s for s in nrb.knots[1] if s >= t]
                v_2.insert(0,v_2[0])
                p = nrb.degree[axis]
                bezier = False
                if len(v_2) == 2*p+2:
                    bezier = True
                if normalize[1] or bezier:
                    _v = [ (v - v_2[0]) / (v_2[-1] - v_2[0]) for v in v_2 ]
                    v_2 = _v
                P_2 = nrb.points[:,it-1:,:]
                W_2 = nrb.weights[:,it-1:]
                nrb_2 = cad_nurbs([u,v_2], P_2, weights=W_2)

        if nrb.dim == 3:
            print("Not yet implemented for 3D objects")
            raise

        self.remove(nrb)
        self.append(nrb_1)
        self.append(nrb_2)
        self.initialize_info()
#        self.update()

    def toBezier(self,patch_id):
        """
        replace the current cad_nurbs by the corresponding extracted Bezier
        elements
        """
        nrb = self[patch_id].clone()
        axis = 0
        list_t = np.unique(nrb.knots[axis])[1:-1]
        geo_t = self.clone()
        for i,t in enumerate(list_t):
            geo_t.split(i,t,axis)
        if nrb.dim == 1:
            print("Not yet implemented")
            raise
        if nrb.dim == 2:
            geo_f = cad_geometry()
            for i in range(0,self.npatchs):
                if i != patch_id:
                    srf = self[i]
                    geo_f.append(srf)

            list_geo = geo_t.expand()
            for _geo in list_geo:
                axis = 1
                list_t = np.unique(nrb.knots[axis])[1:-1]
                for i,t in enumerate(list_t):
                    _geo.split(i,t,axis)
                for srf in _geo:
                    geo_f.append(srf)
        if nrb.dim == 3:
            print("Not yet implemented")
            raise

        geo_f.initialize_info()
        return geo_f

    def add_patch(self, nrb):
        self.append(nrb)
        self.initialize_info()
        self.update()

    def to5patchs(self, face):
        """
        convert the current cad_geometry-containing 1 patch: a domain with one
        hole- to a 5 patchs
        description. the user must provide the internal face
        """
        if self.dim in [1,3]:
            print("This functions is only for 2D domains")
            raise

        if face in [0,2]:
            axis = 0
        if face in [1,3]:
            axis = 1
        geo = self.clone()
        list_t = [0.25,0.5,0.75]
        for i,t in enumerate(list_t[:-1]):
            geo.split(i,t,axis)
        geo.split(-1,list_t[-1],axis, normalize=[True,True])

        _geo = cad_geometry()
        for nrb in geo[::-1]:
            _geo.append(nrb)
        geo = _geo

        # ... Import the circle domain
        c0 = geo[0].extract_face(face)
        c1 = geo[1].extract_face(face)
        c1.reverse(0)
        c2 = geo[2].extract_face(face)
        c2.reverse(0)
        c3 = geo[3].extract_face(face)

        from igakit.cad import coons
        curves = [[c1,c3],[c0,c2]]
        srf = coons(curves)
        geo_t = cad_geometry()
        geo_t.append(cad_nurbs(srf.knots, srf.points, weights=srf.weights))

        geo[1].reverse(1)
        geo[2].reverse(1)

        geo[0].transpose()
        geo[3].transpose()

        geo.update()

        geo_t[0].transpose()

        geo_f = geo.merge(geo_t)

        return geo_f

    def plotMesh(self, MeshResolution=3, color='k'):
        """
        plot the corresponding mesh of the current cad_geometry.

        Kwargs:
            MeshResolution (int):
                Number of points inside each element. Default value is 3

            color (string):
                mesh color

        """
        from matplotlib.pyplot import plot
        geo = self
        for patch_id in range(0, geo.npatchs):
            list_Lines = geo.evalMesh(npts=MeshResolution)[patch_id]
            for Line in list_Lines:
                npts = Line.shape[0]
                list_iS = list(range(0,npts-1)) ; list_iE = list(range(1, npts))
                for (i,i_1) in zip(list_iS, list_iE):
                    P   = Line[i  ,:]
                    P_1 = Line[i_1,:]
                    x  = P[0]   ; y  = P[1]
                    x1 = P_1[0] ; y1 = P_1[1]
                    plot([x,x1], [y,y1], '-'+str(color))

    def plotJacobians(self, MeshResolution=10, vmin=None, vmax=None):
        """
        plot the jacobian of the current cad_geometry object. The plot will be
        done on every patch from the cad_geometry

        Kwargs:
            MeshResolution (int):
                number of points per cell. Default values is 10
        """
        from matplotlib.pyplot import pcolor
        list_jac = []
        list_xyz = []
        for i in range(0, self.npatchs):
            nrb = self[i]

            list_t = []
            for axis in range(0, nrb.dim):
                tx = np.linspace(0,1,MeshResolution)
                list_t.append(tx)
            Dw = nrb.evaluate_deriv(*list_t,nderiv=1)

            if self.dim in [1,3]:
                print("Error: Not yet implemented.")
                raise

            x    = Dw[0,:,:,0]
            xdu  = Dw[1,:,:,0]
            xdv  = Dw[2,:,:,0]

            y    = Dw[0,:,:,1]
            ydu  = Dw[1,:,:,1]
            ydv  = Dw[2,:,:,1]

            jac = xdu * ydv - xdv * ydu
            if np.abs(jac.max()) < 1.e-6:
                print("=== patch ",i, " ===")
                print("jacobian[0,0] : ", jac[0,0])
                print("jacobian[0,-1] : ", jac[0,-1])
                print("jacobian[-1,0] : ", jac[-1,0])
                print("jacobian[-1,-1] : ", jac[-1,-1])
                print("min(jacobian) : ", jac.min())
                print("max(jacobian) : ", jac.max())
            list_jac.append(jac)
            list_xyz.append([x,y])

        if vmin is None:
            vmin = np.min(np.asarray([jac.min() for jac in list_jac]))
        if vmax is None:
            vmax = np.max(np.asarray([jac.max() for jac in list_jac]))
        for (xyz,jac) in zip(list_xyz,list_jac):
            if self.dim == 2:
                x = xyz[0] ; y = xyz[1]
                pcolor(x,y,jac,vmin=vmin,vmax=vmax)

    def bezier_extract(self):
        # TODO to be optimized.
        # construction of local matrices must be done in Fortran or c
        from caid.utils.extraction import BezierExtraction
        from caid.numbering.connectivity import connectivity
        from scipy.sparse import csr_matrix, kron
        from time import time

#        t_begin = time()

        geo = self
        con = connectivity(geo)
        con.init_data_structure()
#        con.printinfo(with_LM=True, with_IEN=False, with_ID=False)
#        con.printinfo()

#        t_end = time()
#        print ">> time for init data structure ", t_end-t_begin
#
#        t_begin = time()

        geo_ref = cad_geometry()
        list_extractors = []
        list_matrices = []
        for i in range(0, geo.npatchs):
            nrb = geo[i]
            extractor = BezierExtraction(nrb, check=False, verbose=False)
            list_extractors.append(extractor)

            list_matrices.append(extractor.matrices)

            nrb_ref = extractor.nrb_ref
            geo_ref.append(nrb_ref)

#            print "**********"
#            print "knots[0] ",nrb.knots[0]
#            print "knots[1] ",nrb.knots[1]
#            print "**********"
#
#            print "**********"
#            print "knots-ref[0] ",nrb_ref.knots[0]
#            print "knots-ref[1] ",nrb_ref.knots[1]
#            print "**********"

#        t_end = time()
#        print ">> time for extraction ", t_end-t_begin

        con_ref = connectivity(geo_ref)
        con_ref.init_data_structure()
#        con_ref.printinfo(with_LM=True, with_IEN=False, with_ID=False)

#        t_begin = time()

        list_lmatrices = []
        list_i     = list(range(0, geo.npatchs))
        for i in list_i:
            nrb             = geo[i]
            nrb_ref         = geo_ref[i]
            local_IEN       = con.IEN[i]
            local_IEN_ref   = con_ref.IEN[i]
            local_LM        = con.LM[i]
            local_LM_ref    = con_ref.LM[i]
#            local_ID        = con.ID_loc[i]
#            local_ID_ref    = con_ref.ID_loc[i]
            nelts           = con.list_nel[i]
            nelts_ref       = con_ref.list_nel[i]
            matrices        = list_matrices[i]

            assert(nelts==nelts_ref)

#            t_mean = []

            lmatrices = []
            for elt in range(0, nelts):
#                t_elt_begin = time()

                # shif values because LM are 1 based indices
                list_iloc       = np.asarray(local_LM[:,elt]) - 1
                list_iloc_ref   = np.asarray(local_LM_ref[:,elt]) - 1

#                list_iloc       = np.asarray(local_IEN[:,elt])
#                list_iloc_ref   = np.asarray(local_IEN_ref[:,elt])

#                print "======================="
#                print ">>>> element ", elt
#                print "list_iloc     ", list_iloc
#                print "list_iloc_ref ", list_iloc_ref

                if geo.dim == 1:
                    M = matrices[0]

                if geo.dim == 2:
                    M1 = matrices[0] ; M2 = matrices[1]
                    M = csr_matrix(kron(M2,M1))
#                    print M.shape, M1.shape, M2.shape

                if geo.dim == 3:
                    M1 = matrices[0] ; M2 = matrices[1] ; M3 = matrices[2]
                    M21 = csr_matrix(kron(M2,M1))
                    M = csr_matrix(kron(M3,M21))


                Mloc = np.zeros((len(list_iloc_ref), len(list_iloc)))
                for j_num, j in enumerate(list_iloc):
#                    print "----"
                    for j_ref_num, j_ref in enumerate(list_iloc_ref):
#                        print j, j_ref, j_num, j_ref_num
                        Mloc[j_ref_num, j_num] = M[j_ref, j]
#                print Mloc.shape
#                print "======================="

                lmatrices.append(Mloc)

#                t_elt_end = time()
#                t_mean.append(t_elt_end-t_elt_begin)
#
#            print ">>> mean time for an element " \
#                    , np.asarray(t_mean).sum()/nelts

#            print lmatrices
#            print [M.shape for M in lmatrices]
            list_lmatrices.append(lmatrices)
#        t_end = time()
#        print ">> time for local matrices ", t_end-t_begin

        return geo_ref, list_lmatrices

    def to_bezier_patchs_1d(self, filename=None):
        geo_ref, list_lmatrices = self.bezier_extract()

    def to_bezier_patchs_2d(self, filename=None):
        geo = self
        from caid.numbering.connectivity import connectivity
        con = connectivity(self)
        con.init_data_structure()

        geo_ref, list_lmatrices = self.bezier_extract()

        # TODO to replace with a loop over patchs
        # MUST BE DONE USING geo AND NOT geo_ref
#        nrb = geo_ref[0]
        nrb = geo[0]
        lmatrices = list_lmatrices[0]
        local_LM = con.LM[0]
        # ...

        # ...
        # we loop over each element and generate the P,
        # ...
        # we start by matching the 1D index with the 2D one
        lpi_n = nrb.shape
        lpi_p = nrb.degree
        list_Index = list(range(0, np.asarray(lpi_n).prod()))
        lpi_Index = np.asarray(list_Index).reshape(lpi_n[::-1])
        lpi_Index = lpi_Index.transpose()

        list_i = list(range(0,lpi_n[0]-1,lpi_p[0]))
        list_j = list(range(0,lpi_n[1]-1,lpi_p[1]))

        lpi_nElt = [len(list_i), len(list_j)]
        list_IndexElt = list(range(0, np.asarray(lpi_nElt).prod()))
        list_IndexElt = np.asarray(list_IndexElt).reshape(lpi_nElt[::-1])
        list_IndexElt = list_IndexElt.transpose()

        # .................................................
        # ... sets the list of Nodes
        list_indexNodes = []
        list_nodeData = []

#        list_i = range(0,lpi_n[0],lpi_p[0])
#        list_j = range(0,lpi_n[1],lpi_p[1])
        list_i = list(range(0,lpi_n[0]))
        list_j = list(range(0,lpi_n[1]))
        for enum_j, j in enumerate(list_j):
            for enum_i, i in enumerate(list_i):
                # compute index element index
                i_elt = enum_i + enum_j * len(list_i)

                pts_x = nrb.points[i,j,0]
                pts_y = nrb.points[i,j,1]

                # ...
                # compute the boundary code, for dirichlet
                # ...
                boundaryCode = 0
                if j in  [0,lpi_n[1] - 1]:
                    boundaryCode = 1
                if i in  [0,lpi_n[0] - 1]:
                    boundaryCode = 1
                # ...

                nodeData = [[boundaryCode], [pts_x, pts_y]]

                lineNodeData = []
                for data in nodeData:
                    for d in data:
                        lineNodeData.append(d)

                list_nodeData.append(lineNodeData)
        # ...
        # .................................................

        # .................................................
        # ... sets the list of Elements
        # MUST BE DONE USING geo_ref AND NOT geo
        nrb = geo_ref[0]
        list_elementData = []
#        list_i = list(range(0,lpi_n[0]-1,lpi_p[0]))
#        list_j = list(range(0,lpi_n[1]-1,lpi_p[1]))
        nx_elt = len(np.unique(nrb.knots[0])) - 1
        ny_elt = len(np.unique(nrb.knots[1])) - 1
        list_i = list(range(0,nx_elt))
        list_j = list(range(0,ny_elt))
        for enum_j, j in enumerate(list_j):
            for enum_i, i in enumerate(list_i):
                # compute index element index
                i_elt = enum_i + enum_j * len(list_i)

                # TODO for each element, we must compute its neighbours
                neighbours  = [-1, -1, -1, -1]

                pts_x = nrb.points[i:i+lpi_p[0]+1,j:j+lpi_p[1]+1,0]
                pts_y = nrb.points[i:i+lpi_p[0]+1,j:j+lpi_p[1]+1,1]
                pts_x = pts_x.reshape(pts_x.size)
                pts_y = pts_x.reshape(pts_y.size)

                # ... vertex indices
                list_indices = []
                for _i in range(i, i+lpi_p[0]+1):
                    for _j in range(j, j+lpi_p[1]+1):
                        ind = _i + _j * lpi_n[0]
                        list_indices.append(ind+1)
                # ...

                ux = nrb.knots[0] ; uy = nrb.knots[1]
                scale2D = ( ux[i+lpi_p[0]+1] - ux[i] ) * ( uy[j+lpi_p[1]+1] - uy[j] )
                elementData = [[i_elt+1], lpi_p, pts_x, pts_y \
                , [scale2D], neighbours, list_indices]

                lineElementData = []
                for data in elementData:
                    for d in data:
                        lineElementData.append(d)

                list_elementData.append(lineElementData)
        # ...
        # .................................................

        # .................................................
        # ... sets the list of Basis
        list_basisData = []
#        list_i = list(range(0,lpi_n[0]-1,lpi_p[0]))
#        list_j = list(range(0,lpi_n[1]-1,lpi_p[1]))
        nx_elt = len(np.unique(nrb.knots[0])) - 1
        ny_elt = len(np.unique(nrb.knots[1])) - 1
        list_i = list(range(0,nx_elt))
        list_j = list(range(0,ny_elt))
        for enum_j, j in enumerate(list_j):
            for enum_i, i in enumerate(list_i):
                # compute index element index
                i_elt = enum_i + enum_j * len(list_i)

                # ... local Bezier-extraction matrix
                M = lmatrices[i_elt]
#                print M.shape
#                print "========= ELT ", str(i_elt+1) , " ============"
#                for iM in range(0, M.shape[0]):
#                    for jM in range(0, M.shape[1]):
#                        print '%.15f' % M[iM,jM]
#                print "====================="
                M = np.ravel(M, order='F')
                # ...

                basisData = [[i_elt+1], M]

                lineBasisData = []
                for data in basisData:
                    for d in data:
                        lineBasisData.append(d)

                list_basisData.append(lineBasisData)
        # ...
        # .................................................

        # .................................................
        # ... sets the list of connectivities
        list_connectivityData = []
#        list_i = list(range(0,lpi_n[0]-1,lpi_p[0]))
#        list_j = list(range(0,lpi_n[1]-1,lpi_p[1]))
        nx_elt = len(np.unique(nrb.knots[0])) - 1
        ny_elt = len(np.unique(nrb.knots[1])) - 1
        list_i = list(range(0,nx_elt))
        list_j = list(range(0,ny_elt))
        for enum_j, j in enumerate(list_j):
            for enum_i, i in enumerate(list_i):
                # compute index element index
                i_elt = enum_i + enum_j * len(list_i)

                # ... local Bezier-extraction matrix
                M = local_LM[:,i_elt]
                M = np.ravel(M, order='F')
#                M = M.reshape(M.size)
                # ...

                # ... number of non vanishing basis per element
                nen = (lpi_p[0] + 1) * (lpi_p[1] + 1)
                # ...

                connectivityData = [[i_elt+1], [nen], M]

                lineConnectivityData = []
                for data in connectivityData:
                    for d in data:
                        lineConnectivityData.append(d)

                list_connectivityData.append(lineConnectivityData)
        # ...
        # .................................................

        # .................................................
        # ... sets the list of Dirichlet Basis functions for each Element
        #     All external faces are set to Dirichlet
        list_DirFaces = []
        for i in range(0, geo.npatchs):
            list_DirFaces.append([])

        list_extFaces = geo.external_faces
        for extFaces in list_extFaces:
            patch_id    = extFaces[0]
            face_id     = extFaces[1]
            list_DirFaces[patch_id].append(face_id)
        # ...

        # ... compute the corresponding connectivity
        from caid.numbering.boundary_conditions import boundary_conditions
        con_dir = connectivity(geo)
        bc = boundary_conditions(geo)
        bc.dirichlet(geo, list_DirFaces)
        con_dir.init_data_structure(bc)
        # ...

        nrb = geo_ref[0]
        local_LM = con_dir.LM[0]

        list_dirichletData = []
#        list_i = list(range(0,lpi_n[0]-1,lpi_p[0]))
#        list_j = list(range(0,lpi_n[1]-1,lpi_p[1]))
        nx_elt = len(np.unique(nrb.knots[0])) - 1
        ny_elt = len(np.unique(nrb.knots[1])) - 1
        list_i = list(range(0,nx_elt))
        list_j = list(range(0,ny_elt))
        for enum_j, j in enumerate(list_j):
            for enum_i, i in enumerate(list_i):
                # compute index element index
                i_elt = enum_i + enum_j * len(list_i)

                nen = (lpi_p[0]+1) * (lpi_p[1]+1)
                list_Dirichlet = np.zeros(nen, dtype=np.int)
                for enum_lm, lm in enumerate(local_LM[:, i_elt]):
                    if lm == 0:
                        list_Dirichlet[enum_lm] = 1


                dirichletData = [[i_elt+1], [nen], list_Dirichlet]

                lineDirichletData = []
                for data in dirichletData:
                    for d in data:
                        lineDirichletData.append(d)

                list_dirichletData.append(lineDirichletData)
        # ...
        # .................................................

        # .................................................
        # ... sets the B-net
        nrb = geo[0]
        lpi_n = nrb.shape
        lpi_p = nrb.degree

        list_BnetData = []
        list_nBnet    = []

#        list_i = list(range(0,lpi_n[0]-1,lpi_p[0]))
#        list_j = list(range(0,lpi_n[1]-1,lpi_p[1]))
        nx_elt = len(np.unique(nrb.knots[0])) - 1
        ny_elt = len(np.unique(nrb.knots[1])) - 1
        list_i = list(range(0,nx_elt))
        list_j = list(range(0,ny_elt))

        for enum_j, j in enumerate(list_j):
            for enum_i, i in enumerate(list_i):
                # compute index element index
                i_elt = enum_i + enum_j * len(list_i)

                # ... vertex indices
                list_indices = []
                for _j in range(j, j+lpi_p[1]):
                    for _i in range(i, i+lpi_p[0]):
                        _i1 = _i + 1
                        _j1 = _j + 1

                        # P00 = [i,j]
                        I_00 = _i + _j * lpi_n[0]
                        # P10 = [i+1,j]
                        I_10 = _i1 + _j * lpi_n[0]
                        # P01 = [i,j+1]
                        I_01 = _i + _j1 * lpi_n[0]
                        # P11 = [i+1,j+1]
                        I_11 = _i1 + _j1 * lpi_n[0]

                        indices = [I_00 + 1, I_10 + 1, I_11 + 1, I_01 + 1]
                        list_indices.append(indices)
                # ...

                nBnet = len(list_indices)

                list_nBnet.append(nBnet)

                BnetData = [[i_elt+1], [nBnet], list_indices]

                lineBnetData = []
                for data in BnetData:
                    for d in data:
                        lineBnetData.append(d)

                list_BnetData.append(lineBnetData)
        # ...
        # .................................................

        if filename is not None:
            # .................................................
            # ... exporting files
            fmt = '%.15f'
            fmt_int = '%d'
            fmt_nodes = '%d, %.15f, %.15f'
            # .................................................

            # .................................................
            a = open(filename+"_nodes.txt", "w")
            # ... write size of list_nodeData
            a.write(str(len(list_nodeData))+' \n')

            for L in list_nodeData:
#                line = ''.join(str(fmt % e)+', ' for e in L)[:-2]+' \n'
                line = fmt_nodes % tuple(L) +' \n'
                a.write(line)
            a.close()
            # .................................................

            # .................................................
            a = open(filename+"_elements.txt", "w")
            # ... write size of list_elementData
            a.write(str(len(list_elementData))+' \n')
            # ... write maximum of spline degrees
            maxDegree = np.max(np.asarray([np.max(np.asarray(nrb.degree)) for nrb in self]))
            a.write(str(maxDegree)+' \n')
            for L in list_elementData:
                # ... element id
                line = str(L[0]) + ' \n'
                a.write(line)
                # ... spline degree
                lpi_p = L[1:3]
                line = str(lpi_p[0]) + ', ' + str(lpi_p[1]) + ' \n'
                a.write(line)
                # ...
                line = ''.join(str(fmt % e)+', ' for e in L[3:])[:-2]+' \n'
                a.write(line)
            a.close()
            # .................................................

            # .................................................
            a = open(filename+"_basis.txt", "w")
            # ... write size of list_basisData
            a.write(str(len(list_basisData))+' \n')
            for L in list_basisData:
                # ... element id
                line = str(L[0]) + ' \n'
                a.write(line)
                line = ''.join(str(fmt % e)+', ' for e in L[1:])[:-2]+' \n'
                a.write(line)
            a.close()
            # .................................................

            # .................................................
            a = open(filename+"_connectivity.txt", "w")
            # ... write size of list_connectivityData
            a.write(str(len(list_connectivityData))+' \n')
            for L in list_connectivityData:
                # ... element id
                line = str(L[0]) + ' \n'
                a.write(line)
                # ... number of non vanishing basis per element
                line = str(L[1]) + ' \n'
                a.write(line)
                # ... local LM
                line = ''.join(str(fmt_int % e)+', ' for e in L[2:])[:-2]+' \n'
                a.write(line)
            a.close()
            # ...

            # .................................................
            a = open(filename+"_dirichlet.txt", "w")
            # ... write size of list_connectivityData
            a.write(str(len(list_dirichletData))+' \n')
            for L in list_dirichletData:
                # ... element id
                line = str(L[0]) + ' \n'
                a.write(line)
                # ... number of non vanishing basis per element
                line = str(L[1]) + ' \n'
                a.write(line)
                # ... dirichlet nodes
                line = ''.join(str(fmt_int % e)+', ' for e in L[2:])[:-2]+' \n'
                a.write(line)
            a.close()
            # ...

            # .................................................
            a = open(filename+"_bnet.txt", "w")
            # ... write size of list_connectivityData
            a.write(str(len(list_BnetData))+' \n')
            # ... write max of n-Bnet per element
            max_nbnet = np.max(np.asarray(list_nBnet))
            a.write(str(max_nbnet)+' \n')
            for L in list_BnetData:
                # ... element id
                line = str(L[0]) + ' \n'
                a.write(line)
                # ... nBnet
                line = str(L[1]) + ' \n'
                a.write(line)
                # ... B-net nodes indices
                for data in L[2:]:
                    line = ''.join(str(fmt_int % e)+', ' for e in data)[:-2]+' \n'
                    a.write(line)
            a.close()
            # ...
        return list_nodeData, list_elementData


    def to_bezier_patchs_3d(self, filename=None):
        geo_ref, list_lmatrices = self.bezier_extract()

    def to_bezier_patchs(self, filename=None):
        geo_ref, list_lmatrices = self.bezier_extract()
        if self.dim == 1:
            self.to_bezier_patchs_1d(filename=filename)
        if self.dim == 2:
            self.to_bezier_patchs_2d(filename=filename)
        if self.dim == 3:
            self.to_bezier_patchs_3d(filename=filename)

    def to_bezier_jorek(self, patch_id, filename=None):
        """
        this routine transforms the current geometry into cubic Bezier patchs
        works only if dim == 2
        """
        list_master_faces = [d['original'] for d in self.connectivity]
        list_slave_faces  = [d['clone'] for d in self.connectivity]

        # ...
        def from_ij_to_face_id(i,j, api_n):
            face_id = None
            if (i == 0) and (j < api_n[1]):
                face_id = 1
            if (i == api_n[0]-1) and (j < api_n[1]):
                face_id = 3
            if (i < api_n[0]) and (j == 0):
                face_id = 0
            if (i < api_n[0]) and (j == api_n[1]-1):
                face_id = 2
            return face_id
        # ...

        # ...
        def duplicated_code_from_ij(i,j, api_n):
            face_id = from_ij_to_face_id(i,j, api_n)

            dupliCode = 0
            # first we need to know if the current face is a master or a slave one
            if [patch_id, face_id] in list_master_faces:
                dupliCode = 1

            if [patch_id, face_id] in list_slave_faces:
                dupliCode = 2
            # ...

            return dupliCode
        # ...

        # ... TODO add loop on patchs here
        nrb = self[patch_id] #.copy()
        if nrb.dim != 2 :
            print("to_bezier_jorek : Only works for dim=2")

        if min(nrb.degree) > 3 :
            print("to_bezier_jorek : Not yet implemented for splines with degree > 3")
        # ...
        # we elevate the spline degree to 3
        # ...
        geo = cad_geometry()
        geo.append(nrb)
        list_p = []
        for axis in range(0,nrb.dim):
            list_p.append(np.max(3 - nrb.degree[axis], 0))
        geo.refine(list_p=list_p)
        # ...

        # ...
        # we elevate the interior knots multiplicities to 3
        # ...
        list_knots = []
#        print ">>>> "
#        print geo[0].knots[0]
#        print geo[0].knots[1]
#        print "<<<< "
#        print nrb.breaks(mults=True)
        for axis in range(0, nrb.dim):
            # ... TODO there is a problem with this part.
            #          use arc circle as test
            list_t, list_mult = nrb.breaks(axis=axis, mults=True)
            list_t = list_t[1:-1]
            list_mult = list_mult[1:-1]
#            list_mult = []
#            for t in list_t:
#                mult = len([s for s in nrb.knots[axis] if s==t])
#                list_mult.append(mult)
#            print "========="
#            print list_mult
#            print list_t
            list_t_new = []
            for t,m in zip(list_t, list_mult):
                new_m = max(3-m,0)
                for i in range(0,new_m):
                    list_t_new.append(t)
            list_knots.append(list_t_new)
#        print list_knots[0]
#        print list_knots[1]
#        print "========="
        geo.refine(list_t=list_knots)
        # ...

        # ...
        list_extFaces = self.external_faces
        list_intFaces = self.internal_faces

        list_DirFaces = []
        for i in range(0, self.npatchs):
            list_DirFaces.append([])
        for extFaces in list_extFaces:
            nrb_id  = extFaces[0]
            face_id = extFaces[1]
            list_DirFaces[nrb_id].append(face_id)
        # ...


        # ... TODO add loop on patchs here
        nrb = geo[0]
        node_index = 0
        # ...

        # ...
        # we loop over each element and generate the P,u,v,w
        # ...
        # we start by matching the 1D index with the 2D one
        lpi_n = nrb.shape
        lpi_p = nrb.degree
        list_Index = list(range(0, np.asarray(lpi_n).prod()))
        lpi_Index = np.asarray(list_Index).reshape(lpi_n[::-1])
        lpi_Index = lpi_Index.transpose()

        # ... create the coarse mesh
        rx = (lpi_n[0] - 1) // lpi_p[0] - 1
        ry = (lpi_n[1] - 1) // lpi_p[1] - 1
        tx = [0.]+list(linspace(0.,1.,rx+2))+[1.]
        ty = [0.]+list(linspace(0.,1.,ry+2))+[1.]
        knots_coarse = [tx,ty]
        C = np.zeros((rx+2,ry+2,3))
        nrb_coarse = cad_nurbs(knots_coarse, C)
        geo_coarse = cad_geometry()
        geo_coarse.append(nrb_coarse)

        geo_coarse._internal_faces = self._internal_faces
        geo_coarse._external_faces = self._external_faces
        geo_coarse._connectivity   = self._connectivity
        # ...

        # ... create the assiacted connectivity
        from caid.numbering.connectivity import connectivity
        con = connectivity(geo_coarse)
        con.init_data_structure()

        local_LM = con.LM[0]
        local_ID = con.ID_loc[0]
        # ...

        pts = nrb.points

        list_i = list(range(0,lpi_n[0]-1,lpi_p[0]))
        list_j = list(range(0,lpi_n[1]-1,lpi_p[1]))

        lpi_nElt = [len(list_i), len(list_j)]
        list_IndexElt = list(range(0, np.asarray(lpi_nElt).prod()))
        list_IndexElt = np.asarray(list_IndexElt).reshape(lpi_nElt[::-1])
        list_IndexElt = list_IndexElt.transpose()

        # ...
        # sets the list of Nodes
        # ...
        list_indexNodes = []
        list_huhvNodes = []
        list_nodeData = []
        Dirichlet_faces = list_DirFaces[patch_id]

        nx_elt = len(np.unique(nrb.knots[0])) - 1
        ny_elt = len(np.unique(nrb.knots[1])) - 1

        for enum_j,j in enumerate(range(0,lpi_n[1],lpi_p[1])):
            for enum_i,i in enumerate(range(0,lpi_n[0],lpi_p[0])):
                node_index += 1

                i1 = i + 1
                j1 = j + 1
                li_signi = 1
                li_signj = 1

                currentElt = -1
                if enum_i < nx_elt and enum_j < ny_elt:
                    currentElt = enum_i + nx_elt * enum_j

                if ( i == lpi_n[0] - 1 ) :
                    i1 = lpi_n[0] - 2
                    li_signi = -1
                if ( j == lpi_n[1] - 1 ) :
                    j1 = lpi_n[1] - 2
                    li_signj = -1

                P00 = np.asarray(pts[i,j])[0:-1] # remove the 3D coordinate
                P10 = np.asarray(pts[i1,j])[0:-1]
                P01 = np.asarray(pts[i,j1])[0:-1]
                P11 = np.asarray(pts[i1,j1])[0:-1]

                li_00 = lpi_Index[tuple([i,j])]
                li_10 = lpi_Index[tuple([i1,j])]
                li_01 = lpi_Index[tuple([i,j1])]
                li_11 = lpi_Index[tuple([i1,j1])]

                list_indexNodes.append(li_00)

                globID = local_ID[enum_i,enum_j]
                print currentElt, globID
                # ...
                # compute u, v and w
                # ...
                u = P10 - P00 ; hu = np.sqrt(u[0]**2+u[1]**2)
                v = P01 - P00 ; hv = np.sqrt(v[0]**2+v[1]**2)
                w = P11 + P00 - P10 - P01

                if (hu < 1.e-10):
                    hu = 1.0
                if (hv < 1.e-10):
                    hv = 1.0

                u /= hu
                v /= hv
                w /= ( hu * hv )

                u *= li_signi
                v *= li_signj
                w *= li_signi * li_signj

                list_huhvNodes.append([hu,hv])
                # ...

                # ...................................
                #         Boundary treatment
                # ...................................
                face_id = from_ij_to_face_id(i,j,lpi_n)

                # ...
                # compute the boundary code for external faces
                # ...
                boundaryCode = 0

                if face_id in Dirichlet_faces:
                    if j in  [0,lpi_n[1] - 1]:
                        boundaryCode += 1
                    if i in  [0,lpi_n[0] - 1]:
                        boundaryCode += 2
                # ...

                # ...
                # Duplication code internal faces
                # 2 son
                # 1 father
                # 0 other
                # TODO make compatible with multi patch => add test on faces
                # ...
                dupliCode = 0
                dupliCode = duplicated_code_from_ij(i,j, lpi_n)
                # ...
                # ...................................

                # ...
                nodeData = [P00 \
                , u, v, w \
                , [boundaryCode], [globID], [dupliCode]]

                lineNodeData = []
                for data in nodeData:
                    for d in data:
                        lineNodeData.append(d)

                list_nodeData.append(lineNodeData)
                # ...
        # ...

        # ...
        list_elementData = []
        for j in list_j:
            for i in list_i:

                P00 = pts[i  ,j  ,0:3] # remove the 3D coordinate
                P10 = pts[i+1,j  ,0:3]
                P01 = pts[i  ,j+1,0:3]
                P11 = pts[i+1,j+1,0:3]

                # ...
                # compute u, v and w
                # ...
                u = P10 - P00 ; hu = sqrt(u[0]**2+u[1]**2)
                v = P01 - P00 ; hv = sqrt(v[0]**2+v[1]**2)
                w = P11 + P00 - P10 - P01

                u /= hu
                v /= hv
                w /= ( hu * hv )
                # ...

                # ...
                # compute neighbours element
                # neighbours[0] : bottom
                # neighbours[1] : left
                # neighbours[2] : top
                # neighbours[3] : right
                # neighbours[d] = -1 if no neighbour in the direction d
                # ...
                neighbours = zeros(4)#  array([-1, -1, -1, -1])
                # bottom
                if j == list_j[0]:
                    neighbours[0] = -1
                else:
                    iElt = list_i.index(i) ; jElt = list_j.index(j)
                    neighbours[0] = list_IndexElt[tuple([iElt,jElt-1])]
                # left
                if i == list_i[0]:
                    neighbours[1] = -1
                else:
                    iElt = list_i.index(i) ; jElt = list_j.index(j)
                    neighbours[1] = list_IndexElt[tuple([iElt-1,jElt])]
                # top
                if j == list_j[-1]:
                    neighbours[2] = -1
                else:
                    iElt = list_i.index(i) ; jElt = list_j.index(j)
                    neighbours[2] = list_IndexElt[tuple([iElt,jElt+1])]
                # right
                if i == list_i[-1]:
                    neighbours[3] = -1
                else:
                    iElt = list_i.index(i) ; jElt = list_j.index(j)
                    neighbours[3] = list_IndexElt[tuple([iElt+1,jElt])]
                neighbours += 1
                # ...

                i_00 = lpi_Index[tuple([         i,         j])]
                i_30 = lpi_Index[tuple([i+lpi_p[0],         j])]
                i_03 = lpi_Index[tuple([         i,j+lpi_p[1]])]
                i_33 = lpi_Index[tuple([i+lpi_p[0],j+lpi_p[1]])]

                I_00 = list_indexNodes.index(i_00)
                I_30 = list_indexNodes.index(i_30)
                I_03 = list_indexNodes.index(i_03)
                I_33 = list_indexNodes.index(i_33)

#                print "I_00, I_30, I_03, I_33 = ", I_00, I_30, I_03, I_33

                [hu_00,hv_00] = list_huhvNodes[I_00]
                [hu_03,hv_03] = list_huhvNodes[I_03]
                [hu_30,hv_30] = list_huhvNodes[I_30]
                [hu_33,hv_33] = list_huhvNodes[I_33]

                # ...
                # For node 2  and 3 of an element in a square grid the direction of u
                # has to point to the left, i.e., the size has to be negative.
                # 30 and 33 => hu
                hu_30 *= -1.0
                hu_33 *= -1.0
                # ...

                # ...
                # For node 3 and 4, the vector v has to be negative.
                # 33 and 03 => hu
                hv_03 *= -1.0
                hv_33 *= -1.0
                # ...

                list_indexP = [I_00+1, I_30+1, I_33+1, I_03+1]
                list_huhv = [hu_00,hv_00, hu_30,hv_30, hu_33,hv_33, hu_03,hv_03]

                if ((hu_00-hu)**2 +(hv_00-hv)**2 > 1.e-7) :
                    print("SERIOUS ERROR: hu_00 must be equal to hu and hv_00 to hv. But got the values")
                    print(hu_00, hu)
                    print(hv_00, hv)

                elementData = [list_indexP \
                , list_huhv \
                , neighbours]

                lineElementData = []
                for data in elementData:
                    for d in data:
                        lineElementData.append(d)

                list_elementData.append(lineElementData)
        # ...

        if filename is not None:
            # ...
            # exporting files
            # ...
            fmt = '%.17f'
            a = open(filename+"_nodes.txt", "w")
            a.write(str(len(list_nodeData))+' \n')
            for L in list_nodeData:
                line = ''.join(str(fmt % e)+', ' for e in L)[:-2]+' \n'
                a.write(line)
            a.close()
            #
            a = open(filename+"_elements.txt", "w")
            a.write(str(len(list_elementData))+' \n')
            for L in list_elementData:
                line = ''.join(str(fmt % e)+', ' for e in L)[:-2]+' \n'
                a.write(line)
            a.close()
            # ...

        return list_nodeData, list_elementData
