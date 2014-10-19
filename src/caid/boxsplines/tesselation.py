# -*- coding: UTF-8 -*-
import numpy as np
from numpy import cos, sin, pi
import numpy.linalg as la
import matplotlib.tri as mtri
import matplotlib.pyplot as plt

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

    def __str__(self):
        message = "origin " + str(self.origin) + " \n " + \
                "vectors " + str(self.vectors)
        return message


if __name__ == "__main__":
    n = 1
    h = 0.25
    r1 = h * np.array([ 1.0, 0.0, 0. ])
    r2 = h * np.array([ 0.0, 1.0, 0. ])
    r3 = h * np.array([ 1.0, 1.0, 0. ])
    r4 = h * np.array([-1.0, 1.0, 0. ])

#    list_pts = [r1, r2, r3]
#    times = [4, 4, 4]
#    times = [8, 8, 8]
#    times = [10, 10, 10]
    list_pts = [r1, r2, r3, r4]
    times = [[-n,n+2], [-n,n+2], [-n,n+2], [-n,n+2]]

    n = len(list_pts)
    mat = np.zeros((n,3))
    for i in range(0,n):
        mat[i,:] = list_pts[i][:]

    origin = np.asarray([0.,0.,0.])

    def limiter(x):
        if (x[0]-0.)**2 + (x[1]-0.)**2 <= 1.:
            return True
        else:
            return False

    def boundary(x):
        return (x[0]-0.)**2 + (x[1]-0.)**2

    tess = tesselation(origin, mat)
    tess.set_limiter(limiter)
    tess.stencil()
    tess.plot()

    t = range(-6,6)
    for j in t:
        for i in t:
            v = np.asarray([i*h,j*h,0.])
            tess.translate(v-tess.origin)
            tess.stencil()
            tess.plot()
            if (i==0) and (j==0):
                tess.highlight()

    t = np.linspace(0.,2*np.pi, 100)
    R = [np.cos(t), np.sin(t)]
    plt.plot(R[0], R[1],'-k')
    plt.show()



