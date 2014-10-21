# -*- coding: UTF-8 -*-
import numpy as np
from numpy import cos, sin, pi, array
import numpy.linalg as la
import matplotlib.tri as mtri
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib
from scipy.spatial import Delaunay

def limiter_default(x):
    return True

class stencil(object):
    def __init__(self, origin, mat, limiter=None):
        """
        creates the box-splines tesselation using mat.
        Args:
            mat : list of vectors. mat.shape = [n,3]
        """
        self._origin = origin
        self._control= []
        if limiter is None:
            self.limiter = limiter_default
        else:
            self.limiter = limiter

        n,d = mat.shape
        self._vectors = np.zeros((n,4))
        self._vectors[...,:3] = mat[:,:3]

        self._tri = None
        self._simplices_global_id = None
        self._neighbours = [] # list of stencils that extend the current stencil

        self.update()
        self.triangulate()

    @property
    def origin(self):
        return self._origin

    @property
    def vectors(self):
        return self._vectors

    @property
    def control(self):
        return self._control

    @property
    def simplices_global_id(self):
        return self._simplices_global_id

    def set_limiter(self, limiter):
        self.limiter = limiter

    def update(self):
        mat = self.vectors
        n,d = mat.shape
        list_pts = [self.origin]
        for i in range(0,n):
            V = mat[i,:]
            points = []
            for x in list_pts:
                ll_found = False
                for y in list_pts:
                    ll_found = ( np.linalg.norm(x+V[:3]-y) < 1.e-7 )
                if not ll_found:
                    points.append(x+V[:3])
            list_pts += points

        n = len(list_pts)
        points = np.zeros((n,3))
        for i in range(0,n):
            points[i,:] = list_pts[i][:]
        self._control= points

        self.clean_control()

    def clean_control(self):
        points = self.control
        n,d = points.shape
        list_isoccur = np.zeros(n, dtype=np.int)
        for i in range(0,n):
            x = points[i,:]
            for j in range(i+1,n):
                y = points[j,:]
                if (np.linalg.norm(x-y) < 1.e-7):
                    list_isoccur[j] = 1

        list_pts = []
        for i in range(0,n):
            if list_isoccur[i] == 0:
                list_pts.append(points[i,:])

        n = len(list_pts)
        points = np.zeros((n,3))
        for i in range(0,n):
            points[i,:] = list_pts[i][:]
        self._control= points

    def translate(self, displ):
        self._origin = np.asarray(self._origin) + displ
        self.update()

    def highlight(self):
        x = self.control[:,0]
        y = self.control[:,1]
        z = np.ones_like(x)
        plt.pcolor(x,y,z)

    def filter(self):
        list_pts_in = [] ; list_pts_out = []
        n,d = self.control.shape
        for i in range(0,n):
            P = self.control[i,:3]
            if self.limiter(P):
                list_pts_in.append(P)
            else:
                list_pts_out.append(P)

        list_pts = list_pts_in
        n = len(list_pts)
        points = np.zeros((n,3))
        for i in range(0,n):
            points[i,:] = list_pts[i][:]
        points_in = points

        list_pts = list_pts_out
        n = len(list_pts)
        points = np.zeros((n,3))
        for i in range(0,n):
            points[i,:] = list_pts[i][:]
        points_out = points

        return points_in, points_out

    def plot(self, color='b'):
        points_in, points_out = self.filter()

        plt.plot(points_in[:,0], points_in[:,1], 'o'+color)
        plt.plot(points_out[:,0], points_out[:,1], 'or')

        points = self.control

        plt.triplot(points[:,0], points[:,1], self.tri.simplices.copy())

    @property
    def polygon(self):
        points = self.control[:,:2]
        hull = ConvexHull(points)
        points = points[hull.vertices,:2]
        return Polygon(points, True)

    @property
    def boundary(self):
        points = self.control[:,:2]
        hull = ConvexHull(points)
        return hull.vertices

    @property
    def tri(self):
        return self._tri

    @property
    def neighbours(self):
        return self._neighbours

    def is_inside(self, pts):
        """
        returns a boolean array for each point in pts
        pts must be array((n,d)) with d >= 2
        """
        list_bool = []
        n,d = pts.shape
        for i in range(0, n):
            P = pts[i,:2]
            list_bool.append(self.is_inside_single(P))

        return list_bool


    def is_inside_single(self, P):
        """
        returns True if P is inside the stencil
        """
        x = P[0] ; y = P[1]

        points = self.control[self.boundary,:2]

        n,d = points.shape
        inside =False

        p1x,p1y = points[0,:2]
        for i in range(n+1):
            p2x,p2y = points[i % n,:2]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

    def scale(self, h):
        self._control *= h
        self._origin  *= h

    def __str__(self):
        message = "origin " + str(self.origin) + " \n " + \
                "vectors " + str(self.vectors)
        return message


    def copy(self):
        """
        Copy a stencil object.

        Returns a new instace of the stencil objects with copies of the
        control points and knot vectors. Modifying the knot vector or
        control points of the returned object WILL NOT affect this
        object.

        Examples
        --------

        Create a random curve, copy the curve, change the control points,
        demonstrate that now c1 and c2 are different.

        >>> C = np.random.rand(5,2)
        >>> U = [0,0,1,2,3,4,4]
        >>> c1 = NURBS([U], C)
        >>> c2 = c1.copy()
        >>> c2.control[2,:] = [1.0,1.0,0.0,1.0]
        >>> (abs(c2.control-c1.control)).max() < 1.0e-15
        False

        """
        sten = stencil.__new__(type(self))
        sten._origin  = self.origin.copy()
        sten._vectors = self.vectors.copy()
        sten._control = self.control.copy()
        sten.limiter  = self.limiter
        return sten

    def bounds(self, axis=0):
        i = 0
        ll_condition = True
        while ll_condition and (i<10):
            sten = self.copy()
            v = i*self.vectors[axis,:3]
            sten.translate(v)
            points_in, points_out = sten.filter()
            if points_in.shape[0] == 0:
                ll_condition = False
            M = i
            i += 1

        i = -1
        ll_condition = True
        while ll_condition and (i>-10):
            sten = self.copy()
            v = i*sten.vectors[axis,:3]
            sten.translate(v)
            points_in, points_out = sten.filter()
            if points_in.shape[0] == 0:
                ll_condition = False
            m = i
            i -= 1
        return m+1, M

    def expand(self, axis=0, bounds= None):
        if bounds is None:
            m, M = self.bounds(axis=axis)
        else:
            m = bounds[0] ; M = bounds[1]

        if axis ==0:
            list_i = range(m,M)
            list_j = range(0,1)
        if axis ==1:
            list_i = range(0,1)
            list_j = range(m,M)
        T = tesselation(self.origin, self.vectors, list_i, list_j, limiter=self.limiter)
        return T

    def triangulate(self):
        self._tri = Delaunay(self.control[:,:2])
        self._simplices_global_id = -np.ones(self.tri.simplices.shape[0], dtype=np.int)

    def is_valid(self, resolution=1):
        """
        a stencil is valid with respect to a limiter, if there intersection is
        not reduced to empty, point, face
        """
        dim= 2
        n1 = resolution
        n2 = resolution
        X  = np.zeros((n1,n2))
        Y  = np.zeros((n1,n2))
        P  = np.zeros(dim)

        k1 = np.linspace(0.,1.,n1+2)[1:-1]
        k2 = np.linspace(0.,1.,n2+2)[1:-1]

        R = self.vectors[:2,:2]

        for i in range(n1) :
            for j in range(n2) :
                k = [k1[i], k2[j]]
                [X[i,j], Y[i,j]] = np.dot(R,k)
                P = [X[i,j], Y[i,j]] + self.origin[:2]
                ll_flag = self.limiter(P)
                if ll_flag:
                    return True

        return False

    def __eq__(self, other):
        ll_condition = True
        ll_condition = ll_condition and (np.linalg.norm(self.origin-other.origin) < 1.e-7)

        return ll_condition

    def extend(self, sten):
        ll_flag = False
        for sten_ref in self.neighbours:
            if sten == sten_ref:
