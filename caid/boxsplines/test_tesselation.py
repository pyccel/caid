# -*- coding: UTF-8 -*-
import numpy as np
from numpy import cos, sin, pi
import numpy.linalg as la
import matplotlib.tri as mtri
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib
from tesselation import *


R = 4.
n = 1
h = 0.25
r1 = np.array([ 1.0, 0.0, 0. ])
r2 = np.array([ 0.0, 1.0, 0. ])
r3 = np.array([ 1.0, 1.0, 0. ])
r4 = np.array([-1.0, 1.0, 0. ])

e1 = np.array([ np.sqrt(3)/2., 0.5, 0. ])
e2 = np.array([-np.sqrt(3)/2., 0.5, 0. ])
e3 = np.array([0., 1.0, 0. ])

def test1():
    list_pts = [r1, r2, r1, r2, r3]
    list_t   = range(-6,4)
    return list_pts, list_t

def test2():
    list_pts = [r1, r2, r3, r4]
    list_t   = range(-6,6)
    return list_pts, list_t

def test3():
    list_pts = [e1, e2, e3, e1, e2, e3]
    list_t   = range(-6,6)
    return list_pts, list_t

def create_matrice(list_pts):
    n = len(list_pts)
    mat = np.zeros((n,3))
    for i in range(0,n):
        mat[i,:] = list_pts[i][:]
    return mat

origin = np.asarray([0.,0.,0.])

def limiter(x):
    if (x[0]-0.)**2 + (x[1]-0.)**2 <= 1:
        return True
    else:
        return False

def boundary(x):
    return (x[0]-0.)**2 + (x[1]-0.)**2


# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.

def point_inside_polygon(x,y,tess):
    points = tess.control[:,:2]
    hull = ConvexHull(points)
    points = points[hull.vertices,:2]

    n,d = points.shape
    inside =False

    p1x,p1y = points[0,:2]
    for i in range(n+1):
        p2x,p2y = points[i % n,:2]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


if __name__ == "__main__":

    fig, ax = plt.subplots()
    patches = []

#    list_pts, list_t = test1()
#    list_pts, list_t = test2()
    list_pts, list_t = test3()

    mat = create_matrice(list_pts)


    tess = tesselation(origin, mat)
    tess.set_limiter(limiter)
    tess.stencil()
    tess.scale(h)
    tess.plot()

    print point_inside_polygon(0.25,0.25,tess)

    patches.append(tess.polygon)

#    for P in list_pts[-3:]:
#        pts = list_pts[:-3]+[q for q in list_pts if np.linalg.norm(q-P) < 1.e-7]
#        mat = create_matrice(pts)
#        tess = tesselation(origin, mat)
#        tess.set_limiter(limiter)
#        tess.stencil()
#        tess.scale(h)
#
#        tess.scale(1./h)
#        v = P[:3]
#        print v
#        tess.translate(-v)
#        tess.stencil()
#        tess.scale(h)
#
#        patches.append(tess.polygon)
#        tess.plot()

    print len(patches)

    colors = 100*np.random.rand(len(patches))
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
    p.set_array(np.array(colors))
    ax.add_collection(p)

    t = np.linspace(0.,2*np.pi, 100)
    r = [np.cos(t), np.sin(t)]
    plt.plot(r[0], r[1],'-k')

    plt.show()


