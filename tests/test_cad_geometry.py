# coding: utf-8
import numpy as np
from caid import cad_geometry as cg
from caid.cad_geometry import line, periodic_line
from caid.cad_geometry import square, periodic_square
import matplotlib.pyplot as plt

def refine(geo, n=None, p=None):
    if n is None:
        n = np.zeros(geo.dim, dtype=np.int)
    if p is None:
        p = np.zeros(geo.dim, dtype=np.int)
    n = np.asarray(n)
    p = np.asarray(p)
    geo_t = cg.cad_geometry()

    nrb = geo[0]
    geo_t.append(nrb)
    # ... refinement
    list_t = None
    if n.sum() > 0:
        list_t = []
        for axis in range(0,nrb.dim):
            ub = nrb.knots[axis][0]
            ue = nrb.knots[axis][-1]
            t = []
            if n[axis] > 0:
                t = np.linspace(ub,ue,n[axis]+2)[1:-1]
            list_t.append(t)

    list_p = None
    if p.sum() > 0:
        list_p = []
        for axis in range(0,nrb.dim):
            list_p.append(np.max(p[axis] - nrb.degree[axis], 0))

    geo_t.refine(list_t=list_t, list_p=list_p)
    return geo_t

def test1():
    geo = line()

    geo_r = refine(geo, n=[2], p=[2])
#    geo_r.plotMesh()
#    plt.show()

def test2():
    geo = square()

    geo_r = refine(geo, n=[2,2], p=[2,2])
#    geo_r.plotMesh()
#    plt.show()

def test3():
    n = 3 ; p = 2
    geo = periodic_line(n=[n], p=[p])
    geo_ref, list_lmatrices = geo.bezier_extract()
    from scipy.io import mmwrite
    M = list_lmatrices[0][0]
    mmwrite("M_conversion_test_3.mtx", M)
#    print geo[0].knots
#    print "====="
#    print geo_ref[0].knots

def test4():
    n = 3 ; p = 2
    geo = periodic_square(n=[n,n], p=[p,p])
    geo_ref, list_lmatrices = geo.bezier_extract()
    from scipy.io import mmwrite
    M = list_lmatrices[0][0]
    mmwrite("M_conversion_test_4.mtx", M)
#    print geo[0].knots
#    print "====="
#    print geo_ref[0].knots


###############################################################################
if __name__=="__main__":
#    test1()
#    test2()
    test3()
    test4()


