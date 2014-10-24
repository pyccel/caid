import numpy as np
from igakit.nurbs import NURBS
from igakit.transform import transform

def stickC1(crv_m,crv_s,face_m,face_s,ib=None,ie=None):
    """
    ib and ie needed in 2D. These are the two extremeties of the face. We can
    fix them or ask igakit to change them too
    ib is always >= 0
    ie is always <= 0
    """
    # ...
    def derivatives_curve(crv,face):
        if face == 0:
            u = crv.knots[0][0]
        if face == 1:
            u = crv.knots[0][-1]
        D = crv.evaluate_deriv(u)
        return D[1,...]
    # ...
    # ...
    def derivatives_surface(srf,face):
        P = srf.points
        if face == 0:
            degree = srf.degree[1]
            c =  degree / srf.knots[1][degree+1]
            A = srf.points[:,0,:]
            B = srf.points[:,1,:]
        if face == 1:
            degree = srf.degree[0]
            c =  degree / srf.knots[0][degree+1]
            A = srf.points[0,:,:]
            B = srf.points[1,:,:]
        if face == 2:
            degree = srf.degree[1]
            n = srf.shape[1]
            c =  degree / (1.-srf.knots[1][n-1])
            A = srf.points[:,-2,:]
            B = srf.points[:,-1,:]
        if face == 3:
            degree = srf.degree[0]
            c =  degree / (1.-srf.knots[0][n-1])
            A = srf.points[-2,:,:]
            B = srf.points[-1,:,:]
        D = c * (B - A)

        return D
    # ...
    # ...
    def stickC1_curve(crv_m,crv_s,face_m,face_s):
        # TODO: does not treat NURBS: weights
        # ...
        def updatePoints(crv,face,D):
            P = crv.points
            if face == 0:
                degree = crv.degree[0]
                c =  degree / crv.knots[0][degree+1]
                A = crv.points[0,:]
                B = A + D / c
                P[1,:] = B
            if face == 1:
                degree = crv.degree[0]
                n = crv.shape[0]
                c =  degree / (1.-crv.knots[0][n-1])
                A = crv.points[n-1,:]
                B = A - D / c
                P[n-2,:] = B
            crv.set_points(P)
        # ...

        D_m = derivatives_curve(crv_m, face_m)
        updatePoints(crv_s,face_s,D_m[1,...])
        return crv_s
    # ...
    # ...
    def stickC1_surface(srf_m,srf_s,face_m,face_s,ib=None,ie=None):
        # TODO: does not treat NURBS: weights
        # ...
        def updatePoints(srf,face,D,ib=None,ie=None):
            if ib is None:
                ib = 0
            if ie is None:
                ie = 0
            P = srf.points
            if face == 0:
                n = srf.shape[1]
                degree = srf.degree[1]
                c =  degree / srf.knots[1][degree+1]
                A = srf.points[:,0,:]
                B = A + D / c
                P[ib:n+ie,1,:] = B[ib:n+ie,:]
            if face == 1:
                n = srf.shape[0]
                degree = srf.degree[0]
                c =  degree / srf.knots[0][degree+1]
                A = srf.points[0,:,:]
                B = A + D / c
                P[1,ib:n+ie,:] = B[ib:n+ie,:]
            if face == 2:
                n = srf.shape[1]
                degree = srf.degree[1]
                c =  degree / (1.-srf.knots[1][n-1])
                A = srf.points[:,-1,:]
                B = A - D / c
                P[ib:n+ie,-2,:] = B[ib:n+ie,:]
            if face == 3:
                n = srf.shape[0]
                degree = srf.degree[0]
                c =  degree / (1.-srf.knots[0][n-1])
                A = srf.points[-1,:,:]
                B = A - D / c
                P[-2,ib:n+ie,:] = B[ib:n+ie,:]

            srf.set_points(P)
        # ...

        D_m = derivatives_surface(srf_m, face_m)
        if face_m in [0,2]:
            updatePoints(srf_s,face_s,D_m[1,...],ib=ib,ie=ie)
        if face_m in [1,3]:
            updatePoints(srf_s,face_s,D_m[2,...],ib=ib,ie=ie)

        return srf_s
    # ...
    # ...

    # ...
    dim = crv_m.dim
    if dim == 1:
        return stickC1_curve(crv_m,crv_s,face_m,face_s)
    if dim == 2:
        return stickC1_surface(crv_m,crv_s,face_m,face_s,ib=ib,ie=ie)

