# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from caid.core.hbezier import hbezier_square
from caid.core.hbezier import hbezier_polar
from .quadrangles import Quadrangles

def rectangle(n=None, origin=None, lengths=None):

    if n is not None:
        N_r = n[0] ; N_p = n[1]
    else:
        N_r = 10 ;  N_p = 10

    if origin is None:
        Xmin = 0. ; Ymin = 0.
    else:
        Xmin = origin[0] ; Ymin = origin[1]

    if lengths is None:
        Lx = 1. ; Ly = 1.
    else:
        Lx = lengths[0] ; Ly = lengths[1]

    coor2d, vertices, boundary_type, scales = \
            hbezier_square.construct_grid(Lx, Ly, Xmin, Ymin, N_r, N_p)

    x = coor2d[0, 0, :]
    y = coor2d[1, 0, :]

    u = coor2d[0:2, 1, :].transpose()
    v = coor2d[0:2, 2, :].transpose()
    w = coor2d[0:2, 3, :].transpose()

    hu = scales[1, :, :].transpose()
    hv = scales[2, :, :].transpose()

#    n_elmts = scales.shape[2]
#    for e in range(0, n_elmts):
#        ones  = scales[0, :, e]
#        hu = scales[1, :, e]
#        hv = scales[2, :, e]
#        huhv = scales[3, :, e]

    quads = vertices.transpose()
    quads -= 1

    geo = CubicHermiteBezier(x, y, u, v, w, hu, hv, quads \
                         , colors=None, vertices_colors=None \
                         , bnd_type=boundary_type, bnd_ind=None)

    return geo

def square(n=None):
    """
    Creates a unit square Cubic Hermite Bezier object.
    """
    return rectangle(n=n, origin=[0.,0.], lengths=[1.,1.])

def circle(n=None, center=None, rmin=0., rmax=1.):
    if center is None:
        RGEO = 0. ; ZGEO = 0.
    else:
        RGEO = center[0] ; ZGEO = center[1]

    if n is not None:
        N_r = n[0] ; N_p = n[1]
    else:
        N_r = 10 ;  N_p = 10

    ANGLE_START = 0.

    coor2d, vertices, boundary_type, scales = \
            hbezier_polar.construct_grid(RGEO, ZGEO, rmax, rmin, ANGLE_START, N_r, N_p)

    x = coor2d[0, 0, :]
    y = coor2d[1, 0, :]

    u = coor2d[0:2, 1, :].transpose()
    v = coor2d[0:2, 2, :].transpose()
    w = coor2d[0:2, 3, :].transpose()

    hu = scales[1, :, :].transpose()
    hv = scales[2, :, :].transpose()

#    n_elmts = scales.shape[2]
#    for e in range(0, n_elmts):
#        ones  = scales[0, :, e]
#        hu = scales[1, :, e]
#        hv = scales[2, :, e]
#        huhv = scales[3, :, e]

    quads = vertices.transpose()
    quads -= 1

    geo = CubicHermiteBezier(x, y, u, v, w, hu, hv, quads \
                         , colors=None, vertices_colors=None \
                         , bnd_type=boundary_type, bnd_ind=None)

    return geo

