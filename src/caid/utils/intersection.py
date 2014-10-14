import numpy as np
from igakit.nurbs import NURBS
from igakit.transform import transform
from caid.core import bspline as bsplinelib
_bsp = bsplinelib.bsp

# -----
def intersect_crv(C1, C2, npts=50):
    """
    this function works ONLY with curves
    in order to find the intersection of 2 curves, we refine them and check
    fo the intersection of their control polygons
    based on the algorithm by Morken, Reimers, Schulz
    """

    # ...

    Greville = _bsp.Greville
    # ...

    # ...
    def intersect_segseg(A,B):
        """
        cette fonction recherche l'intersection de deux segments
        OUTPUT :
        ierr =  1, si l'intersection existe
        0, sinon

        P   : le point d'intesection
        t   : la valeur de la parametrisation du segment A
        s   : la valeur de la parametrisation du segment B
        """

        alpha 	= np.array(A[1]) - np.array(A[0])
        beta  	= np.array(B[1]) - np.array(B[0])
        a 	= np.array(A[0])
        b	= np.array(B[0])
        e	= b - a

        D	= - alpha[0] * beta[1] + alpha[1] * beta[0]
        if D == 0. :
            ierr = 0
            P = [] ; t = None ; s = None
            return P, t, s, ierr
        else :
            t	= - e[0]     * beta[1] + e[1]     * beta[0]
            s	=   alpha[0] * e[1]    - alpha[1] * e[0]
            t /= D
            s /= D

            if ( (0. <= t) and  (t <= 1.) and  (0. <= s) and  (s <= 1.) ):
                ierr = 1
                P = t * np.array(A[1]) + (1. - t) * np.array(A[0])
                return P, t, s, ierr
            else :
                ierr = 0
                P = [] ; t = None ; s = None
                return P, t, s, ierr
    # ...

    # ...
    def intersect_crvseg(crv, Seg, a, npts):
        p = crv.degree[0] ; U = crv.knots[0]

        Umin, Umax = U[p], U[-p-1]

        lpr_t = np.linspace(Umin, Umax,npts+2)[1:-1]
        # we must remove repeated knots
        list_t = [t for t in lpr_t if t not in U]

        C = crv.clone().refine(0, list_t)

        list_th = Greville(C.degree[0], C.knots[0])

        list_Seg = []
        for (Pi,Pip1) in zip(C.points[:-1,...], C.points[1:,...]):
            list_Seg.append([Pi,Pip1])

        list_P = [] ; list_u = [] ; list_v = [] ; ierr = 0
        li_i = 0
        for A in list_Seg:
            P,t,s,_ierr = intersect_segseg(A,Seg)
            if _ierr == 1:
                u = t * ( list_th[li_i+1] - list_th[li_i] ) + list_th[li_i]
                v = s * ( a[1] - a[0] ) + a[0]
                list_P.append(P)
                list_u.append(u)
                list_v.append(v)
                ierr = 1
            li_i += 1

        return list_P, list_u, list_v, ierr
    # ...

    # ...
    # we check weither we need to refine the curve
    # then we extract the control points
    # ...
    p2 = C2.degree[0] ; U2 = C2.knots[0]

    U2min, U2max = U2[p2], U2[-p2-1]

    lpr_t = np.linspace(U2min, U2max,npts+2)[1:-1]
    C = C2.clone().refine(0, lpr_t)
    list_P = C.points
    list_sh = Greville(C.degree[0], C.knots[0])
    # ...

    # ...
    # we construct the control polygon as a list of segments
    # ...
    list_Seg = []
    for (P, Pip) in zip(list_P[:-1], list_P[1:]):
        Seg = [list(P), list(Pip)]
        list_Seg.append(Seg)
    # ...

    # ...
    list_t = [] ; list_s = []; list_P = []
    li_i = 0
    for Seg in list_Seg:
        _list_P, _list_t, _list_s, ierr = intersect_crvseg(C1, Seg, [list_sh[li_i], list_sh[li_i+1]], npts)
        if ierr == 1:
            list_t += _list_t ; list_s += _list_s ; list_P += _list_P
        li_i += 1

    return list_P, list_t, list_s, ierr
    # ...

# -----
