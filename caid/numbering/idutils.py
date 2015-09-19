# -*- coding: UTF-8 -*-

__author__ = 'ARA'
__all__ = ['computeLocalID', 'computeGlobalID']

import numpy as np


# ...
def initLocalID(faces, n, base):
    dim = len(n)
    if dim == 1:
        return initLocalID_1D(faces, n, base)
    if dim == 2:
        return initLocalID_2D(faces, n, base)

def initLocalID_1D(faces, n, base):
#    print ">>> Enter initLocalID_1D"
#    print "faces ", faces
#    print "n ", n
#    print "base ", base

    id =- np.ones(n, dtype=np.int)

    dim = len(n)

    ib = 0 ; ie = n[0]-1

    for f in faces:

        if f==0:
            ib += 1

        if f==1:
            ie -= 1

    for i in range(ib,ie+1):
        A = i - ib
        id[i] = A + base

    id += 1
    base += ie - ib + 1
#    print id
#    print ">>> Leave initLocalID_1D"

    return id, base

def initLocalID_2D(faces, n, base):
    id =- np.ones(n, dtype=np.int)

    dim = len(n)

    ib = 0 ; ie = n[0]-1
    jb = 0 ; je = n[1]-1

    for f in faces:

        if f==0:
            jb += 1

        if f==2:
            je -= 1

        if f==1:
            ib += 1

        if f==3:
            ie -= 1

    ne = ie  - ib + 1

#    print "ib,ie = ", ib,ie
#    print "jb,je = ", jb,je

    for j in range(jb,je+1):
        for i in range(ib,ie+1):
            A = ( j - jb ) * ne + i - ib
            id[i,j] = A + base

    id += 1
    base += ( je - jb ) * ne + ie - ib + 1

    return id, base
# ...
def print_id(id):
    dim = len(id.shape)
    if dim ==1:
        print_id_1D(id)
    if dim ==2:
        print_id_2D(id)

def print_id_1D(id):
    id_ = np.zeros_like(id)
    n, = id.shape
    for i in range(0,n):
        id_[i] = id[i]
    print(id_.transpose())

def print_id_2D(id):
    id_ = np.zeros_like(id)
    n,m = id.shape
    for j in range(0,m):
        for i in range(0,n):
            id_[i,j] = id[i,-j-1]
    print(id_.transpose())
    print(id.transpose().reshape(id.size))
# ...

# ...
def isDuplicata(patch_id, face, DuplicataPatchs):
    for data in DuplicataPatchs:
        if (data[0]==patch_id) and (data[1]==face):
            return True
    return False
# ...

# ...
def get_ij_1D(n, f):
    if f==0:
        list_i = [0]

    if f==1:
        list_i = [n[0]-1]

    return list_i

def get_ij_2D(n, f):
    if f==0:
        list_i = list(range(0, n[0]))
        list_j = [0] * n[0]

    if f==1:
        list_i = [0] * n[1]
        list_j = list(range(0, n[1]))

    if f==2:
        list_i = list(range(0, n[0]))
        list_j = [n[1] - 1] * n[0]

    if f==3:
        list_i = [n[0] - 1] * n[1]
        list_j = list(range(0, n[1]))

    return list_i, list_j

# ...
def updateDuplicated_1D(n_m, n_s, list_id, p_m, f_m, p_s, f_s, s_m=0, s_s=0):
    """
    p_m : master patch
    f_m : master face
    p_s : slave patch
    f_s : slave face
    """
    list_i_m = get_ij_1D(n_m, f_m)
    list_i_s = get_ij_1D(n_s, f_s)
#    print ">>> Enter updateDuplicated_1D"
#    print " p_m, f_m, n_m, s_m  ", p_m, f_m, n_m, s_m
#    print " p_s, f_s, n_s, s_s  ", p_s, f_s, n_s, s_s
#    print " list_i_m ", list_i_m
#    print " list_i_s ", list_i_s

    for (i_m,i_s) in zip(list_i_m, list_i_s):
        id_s = list_id[p_s]
        id_m = list_id[p_m]
#        print " id_s ", id_s
#        print " id_m ", id_m
#        print " i_s ", i_s
#        print " i_m ", i_m

        id_s[i_s+s_s] = id_m[i_m+s_m]
#    print list_id
#    print ">>> Leave updateDuplicated_1D"
    return list_id

def updateDuplicated_2D(n_m, n_s, list_id, p_m, f_m, p_s, f_s, s_m=0, s_s=0):
    """
    p_m : master patch
    f_m : master face
    p_s : slave patch
    f_s : slave face
    s_m : master shift
    s_s : slave shift
    """
    list_i_m, list_j_m = get_ij_2D(n_m, f_m)
    list_i_s, list_j_s = get_ij_2D(n_s, f_s)

