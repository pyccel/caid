# -*- coding: UTF-8 -*-
#! /usr/bin/python

import numpy as np
from matplotlib import pyplot as plt
from caid.io import geopdes
from caid.cad_geometry import cad_geometry

geo = cad_geometry()

filename = "/home/macahr/Téléchargements/geopdes_geometries/geo_Lshaped_mp.txt"
#filename = "geo_Lshaped_mp_b.txt"

IO = geopdes()
IO.read(filename, geo)

fig = plt.figure()
geo.plotMesh()
plt.xlim(-1.1,1.1)
plt.ylim(-1.1,1.1)
plt.show()
#geo.save(filename.split(".")[0]+".xml")



#nml_io.write('domain_selalib.nml',geo)


