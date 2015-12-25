# -*- coding: UTF-8 -*-
#! /usr/bin/python

from matplotlib import pyplot as plt
import numpy as np

# ... creates miller equilibrium with default parameters
from caid.cad_geometry import miller_equilibrium
geo = miller_equilibrium(n=[31,31], p=[3,3])

geo.plotMesh(MeshResolution=3)
plt.savefig("plasma_equilibrium_2d_miller_ex1.png")
# ...

plt.clf()

# ... creates miller equilibrium
rmin=0.3 ; rmax=1.

params_shape = {}
params_shape['A']         = 3.17
params_shape['psi_tilde'] = 0.77
params_shape['kappa0']    = 1.66
params_shape['delta0']    = 0.416
params_shape['alpha']     = 1.22

params_eq = {}
params_eq['sk']  = 0.7
params_eq['sd']  = 1.37
params_eq['dR0'] =-0.354
params_eq['q']   = 3.03
params_eq['s']   = 2.47

from caid.cad_geometry import miller_equilibrium
geo = miller_equilibrium(rmin=rmin, rmax=rmax, n=[31,31], p=[3,3],
                         params_shape=params_shape, params_eq=params_eq)
geo.plotMesh(MeshResolution=3)
plt.savefig("plasma_equilibrium_2d_miller_ex2.png")
# ...

plt.clf()

# ... creates miller equilibrium with default parameters
from caid.cad_geometry import miller_equilibrium
geo = miller_equilibrium(rmin=0.4,n=[31,31], p=[3,3])

nrb = geo[0]
points = nrb.points
points[0,:,0] = points[0,:,0].mean()
points[0,:,1] = points[0,:,1].mean()
nrb.set_points(points)
geo.plotMesh(MeshResolution=3)
plt.savefig("plasma_equilibrium_2d_miller_ex3.png")
# ...

plt.clf()

# ... creates miller equilibrium
from caid.cad_geometry import miller_equilibrium
geo = miller_equilibrium(rmin=0.4, n=[31,31], p=[3,3])

#     print boundaries info in order to know what is the internal boundary
geo[0].plotBoundariesInfo()
plt.savefig("plasma_equilibrium_2d_miller_ex4_info.png")
plt.clf()

#     now that we know that the internal face is 1
#     we can use it to split the geometry into 5 patchs
geo = geo.to5patchs(1)
geo.plotMesh(MeshResolution=3)
plt.savefig("plasma_equilibrium_2d_miller_ex4.png")
# ...
