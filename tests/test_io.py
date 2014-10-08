# -*- coding: UTF-8 -*-
import numpy as np
import caid.cad_geometry  as cg
from caid.cad_geometry import line, square, cad_geometry
from caid.utils.extraction import BezierExtraction
import matplotlib.pyplot as plt
#from caid.utils.extraction import splineRefMat
#
#DIM_1D = 1
#DIM_2D = 2
#
## ...
#spl = splineRefMat(DIM_1D)
#nx = 3
#px = 3
#geo = line(n=[nx], p=[px])
#
#nrb     = geo[0]
#print "== shape before ", nrb.shape
#print nrb.knots
#axis = 0
#brk, mult = nrb.breaks(axis=axis, mults=True)
#nbrk = len(mult)
#mult = np.asarray(mult)
#times = nrb.degree[axis] * np.ones(nbrk, dtype=np.int) - mult
#
#list_r = []
#for t,k in zip(brk, times):
#    for i in range(0, k):
#        list_r.append(t)
#
#knots   = nrb.knots[0]
#n       = nrb.shape[0]
#p       = nrb.degree[0]
#P       = nrb.points
#dim     = P.shape[1]
#
#M = spl.construct(list_r, p, n, knots)
#print "matrix shape ", M.shape
#R = M.dot(nrb.points[:,0])
#
#geo.refine(id=0, list_t=[list_r])
#nrb     = geo[0]
#print "== shape after ", nrb.shape
#print nrb.knots
#
#P = np.asarray(nrb.points[:,0])
#assert(np.allclose(P,R))
#print "test1D1: OK"
## ...

print "====== test 1  ====="
nx = 3
px = 3
geo = line(n=[nx], p=[px])
nrb = geo[0]
extractor = BezierExtraction(nrb, check=True, verbose=True)
nrb_ref = extractor.nrb_ref
matrices = extractor.matrices
M = matrices[0]
print M.shape
geo.local_matrices()
print "//////////////////////////"
print "//////////////////////////"
print "//////////////////////////"
print "//////////////////////////"
print "//////////////////////////"
print "//////////////////////////"
geo_ref = cad_geometry()
geo_ref.append(nrb_ref)
geo_ref.local_matrices()

#print len(lmatrices)
#print "******"
#for M in lmatrices:
#    print M.shape

#print "====== test 2  ====="
#nx = 3 ; ny = 2
#px = 2 ; py = 3
#geo = square(n=[nx,ny], p=[px,py])
#nrb = geo[0]
#extractor = BezierExtraction(nrb, check=True, verbose=True)
#matrices = extractor.matrices
#M0 = matrices[0]
#M1 = matrices[1]
#print M0.shape, M1.shape
#lmatrices = extractor.local_matrices()
#print len(lmatrices)
#print "******"
#for M0M1 in lmatrices:
#    M0 = M0M1[0] ; M1 = M0M1[1]
#    print M0.shape, M1.shape
#
#
