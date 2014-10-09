# -*- coding: UTF-8 -*-
import numpy as np
import caid.cad_geometry  as cg
from caid.cad_geometry import line, square, cad_geometry
import matplotlib.pyplot as plt

#print "====== test 1  ====="
#nx = 3
#px = 3
#geo = line(n=[nx], p=[px])
#geo.append(geo[0])
#list_lmatrices = geo.bezier_extract()

print "====== test 2  ====="
nx = 1 ; ny = 2
px = 2 ; py = 3
geo = square(n=[nx,ny], p=[px,py])
#geo.append(geo[0])
#list_lmatrices = geo.bezier_extract()
filename = "bezier"
geo.to_bezier_patchs(filename)
