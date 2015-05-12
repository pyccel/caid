# coding: utf-8
import numpy as np
from caid.numbering.connectivity import connectivity
from caid.utils.quadratures import *
from bernstein import *

############################################################
if __name__=="__main__":
    from caid.cad_geometry import square, circle, circle_5mp
#    geo = square(n=[3,3], p=[3,3])
    geo = square(n=[7,7], p=[3,3])
#    geo = circle_5mp(n=[3,3], p=[3,3])

    basename = "splines"
    from caid.io import BZR
    rw = BZR()
    rw.write(basename, geo, fmt="txt")