#            if id(sten) == id(sten_ref):
                ll_flag = True
        if not ll_flag:
            self._neighbours.append(sten)

class triangle(object):
    def __init__(self):
        self._list = []
        self._currentElt = -1

    def __len__(self):
        return len(self._list)

    def index(self, tri):
        return self._list.index(tri)

    def next(self):
        if len(self) == 0:
            raise StopIteration
        self._currentElt += 1
        if self._currentElt >= len(self):
            self._currentElt = -1
            raise StopIteration
        return self._list[self._currentElt]

    def __iter__(self):
        return self

    def __getitem__(self, key):
        return self._list[key]

    def append(self, sten, simplex_id):
        self._list.append({'stencil':sten, 'simplex_id':simplex_id})

    def __str__(self):
        message = ""
        for data in self:
            sten = data['stencil']
            simplex_id = data['simplex_id']
            message +=  str(id(sten)) + "   " + str(simplex_id) + ", "
        return message

    def extend(self):
        """
        returns the list of stencil that are valid
        """
        list_flag = []
        list_stencil = []
        for data in self:
            sten = data['stencil']
            simplex_id = data['simplex_id']
            flag = sten.is_valid()
            list_flag.append(flag)
            if flag:
                list_stencil.append(sten)
        return list_stencil


class triangulation(object):
    def __init__(self, list_stencil):
        self._list = []
        self._currentElt = -1

        self._list_stencil = list_stencil

    def __len__(self):
        return len(self._list)

    def index(self, tri):
        return self._list.index(tri)

    def next(self):
        if len(self) == 0:
            raise StopIteration
        self._currentElt += 1
        if self._currentElt >= len(self):
            self._currentElt = -1
            raise StopIteration
        return self._list[self._currentElt]

    def __iter__(self):
        return self

    def __getitem__(self, key):
        return self._list[key]

    def append(self, T):
        self._list.append(T)
        # update the triangle's stencils with its id
        global_id = len(self) - 1
        for data in T:
            sten = data['stencil']
            simplex_id = data['simplex_id']
            sten.simplices_global_id[simplex_id] = global_id

    def initialize(self):
        """
        """
        nstencil = len(self._list_stencil)
        i_sten_ref = 0
        sten_ref = self._list_stencil[i_sten_ref]
        for enum, simplex in enumerate(sten_ref.tri.simplices):
            T = triangle()
            T.append(sten_ref, enum)
            triang.append(T)

        for i_sten_ref in range(0, nstencil):
            sten_ref = self._list_stencil[i_sten_ref]
            for i_sten in range(i_sten_ref+1, nstencil):
                sten = self._list_stencil[i_sten]
                list_brc = []
                points = sten.control
                for T in sten.tri.simplices:
                    pts = points[T]
                    A = array(pts[0,:]) ; B = array(pts[1,:]) ; C = array(pts[2,:])
                    b = (A+B+C) / 3.
                    list_brc.append(b)
                list_pts = list_brc
                n = len(list_pts)
                points = np.zeros((n,3))
                for i in range(0,n):
                    points[i,:] = list_pts[i][:]
                list_flag = sten_ref.is_inside(points)

                for i in range(0, len(sten.tri.simplices)):
                    barycenter = list_brc[i]
                    flag = list_flag[i]
                    if not flag:
                        T = triangle()
                        T.append(sten, i)
                        triang.append(T)
                    else:
                        # find the triangle and then append [sten, vertices]
                        simplex_id = sten_ref.tri.find_simplex(barycenter[:2])
                        global_id = sten_ref.simplices_global_id[simplex_id]
