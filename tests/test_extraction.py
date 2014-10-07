# -*- coding: UTF-8 -*-
import numpy as np
#import caid.cad_geometry  as cg
from caid.cad_geometry import line, square
from caid.utils.extraction import splineRefMat

DIM_1D = 1
DIM_2D = 2

# ...
def test1D1():
    spl = splineRefMat(DIM_1D)
    list_r = list(np.random.random(20))
    for r in list_r:
        nx = 7
        px = 2
        geo = line(n=[nx], p=[px])

        nrb     = geo[0]
        knots   = nrb.knots[0]
        n       = nrb.shape[0]
        p       = nrb.degree[0]
        P       = nrb.points
        dim     = P.shape[1]

        Q = spl.refineSpline(dim, r, p, n, knots, P)
        M = spl.construct([r], p, n, knots)
        R = M.dot(nrb.points[:,0])

        geo.refine(id=0, list_t=[[r]])
        nrb     = geo[0]
        #print nrb.knots[0]
        Q = np.asarray(Q[:,0])
        P = np.asarray(nrb.points[:,0])
        assert(np.allclose(P,Q))
        assert(np.allclose(P,R))

    print "test1D1: OK"
# ...

# ...
def test1D2():
    spl = splineRefMat(DIM_1D)
#    list_r = list(np.random.random(20))
    list_r = [0.1,0.2,0.3]

    nx = 3
    px = 2
    geo = line(n=[nx], p=[px])

    nrb     = geo[0]
    knots   = nrb.knots[0]
    n       = nrb.shape[0]
    p       = nrb.degree[0]
    P       = nrb.points

    M = spl.construct(list_r, p, n, knots)
    from scipy.io import mmwrite
    mmwrite('M.mtx', M)
    R = M.dot(nrb.points[:,0])

    geo = line(n=[nx], p=[px])
    geo.refine(id=0, list_t=[list_r])
    nrb     = geo[0]
    P = np.asarray(nrb.points[:,0])

    assert(np.allclose(P,R))
    print "test1D2: OK"
# ...

# ...
def test2D1():
    spl = splineRefMat(DIM_1D)
    list_r1 = list(np.random.random(20))
    list_r2 = list(np.random.random(20))

    nx = 10 ; ny = 15
    px = 3 ; py = 2
    geo = square(n=[nx, ny], p=[px, py])

    dim     = geo.dim
    nrb     = geo[0]

    u1,u2   = nrb.knots
    n1,n2   = nrb.shape
    p1,p2   = nrb.degree

    M1      = spl.construct(list_r1, p1, n1, u1)
    M2      = spl.construct(list_r2, p2, n2, u2)
    tM2     = M2.transpose().tocsr()

    Px      = nrb.points[:,:,0].copy()
    Py      = nrb.points[:,:,1].copy()

    geo.refine(id=0, list_t=[list_r1, list_r2])
    nrb     = geo[0]
    Qx      = np.asarray(nrb.points[:,:,0])
    Qy      = np.asarray(nrb.points[:,:,1])

    from scipy.sparse import csr_matrix

    list_P = [Px, Py]
    list_Q = [Qx, Qy]
#    list_P = [Px]
#    list_Q = [Qx]
    for (U,Q) in zip(list_P, list_Q):
        Us  = csr_matrix(U).dot(tM2)
        tV  = M1.dot(Us).todense()

        assert(np.allclose(tV, Q))

    print "test2D1: OK"
# ...

# ...
def test2D2():
    spl = splineRefMat(DIM_2D)
    list_r1 = list(np.random.random(20))
    list_r2 = list(np.random.random(20))
#    list_r1 = [0.1, 0.2]
#    list_r2 = [0.9]

    nx = 20 ; ny = 31
    px = 3 ; py = 2
    geo = square(n=[nx, ny], p=[px, py])

    n = nx + px + 1 + len(list_r1)
    m = ny + py + 1 + len(list_r2)

    dim     = geo.dim
    nrb     = geo[0]

    u1,u2   = nrb.knots
    n1,n2   = nrb.shape
    p1,p2   = nrb.degree

    H = spl.construct(list_r1, list_r2, p1, p2, n1, n2, u1, u2)

    Px      = nrb.points[:,:,0].copy()
    Py      = nrb.points[:,:,1].copy()

    geo.refine(id=0, list_t=[list_r1, list_r2])
    nrb     = geo[0]
    Qx      = np.asarray(nrb.points[:,:,0])
    Qy      = np.asarray(nrb.points[:,:,1])

    list_P = [Px, Py]
    list_Q = [Qx, Qy]
#    list_P = [Px]
#    list_Q = [Qx]
    for (U,Q) in zip(list_P, list_Q):
        nU,mU = U.shape
        vecU    = U.transpose().reshape(nU*mU)
        vecP    = H.dot(vecU)
        P       = vecP.reshape((m,n)).transpose()

        assert(np.allclose(P, Q))

    print "test2D2: OK"
# ...

# ...
def test2D3():
    spl = splineRefMat(DIM_2D, useDecouple=True)
    list_r1 = list(np.random.random(20))
    list_r2 = list(np.random.random(20))
#    list_r1 = [0.1, 0.2]
#    list_r2 = [0.9]

    nx = 20 ; ny = 31
    px = 3 ; py = 2
    geo = square(n=[nx, ny], p=[px, py])

    n = nx + px + 1 + len(list_r1)
    m = ny + py + 1 + len(list_r2)

    dim     = geo.dim
    nrb     = geo[0]

    u1,u2   = nrb.knots
    n1,n2   = nrb.shape
    p1,p2   = nrb.degree

    H1, H2 = spl.construct(list_r1, list_r2, p1, p2, n1, n2, u1, u2)

    assert(np.allclose(np.array(H1.shape), np.array((44,24))))
    assert(np.allclose(np.array(H2.shape), np.array((54,34))))

    print "test2D3: OK"
# ...

test1D1()
test1D2()
test2D1()
test2D2()
test2D3()
