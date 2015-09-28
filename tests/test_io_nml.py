import numpy as np
from caid.cad_geometry import square
from caid.io import NML

geo = square(n=[31,31],p=[1,1])
nml_io = NML()
nml_io.write('domain_selalib.nml',geo)


