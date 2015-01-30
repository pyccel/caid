# -*- coding: UTF-8 -*-
#! /usr/bin/python

__author__ = "ratnani"
__date__ = "$Dec 20, 2011 3:56:49 PM$"
__all__ = ['connectivity']

import numpy as np
array = np.array
class connectivity:
    def __init__(self, geometry, ai_ndof=1):

        self._geo = geometry
        self._boundary_condition = None

        # computing the number of patchs
        self._npatch = geometry.npatchs

        # for each patch, we copy n,p, nel, nen
        self.list_n = []
        self.list_p = []
        self.list_nel = []
        self.list_nen = []
        self.list_nnp = []
        self.list_elt_st = [] # the left-index of the element, per direction
        for li_id in range(0, self.npatch):
            nrb = geometry[li_id]
            li_dim = nrb.dim

            self.list_n.append(nrb.shape)
            self.list_p.append(nrb.degree)

            list_info_knots = self.list_info_knots(nrb)

            # calcul des nen
            li_nen = 1
            for li_d in range(0, li_dim):
                li_nen *= nrb.degree[li_d] + 1
            self.list_nen.append(li_nen)

            # indexation des elements
            li_nel = 1
            for li_d in range(0, li_dim):
                # we test if the knot vector is periodic
                li_n = nrb.shape[li_d]
                li_p = nrb.degree[li_d]
                if len(list_info_knots[li_d][0]) == li_n + li_p + 1:
                    li_nel *= li_n - li_p
                else :
                    li_nel *= list_info_knots[li_d][0].__len__() - 1
            self.list_nel.append(li_nel)

            # calcul des nnp
            li_nnp = 1
            for li_d in range(0, li_dim):
                # we test if the knot vector is periodic
                li_n = nrb.shape[li_d]
                li_p = nrb.degree[li_d]
                if len(list_info_knots[li_d][0]) == li_n + li_p + 1:
                    li_nnp *= li_n
                else:
                    li_nnp *= nrb.shape[li_d]
            self.list_nnp.append(li_nnp)

            # compute list_elt_st
            list_elt_st = []
            for li_d in range(0, li_dim):
                list_elt_st.append(list_info_knots[li_d][2][0:-1])
            self.list_elt_st.append(list_elt_st)

        self.ndof = ai_ndof

        self.nnp = sum (self.list_nnp)
        self.size = 0
        self.maxnel = 0
        self.maxnen = 0

        self.baseID = [] # this is the length of ID for each patch

        self.ID  = []
        self.IEN = []
        self.LM  = []
        self.ID_loc  = [[]]*self.npatch

        self.list_Elt_Index = []

        self.init_ELT()

    @property
    def geometry(self):
        return self._geo

    @property
    def npatch(self):
        return self._npatch

    @property
    def dim(self):
        return self._geo.dim

    @property
    def boundary_condition(self):
        return self._boundary_condition

    def init_ELT_1d(self):
        geometry = self.geometry
        dim = self.dim
        for li_id in range(0, self.npatch):
            nrb = geometry[li_id]
            list_info_knots = self.list_info_knots(nrb)

            list_Elt_Index = []
            # acces a l 'indice du noeud
            for i in list_info_knots[0][2]:
                list_Elt_Index.append([i])

            self.list_Elt_Index.append(list_Elt_Index)

    def init_ELT_2d(self):
        geometry = self.geometry
        dim = self.dim
        for li_id in range(0, self.npatch):
            nrb = geometry[li_id]
            list_info_knots = self.list_info_knots(nrb)

            list_Elt_Index = []
            # acces a l 'indice du noeud
            for j in list_info_knots[1][2]:
                for i in list_info_knots[0][2]:
                    list_Elt_Index.append([i, j])

            self.list_Elt_Index.append(list_Elt_Index)

    def init_ELT_3d(self):
        geometry = self.geometry
        dim = self.dim
        for li_id in range(0, self.npatch):
            nrb = geometry[li_id]
            list_info_knots = self.list_info_knots(nrb)

            list_Elt_Index = []
            # acces a l 'indice du noeud
            for k in list_info_knots[2][2]:
                for j in list_info_knots[1][2]:
                    for i in list_info_knots[0][2]:
                        list_Elt_Index.append([i, j, k])

            self.list_Elt_Index.append(list_Elt_Index)

    def init_ELT(self):
        geometry = self.geometry
        dim = self.dim
        if dim == 1:
            self.init_ELT_1d()
        if dim == 2:
            self.init_ELT_2d()
        if dim == 3:
            self.init_ELT_3d()

    def init_data_structure_1d(self):
        geometry = self.geometry
        dim = self.dim
        bound_cond = self.boundary_condition
        for li_id in range(0, self.npatch):

            lpi_Elt_Index = self.list_Elt_Index[li_id]
            li_nen = self.list_nen[li_id]
            li_nel = self.list_nel[li_id]
            lpi_N = self.list_n[li_id]
            lpi_P = self.list_p[li_id]

            _list_elt_st = self.list_elt_st[li_id]
            list_elt_st = [ [i for i in _list_elt_st[0] if lpi_P[0]+1<=i and i<=lpi_N[0]]]

            list_IEN  = np.zeros((li_nen, li_nel), dtype=np.int)

            li_baseA = 0
            li_baseB = 0

            for li_dof in range(0, self.ndof):
                li_e = 0
                for li_i in list_elt_st[0]:

                    # A starts from 1
                    li_A = li_i
                    li_A = li_A + li_baseA
                    for li_iloc in range(0, lpi_P[0] + 1):

                        li_B = li_A -(lpi_P[0] - li_iloc)
                        li_Bloc = li_iloc
                        li_Bloc = li_Bloc + li_baseB

                        # as A starts from 1, we must deduce 1
                        list_IEN[li_Bloc, li_e] = ( li_B - 1 )

                    li_e += 1

                li_baseA = li_baseA + li_A
                li_baseB = li_baseB + li_nen

            self.IEN.append(list_IEN)

    def init_data_structure_2d(self):
        geometry = self.geometry
        dim = self.dim
        bound_cond = self.boundary_condition
        for li_id in range(0, self.npatch):

            lpi_Elt_Index = self.list_Elt_Index[li_id]
            li_nen = self.list_nen[li_id]
            li_nel = self.list_nel[li_id]
            lpi_N = self.list_n[li_id]
            lpi_P = self.list_p[li_id]

            _list_elt_st = self.list_elt_st[li_id]
