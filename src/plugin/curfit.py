# -*- coding: UTF-8 -*-
from pigasus.utils.manager import context

def run(patch, method, nx, px, alpha, nsteps, ub=None, ue=None):
    with context():
        import numpy as np
        if ub is None:
            ub = patch.knots[0][0]
        if ue is None:
            ue = patch.knots[0][-1]
        u = np.linspace(ub,ue,nsteps)
        P = patch.evaluate(u)
        x = P[:,0] ; y = P[:,1] ; z = P[:,2]

        #-----------------------------------
        def MakeConstraint(cond, face=None, value=None):
            if cond.lower() == "closed":
                constraint = {}
                constraint['patch_id_m'] = 0
                constraint['face_m']     = 0
                constraint['patch_id_s'] = 0
                constraint['face_s']     = 1
            if cond.lower() == "c0":
                constraint = {}
                constraint['patch_id_m'] = 0
                constraint['face_m']     = face
                constraint['type']       = "C0"
                constraint['values']     = [value]
            if cond.lower() == "c1":
                constraint = {}
                constraint['patch_id_m'] = 0
                constraint['face_m']     = face
                constraint['type']       = "C1"
                constraint['values']     = [value]
            return constraint
        #-----------------------------------

        from pigasus.fit.curfit import curfit
        from pigasus.fit.curfit import compute_uk

        #-----------------------------------
        print(("Approximation using " + method + " knots"))
        print(("n " + str(nx) + " p ", str(px)))
        #-----------------------------------

        #-----------------------------------
        # ...
        list_x = list(x) ; list_y = list(y)
        # ...

        # ...
        list_Q = list(zip(list_x, list_y))
        uk = compute_uk(list_Q, method=method)
        U1       = []
        U1      += list(uk)
        list_xk  = []     ; list_yk  = []
        list_xk += list_x ; list_yk += list_y

        lists_uk = [U1]
        lists_xk = [list_xk]
        lists_yk = [list_yk]
        # ...
        #-----------------------------------

        #-----------------------------------
        constraints = []

        # ... C0_COND
        constraint = MakeConstraint("C0", 0, [x[0], y[0]])
        constraints.append(constraint)

        constraint = MakeConstraint("C0", 1, [x[-1], y[-1]])
        constraints.append(constraint)
        #-----------------------------------

        #-----------------------------------
        from igakit.cad_geometry import line
        geo = line(n=[nx], p=[px])
        #-----------------------------------

        #-----------------------------------
        fit = curfit(geometry=geo, constraints=constraints, alpha=alpha)
        #-----------------------------------

        #-----------------------------------
        patch_id = 0
        xk = lists_xk[patch_id]
        yk = lists_yk[patch_id]

        geo = fit.construct([xk, yk], uk=lists_uk)
        #-----------------------------------

        fit.PDE.free()

        return geo
