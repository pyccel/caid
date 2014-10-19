# -*- coding: UTF-8 -*-
import numpy as np
from numpy import cos, sin, pi
import numpy.linalg as la
import matplotlib.tri as mtri
import matplotlib.pyplot as plt

class tesselation:
    def __init__(self, x0, mat, times):
        """
        creates the box-splines tesselation using mat and times.
        the result is [i_0 v_0, i_1 v_1, ..., i_(n-1) v_(n-1)] for all [i_0,
        ..., i_(n-1)] in [0,m_0]x...x[0,m_(n-1)]
        Args:
            mat : list of vectors. mat.shape = [n,3]
            times: multiplicity for each vector. times.shape = [n,1]
            limiter: a function that returns True if x+iv is also inside the domain
        """
        list_pts = [x0]
        n,d = mat.shape
        for i in range(0,n):
            m = times[i]
            V = mat[i,:]
            points = []
            for i in range(0,m):
                for x in list_pts:
                    points.append(x+i*V)
                list_pts += points

        n = len(list_pts)
        points = np.zeros((n,3))
        for i in range(0,n):
            points[i,:] = list_pts[i][:]
        self._points = points
        self.limiter = None

        print "=== done ==="

    @property
    def points(self):
        return self._points

    def set_limiter(self, limiter):
        self.limiter = limiter

    def plot(self):
        list_pts_in = [] ; list_pts_out = []
        for p in self.points:
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

        plt.plot(points_in[:,0], points_in[:,1], 'ob')
        plt.plot(points_out[:,0], points_out[:,1], 'or')
        plt.show()



if __name__ == "__main__":
    h = 0.2
    r1 = h * np.array([ 1.0, 0.0, 0. ])
    r2 = h * np.array([ 0.0, 1.0, 0. ])
    r3 = h * np.array([ 1.0, 1.0, 0. ])
    r4 = h * np.array([-1.0, 1.0, 0. ])

#    list_pts = [r1, r2, r3]
#    times = [4, 4, 4]
#    times = [8, 8, 8]
#    times = [10, 10, 10]
    list_pts = [r1, r2, r3, r4]
    times = [4, 4, 4, 4]
#    times = [40, 40, 40, 40]

    n = len(list_pts)
    mat = np.zeros((n,3))
    for i in range(0,n):
        mat[i,:] = list_pts[i][:]

    origin = np.asarray([-0.,-2.,0.])

    def limiter(x):
        if (x[0]-0.)**2 + (x[1]-0.)**2 <= 1.:
            return True
        else:
            return False

    def boundary(x):
        return (x[0]-0.)**2 + (x[1]-0.)**2

    tess = tesselation(origin, mat, times)
    tess.set_limiter(limiter)

    t = np.linspace(0.,2*np.pi, 100)
    R = [np.cos(t), np.sin(t)]
    plt.plot(R[0], R[1],'-g')
    tess.plot()



