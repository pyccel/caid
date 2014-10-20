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

class tesselation:
    def __init__(self, origin, mat):
        """
        creates the box-splines tesselation using mat.
        Args:
            mat : list of vectors. mat.shape = [n,3]
        """
        self._origin = origin
        self._control= []
        self.limiter = None

        n,d = mat.shape
        self._vectors = np.zeros((n,4))
        self._vectors[...,:3] = mat[:,:3]

    @property
    def origin(self):
        return self._origin

    @property
    def vectors(self):
        return self._vectors

    @property
    def control(self):
        return self._control

    def set_limiter(self, limiter):
        self.limiter = limiter

    def stencil(self):
        mat = self.vectors
        n,d = mat.shape
        list_pts = [self.origin]
        for i in range(0,n):
            V = mat[i,:]
            points = []
            for x in list_pts:
                points.append(x+V[:3])
            list_pts += points

        n = len(list_pts)
        points = np.zeros((n,3))
        for i in range(0,n):
            points[i,:] = list_pts[i][:]
        self._control= points

    def translate(self, displ):
        self._origin = np.asarray(self._origin) + displ

    def highlight(self):
        x = self.control[:,0]
        y = self.control[:,1]
        z = np.ones_like(x)
        plt.pcolor(x,y,z)

    def plot(self, color='b'):
        list_pts_in = [] ; list_pts_out = []
        for p in self.control:
            if self.limiter(p):
                list_pts_in.append(p)
            else:
                list_pts_out.append(p)

        list_pts = list_pts_in
        n = len(list_pts)
        points = np.zeros((n,3))
        for i in range(0,n):
            points[i,:] = list_pts[i][:]
        points_in = points

        list_pts = list_pts_out
        n = len(list_pts)
        points = np.zeros((n,3))
        for i in range(0,n):
            points[i,:] = list_pts[i][:]
        points_out = points

        plt.plot(points_in[:,0], points_in[:,1], 'o'+color)
        plt.plot(points_out[:,0], points_out[:,1], 'or')

    @property
    def polygon(self):
        points = self.control[:,:2]
        hull = ConvexHull(points)
        points = points[hull.vertices,:2]
        return Polygon(points, True)

    def scale(self, h):
        self._control *= h
        self._origin  *= h

    def __str__(self):
        message = "origin " + str(self.origin) + " \n " + \
                "vectors " + str(self.vectors)
        return message


if __name__ == "__main__":
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


#    list_pts, list_t = test1()
#    list_pts, list_t = test2()
    list_pts, list_t = test3()

    n = len(list_pts)
    mat = np.zeros((n,3))
    for i in range(0,n):
        mat[i,:] = list_pts[i][:]

    origin = np.asarray([0.,0.,0.])

    def limiter(x):
        if (x[0]-0.)**2 + (x[1]-0.)**2 <= 1:
            return True
        else:
            return False

    def boundary(x):
        return (x[0]-0.)**2 + (x[1]-0.)**2

    fig, ax = plt.subplots()

    tess = tesselation(origin, mat)
    tess.set_limiter(limiter)
    tess.stencil()
    tess.scale(h)
    tess.plot()

    patches = []
    patches.append(tess.polygon)

#    plt.colorbar(p)

    for j in list_t:
        for i in list_t:
            v = i*tess.vectors[0,:3] + j*tess.vectors[1,:3]
            tess.translate(v-tess.origin)
            tess.stencil()
            tess.scale(h)
#            tess.plot()

            if ((i == 0) and (j == 0)) or \
               ((i == 1) and (j == 0)) or \
               ((i == -3) and (j == -3)):

#                tess.highlight()
                patches.append(tess.polygon)
                tess.plot()

    colors = 100*np.random.rand(len(patches))
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
    p.set_array(np.array(colors))
    ax.add_collection(p)

    t = np.linspace(0.,2*np.pi, 100)
    r = [np.cos(t), np.sin(t)]
    plt.plot(r[0], r[1],'-k')

    plt.show()



