# -*- coding: UTF-8 -*-
import numpy as np

# ...
def alphaFct(i, k, t, n, p, knots):
    if   (i <= k-p):
        return 1.
    elif (k-p < i) and ( i <= k):
        return (t - knots[i]) / (knots[i+p] - knots[i])
    else:
        return 0.
# ...

# ...
def interv(knots, t):
    k = -1
    if t < knots[0]:
        return k

    if t > knots[-1]:
        return k

    # now knots[0] < t < knots[-1]
    for u in knots:
        if u>t:
            return k
        k += 1
# ...

class splineRefMat(object):
    def __init__(self, dim, useDecouple=False):
        self.dim = dim
        self.useDecouple = useDecouple

    def construct(self, *args, **kwargs):
        if self.dim ==1:
            M = self.constructCurveMatrix(*args, **kwargs)
            return M

        if self.dim ==2:
            M = self.constructSurfaceMatrix(*args, **kwargs)
            return M

        if self.dim ==3:
            print("Not done yet")
            import sys; sys.exit(1)

    # ...
    def refineSpline(self, dim, t, p, n, knots, P):
        N       = n+1
        Q       = np.zeros((N,dim))

        # WE MUST LOCATE x WITH RESPECT TO THE KNOT VECTOR
        k = interv(knots, t)

        # UPDATE Q
        # WE USE THE FACT THAT [B]_j = w_j*alpha_j/w B_j + w_[j-1]*[1-alpha_j]/w B_[j-1]
        j = 0
        alpha = alphaFct(j, k, t, n, p, knots)
        Q[j,:] = alpha * P[j,:]

        for j in range(1,n):
            alpha = alphaFct(j, k, t, n, p, knots)
            Q[j,:] = alpha * P[j,:] + (1. - alpha) * P[j-1,:]

        j = n
        alpha = alphaFct(j, k, t, n, p, knots)
        Q[j,:] = (1. - alpha) * P[j-1,:]

        return Q
    # ...

    # ...
    def constructCurveMatrix_single(self, t, p, n, knots):
        N       = n+1
        M       = np.zeros((N,n))

        # WE MUST LOCATE x WITH RESPECT TO THE KNOT VECTOR
        k = interv(knots, t)

        knots_new = np.asarray(list(knots)[:k+1] + [t] + list(knots)[k+1:])

        # UPDATE Q
        # WE USE THE FACT THAT [B]_j = w_j*alpha_j/w B_j + w_[j-1]*[1-alpha_j]/w B_[j-1]
        j = 0
        alpha = alphaFct(j, k, t, n, p, knots)
        M[0,0] = alpha

        for j in range(1,n):
            alpha = alphaFct(j, k, t, n, p, knots)
            M[j,j]      = alpha
            M[j,j-1]    = 1. - alpha

        j = n
        alpha = alphaFct(j, k, t, n, p, knots)
        M[n,n-1] = 1. - alpha

        return M, knots_new
    # ...

    # ...
    def constructCurveMatrix(self, list_t, p, n, knots):
        from scipy.sparse import csr_matrix
        if len(list_t) == 0:
            return csr_matrix(np.identity(n))

        r = list_t[0]
        M, knots_new= self.constructCurveMatrix_single(r, p, n, knots)
        knots = knots_new
        n += 1
        for r in list_t[1:]:
            M_tmp, knots_new = self.constructCurveMatrix_single(r, p, n, knots)
            knots = knots_new
            n = len(knots)-p-1
            M = np.dot(M_tmp, M)

        M = csr_matrix(M)

        # ... Dirichlet boundary condition
        n,m = M.shape
        ib = 0 ; ie = n
        jb = 0 ; je = m

        return csr_matrix(M.todense()[ib:ie,jb:je])
    # ...

    # ...
    def constructSurfaceMatrix(self, list_r1, list_r2, p1, p2, n1, n2, u1, u2):
        from scipy.sparse import csr_matrix, kron

        M1      = self.constructCurveMatrix(list_r1, p1, n1, u1)
        M2      = self.constructCurveMatrix(list_r2, p2, n2, u2)

        if self.useDecouple:
            return M1, M2
        else:
            return csr_matrix(kron(M2,M1))
    # ...

class BezierExtraction():
    def __init__(self, nrb, check=False, verbose=False):

        self._matrices = []
        self._lmatrices = []
        self._nrb  = nrb
        self._nrb_ref = None

        from caid.cad_geometry import cad_geometry
        # ...
        spl = splineRefMat(1)
        geo = cad_geometry()
        geo.append(nrb)

        if verbose:
            print(("== shape before ", nrb.shape))
            print((nrb.knots))

        list_t = []
        for axis in range(0, nrb.dim):
            brk, mult = nrb.breaks(axis=axis, mults=True)
#            print ">> axis ", axis
#            print brk
#            print mult
            nbrk = len(mult)
            mult = np.asarray(mult)
            times = nrb.degree[axis] * np.ones(nbrk, dtype=np.int) - mult
#            print ">> spans ", nrb.spans(axis=axis)

            list_r = []
            for t,k in zip(brk, times):
                for i in range(0, k):
                    list_r.append(t)
            list_t.append(list_r)

            knots   = nrb.knots[axis]
            n       = nrb.shape[axis]
            p       = nrb.degree[axis]
            P       = nrb.points
            dim     = P.shape[1]
#            print "%%%%%%%%%%%%"
#            print list_r
#            print p
#            print n
#            print knots
#            print "%%%%%%%%%%%%"

            M = spl.construct(list_r, p, n, knots)

            # ...
            if check:
                if nrb.dim == 1:
                    if verbose:
                        print(("matrix shape ", M.shape))
                    R = M.dot(nrb.points[:,0])

#                    geo.refine(id=0, list_t=[list_r])
                    nrb     = geo[0]
                    if verbose:
                        print(("== shape after ", nrb.shape))
                        print((nrb.knots))

                    P = np.asarray(nrb.points[:,0])
                    assert(np.allclose(P,R))
                    if verbose:
                        print("check: OK")
            # ...

            self._matrices.append(M)

        geo.refine(id=0, list_t=list_t)
        self._nrb_ref = geo[0]

    @property
    def matrices(self):
        return self._matrices

    @property
    def nrb(self):
        return self._nrb

    @property
    def nrb_ref(self):
        return self._nrb_ref

    @property
    def dim(self):
        return self._nrb.dim

    @property
    def nelts(self):
        n = np.asarray(self.nrb.shape)
        return n.prod()

if __name__ == '__main__':

    import caid.cad_geometry  as cg
    from caid.cad_geometry import line, square

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

        print("test1D1: OK")
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
        print("test1D2: OK")
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

        print("test2D1: OK")
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

        print("test2D2: OK")
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

        print("test2D3: OK")
    # ...

    test1D1()
    test1D2()
    test2D1()
    test2D2()
    test2D3()
