# -*- coding: UTF-8 -*-
import numpy as np
import caid.cad_geometry  as cg
from caid.cad_geometry import line, square, cad_geometry
import matplotlib.pyplot as plt
import sys

try:
    nx = int(sys.argv[1])
    ny = int(sys.argv[2])
    px = int(sys.argv[3])
    py = int(sys.argv[4])
except:
    raise("Error: you should run this script as: python test_io.py nx ny px py.")

#print "====== test 1  ====="
#nx = 3
#px = 3
#geo = line(n=[nx], p=[px])
#geo.append(geo[0])
#list_lmatrices = geo.bezier_extract()

print("====== test 2 : splines patch =====")
geo = square(n=[nx,ny], p=[px,py])
geo.translate([3.,0.])
#geo.plotMesh() ; plt.show()
#geo.append(geo[0])
#list_lmatrices = geo.bezier_extract()

nrb = geo[0]
print(">>> shape ", nrb.shape)
print(">>> ux    ", nrb.knots[0])
print(">>> uy    ", nrb.knots[1])
filename = "bezier"
geo.to_bezier_patchs(filename)

#print "====== test 3 : bezier patchs  ====="
#geo = square(p=[px,py])
#u = np.linspace(0., 1.0, nx+2)[1:-1]
#v = np.linspace(0., 1.0, ny+2)[1:-1]
#tx = []
#for t in u:
#    tx += [t]*px
#ty = []
#for t in u:
#    ty += [t]*py
#
#geo.refine(list_t=[tx,ty])
#
#filename = "bezier"
#geo.to_bezier_patchs(filename)
