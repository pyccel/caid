# coding: utf-8
import numpy as np
from caid import cad_geometry as cg
import matplotlib.pyplot as plt

#geo = cg.square()
geo = cg.line()

#geo.plotMesh()
#plt.show()

zero = np.zeros(geo.dim, dtype=np.int)
def refine(geo, n=zero, p=zero):
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

#geo_r = refine(geo, n=[2,2], p=[2,2])
geo_r = refine(geo, n=[2], p=[2])

#geo_r.plotMesh()
#plt.show()