#    print " list_i_m ", list_i_m
#    print " list_j_m ", list_j_m
#    print " list_i_s ", list_i_s
#    print " list_j_s ", list_j_s

    for (i_m,j_m,i_s,j_s) in zip(list_i_m, list_j_m, list_i_s, list_j_s):
        id_s = list_id[p_s]
        id_m = list_id[p_m]

        id_s[i_s,j_s] = id_m[i_m,j_m]
#        print ">> ",i_m, j_m, id_m[i_m,j_m]

#    print id_s

    return list_id

def updateDuplicated(n_m, n_s, list_id, p_m, f_m, p_s, f_s, s_m=0, s_s=0):
    dim = len(n_m)
    if dim == 1:
        return updateDuplicated_1D(n_m, n_s, list_id, p_m, f_m, p_s, f_s, s_m=s_m, s_s=s_s)
    if dim == 2:
        return updateDuplicated_2D(n_m, n_s, list_id, p_m, f_m, p_s, f_s, s_m=s_m, s_s=s_s)
# ...

# ...
def computeLocalID(list_n, DirFaces, DuplicatedFaces, DuplicataFaces):
    dim       = len(list_n[0])
    npatchs   = len(list_n)
    AllFaces  = list(range(0,2 * dim))
    AllPatchs = list(range(0,npatchs))

    BasePatchs = [0]
    DuplicatedPatchs = list(np.unique(np.array([data[0] for data in DuplicatedFaces])))
    DuplicataPatchs = list(np.unique(np.array([data[0] for data in DuplicataFaces])))

    base = 0
    list_id = []
    for i in range(0, npatchs):
        list_id.append([])
    for patch_id,faces in enumerate(DirFaces):
        _faces = [f for f in faces]
        # ... mettre a jour faces, en rajoutant les faces dupliquees
        if patch_id in DuplicataPatchs:
            list_faces = [f for f in AllFaces if f not in faces]
            for f in list_faces:
                if isDuplicata(patch_id, f, DuplicataFaces):
                    _faces.append(f)

        id, base = initLocalID(_faces, list_n[patch_id], base)
        list_id[patch_id] = id

#    print "-------------- INIT  ------------------"
#    for i,id in enumerate(list_id):
#        print "...... patch id : ", i, " ......"
#        print_id(id)
#
#    print " DuplicatedFaces ", DuplicatedFaces
#    print " DuplicataFaces ", DuplicataFaces

    for data_m, data_s in zip(DuplicatedFaces, DuplicataFaces):
        p_m = data_m[0]   ; f_m = data_m[1]
        try:
            s_m = data_m[2]
        except:
            s_m = 0
        p_s = data_s[0]   ; f_s = data_s[1]
        try:
            s_s = data_s[2]
        except:
            s_s = 0
        n_m = list_n[p_m] ; n_s = list_n[p_s]
        list_id = updateDuplicated(n_m, n_s, list_id \
                                   , p_m, f_m \
                                   , p_s, f_s \
                                   , s_m=s_m, s_s=s_s)

    return list_id
# ...

# ...
def computeGlobalID(list_id):
    ID = []
    for id in list_id:
        ID += list(id.transpose().reshape(id.size))
    return ID
# ...



def init_ID_object_uniform_1d(n, p):
    IEN = - (p-1) * np.ones((n, p+1), dtype=np.int)
    for elmt in range(0, n):
        IEN[elmt, :] += np.asarray(range(elmt, elmt+p+1))
    print IEN
    for elmt in range(0, p):
        IEN[elmt, 0:(p-elmt)] = IEN[-elmt-1, elmt+1:p+1]
    return IEN
# ...

# ... construct ID_object_uniform matrix in 2D
def init_ID_object_uniform_2d(list_n, list_p):
    IEN_u = init_ID_object_uniform_1d(list_n[0], list_p[0])
    IEN_v = init_ID_object_uniform_1d(list_n[1], list_p[1])
    print "IEN_u"
    print IEN_u
    print "IEN_v"
    print IEN_v

    n_u = list_n[0]
    n_v = list_n[1]
    p_u = list_p[0]
    p_v = list_p[1]
    n_elements = n_u * n_v
    n_non_vanishing_basis = (p_u+1) * (p_v+1)

    IEN = np.zeros((n_elements, n_non_vanishing_basis), dtype=np.int)

    elmt = 0
    for elmt_u in range(0, n_u):
        for elmt_v in range(0, n_v):
            ind = 0
            for ind_v in range(0, p_v+1):
                for ind_u in range(0, p_u+1):
                    i_u = IEN_u[elmt_u, ind_u]
                    i_v = IEN_v[elmt_v, ind_v]
                    print i_u, i_v
                    IEN[elmt, ind] = i_u + (i_v-1) * n_u

                    ind += 1
            elmt += 1
    return IEN