#                        print ">>> ", global_id, simplex_id, i
                        T = triang[global_id]
                        T.append(sten, i)

    def extend(self):
        for T in self:
            l_stencils = T.extend()

            n = len(l_stencils)
            for i_sten_ref in range(0,n):
                sten_ref = l_stencils[i_sten_ref]
                for i_sten in range(0,n):
                    sten = l_stencils[i_sten]
                    if (i_sten_ref != i_sten):
                        sten_ref.extend(sten)

class tesselation:
    def __init__(self, origin, mat, list_i, list_j, limiter=None):
        self._list = []
        self._currentElt = -1

        self._list_i = list_i
        self._list_j = list_j
        self._origin = origin

        n,d = mat.shape
        self._vectors = np.zeros((n,4))
        self._vectors[...,:3] = mat[:,:3]

        if limiter is None:
            self.limiter = limiter_default
        else:
            self.limiter = limiter

        sten = stencil(origin, mat, limiter=limiter)
        self.append(sten)
        for j in list_j:
            for i in list_i:
                new_sten = sten.copy()
                v = i*new_sten.vectors[0,:3] + j*new_sten.vectors[1,:3]
                new_sten.translate(v-new_sten.origin)
                self.append(new_sten)

    @property
    def origin(self):
        return self._origin

    @property
    def vectors(self):
        return self._vectors

    def plot(self):
        for sten in self:
            sten.plot()

    def scale(self, h):
        for sten in self:
            sten.scale(h)

    @property
    def stencils(self):
        return self._list

    def append(self, sten):
        self._list.append(sten)

    def __len__(self):
        return len(self._list)

    def index(self, sten):
        return self._list.index(sten)

    def next(self):
        if len(self) == 0:
            raise StopIteration
        self._currentElt += 1
        if self._currentElt >= len(self):
            self._currentElt = -1
            raise StopIteration
        return self._list[self._currentElt]

    def __iter__(self):
        return self

    def __getitem__(self, key):
        return self._list[key]

    def bounds(self, axis=1):
        M = -10000
        m =  10000
        for stn in self:
            i = 0
            ll_condition = True
            while ll_condition and (i<10):
                sten = stn.copy()
                v = i*stn.vectors[axis,:3]
                sten.translate(v)
                points_in, points_out = sten.filter()
                if points_in.shape[0] == 0:
                    ll_condition = False
                _M = i
                i += 1

            i = 0
            ll_condition = True
            while ll_condition and (i>-10):
                sten = stn.copy()
                v = i*stn.vectors[axis,:3]
                sten.translate(v)
                points_in, points_out = sten.filter()
                if points_in.shape[0] == 0:
                    ll_condition = False
                _m = i
                i -= 1

            M = max(_M,M)
            m = min(_m,m)
        return m+1, M

    def expand(self, axis=1, bounds=None):
        if bounds is None:
            m, M = self.bounds(axis=axis)
        else:
            m = bounds[0] ; M = bounds[1]

        if axis ==0:
            ib = min(self._list_i) + m ; ie = max(self._list_i) + M + 1
            list_i = range(ib,ie)
            list_j = self._list_j
        if axis ==1:
            jb = min(self._list_j) + m ; je = max(self._list_j) + M + 1
            list_i = self._list_i
            list_j = range(jb,je)
        T = tesselation(self.origin, self.vectors, list_i, list_j, limiter=self.limiter)
        return T


