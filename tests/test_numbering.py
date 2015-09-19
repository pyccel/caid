# -*- coding: UTF-8 -*-
#! /usr/bin/python

import caid.cad_geometry  as cg
from caid.cad_geometry import cad_geometry, trilinear
from caid.cad_geometry import line, periodic_line
from caid.cad_geometry import square, periodic_square
from caid.numbering.boundary_conditions import boundary_conditions
from caid.numbering.connectivity import connectivity

def test1():
    geo1d = line(n=[5], p=[3])

    # ...
    print ("========= connectivity on a line =========")
    con1d = connectivity(geo1d)
    con1d.init_data_structure()
    con1d.printinfo()
    print ("==========================================")
    # ...

def test2():
    geo1d = line(n=[5], p=[3])

    # ...
    print ("========= dirichlet connectivity on a line =========")
    con1d_dir = connectivity(geo1d)
    bc1d_dir = boundary_conditions(geo1d)
    list_DirFaces = [[0,1]]
    bc1d_dir.dirichlet(geo1d, list_DirFaces)
    con1d_dir.init_data_structure(bc1d_dir)
    con1d_dir.printinfo()
    print ("==========================================")
    # ...

# ...
#print ("========= periodic connectivity on a line =========")
#con1d_per = connectivity(geo1d)
#bc1d_per = boundary_conditions(geo1d)
#faces_base = [[0,0,0]]
#faces      = [[0,1,0]]
#bc1d_per.duplicate(geo1d, faces_base, faces, shift_base=None, shift=None)
#con1d_per.init_data_structure(bc1d_per)
#con1d_per.printinfo()
#print ("==========================================")
# ...

# ...
#print ("========= full periodic connectivity on a line =========")
#con1d_per = connectivity(geo1d)
#bc1d_per = boundary_conditions(geo1d)
##    # p = 2
##    faces_base = [[0,0,0],[0,0,1]]
##    faces      = [[0,1,-1],[0,1,0]]
## p = 3
#faces_base = [[0,0,0] ,[0,0,1],[0,0,2]]
#faces      = [[0,1,-2],[0,1,-1],[0,1,0]]
#
#
#bc1d_per.duplicate(geo1d, faces_base, faces)
#con1d_per.init_data_structure(bc1d_per)
#con1d_per.printinfo()
#print ("==========================================")
# ...

def test3():
    # ...
    geo2d = square(n=[3,3], p=[2,2])
    con2d = connectivity(geo2d)

    con2d.init_data_structure()
    con2d.printinfo()
    # ...


def test4():
    # ... number of elemens
    n = 4

    # ... k is the b-spline order
    k = 3

    #
    geo1d = periodic_line(n=[n-1], p=[k-1])

    # ...
    print ("===== connectivity on a periodic line ====")
    con1d = connectivity(geo1d)
    con1d.init_data_structure()

    con1d.printinfo()
    print ("==========================================")
    # ...


def test5():
    # ... number of elemens
    n = 4

    # ... k is the b-spline order
    k = 3

    # ...
    print ("==== connectivity on a periodic square ====")
    geo2d = periodic_square(n=[n-1,n-1], p=[k-1,k-1])
    con2d = connectivity(geo2d)
    con2d.init_data_structure()

    con2d.printinfo()
    print ("==========================================")
    # ...


# ...
#def test():
#    geo3d = trilinear(n=[5,3,1], p=[2,3,4])
#    con3d = connectivity(geo3d)
#
#    con3d.init_data_structure()
#    con3d.printinfo()
# ...

###############################################################################
if __name__=="__main__":
#    test1()
#    test2()
#    test3()
    test4()
    test5()
#    test6()
