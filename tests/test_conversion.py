# -*- coding: UTF-8 -*-
#! /usr/bin/python

import numpy as np
import caid.cad_geometry  as cg
from caid.cad_geometry import cad_geometry, trilinear
from caid.cad_geometry import line, periodic_line
from caid.cad_geometry import square, periodic_square
from caid.numbering.boundary_conditions import boundary_conditions
from caid.numbering.connectivity import connectivity
from caid.conversion.tensorial_bsplines import matrix_conversion_ubspline_to_bernstein

def test1():
    # ...
    print ("==== conversion on a periodic line =======")

    k = 3
    S = matrix_conversion_ubspline_to_bernstein(k)
#    for i in range(0,k):
#        print S[i,:]

    geo0 = line(n=[0], p=[k-1])
    c0 = geo0[0]
    points = c0.points
    points[0, 0:2] = [0.0, 0.0]
    points[1, 0:2] = [1.0, -1.0]
    points[2, 0:2] = [2.0, -2.0]
    c0.set_points(points)
    print ">>> coeff for Bernstein curve"
    m = c0.shape[0]
    y0 = c0.points
    for i in range(0, m):
        print c0.points[i, :]

    c1 = c0.copy().unclamp(0)
    m = c1.shape[0]
    print ">>> coeff for Uniform-BSpline curve"
    for i in range(0, m):
        print c1.points[i, 0:2]

    x = c1.points[:, 0]
    y = S.dot(c1.points)
    print "conversion using the conversion Matrix"
    print y
    assert (np.linalg.norm(y-y0) < 1.e-7)
    print ("==========================================")
    # ...

###############################################################################
if __name__=="__main__":
    test1()