class CubicHermiteBezier(Quadrangles):
    def __init__(self \
                 , x=None, y=None, u=None, v=None, w=None, hu=None, hv=None, quads=None \
                 , colors=None, vertices_colors=None \
                 , bnd_type=None, bnd_ind=None \
                 , nodes_filename=None, elements_filename=None, huhv_filename=None):

        if  (nodes_filename is not None) \
            and (elements_filename is not None):
            self._read_from_file(nodes_filename, elements_filename, huhv_filename)

        else:
            Quadrangles.__init__(self, x, y, quads=quads)

            # elements attributs
            self._colors    = colors

            # nodes attributs
            self._hu        = hu
            self._hv        = hv
            self._u         = u
            self._v         = v
            self._w         = w
            self._bnd_type  = bnd_type
            self._bnd_index = bnd_ind
            self._vertices_colors = vertices_colors

        if self.colors is not None:
            self._compute_colored_neighbors()

    def _read_nodes_from_file(self, nodes_filename):
        # node,R,Z,u1,u2,v1,v2,w1,w2,boundary type,boundary index,color
        fmt_nodes = [int, float, float, float, float, float, float, float, float, int, int, int]
        nodes    = np.genfromtxt(nodes_filename, comments="#")
        return nodes

    def _read_elements_from_file(self, elements_filename):
        # element,vertex(1:4),color
        fmt_elements = [int, int, int, int, int, int]
        elements = np.genfromtxt(elements_filename, comments="#")
        elements = np.array(elements, dtype=np.int32)
        try:
            colors    = np.array(elements[:,-1], dtype=np.int32)
        except:
            colors    = np.zeros_like(elements[:,0])
        return elements, colors

    def _read_huhv_from_file(self, huhv_filename):
        huhv = None
        hu = None
        hv = None
        if huhv_filename is not None:
            # node,hu,hv
            fmt_huhv = [int, float, float]
            huhv     = np.genfromtxt(huhv_filename, comments="#")

        # extract hu and hv
        if huhv is not None:
            hu       = huhv[...,1]
            hv       = huhv[...,2]

        return hu, hv

    def _read_from_file(self, nodes_filename, elements_filename, huhv_filename):
        """
        TODO: remove huhv_filename when huhv will be given in the nodes file
        """
        # ... read nodes data
        nodes = self._read_nodes_from_file(nodes_filename)
        # ...

        # ... read elements data
        elements, colors = self._read_elements_from_file(elements_filename)
        # ...

        # ... read scales
        hu, hv = self._read_huhv_from_file(huhv_filename)
        # ...

        # ... extract quadrangles and use 0 based indexing
        # TODO check before change from 1-based index to 0-based index
        quads = elements[:,1:-1] - 1
        # ...

        # ...
        R        = nodes[:,1]
        Z        = nodes[:,2]
        u        = nodes[:,3:5]
        v        = nodes[:,5:7]
        w        = nodes[:,7:9]
        bnd_type = np.array(nodes[:,9], dtype=np.int32)
        bnd_ind  = np.array(nodes[:,10], dtype=np.int32)
        vertices_colors  = np.array(nodes[:,11], dtype=np.int32)
        # ...

        # ... create quandrangulation
        Quadrangles.__init__(self, R, Z, quads=quads)
        # ...

        # ... elements attributs
        self._colors    = colors
        # ...

        # ... nodes attributs
        self._hu        = hu
        self._hv        = hv
        self._u         = u
        self._v         = v
        self._w         = w
        self._bnd_type  = bnd_type
        self._bnd_index = bnd_ind
        self._vertices_colors = vertices_colors
        # ...

    def _compute_colored_neighbors(self):
        n = self.colors.shape[0]
        color_neighbors = -np.ones((n,4), dtype=np.int32)
        elements_bnd_patchs = np.zeros(n, dtype=np.int32)
        for i in range(0,n):
            neighbors = self.neighbors[i]
            my_color = self.colors[i]
            for j in range(0,4):
                if neighbors[j] >= 0:
                    color_neighbors[i,j] = self.colors[neighbors[j]]
                    if color_neighbors[i,j] !=  my_color:
                        elements_bnd_patchs[i] += 1
                else:
                    elements_bnd_patchs[i] += 1
        self._elements_bnd_patchs = elements_bnd_patchs
        self._color_neighbors = color_neighbors

    @property
    def elements_bnd_patchs(self):
        """
        returns an array of number of neighbors having the same color
        """
        return self._elements_bnd_patchs

    @property
    def color_neighbors(self):
        """
        returns an array of number of neighbors colors for each element
        """
        return self._color_neighbors

    @property
    def colors(self):
        """
        returns an array of colors for each quadrangle
        """
        return self._colors

    @property
    def vertices_colors(self):
        """
        returns an array of colors for each quadrangle
        """
        return self._vertices_colors

    @property
    def hu(self):
        """
        returns a 2D array of hu-length for each element/vertex
        """
        return self._hu

    @property
    def hv(self):
        """
        returns a 2D array of hv-length for each element/vertex
        """
        return self._hv

    @property
    def u(self):
        """
        returns a 2D array of u vector for each vertex
        """
        return self._u

    @property
    def v(self):
        """
        returns a 2D array of v vector for each vertex
        """
        return self._v

    @property
    def w(self):
        """
        returns a 2D array of w vector for each vertex
        """
        return self._w

    @property
    def boundary_type(self):
        """
        returns a 1D array of boundary type for each vertex
        """
        return self._bnd_type

    @property
    def boundary_index(self):
        """
        returns a 1D array of boundary index for each vertex
        """
        return self._bnd_index

    def extremal_elements(self, color):
        """
        returns elements with at least 2 neighbors of the same color
        """
        list_elements = []
        for i in range(0, self.quads.shape[0]):
            if self.elements_bnd_patchs[i] > 1 and self.colors[i]==color:
                list_elements.append(i)
        return list_elements

    def save(self, label=None, colors=False, neighbours=True \
             , with_id=False, header_full=False):
        if label is None:
            label = ""
        else:
            label = str(label) + "_"
        # ... save elements file
        n_attributs = 0
        fmt = ""

        if with_id:
            n_attributs += 1
            fmt += " \t %d"

        # vertices id
        n_attributs += 4
        fmt +=' \t %d \t %d \t %d \t %d'

        # hu hv for each vertex
        for i in range(0, 4):
            n_attributs += 2
            fmt +=' \t %.17f \t %.17f'

        if colors:
            n_attributs += 1
            fmt += " \t %d"
        if neighbours:
            n_attributs += 4
            fmt +=' \t %d \t %d \t %d \t %d'

        elements_filename = label + "elements.txt"

        n_elmts = self.quads.shape[0]
        elements = np.zeros((n_elmts, n_attributs), dtype=np.float)

        list_elmts_id = list(range(1, n_elmts + 1))

        i_end = 0
        if with_id:
            elements[:,0] = np.array(list_elmts_id)
            i_end += 1

        elements[:,i_end:i_end+4] = self.quads + 1
        i_end += 4

        # hu hv for each vertex
        for i in range(0, 4):
            elements[:,i_end]   = self.hu[:,i]
            elements[:,i_end+1] = self.hv[:,i]
            i_end += 2

        if colors:
            elements[:,i_end] = np.ones(n_elmts)
            i_end += 1

        if neighbours:
            elements[:,i_end:i_end+4] = -np.ones((n_elmts,4))
            i_end += 4

        if header_full:
            header = " Number of elements"
            header += "\n"
            header += " " + str(n_elmts)
            header += "\n"
            header += " Element Data: "
            if with_id:
                header += ", element-id"
            header += " , vertex(1:4), hu, hv"
            if colors:
                header += ", color"
            if neighbours:
                header += ", neighbours(1:4)"

            comments = "# "
        else:
            header = str(n_elmts)
            comments = ""

        np.savetxt(elements_filename, elements, fmt=fmt, header=header, comments=comments)
        # ...

        # ... save nodes file
        nodes_filename = label + "nodes.txt"

        n_attributs = 0
        fmt = ""

        if with_id:
            n_attributs += 1
            fmt += " \t %d"

        # vertices coordinates
        n_attributs += 2
        fmt +=' \t %.17f \t %.17f'

        # u, v, w
        for i in range(0, 3):
            n_attributs += 2
            fmt +=' \t %.17f \t %.17f'

        # boundary type
        n_attributs += 1
        fmt += " \t %d"

        # Global ID
        n_attributs += 1
        fmt += " \t %d"

        # duplicated code
        n_attributs += 1
        fmt += " \t %d"

        if colors:
            n_attributs += 1
            fmt += " \t %d"

        n_nodes = self.x.shape[0]
        nodes = np.zeros((n_nodes, n_attributs), dtype=np.float)

        list_nodes_id = list(range(1, n_nodes + 1))

        i_end = 0
        if with_id:
            # vertices id
            nodes[:,0] = np.array(list_nodes_id)
            i_end += 1

        # x coordinate
        nodes[:,i_end] = self.x
        i_end += 1

        # y coordinate
        nodes[:,i_end] = self.y
        i_end += 1

        # u vector 
        nodes[:,i_end:i_end+2] = self.u
        i_end += 2

        # v vector 
        nodes[:,i_end:i_end+2] = self.v
        i_end += 2

        # w vector 
        nodes[:,i_end:i_end+2] = self.w
        i_end += 2

        # boundary type 
        nodes[:,i_end] = self.boundary_type
        i_end += 1

        # global id
        nodes[:,i_end] = list_nodes_id
        i_end += 1

        # duplicated code
        nodes[:,i_end] = 0
        i_end += 1

        # color
        if colors:
            nodes[:,i_end] = np.ones(n_nodes)
            i_end += 1

        if header_full:
            header = " Number of nodes"
            header += "\n"
            header += " " + str(n_nodes)
            header += "\n"
            header += " Number of DOF"
            header += "\n"
            header += " TODO " #+ str(n_nodes)
            header += "\n"
            header += " Node Data: "
            if with_id:
                header += ", node-id"
            header += ",R,Z,u1,u2,v1,v2,w1,w2,boundary type,boundary index"
            if colors:
                header += ", color"

            comments = "# "
        else:
            header = str(n_nodes)
            comments = ""

        np.savetxt(nodes_filename, nodes, fmt=fmt, header=header, comments=comments)
        # ...