if __name__ == "__main__":
    patches = []

    R = 4.
    n = 1
    h = 1. # 0.25
    r1 = np.array([ 1.0, 0.0, 0. ])
    r2 = np.array([ 0.0, 1.0, 0. ])
    r3 = np.array([ 1.0, 1.0, 0. ])
    r4 = np.array([-1.0, 1.0, 0. ])

    e1 = np.array([ np.sqrt(3)/2., 0.5, 0. ])
    e2 = np.array([-np.sqrt(3)/2., 0.5, 0. ])
    e3 = np.array([0., 1.0, 0. ])

    def test1():
        list_pts = [r1, r2, r1, r2, r3]
        list_t   = range(-6,4)
        return list_pts, list_t

    def test2():
        list_pts = [r1, r2, r3, r4]
        list_t   = range(-6,6)
        return list_pts, list_t

    def test3():
        list_pts = [e1, e2, e3, e1, e2, e3]
        list_t   = range(-6,6)
#        list_t   = range(-2,2)
        return list_pts, list_t


#    list_pts, list_t = test1()
#    list_pts, list_t = test2()
    list_pts, list_t = test3()

    n = len(list_pts)
    mat = np.zeros((n,3))
    for i in range(0,n):
        mat[i,:] = list_pts[i][:]

    origin = np.asarray([0.,0.,0.])
    origin1 = 2 * list_pts[0]
    origin2 = list_pts[0] + list_pts[1]
    origin3 = 2 * list_pts[1]
    origin_far = 5 * list_pts[1]

    def limiter(x):
        if (x[0]-0.)**2 + (x[1]-0.)**2 <= R**2:
            return True
        else:
            return False

    def boundary(x):
        return (x[0]-0.)**2 + (x[1]-0.)**2

    fig, ax = plt.subplots()

    sten_ref = stencil(origin, mat, limiter=limiter)
    sten_ref.scale(h)
    patches.append(sten_ref.polygon)
    sten_ref.plot()

    sten1 = stencil(origin1, mat, limiter=limiter)
    sten1.scale(h)
    patches.append(sten1.polygon)
    sten1.plot()

    sten2 = stencil(origin2, mat, limiter=limiter)
    sten2.scale(h)
    patches.append(sten2.polygon)
    sten2.plot()

    sten3 = stencil(origin3, mat, limiter=limiter)
    sten3.scale(h)
    patches.append(sten3.polygon)
    sten3.plot()

    sten_far = stencil(origin_far, mat, limiter=limiter)
    sten_far.scale(h)
    patches.append(sten_far.polygon)
    sten_far.plot()

