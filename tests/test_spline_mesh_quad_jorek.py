# coding: utf-8
import numpy as np
from caid.numbering.connectivity import connectivity
from caid.utils.quadratures import *
from bernstein import *

############################################################
if __name__=="__main__":
    from caid.cad_geometry import square, circle, circle_5mp

#    px = 1; py = 1
    px = 2; py = 2
#    px = 3; py = 3
#    px = 4; py = 4
#    px = 5; py = 5

    geo = square(n=[1,1], p=[px,py])
#    geo = square(n=[3,3], p=[px,py])
#    geo = square(n=[7,7], p=[px,py])
#    geo = square(n=[15,15], p=[px,py])
#    geo = square(n=[31,31], p=[px,py])
#    geo = square(n=[63,63], p=[px,py])




#    geo = circle_5mp(n=[3,3], p=[3,3])

    basename = "splines"
    from caid.io import BZR
    rw = BZR()
    rw.write(basename, geo, fmt="txt")

