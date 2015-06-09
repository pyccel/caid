# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.tri as tri
import matplotlib.pyplot as plt

class Quadrangles(object):
    def __init__(self, x, y, quads=None):
        """
        a quadrangular mesh is represented by a triangulation. However, we must
        pay attention to degenerated quadangles and those with an angle > pi
        """
        self._x = x
        self._y = y
        if quads is None:
            print ("quadrangles automatic construction from vertices not yet implemented")
            raise()
        self._quads = quads

        self._triangles = None
        self._triang    = None
        self._ancestors = None
        self._sons      = None

        self._create_triangulation()
        self._compute_neighbors()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def quads(self):
        return self._quads

    @property
    def triangles(self):
        return self._triangles

    @property
    def triang(self):
        return self._triang

    @property
    def ancestors(self):
        return self._ancestors

    @property
    def neighbors(self):
        return self._neighbors

    @property
    def sons(self):
        return self._sons

    def _uniform_split_quad(self, quad):
        """
        splits a quadrangle into 2 triangles
        Args:
            quad: list of 4 vertices ids
        Returns:
            2 triangles
        """
        I00,I10,I11,I01 = quad
        T1 = [I00,I10,I11]
        T2 = [I00,I11,I01]
        return T1,T2

    def _create_triangulation(self):
        triangles = [] ; ancestors = [] ; sons = []
        for enum,quad in enumerate(self.quads):
            T1,T2 = self._uniform_split_quad(quad)

            triangles.append(T1) ; ancestors.append(enum)
            triangles.append(T2) ; ancestors.append(enum)
            sons.append([2*enum, 2*enum+1])
        self._triangles = np.asarray(triangles)
        self._ancestors = np.asarray(ancestors)
        self._sons = np.array(sons, dtype=np.int32)

        self._triang = tri.Triangulation(self.x,self.y,self.triangles)

    def _compute_neighbors(self):
        n_quad = len(self.quads)
        ancestors = self.ancestors
#        print ancestors
        _neighbors = []
        for i in range(0, n_quad):
            T1 = 2*i ; T2 = 2*i+1
            ancestor = i
            neighbors = list(self.triang.neighbors[T1][0:2]) \
                    + list(self.triang.neighbors[T2][1:])
            neighbors = np.array(neighbors, dtype=np.int32)
#            print neighbors
            quad_neighbors = -np.ones(4, dtype=np.int32)
            for enum,T in enumerate(neighbors):
                if T > -1:
                    quad_neighbors[enum] = ancestors[T]
            _neighbors.append(quad_neighbors)
        self._neighbors = np.array(_neighbors, dtype=np.int32)
#        print "========="
#        print self._neighbors

    def plot(self):
        plt.triplot(self.triang, '-', lw=0.75, color="red")


class CubicHermiteBezier(Quadrangles):
    def __init__(self, nodes_filename, elements_filename, huhv_filename=None):
        """
        TODO: remove huhv_filename when huhv will be given in the nodes file
        """
        # node,R,Z,u1,u2,v1,v2,w1,w2,boundary type,boundary index,color
        fmt_nodes = [int, float, float, float, float, float, float, float, float, int, int, int]
        nodes    = np.genfromtxt(nodes_filename, comments="#")
#        print nodes.shape

        # element,vertex(1:4),color
        fmt_elements = [int, int, int, int, int, int]
        elements = np.genfromtxt(elements_filename, comments="#")
        elements = np.array(elements, dtype=np.int32)
        colors    = np.array(elements[:,-1], dtype=np.int32)
#        print elements.shape

        if huhv_filename is not None:
            # node,hu,hv
            fmt_huhv = [int, float, float]
            huhv     = np.genfromtxt(huhv_filename, comments="#")
            print huhv.shape
        else:
            huhv = None
            hu   = None
            hv   = None

        # extract quadrangles and use 0 based indexing
        quads = elements[:,1:-1] - 1

        R        = nodes[:,1]
        Z        = nodes[:,2]
        u        = nodes[:,3:5]
        v        = nodes[:,5:7]
        w        = nodes[:,7:9]
        bnd_type = np.array(nodes[:,9], dtype=np.int32)
        bnd_ind  = np.array(nodes[:,10], dtype=np.int32)
        vertices_colors  = np.array(nodes[:,11], dtype=np.int32)

        # extract hu and hv
        if huhv is not None:
            hu       = huhv[:,1]
            hv       = huhv[:,2]


        Quadrangles.__init__(self, R, Z, quads=quads)

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

        self._compute_colored_neighbors()

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
    def n_quads(self):
        return self.quads.shape[0]

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
        returns a 1D array of hu-length for each vertex
        """
        return self._hu

    @property
    def hv(self):
        """
        returns a 1D array of hv-length for each vertex
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