#    print sten_ref.is_valid()
#
#    P = [1.,5.]
#    pts = np.zeros((3,2))
#    pts[0,0] = 1.; pts[0,1] = 1.
#    pts[1,0] = 1.5; pts[1,1] = 1.
#    pts[2,0] = 1.; pts[2,1] = 2.
#
#    plt.plot(pts[:,0], pts[:,1], 'og')
#    print sten_ref.is_inside(pts)

#    P = [1.,5.]
#    pts = np.zeros((3,2))
#    pts[0,0] = 1.; pts[0,1] = 1.
#    pts[1,0] = 1.5; pts[1,1] = 1.
#    pts[2,0] = 1.; pts[2,1] = 2.
#
#    plt.plot(pts[:,0], pts[:,1], 'og')
#    print sten.is_inside(pts)
#
#    tri = sten.tri
#    list_brc = []
#    points = sten.control
#    for T in tri.simplices:
#        pts = points[T]
#        A = array(pts[0,:]) ; B = array(pts[1,:]) ; C = array(pts[2,:])
#        b = (A+B+C) / 3.
#        list_brc.append(b)
#
#    list_pts = list_brc
#    n = len(list_pts)
#    points = np.zeros((n,3))
#    for i in range(0,n):
#        points[i,:] = list_pts[i][:]
#    print sten_ref.is_inside(points)

    list_stencil = [sten_ref, sten1, sten2, sten3, sten_far]
    triang = triangulation(list_stencil)
    triang.initialize()

    triang.extend()

    print len(sten_ref.neighbours)

#    for enum, simplex in enumerate(sten_ref.tri.simplices):
#        T = triangle()
#        T.append(sten_ref, enum)
#        triang.append(T)
#
#    tri = sten.tri
#    list_brc = []
#    points = sten.control
#    for T in tri.simplices:
#        pts = points[T]
#        A = array(pts[0,:]) ; B = array(pts[1,:]) ; C = array(pts[2,:])
#        b = (A+B+C) / 3.
#        list_brc.append(b)
#    list_pts = list_brc
#    n = len(list_pts)
#    points = np.zeros((n,3))
#    for i in range(0,n):
#        points[i,:] = list_pts[i][:]
#    list_flag = sten_ref.is_inside(points)
#
#    for i in range(0, len(sten.tri.simplices)):
#        barycenter = list_brc[i]
#        flag = list_flag[i]
#        if not flag:
#            T = triangle()
#            T.append(sten, i)
#            triang.append(T)
#        else:
#            # find the triangle and then append [sten, vertices]
#            simplex_id = sten_ref.tri.find_simplex(barycenter[:2])
#            global_id = sten_ref.simplices_global_id[simplex_id]
#            print ">>> ", global_id, simplex_id, i
#            T = triang[global_id]
#            T.append(sten, i)


#    for T in triang:
#        print T

    print len(triang)

#    tess = sten_ref.expand(axis=0, bounds=[-7,7])
#    tess.scale(h)
#    print len(tess)

#    T = tess.expand(axis=1, bounds=[-7,7])
#    T.scale(h)
#    print len(T)

#    for sten in tess:
##        sten.plot()
#        patches.append(sten.polygon)

#    for sten in T:
#        sten.plot()
#        patches.append(sten.polygon)

#    for i in [0,1,2]:
#        patches.append(T.stencils[i].polygon)


#    sten = stencil(origin, mat)
#    sten.set_limiter(limiter)
#    sten.scale(h)
#    sten.plot()
#
#    patches = []
#    patches.append(sten.polygon)
#
##    plt.colorbar(p)
#
#    for j in list_t:
#        for i in list_t:
#            v = i*sten.vectors[0,:3] + j*sten.vectors[1,:3]
#            sten.translate(v-sten.origin)
#            sten.scale(h)
##            sten.plot()
#
#            if ((i == 0) and (j == 0)) or \
#               ((i == 1) and (j == 0)) or \
#               ((i == -3) and (j == -3)):
#
##                sten.highlight()
#                patches.append(sten.polygon)
#                sten.plot()

    colors = 100*np.random.rand(len(patches))
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
    p.set_array(np.array(colors))
    ax.add_collection(p)

    t = np.linspace(0.,2*np.pi, 100)
    r = [R*np.cos(t), R*np.sin(t)]
    plt.plot(r[0], r[1],'-k')

    plt.show()



