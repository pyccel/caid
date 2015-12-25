# -*- coding: UTF-8 -*-
#! /usr/bin/python

import numpy as np
from caid.cad_geometry import cad_nurbs, cad_geometry
from matplotlib import pyplot as plt
from numpy import pi, array

# ... create a 3D curve
def make_curve():
    T = np.array([0., 0., 0., 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1., 1., 1.])
    C = [[ 0.,-2., 0.],
         [ 1.,-2., 0.],
         [ 1., 0., 0.],
         [ 1., 1., 0.],
         [ 0., 1., 0.],
         [-1., 1., 0.],
         [-1., 0., 0.],
         [-1.,-2., 0.],
         [ 0.,-2., 0.],]

    crv = cad_nurbs([T], C)
    return crv
# ...

# ... create a 3D curve
crv0 = make_curve()
geo = cad_geometry()
geo.append(crv0)
geo.plotMesh(MeshResolution=20)
plt.savefig("polar_extrude_ex1_original.png")
plt.clf()
# ...

# ... polar extrude
geo_1 = geo.polarExtrude()
U = np.linspace(0., 1., 9)[1:-1]
V = np.linspace(0., 1., 17)[1:-1]
V = [v for v in V if v not in crv0.knots[0]]
geo_1.refine(list_t=[U, V])
geo_1.plotMesh()
plt.savefig("polar_extrude_ex1_geo1.png")
plt.clf()
# ...

# ... polar extrude
geo_2 = geo.polarExtrude(t=0.25)
U = np.linspace(0., 1., 9)[1:-1]
V = np.linspace(0., 1., 17)[1:-1]
V = [v for v in V if v not in crv0.knots[0]]
geo_2.refine(list_t=[U, V])
geo_2.plotMesh()
plt.savefig("polar_extrude_ex1_geo2.png")
plt.clf()
# ...

# ... polar extrude into 5 patchs
geo_3 = geo.polarExtrude(t=0.25)
#     print boundaries info in order to know what is the internal boundary
nrb = geo_3[0]
nrb.plotBoundariesInfo()
plt.savefig("polar_extrude_ex1_geo3_info.png")
plt.clf()

#     now that we know that the internal face is 1
#     we can use it to split the geometry into 5 patchs
geo_3 = geo_3.to5patchs(1)

U = np.linspace(0., 1., 9)[1:-1]
geo_3.refine(list_t=[U, U])
geo_3.plotMesh()
plt.savefig("polar_extrude_ex1_geo3.png")
plt.clf()
# ...