#            print "list_elt_st ", _list_elt_st
            list_elt_st = [ [i for i in _list_elt_st[0] if lpi_P[0]+1<=i and i<=lpi_N[0]] \
                           , [i for i in _list_elt_st[1] if lpi_P[1]+1<=i and i<=lpi_N[1]]]

#            print "li_nel=", li_nel
            import numpy as np
            list_IEN  = np.zeros((li_nen, li_nel), dtype=np.int)

            li_baseA = 0
            li_baseB = 0

            for li_dof in range(0, self.ndof):
                li_e = 0
#                print "list_elt_st[0] = ", list_elt_st[0]
#                print "list_elt_st[1] = ", list_elt_st[1]
                for li_j in list_elt_st[1]:
                    for li_i in list_elt_st[0]:
#                        print "li_i,li_j=", li_i,li_j
                        # A starts from 1
                        li_A = (li_j - 1) * lpi_N[0] + li_i
                        li_A = li_A + li_baseA

                        for li_jloc in range(0, lpi_P[1] + 1):

                            for li_iloc in range(0, lpi_P[0] + 1):

                                li_B = li_A - (lpi_P[1] - li_jloc) * lpi_N[0] -(lpi_P[0] - li_iloc)
                                li_Bloc = li_jloc * (lpi_P[0] + 1) + li_iloc
                                li_Bloc = li_Bloc + li_baseB

                                # as A starts from 1, we must deduce 1
                                list_IEN[li_Bloc, li_e] = li_B - 1

#                        print "list_IEN=", list_IEN[:,li_e]
                        li_e += 1

                li_baseA = li_baseA + li_A
                li_baseB = li_baseB + li_nen

            self.IEN.append(list_IEN)
