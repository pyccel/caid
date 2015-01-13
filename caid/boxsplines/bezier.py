# -*- coding: UTF-8 -*-
import numpy as np
from numpy import cos, sin, pi
import numpy.linalg as la
from scipy.spatial import Delaunay
import matplotlib.tri as mtri
import matplotlib.pyplot as plt
import scipy
from scipy.special import binom as sc_binom

# ...
targets = np.array([[.1,0.], [.9,.49], [.1,.6], [.4,.9]])
# ...

# ... pre-compute all binomial coef needed
degree = 4
allBinom = []
for d in range(0,degree+1):
    values = np.zeros(d+1)
    for i in range(0, d+1):
        values[i] = sc_binom(d,i)
    allBinom.append(values)

for d in range(0, degree+1):
    print(len(allBinom[d]))

def binom(n,i):
    return allBinom[n][i]
# ...

# ...
def barycentric_coords(vertices, point):
    T = (np.array(vertices[:-1])-vertices[-1]).T
    v = np.dot(la.inv(T), np.array(point)-vertices[-1])
    v.resize(len(vertices))
    v[-1] = 1-v.sum()
    return v
# ...

# ...
def bezier(x,y,i,j,n):
    A = np.array([x,y])
    t_id = tri.find_simplex(targets)[0]
    vertices = tri.points[tri.vertices[t_id,:]]
    c = barycentric_coords(vertices, A)
    t0 = c[0] ; t1 = c[1] ; t2 = c[2]
    k = n - j - i
    v = 1.
#    v = t0**i * t1**j * t2**k
    v *= binom(n,i)
    v *= binom(n-i,j)
    return v
# ...


# ...
n = 10
u = np.linspace(0.,1.,n)
v = np.linspace(0.,1.,n)

U,V = np.meshgrid(u,v)

u = U.reshape(U.size)
v = V.reshape(V.size)
# ...

# ...
eps = 0.1
k1 = 1. ; k2 = 1.
X = 2*(u + eps * sin(2*pi*k1*u) * sin(2*pi*k2*v)) -1.
Y = 2*(v + eps * sin(2*pi*k1*u) * sin(2*pi*k2*v)) - 1.
# ...

# ...
points = np.zeros((X.size, 2))
points[:,0] = X
points[:,1] = Y
# ...

# ... create the tesselation, triangulation
tess = Delaunay(points)
tri = tess.vertices # or tess.simplices depending on scipy version
triang = mtri.Triangulation(x=points[:, 0], y=points[:, 1], triangles=tri)
# ...

tri = tess

# ... plot
#plt.triplot(triang, lw=0.5, color='black')
#for A in targets:
#    plt.plot(A[0], A[1], "or")
#plt.axis('equal')
#plt.show()
# ...

# ...
#curT = tri.find_simplex(targets)
#for i,A in zip(curT, targets):
#    vertices = tri.points[tri.vertices[i,:]]
#    c = barycentric_coords(vertices, A)
#    print "--- " , i, " ---"
#    print c
# ...


# ...
v = bezier(targets[0,0], targets[0,1], 1, 1, degree)
print(v)
# ...

