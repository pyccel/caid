import numpy as np
from caid.cad_geometry import square
from caid.io import NML

geo = square(n=[3,3],p=[3,3])
nml_io = NML()
nml_io.write('test.nml',geo)


