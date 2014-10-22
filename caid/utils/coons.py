import numpy as np
from igakit.nurbs import NURBS
from igakit.transform import transform



def coonsInitialize(curves, tol=1.e-3):
    [[c1,c3],[c0,c2]] = curves

    (c0, c2) = compat(c0, c2)
    (c1, c3) = compat(c1, c3)

    p, U = c0.degree[0], c0.knots[0]
    ub, ue = U[p], U[-p-1]

    q, V = c1.degree[0], c1.knots[0]
    vb, ve = V[q], V[-q-1]


    # c0 and c1 compatibility
    P = c0(ub)
    Q = c1(vb)
    if not np.allclose(P, Q, rtol=0, atol=tol):
        c1.reverse()
        Q = c1(vb)
        assert np.allclose(P, Q, rtol=0, atol=tol)

    # c1 and c2 compatibility
    P = c1(ve)
    Q = c2(ub)
    if not np.allclose(P, Q, rtol=0, atol=tol):
        c2.reverse()
        Q = c2(ub)
        assert np.allclose(P, Q, rtol=0, atol=tol)

    # c2 and c3 compatibility
    P = c2(ue)
    Q = c3(ve)
    if not np.allclose(P, Q, rtol=0, atol=tol):
        c3.reverse()
        Q = c3(ve)
        assert np.allclose(P, Q, rtol=0, atol=tol)

    # c3 and c0 compatibility
    P = c3(vb)
    Q = c0(ue)
    assert np.allclose(P, Q, rtol=0, atol=tol)

    return [[c1,c3],[c0,c2]]

def coons(curves, tol=1.e-10):
    """
                C[1,1]
           o--------------o
           |  v           |
           |  ^           |
    C[0,0] |  |           | C[0,1]
           |  |           |
           |  +------> u  |
           o--------------o
                C[1,0]
    """
    (C00, C01), (C10, C11) = curves
    assert C00.dim == C01.dim == 1
    assert C10.dim == C11.dim == 1
    #
    (C00, C01) = compat(C00, C01)
    (C10, C11) = compat(C10, C11)
    #
    p, U = C10.degree[0], C10.knots[0]
    u0, u1 = U[p], U[-p-1]
    P = np.zeros((2,2,3), dtype='d')
    P[0,0] = C10(u0)
    P[1,0] = C10(u1)
    P[0,1] = C11(u0)
    P[1,1] = C11(u1)
    #
    q, V = C00.degree[0], C00.knots[0]
    v0, v1 = V[q], V[-q-1]
    Q = np.zeros((2,2,3), dtype='d')
    Q[0,0] = C00(v0)
    Q[0,1] = C00(v1)
    Q[1,0] = C01(v0)
    Q[1,1] = C01(v1)
    #

#    print "P[0,0] ", P[0,0] , "  Q[0,0] ", Q[0,0]
#    print "P[1,0] ", P[1,0] , "  Q[1,0] ", Q[1,0]
#    print "P[0,1] ", P[0,1] , "  Q[0,1] ", Q[0,1]
#    print "P[1,1] ", P[1,1] , "  Q[1,1] ", Q[1,1]

    assert np.allclose(P, Q, rtol=0, atol=tol)
    #
    R0 = ruled(C00, C01).transpose()
    R1 = ruled(C10, C11)
    B = bilinear(P)
    R0, R1, B = compat(R0, R1, B)
    control = R0.control + R1.control - B.control
    knots = B.knots
    return NURBS(knots, control)

# -----

