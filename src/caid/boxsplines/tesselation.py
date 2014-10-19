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

    @property
    def points(self):
        return self._points

    def plot(self):
        points = self.points
        plt.plot(points[:,0], points[:,1], 'ob')
        plt.show()



if __name__ == "__main__":
    r1 = [ 1.0, 0.0, 0. ]
    r2 = [ 0.0, 1.0, 0. ]
    r3 = [ 1.0, 1.0, 0. ]
#    r4 = [-1.0, 1.0, 0. ]

    list_pts = [r1, r2, r3]
#    list_pts = [r1, r2, r3, r4]
    n = len(list_pts)
    mat = np.zeros((n,3))
    for i in range(0,n):
        mat[i,:] = list_pts[i][:]

    origin = np.asarray([0.,0.,0.])
    times = [4, 4, 4, 4]

    tess = tesselation(origin, mat, times)
    tess.plot()