#        print "list_IEN.shape=", list_IEN.shape

    def init_data_structure_3d(self):
        geometry = self.geometry
        dim = self.dim
        bound_cond = self.boundary_condition
        for li_id in range(0, self.npatch):

            lpi_Elt_Index = self.list_Elt_Index[li_id]
            li_nen = self.list_nen[li_id]
            li_nel = self.list_nel[li_id]
            lpi_N = self.list_n[li_id]
            lpi_P = self.list_p[li_id]

            list_elt_st = self.list_elt_st
            list_elt_st[0] = [i for i in self.list_elt_st[0] if lpi_P[0]+1<=i and i<=lpi_N[0]]
            list_elt_st[1] = [i for i in self.list_elt_st[1] if lpi_P[1]+1<=i and i<=lpi_N[1]]
            list_elt_st[2] = [i for i in self.list_elt_st[2] if lpi_P[2]+1<=i and i<=lpi_N[2]]

            list_IEN  = np.zeros((li_nen, li_nel), dtype=np.int)

            li_baseA = 0 ;li_baseB = 0

            for li_dof in range(0, self.ndof):
                li_e = 0
                for li_k in list_elt_st[2]:
                    for li_j in list_elt_st[1]:
                        for li_i in list_elt_st[0]:

                            # A starts from 1
                            li_A = (li_k - 1) * lpi_N[1] * lpi_N[0] \
                            + (li_j - 1) * lpi_N[0] \
                            + li_i
                            li_A = li_A + li_baseA

                            for li_kloc in range(0, lpi_P[2] + 1):
                                for li_jloc in range(0, lpi_P[1] + 1):
                                    for li_iloc in range(0, lpi_P[0] + 1):

                                        li_B = li_A     \
                                        - (lpi_P[2] - li_kloc) * lpi_N[1] * lpi_N[0] \
                                        - (lpi_P[1] - li_jloc) * lpi_N[0] \
                                        - (lpi_P[0] - li_iloc)

                                        li_Bloc = li_kloc * (lpi_P[1] + 1) * (lpi_P[0] + 1)  \
                                        + li_jloc * (lpi_P[0] + 1) + li_iloc

                                        li_Bloc += li_baseB

                                        # as A starts from 1, we must deduce 1
                                        list_IEN[li_Bloc, li_e] = li_B - 1

                            li_e += 1

                li_baseA = li_baseA + li_A
                li_baseB = li_baseB + li_nen

            self.IEN.append(list_IEN)

    def init_data_structure(self, bound_cond=None):
        geometry = self.geometry
        dim = self.dim
        if bound_cond is None:
            from . import boundary_conditions as bc
            bound_cond = bc.boundary_conditions(geometry)
        self._boundary_condition = bound_cond
        if dim == 1:
            self.init_data_structure_1d()
        if dim == 2:
            self.init_data_structure_2d()
        if dim == 3:
            self.init_data_structure_3d()

        # INITIALIIZING THE ID ARRAY
        self.init_ID(bound_cond)

        # INITIALIIZING THE LOCATION MATRIX LM ARRAY
        self.init_LM()

    def init_ID(self, bound_cond):
        list_n = self.list_n
#        print " list_n ", list_n

        DirFaces = bound_cond.DirFaces
        DuplicatedFaces = bound_cond.DuplicatedFaces
        DuplicataFaces = bound_cond.DuplicataFaces

#        print " DirFaces ", DirFaces
#        print " DuplicatedFaces  ", DuplicatedFaces
#        print " DuplicataFaces ", DuplicataFaces

        from .idutils import computeLocalID, computeGlobalID
        list_id = computeLocalID(list_n, DirFaces, DuplicatedFaces, DuplicataFaces)
        ID = computeGlobalID(list_id)

        self.ID_loc = list_id
        self.ID = array(ID)

        self.size = max(self.ID)

    def init_LM(self):
#        print "self.baseID=", self.baseID
        import numpy as np
        for li_id in range(0, self.npatch):
            size = self.ID_loc[li_id].size
            ID_loc = list(self.ID_loc[li_id].transpose().reshape(size))
#            print "li_id = ", li_id
#            print "self.ID=", self.ID
#            print "self.IEN[li_id]=", self.IEN[li_id]
#            list_LM = li_maxLM + np.asarray(self.ID[self.IEN[li_id][:,:]])
#            print "self.baseID = ", self.baseID
#            li_baseID = self.baseID[li_id]
#            print "li_baseID = ", li_baseID
            list_LM = []
            lpr_IEN = np.asarray(self.IEN[li_id]).transpose()
            for P in lpr_IEN:
                Q = []
#                print "P = ", P
                for t in P:
#                    print "t, ID_loc[t]=", t, ID_loc[t]
                    Q.append(ID_loc[t])
                list_LM.append(Q)

#            lpi_shape = np.asarray(self.IEN).shape
#            list_maxLM = np.ones(lpi_shape, dtype=np.int)
#            print "li_maxLM = ", li_maxLM
#            list_maxLM *= li_maxLM
#            list_IEN = ( list_maxLM + np.asarray(self.IEN[li_id]).tolist())
#            print "list_maxLM =", list_maxLM
#            list_LM = self.ID[list_IEN]

#            print "list_LM=", list_LM
            self.LM.append(np.asarray(list_LM).transpose())