class QuadSticker(object):
    def __init__(self, quadrangles, find=False):
        self._quadrangles = quadrangles
        self._treated_elements = -np.ones(quadrangles.n_quads, dtype=np.int32)
        self._dict_elements = {}
        if find:
            self.find_elements()

    @property
    def quadrangles(self):
        return self._quadrangles

    @property
    def available_colors(self):
        return np.unique(self.quadrangles.colors)

    def tensor_elements(self,color):
        return self._dict_elements[color]

    def _distance_point_quad(self, quad, x, y):
        """
        computes distances of a point to the 4 lines generated by a
        quadrangle
        """
        vertices_x = np.zeros((4,2))
        vertices_y = np.zeros((4,2))

        list_edgeb = [0,1,2,3]
        list_edgee = [1,2,3,0]
        for edge in range(0,4):
            Vb = quad[list_edgeb[edge]]
            Ve = quad[list_edgee[edge]]

            vertices_x[edge,0] = self.quadrangles.x[Vb]
            vertices_x[edge,1] = self.quadrangles.x[Ve]
            vertices_y[edge,0] = self.quadrangles.y[Vb]
            vertices_y[edge,1] = self.quadrangles.y[Ve]

        distances = np.zeros(4)
        for edge in range(0,4):
            d     = (vertices_x[edge,1]-vertices_x[edge,0]) \
                  * (vertices_y[edge,0]-y) \
                  - (vertices_y[edge,1]-vertices_y[edge,0]) \
                  * (vertices_x[edge,0]-x)
            denom = (vertices_x[edge,1]-vertices_x[edge,0])**2 \
                  + (vertices_y[edge,1]-vertices_y[edge,0])**2

            distances[edge] = np.abs(d) / np.sqrt(denom)
        return distances

    def find_next_stage(self, color, stage):
        """
        returns elements to be treated for the sticking algorithm
        updates the array self._treated_elements
        2: element has been treated and is inside the patch
        1: new boundary patch elements
        0: neighbors of the boundary patch elements
        -1: remaining elements
        """
        pass

    def find_elements(self, color=None, str_color=None):
        col = ["r","g","y","k","c"]
        if color is None:
            list_colors = self.available_colors
        else:
            list_colors = [color]

        def _find_stage_elements(elmt, direction, marked_elements, stage, str_color=None):
            e = elmt
            marked_elements[e] = 1
            if str_color is None:
                str_color = col[stage % 5]
#            plt.plot(x[quads[e]],y[quads[e]],"o"+str_color)
            list_elements = []
            ll_condition = True
            while ll_condition:
#                print mask
                neighbors = self.quadrangles.neighbors[e]
                e = neighbors[direction]
                ll_condition = not (e == -1)
                ll_condition = ll_condition \
                        and (self.quadrangles.colors[e]==color) \
                        and (marked_elements[e] == 0)
                if ll_condition:
                    list_elements.append(e)
                    marked_elements[e] = 1
                    quad = quads[e]
#                    plt.plot(x[quad],y[quad],"o"+str_color)
            return list_elements

        for color in list_colors:
            x = self.quadrangles.x
            y = self.quadrangles.y
            quads = self.quadrangles.quads
            list_all_elements = []
            marked_elements = np.zeros(self.quadrangles.n_quads, dtype=np.int32)

            elmts = self.quadrangles.extremal_elements(color)
            elmt_base = elmts[0]
            quad_base = quads[elmt_base]

            mask = np.logical_and(self.quadrangles.neighbors[elmt_base] >= 0, \
                                  self.quadrangles.colors[self.quadrangles.neighbors[elmt_base]]==color)
            directions = np.where(mask)[0]


            list_elements = _find_stage_elements(elmt_base, directions[0], marked_elements, 0, str_color=str_color)
            list_all_elements.append(list_elements)

            ll_all_condition = True
            i_stage = 1
            while ll_all_condition:
                direction = directions[1]
                neighbors = self.quadrangles.neighbors[elmt_base]
                elmt_base = neighbors[direction]
                ll_all_condition = not (elmt_base == -1)
                ll_all_condition = ll_all_condition \
                        and (self.quadrangles.colors[elmt_base]==color)\
                        and (marked_elements[elmt_base] == 0)
    #            ll_all_condition = ll_all_condition and (i_stage < 10)

                if ll_all_condition:
    #                print i_stage
                    list_elements = _find_stage_elements(elmt_base, directions[0], marked_elements, i_stage, str_color=str_color)
                    list_all_elements.append(list_elements)
                    i_stage += 1

            assert_condition = True
            my_len = len(list_all_elements[0])
            for all_elements in list_all_elements:
                if len(all_elements) != my_len:
                    assert_condition = False
                    print ("Error. Not a tensor product structure")
            assert(assert_condition)

            self._dict_elements[color] = list_all_elements
