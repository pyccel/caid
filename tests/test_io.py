# -*- coding: UTF-8 -*-
import numpy as np
import caid.cad_geometry  as cg
from caid.cad_geometry import cad_geometry
from caid.cad_geometry import line, periodic_line
from caid.cad_geometry import square, periodic_square
import matplotlib.pyplot as plt
import sys


def test1():
    print "====== test 1  ====="
    nx = 3
    px = 3
    geo = line(n=[nx], p=[px])
    geo.append(geo[0])
    list_lmatrices = geo.bezier_extract()

def test2():
    print("====== test 2 : splines patch =====")
    nx = 3 ; ny = 3
    px = 2 ; py = 2
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

def test3():
    print "====== test 3 : bezier patchs  ====="
    geo = square(p=[px,py])
    u = np.linspace(0., 1.0, nx+2)[1:-1]
    v = np.linspace(0., 1.0, ny+2)[1:-1]
    tx = []
    for t in u:
        tx += [t]*px
    ty = []
    for t in u:
        ty += [t]*py

    geo.refine(list_t=[tx,ty])

    filename = "bezier"
    geo.to_bezier_patchs(filename)

def test4():
    print "====== test 4  ====="
    nx = 3 ; px = 3
    geo = periodic_line(n=[nx], p=[px])

    basis_only = False
    #basis_only = True

    basename = "splines"
    #basename = None

    dirname  = "tmp"
    #dirname  = None

    import os
    os.system("mkdir -p " + dirname)

    from caid.io import BZR
    rw = BZR()
    rw.write(geo, fmt="txt", basename=basename, dirname=dirname, basis_only=basis_only)

def test5():
    print "====== test 5  ====="
#    nx = 3 ; px = 2
#    ny = 3 ; py = 2
#    nx = 7 ; px = 2
#    ny = 7 ; py = 2
#    nx = 15 ; px = 2
#    ny = 15 ; py = 2
#    nx = 31 ; px = 2
#    ny = 31 ; py = 2
#    nx = 63 ; px = 2
#    ny = 63 ; py = 2
#    nx = 3 ; px = 3
#    ny = 3 ; py = 3
#    nx = 7 ; px = 3
#    ny = 7 ; py = 3
#    nx = 15 ; px = 3
#    ny = 15 ; py = 3
#    nx = 31 ; px = 3
#    ny = 31 ; py = 3
#    nx = 63 ; px = 3
#    ny = 63 ; py = 3
    nx = 3 ; px = 4
    ny = 3 ; py = 4
    nx = 7 ; px = 4
    ny = 7 ; py = 4
    nx = 15 ; px = 4
    ny = 15 ; py = 4
    nx = 31 ; px = 4
    ny = 31 ; py = 4
    nx = 63 ; px = 4
    ny = 63 ; py = 4

#    geo = square(n=[nx, ny], p=[px, py])
    geo = periodic_square(n=[nx, ny], p=[px, py])

    basis_only = False
    #basis_only = True

    basename = "splines"
    #basename = None

    dirname  = "tmp"
    #dirname  = None

    import os
    os.system("mkdir -p " + dirname)

    from caid.io import BZR
    rw = BZR()
    rw.write(geo, fmt="txt", basename=basename, dirname=dirname, basis_only=basis_only)
###############################################################################
if __name__=="__main__":
#    test1()
#    test2()
#    test3()
#    test4()
    test5()