#        print "self.LM=", self.LM

    def printinfo(self, with_IEN=True, with_LM=True, with_ID=True):
        print("*******************************")
        print(" global informations ")
        print("*******************************")
        print(" number of patchs :", self.npatch)
        print(" nnp :", self.nnp)
        print("*******************************")
        if (with_IEN or with_LM):
            for li_id in range(0, self.npatch):
                print("*******************************")
                print(" Current Patch-id =", li_id)
                li_nel = self.list_nel[li_id]
                li_nen = self.list_nen[li_id]
                li_nnp = self.list_nnp[li_id]
                print("-- nel =", li_nel)
                print("-- nen =", li_nen)
                print("-- nnp =", li_nnp)
                print("*******************************")

                if with_IEN:
                    print("======")
                    print(" IEN ")
                    print("======")
                    for li_e in range(0, li_nel):
                        print("     elt =", li_e)
                        print("          ", self.IEN[li_id][:, li_e])
                    print("======")

                if with_LM:
                    print("======")
                    print(" LM ")
                    print("======")
                    for li_e in range(0, li_nel):
                        print("     elt =", li_e)
                        print("          ", self.LM[li_id][:, li_e])
                    print("======")

                print("*******************************")

        if with_ID:
            print("===============================")
            print(" ID ")
            print("===============================")
            print(" ", self.ID[:])
            print("===============================")

    def save(self, etiq="", fmt='zip', name=None):
        """
        name needed for zip format
        """
        # ...
        def exportTXT(etiq):
            np.savetxt(etiq+"ID.txt"\
                       ,np.asarray(self.ID)\
                      , fmt='%d')
            for li_id in range(0, self.npatch):
                li_nel = self.list_nel[li_id]
                li_nen = self.list_nen[li_id]
                li_nnp = self.list_nnp[li_id]
                np.savetxt(etiq+"IEN_"+str(li_id)+".txt"\
                           ,np.asarray(self.IEN[li_id][:, :])\
                          , fmt='%d')
                np.savetxt(etiq+"LM_"+str(li_id)+".txt"\
                           ,np.asarray(self.LM[li_id][:, :])\
                          , fmt='%d')
        # ...

        # ...
        if fmt == "txt":
            exportTXT(etiq)
        # ...

        # ...
        if (fmt == "zip") and (name is not None):
            import os
            from contextlib import closing
            from zipfile import ZipFile, ZIP_DEFLATED

            # ...
            def zipdir(basedir, archivename):
                assert os.path.isdir(basedir)
                with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
                    for root, dirs, files in os.walk(basedir):
                        #NOTE: ignore empty directories
                        for fn in files:
                            absfn = os.path.join(root, fn)
                            zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                            z.write(absfn, zfn)
            # ...

            os.system("mkdir -p " + name)
            etiq = name+"/"
            exportTXT(etiq=etiq)
            basedir = name
            archivename = name+".zip"
            zipdir(basedir, archivename)
            os.system("rm -R " + name)
        # ...



    def list_info_knots(self, nrb):
        # contient la multiplicite de chaque noeud,
        # et l'indice du dernier noeud duplique, selon chaque direction
        from itertools import groupby
        li_dim = nrb.dim
        list_info = []
        for li_d in range(0, li_dim):
            lpr_knots = nrb.knots[li_d]
            u = [k for k, g in groupby(lpr_knots)]
            m = [len(list(g)) for k, g in groupby(lpr_knots)]
            index = [sum(m[0:i+1]) for i in range(0,m.__len__())]
            list_info.append((u,m,index))
        return list_info


if __name__ == '__main__':

    import caid.cad_geometry  as cg
    from caid.cad_geometry import line, square, trilinear
    from .boundary_conditions import boundary_conditions

    geo1d = line(n=[5], p=[3])

    # ...
    print ("========= connectivity on a line =========")
    con1d = connectivity(geo1d)
    con1d.init_data_structure()
    con1d.printinfo()
    print ("==========================================")
    # ...

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
    print ("========= periodic connectivity on a line =========")
    con1d_per = connectivity(geo1d)
    bc1d_per = boundary_conditions(geo1d)
    faces_base = [[0,0,0]]
    faces      = [[0,1,0]]
    bc1d_per.duplicate(geo1d, faces_base, faces, shift_base=None, shift=None)
    con1d_per.init_data_structure(bc1d_per)
    con1d_per.printinfo()
    print ("==========================================")
    # ...

    # ...
    print ("========= full periodic connectivity on a line =========")
    con1d_per = connectivity(geo1d)
    bc1d_per = boundary_conditions(geo1d)
#    # p = 2
#    faces_base = [[0,0,0],[0,0,1]]
#    faces      = [[0,1,-1],[0,1,0]]
    # p = 3
    faces_base = [[0,0,0] ,[0,0,1],[0,0,2]]
    faces      = [[0,1,-2],[0,1,-1],[0,1,0]]


    bc1d_per.duplicate(geo1d, faces_base, faces)
    con1d_per.init_data_structure(bc1d_per)
    con1d_per.printinfo()
    print ("==========================================")
    # ...

    # ...
#    geo2d = square(n=[5,3], p=[2,3])
#    con2d = connectivity(geo2d)
#
#    con2d.init_data_structure()
#    con2d.printinfo()
    # ...

    # ...
#    geo3d = trilinear(n=[5,3,1], p=[2,3,4])
#    con3d = connectivity(geo3d)
#
#    con3d.init_data_structure()
#    con3d.printinfo()
    # ...

