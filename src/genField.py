# coding: utf-8
import numpy                as np
from igakit.cad_geometry import square as domain
from pigasus.gallery.poisson import *
sin = np.sin ; pi = np.pi
# ...
# ...
kx = 2. * pi
ky = 2. * pi
# ... exact solution
u = lambda x,y : [sin ( kx * x ) * sin ( ky * y )]
# ... rhs
f = lambda x,y : [( kx**2 + ky**2 ) * sin ( kx * x ) * sin ( ky * y )]
AllDirichlet = True
nx=15; ny = 15; px = 2; py = 2
geo = domain(n=[nx,ny],p=[px,py])
PDE = poisson(geometry=geo, AllDirichlet=AllDirichlet)
PDE.assembly(f=f)
PDE.solve()
# ...
# ...
normU = PDE.norm(exact=u)
print "norm U   = ", normU
U = PDE.unknown
u = U.tomatrix(0)
from igakit.cad_geometry import cad_nurbs
nrb = geo[0]
C = np.zeros_like(nrb.points)
C[...,0]=u
nrb_f = cad_nurbs(nrb.knots, C, weights=nrb.weights)
from igakit.cad_geometry import cad_geometry
geo_f = cad_geometry()
geo_f.append(nrb_f)
geo_f.save("u.xml")
geo.save("geo.xml")