# ...

class ID_object_uniform:
    def __init__(self, list_n, list_p):
        self._ID_extended = None
        self._degrees = list_p
        self._shape   = list_n

        self.initialize()

    @property
    def degrees(self):
        return self._degrees

    @property
    def shape(self):
        return self._shape

    @property
    def dim(self):
        return len(self.shape)

    @property
    def ID_extended(self):
        return self._ID_extended

    def initialize(self):
        shape_total = np.asarray(self.shape) + 2 * np.asarray(self.degrees)
        self._ID_extended = np.zeros(tuple(shape_total), dtype=np.int)

class ID_object_uniform_1d(ID_object_uniform):
    def __init__(self, n, p):
        ID_object_uniform.__init__(self, [n], [p])
        self.initialize_ID()

    @property
    def n(self):
        return self.shape[0]

    @property
    def p(self):
        return self.degrees[0]

    @property
    def ID(self):
        return [self._ID_extended[self.p:]]

    @property
    def local_ID(self):
        return [self._ID_extended[self.p:]]

    def initialize_ID(self):
        self._ID_extended[self.p:-self.p] = range(1, self.n+1)
        self._ID_extended[:self.p] = self.ID[0][-self.p:]
        self._ID_extended[-self.p:] = self.ID[0][:self.p]

class ID_object_uniform_2d(ID_object_uniform):
    def __init__(self, list_n, list_p):
        ID_object_uniform.__init__(self, list_n, list_p)
        self.initialize_ID()

    @property
    def n_u(self):
        return self.shape[0]

    @property
    def n_v(self):
        return self.shape[1]

    @property
    def p_u(self):
        return self.degrees[0]

    @property
    def p_v(self):
        return self.degrees[1]

    @property
    def local_ID(self):
        return [self._ID_extended[self.p_u:, self.p_v:]]

    @property
    def ID(self):
        ID = []
        for id in self.local_ID:
            ID += list(id.transpose().reshape(id.size))
        return ID


    def initialize_ID(self):
        con_1d = ID_object_uniform_1d(self.n_u, self.p_u)
        ID_extended_1d = con_1d.ID_extended

        for j in range(self.p_v, self.n_v + self.p_v):
            self._ID_extended[:, j] = (j - self.p_v) * self.n_u + ID_extended_1d

        self._ID_extended[:, :self.p_v] = self.ID_extended[:, -2*self.p_v:-self.p_v]
        self._ID_extended[:, -self.p_v:] = self.ID_extended[:, self.p_v:2*self.p_v]

if __name__ == '__main__':
    if True:
        from time import time

        t_start = time()

        PRINT = True
    #    PRINT = False

    ##    list_n = [[4]]*3
    #    list_n = [[1024]]*3
    #    DirFaces = [[0],[],[1]]
    #    DuplicatedFaces = [[0,1],[1,1]]
    #    DuplicataFaces  = [[1,0],[2,0]]

        list_n = [[3,3]]*4
    #    list_n = [[1024,1024]]*4

        DirFaces = [[1,2],[2,3],[0,3],[0,1]]
        DuplicatedFaces = [[0,3],[1,0],[2,1],[0,0]]
        DuplicataFaces  = [[1,1],[2,2],[3,3],[3,2]]

        list_id = computeLocalID(list_n, DirFaces, DuplicatedFaces, DuplicataFaces)
        ID = computeGlobalID(list_id)

        if PRINT :
            print("--------------  FINAL ------------------")
            for i,id in enumerate(list_id):
                print("...... patch id : ", i, " ......")
                print_id(id)
            print("--------------  ID ------------------")
            print(ID)

        t_end = time()
        print("Elapsed time ", t_end - t_start)





        # ... number of elemens
        n = 4

        # ... k is the b-spline order
        k = 3

        con_1d = ID_object_uniform_1d(n, k-1)
        print con_1d.ID[0].shape
    #    print con_1d.ID_extended
        print con_1d.ID

        con_2d = ID_object_uniform_2d([n, n], [k-1, k-1])
    #    con_2d = ID_object_uniform_2d([n, n+1], [k-1, k])
        print con_2d.ID[0].shape
    #    print con_2d.ID_extended.transpose()[::-1, :]
        print con_2d.local_ID[0].transpose()[::-1, :]
        print con_2d.ID

