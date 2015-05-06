# coding: utf-8
import numpy as np
from caid.numbering.connectivity import connectivity
from caid.utils.quadratures import *
from bernstein import *

#def get_nodes_2d(geo):
#    # ... sets the list of Nodes
#    geo_ref, list_lmatrices = geo.bezier_extract()
#
#    list_nodeData = []
#
#    node_index = 0
#    for nrb in geo_ref:
#        # ...
#        # we loop over each element and generate the P,
#        # ...
#        # we start by matching the 1D index with the 2D one
#        lpi_n = nrb.shape
#        lpi_p = nrb.degree
#
#        # .................................................
#        list_i = list(range(0,lpi_n[0],lpi_p[0]))
#        list_j = list(range(0,lpi_n[1],lpi_p[1]))
#        for enum_j, j in enumerate(list_j):
#            for enum_i, i in enumerate(list_i):
#                node_index += 1
#
#                # compute index element index
#                i_elt = enum_i + enum_j * len(list_i)
#
#                pts_x = nrb.points[i,j,0]
#                pts_y = nrb.points[i,j,1]
#
#                # ...
#                # compute the boundary code, for dirichlet
#                # ...
#                boundaryCode = 0
#                if j in  [0,lpi_n[1] - 1]:
#                    boundaryCode = 1
#                if i in  [0,lpi_n[0] - 1]:
#                    boundaryCode = 1
#                # ...
#
#                nodeData = [[node_index], [pts_x, pts_y], [boundaryCode]]
#
#                lineNodeData = []
#                for data in nodeData:
#                    for d in data:
#                        lineNodeData.append(d)
#
#                list_nodeData.append(lineNodeData)
#        # ...
#    return list_nodeData
#    # .................................................
#
#def save_nodes_2d(geo, filename):
#    list_nodeData = get_nodes_2d(geo)
#
#    # .................................................
#    # ... exporting files
#    fmt_nodes = '%d, %.15f, %.15f, %d'
#    # .................................................
#
#    # .................................................
#    a = open(filename+"_nodes.txt", "w")
#    # ... write size of list_nodeData
#    a.write(str(len(list_nodeData))+' \n')
#
#    for L in list_nodeData:
#        line = fmt_nodes % tuple(L) +' \n'
#        a.write(line)
#    a.close()
#    # .................................................
#
#def get_nodes_bezier_2d(geo):
#    # ... sets the list of Nodes
#    geo_ref, list_lmatrices = geo.bezier_extract()
#
#    list_nodeData = []
#    node_index = 0
#
#    for nrb in geo_ref:
#        # ...
#        # we loop over each element and generate the P,
#        # ...
#        # we start by matching the 1D index with the 2D one
#        lpi_n = nrb.shape
#        lpi_p = nrb.degree
#
#        # .................................................
#        list_i = list(range(0,lpi_n[0]))
#        list_j = list(range(0,lpi_n[1]))
#        for enum_j, j in enumerate(list_j):
#            for enum_i, i in enumerate(list_i):
#                node_index += 1
#
#                # compute index element index
#                i_elt = enum_i + enum_j * len(list_i)
#
#                pts_x = nrb.points[i,j,0]
#                pts_y = nrb.points[i,j,1]
#
#                # ...
#                # compute the boundary code, for dirichlet
#                # ...
#                boundaryCode = 0
#                if j in  [0,lpi_n[1] - 1]:
#                    boundaryCode = 1
#                if i in  [0,lpi_n[0] - 1]:
#                    boundaryCode = 1
#                # ...
#
#                nodeData = [[node_index], [pts_x, pts_y], [boundaryCode]]
#
#                lineNodeData = []
#                for data in nodeData:
#                    for d in data:
#                        lineNodeData.append(d)
#
#                list_nodeData.append(lineNodeData)
#        # ...
#    return list_nodeData
#    # .................................................
#
#def save_nodes_bezier_2d(geo, filename):
#    list_nodeData = get_nodes_bezier_2d(geo)
#
#    # .................................................
#    # ... exporting files
#    fmt_nodes = '%d, %.15f, %.15f, %d'
#    # .................................................
#
#    # .................................................
#    a = open(filename+"_nodes_bezier.txt", "w")
#    # ... write size of list_nodeData
#    a.write(str(len(list_nodeData))+' \n')
#
#    for L in list_nodeData:
#        line = fmt_nodes % tuple(L) +' \n'
#        a.write(line)
#    a.close()
#    # .................................................
#
#def get_elements_2d(geo):
#    # TODO ancestor and sons
#    list_elementData = []
#
#    # .................................................
#    for nrb in geo:
#        lpi_n = nrb.shape
#        lpi_p = nrb.degree
#
#        nx_elt = len(np.unique(nrb.knots[0])) - 1
#        ny_elt = len(np.unique(nrb.knots[1])) - 1
#        list_i = list(range(0,nx_elt))
#        list_j = list(range(0,ny_elt))
#        for enum_j, j in enumerate(list_j):
#            for enum_i, i in enumerate(list_i):
#                # compute index element index
#                i_elt = enum_i + enum_j * len(list_i)
#
#                # TODO for each element, we must compute its neighbours
#                neighbours  = [-1, -1, -1, -1]
#
#                # ... vertex indices
#                index_vertices = []
#
#                _i = i ; _j = j
#                ind = _i + _j * lpi_n[0]
#                index_vertices.append(ind+1)
#
#                _i = i+lpi_p[0]; _j = j
#                ind = _i + _j * lpi_n[0]
#                index_vertices.append(ind+1)
#
#                _i = i+lpi_p[0]; _j = j+lpi_p[1]
#                ind = _i + _j * lpi_n[0]
#                index_vertices.append(ind+1)
#
#                _i = i; _j = j+lpi_p[1]
#                ind = _i + _j * lpi_n[0]
#                index_vertices.append(ind+1)
#                # ...
#
#                elementData = [[i_elt+1], index_vertices, neighbours]
#
#                lineElementData = []
#                for data in elementData:
#                    for d in data:
#                        lineElementData.append(d)
#
#                list_elementData.append(lineElementData)
#    # ...
#    return list_elementData
#    # .................................................
#
#def save_elements_2d(geo, filename):
#    list_elementData = get_elements_2d(geo)
#
#    # .................................................
#    # ... exporting files
#    fmt_int = '%d'
#    # .................................................
#
#    # .................................................
#    a = open(filename+"_elements.txt", "w")
#    # ... write size of list_elementData
#    a.write(str(len(list_elementData))+' \n')
#
#    for L in list_elementData:
#        line = ''.join(str(fmt_int % e)+', ' for e in L[0:])[:-2]+' \n'
#        a.write(line)
#    a.close()
#    # .................................................
#
#def get_elements_bezier_2d(geo):
#    geo_ref, list_lmatrices = geo.bezier_extract()
#    list_elementData = []
#
#    # .................................................
#    for nrb in geo_ref:
#        lpi_n = nrb.shape
#        lpi_p = nrb.degree
#
#        nx_elt = lpi_n[0]-1
#        ny_elt = lpi_n[1]-1
#        list_i = list(range(0,nx_elt))
#        list_j = list(range(0,ny_elt))
#        for enum_j, j in enumerate(list_j):
#            for enum_i, i in enumerate(list_i):
#                # compute index element index
#                i_elt = enum_i + enum_j * len(list_i)
#
#                # TODO for each element, we must compute its neighbours
#                neighbours  = [-1, -1, -1, -1]
#
#                # ... vertex indices
#                index_vertices = []
#
#                _i = i ; _j = j
#                ind = _i + _j * lpi_n[0]
#                index_vertices.append(ind+1)
#
#                _i = i+1; _j = j
#                ind = _i + _j * lpi_n[0]
#                index_vertices.append(ind+1)
#
#                _i = i+1; _j = j+1
#                ind = _i + _j * lpi_n[0]
#                index_vertices.append(ind+1)
#
#                _i = i; _j = j+1
#                ind = _i + _j * lpi_n[0]
#                index_vertices.append(ind+1)
#                # ...
#
#                elementData = [[i_elt+1], index_vertices, neighbours]
#
#                lineElementData = []
#                for data in elementData:
#                    for d in data:
#                        lineElementData.append(d)
#
#                list_elementData.append(lineElementData)
#    # ...
#    return list_elementData
#    # .................................................
#
#def save_elements_bezier_2d(geo, filename):
#    list_elementData = get_elements_bezier_2d(geo)
#
#    # .................................................
#    # ... exporting files
#    fmt_int = '%d'
#    # .................................................
#
#    # .................................................
#    a = open(filename+"_elements_bezier.txt", "w")
#    # ... write size of list_elementData
#    a.write(str(len(list_elementData))+' \n')
#
#    for L in list_elementData:
#        line = ''.join(str(fmt_int % e)+', ' for e in L[0:])[:-2]+' \n'
#        a.write(line)
#    a.close()
#    # .................................................
#
#def get_nodes_sons_2d(geo):
#    # ... sets the list of Nodes
#    geo_ref, list_lmatrices = geo.bezier_extract()
#
#    list_nodeData = []
#
#    node_index = 0
#    for nrb_ref, nrb in zip(geo_ref, geo):
#        # ...
#        # we loop over each element and generate the P,
#        # ...
#        # we start by matching the 1D index with the 2D one
#        lpi_n = nrb_ref.shape
#        lpi_p = nrb_ref.degree
#
#        # .................................................
#        nx_elt = len(np.unique(nrb.knots[0])) - 1
#        ny_elt = len(np.unique(nrb.knots[1])) - 1
#        list_i = list(range(0,nx_elt))
#        list_j = list(range(0,ny_elt))
#        for elt_j in list_j:
#            for elt_i in list_i:
#                node_index += 1
#
#                # compute index element index
#                i_elt = elt_i + elt_j * len(list_i)
#
#                # ... vertex indices
#                list_indices = []
#                for _j in range(0, lpi_p[1]+1):
#                    j = _j + lpi_p[1] * elt_j
#                    for _i in range(0, lpi_p[0]+1):
#                        i = _i + lpi_p[0] * elt_i
#
#                        I = i + j * lpi_n[0]
#                        list_indices.append(I+1)
#                # ...
#
#                # ... number of nodes
#                n_nodes = len(list_indices)
#
#                nodeData = [[i_elt+1, n_nodes], list_indices]
#                list_nodeData.append(nodeData)
#        # ...
#    return list_nodeData
#    # .................................................
#
#def save_nodes_sons_2d(geo, filename):
#    list_nodeData = get_nodes_sons_2d(geo)
#
#    # .................................................
#    # ... exporting files
#    fmt_int = '%d'
#    # .................................................
#
#    # .................................................
#    a = open(filename+"_nodes_sons.txt", "w")
#    # ... write size of list_nodeData
#    a.write(str(len(list_nodeData))+' \n')
#
#    for multiL in list_nodeData:
#        # ... element id  and  number of sons nodes
#        L = multiL[0]
#        line = str(L[0]) + ", "+ str(L[1]) +  ' \n'
#        a.write(line)
#        # ... sons nodes indices
#        L = multiL[1]
#        line = ''.join(str(fmt_int % e)+', ' for e in L[0:])[:-2]+' \n'
#        a.write(line)
#    a.close()
#    # .................................................
#
#
#def get_elements_sons_2d(geo):
#    # ... sets the list of Nodes
#    geo_ref, list_lmatrices = geo.bezier_extract()
#
#    list_elementData = []
#
#    element_index = 0
#    for nrb_ref, nrb in zip(geo_ref, geo):
#        # ...
#        # we loop over each element and generate the P,
#        # ...
#        # we start by matching the 1D index with the 2D one
#        lpi_n = nrb_ref.shape
#        lpi_p = nrb_ref.degree
#
#        # .................................................
#        nx_elt = len(np.unique(nrb.knots[0])) - 1
#        ny_elt = len(np.unique(nrb.knots[1])) - 1
#        list_i = list(range(0,nx_elt))
#        list_j = list(range(0,ny_elt))
#        for elt_j in list_j:
#            for elt_i in list_i:
#                element_index += 1
#
#                # compute index element index
#                i_elt = elt_i + elt_j * len(list_i)
#
#                # ... vertex indices
#                list_indices = []
#                for _j in range(0, lpi_p[1]):
#                    j = _j + lpi_p[1] * elt_j
#                    for _i in range(0, lpi_p[0]):
#                        i = _i + lpi_p[0] * elt_i
#
#                        I = i + j * (lpi_n[0]-1)
#                        list_indices.append(I+1)
#                # ...
#
#                # ... number of elements
#                n_elements = len(list_indices)
#
#                elementData = [[i_elt+1, n_elements], list_indices]
#                list_elementData.append(elementData)
#        # ...
#    return list_elementData
#    # .................................................
#
#def save_elements_sons_2d(geo, filename):
#    list_elementData = get_elements_sons_2d(geo)
#
#    # .................................................
#    # ... exporting files
#    fmt_int = '%d'
#    # .................................................
#
#    # .................................................
#    a = open(filename+"_elements_sons.txt", "w")
#    # ... write size of list_nodeData
#    a.write(str(len(list_elementData))+' \n')
#
#    for multiL in list_elementData:
#        # ... element id  and  number of sons elements
#        L = multiL[0]
#        line = str(L[0]) + ", "+ str(L[1]) +  ' \n'
#        a.write(line)
#        # ... sons elements indices
#        L = multiL[1]
#        line = ''.join(str(fmt_int % e)+', ' for e in L[0:])[:-2]+' \n'
#        a.write(line)
#    a.close()
#    # .................................................
#
#def get_bernstein_representation_2d(geo):
#    # .................................................
#    from caid.numbering.connectivity import connectivity
#    con = connectivity(geo)
#    con.init_data_structure()
#
#    geo_ref, list_lmatrices = geo.bezier_extract()
#
#    # ... sets the list of connectivities
#    list_bernstein_representationData = []
#
#    for patch_id in range(0, geo.npatchs):
#        nrb = geo[patch_id]
#        lmatrices = list_lmatrices[patch_id]
#        local_LM = con.LM[patch_id]
#
#        lpi_n = nrb.shape
#        lpi_p = nrb.degree
#        nx_elt = len(np.unique(nrb.knots[0])) - 1
#        ny_elt = len(np.unique(nrb.knots[1])) - 1
#        list_i = list(range(0,nx_elt))
#        list_j = list(range(0,ny_elt))
#        for enum_j, j in enumerate(list_j):
#            for enum_i, i in enumerate(list_i):
#                # compute index element index
#                i_elt = enum_i + enum_j * len(list_i)
#
#                # ... number of non vanishing basis per element
#                nen = (lpi_p[0] + 1) * (lpi_p[1] + 1)
#                # ...
#
#                # ... global index for each local basis function
#                Mat_LM = local_LM[:,i_elt]
#                Mat_LM = np.ravel(Mat_LM, order='F')
#                # ...
#
#                # ... local Bezier-extraction matrix
#                Mat_Bform = lmatrices[i_elt]
#                Mat_Bform = np.ravel(Mat_Bform, order='F')
#                # ...
#
#                bernstein_representationData = [[i_elt+1, nen], Mat_LM, Mat_Bform]
#                list_bernstein_representationData.append(bernstein_representationData)
#    # ...
#    return list_bernstein_representationData
#    # .................................................
#
#def save_bernstein_representation_2d(geo, filename):
#    list_bernstein_representationData = get_bernstein_representation_2d(geo)
#
#    # .................................................
#    # ... exporting files
#    fmt_int   = '%d'
#    fmt_float = '%.15f'
#    # .................................................
#
#    # .................................................
#    a = open(filename+"_bernstein_representation.txt", "w")
#    # ... write size of list_bernstein_representationData
#    a.write(str(len(list_bernstein_representationData))+' \n')
#    for multiL in list_bernstein_representationData:
#        # ... element id  and  number of non vanishing basis per element
#        L = multiL[0]
#        line = str(L[0]) + ", "+ str(L[1]) +  ' \n'
#        a.write(line)
#        # ... local LM
#        L = multiL[1]
#        line = ''.join(str(fmt_int % e)+', ' for e in L[:])[:-2]+' \n'
#        a.write(line)
#        # ... local B-form
#        L = multiL[2]
#        line = ''.join(str(fmt_float % e)+', ' for e in L[:])[:-2]+' \n'
#        a.write(line)
#    a.close()
#    # ...
#    # .................................................
#
## ...
#def save_bernstein_basis_2d(geo, basename=None, quad_rule="legendre", nderiv=1):
#    filename_quad   = "quadrature.txt"
#    filename_values = "bernstein_values.txt"
#    if basename is not None:
#        filename_quad   = basename + "_" + "quadrature.txt"
#        filename_values = basename + "_" + "bernstein_values.txt"
#
#    nrb = geo[0]
#    px = nrb.degree[0] ; py = nrb.degree[1]
#
#    # ... create a Bezier patch of the given polynomial degrees
#    Bx = bernstein(px)
#    By = bernstein(px)
#    qd = quadratures()
#    xint = np.asarray([0.,1.])
#    yint = np.asarray([0.,1.])
#    [x,wx] = qd.generate(xint, px, quad_rule)
#    [y,wy] = qd.generate(yint, py, quad_rule)
#    x = x[0] ; wx = wx[0]
#    y = y[0] ; wy = wy[0]
#    Batx = Bx.evaluate(x, der=nderiv)
#    Baty = By.evaluate(y, der=nderiv)
#
#    lpi_p = np.asarray([px,py])
#
#    # .................................................
#    a = open(filename_quad, "w")
#    # ... write spline degrees
#    line = str(lpi_p[0]) + ', ' + str(lpi_p[1]) + ' \n'
#    a.write(line)
#    # ... write gauss points and their weights
#    for _y,_wy in zip(y,wy):
#        for _x,_wx in zip(x,wx):
#            line = str(_x) + ', ' + str(_y) + ', ' + str(_wx*_wy)
#            line = line + ' \n'
#            a.write(line)
#    a.close()
#    # .................................................
#
#    # .................................................
#    a = open(filename_values, "w")
#    # ... write spline degrees    and     n derivaties
#    line = str(lpi_p[0]) + ', ' + str(lpi_p[1]) + ', ' + str(nderiv) + ' \n'
#    a.write(line)
#    # ... write gauss points and their weights
#    for j in range(0, py+1):
#        for i in range(0, px+1):
#            for jy in range(0,py+1):
#                for ix in range(0,px+1):
#                    line = " "
#                    for dy in range(0,nderiv+1):
#                        for dx in range(0,nderiv+1):
#                            B = Batx[i,ix,dx] * Baty[j,jy,dy]
#                            line += str(B) + ', '
#                    line = line[:-2] + ' \n'
#                    a.write(line)
#    a.close()
#    # .................................................
# ...

############################################################
if __name__=="__main__":
    from caid.cad_geometry import square, circle, circle_5mp
    geo = square(n=[3,3], p=[3,3])
#    geo = circle_5mp(n=[3,3], p=[3,3])

    basename = "splines"
    from caid.io import BZR
    rw = BZR()
    rw.write(basename, geo, fmt="txt")

#    save_nodes_2d(geo, basename)
#    save_nodes_bezier_2d(geo, basename)
#    save_nodes_sons_2d(geo, basename)
#    save_elements_2d(geo, basename)
#    save_elements_bezier_2d(geo, basename)
#    save_elements_sons_2d(geo, basename)
#    save_bernstein_representation_2d(geo, basename)
#    save_bernstein_basis_2d(geo, basename=basename)
