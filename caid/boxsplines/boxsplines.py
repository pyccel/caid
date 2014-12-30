import numpy as np
from numpy import *
from scipy.special import binom
from math import factorial
import pylab as pl

def mceil(n) :
    val = int(n)
    if (val >= n) :
        return val
    return val+1

def boxspline(x,y,n):
    x = -abs(x); y = abs(y);
    u=x-y/sqrt(3); v=x+y/sqrt(3);
    ind = where(v>0);
    v[ind] = -v[ind];
    u[ind]=u[ind]+v[ind];
    ind = where(v>u/2); v[ind]=u[ind]-v[ind];
    val=np.zeros(np.shape(x));
    for K in range(-n,mceil(u.max())):
        for L in range(-n,mceil(v.max())) :
            for i in range(0,min(n+K, n+L)+1):
                coeff=(-1.)**(K+L+i)*binom(n,i-K)*binom(n,i-L)*binom(n,i);
                for d in range (0,n) :
                    aux=abs(v-L-u+K);
                    aux2=(u-K+v-L-aux)/2;
                    aux2[where(aux2<0)]=0;
                    auxis  = aux**(n-1-d)*aux2**(2*n-1+d);
                    factos = factorial(2*n-1+d)*factorial(n-1-d)
                    val = val + coeff*binom(n-1+d,d)/factos*auxis

    return val


# a = -1
# b =  1
# n1 = 51#b - a + 1
# n2 = 51#b - a + 1

# r1 = [0.5, -sqrt(3)/2.]
# r2 = [0.5,  sqrt(3)/2.]
# R  = np.zeros((2,2))
# R[:,0] = r1
# R[:,1] = r2

# k1 = linspace(a,b,n1)
# k2 = linspace(a,b,n2)

# X = np.zeros((n1,n2))
# Y = np.zeros((n1,n2))

# for i in range(n1) :
#     for j in range(n2) :
#         k = [k1[i], k2[j]]
#         [X[i,j], Y[i,j]] = dot(R,k)


# pl.clf()
# Xi1 = boxspline(X,Y,1)
# pl.contourf(X, Y, Xi1)
# pl.colorbar()
# pl.scatter(X,Y,marker='.')
# pl.axis('equal')
# pl.title("chi1 with arbitrary degree algo")
# pl.show(block=True)


# pl.clf()
# Xi2 = boxspline(X,Y,2)
# pl.contourf(X, Y, Xi2)
# pl.colorbar()
# pl.scatter(X,Y,marker='.')
# pl.axis('equal')
# pl.title("chi2 with arbitrary degree algo")
# pl.show(block=True)


# pl.clf()
# Xi2 = boxspline_gen(X,Y,2,r1,r2)
# pl.contourf(X, Y, Xi2)
# pl.colorbar()
# pl.scatter(X,Y,marker='.')
# pl.axis('equal')
# pl.title("chi2 with arbitrary degrre and general hex mesh")
# pl.show(block=True)


# r1 = [ sqrt(3)/2., 0.5 ]
# r2 = [-sqrt(3)/2., 0.5 ]

# R[:,0] = r1
# R[:,1] = r2

# for i in range(n1) :
#     for j in range(n2) :
#         k = [k1[i], k2[j]]
#         [X[i,j], Y[i,j]] = dot(R,k)


# pl.clf()
# Xi2 = boxspline2(X,Y,r1,r2)
# pl.contourf(X, Y, Xi2)
# pl.colorbar()
# pl.scatter(X,Y,marker='.')
# pl.axis('equal')
# pl.title("chi2 algorithm")
# pl.show(block=True)


# *********
# Scaled mesh
# here

a = -2.5
b = 2.5
radius = b
n1 = 51#b - a + 1
n2 = 51#b - a + 1
inf = (n1-1)/2
k1 = linspace(-inf,inf,n1)
k2 = linspace(-inf,inf,n2)
X = np.zeros((n1,n2))
Y = np.zeros((n1,n2))


r1 = np.asarray([ sqrt(3)/2., 0.5 ])
r2 = np.asarray([-sqrt(3)/2., 0.5 ])
R  = np.zeros((2,2))
R[:,0] = r1
R[:,1] = r2

R = R*radius/(n1-1.)*2.

for i in range(n1) :
    for j in range(n1) :
        k = [k1[i], k2[j]]
        [X[i,j], Y[i,j]] = dot(R,k)

pl.clf()
Xi1 = boxspline(X,Y,3)

#
from scipy.spatial import Delaunay
import matplotlib.tri as mtri
print X.shape
print X.size
points = np.zeros((X.size, 2))
points[:,0] = X.reshape(X.size)
points[:,1] = Y.reshape(Y.size)
tess = Delaunay(points)
tri = tess.vertices # or tess.simplices depending on scipy version
triang = mtri.Triangulation(x=points[:, 0], y=points[:, 1], triangles=tri)
#

pl.contourf(X, Y, Xi1)
pl.colorbar()
#pl.scatter(X,Y,marker='-')
pl.triplot(triang, lw=0.5, color='white')
pl.axis('equal')
pl.title("SCALED MESH : chi1 with arbitrary degree and general hex mesh")
pl.show(block=True)

#****************++

# Xi1 = boxspline(X,Y,1)



# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cm
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
# import matplotlib.pyplot as plt
# import numpy as np

# fig = plt.figure()
# ax = fig.gca(projection='3d')
# surf = ax.plot_surface(X, Y, Xi1, rstride=1, cstride=1, cmap=cm.coolwarm,
#         linewidth=0, antialiased=False)
# ax.set_aspect('equal')

# fig.colorbar(surf, shrink=0.5, aspect=5)
# plt.title("chi1")
# plt.show(block=True)


# pl.contourf(X, Y, Xi1)
# pl.scatter(X,Y,marker='.')

#pl.show(block=True)

# pl.clf()
# Xi2 = boxspline(X,Y,2)
# pl.contourf(X, Y, Xi2)
# pl.scatter(X,Y,marker='.')
# pl.show(block=True)

# pl.show(block=True)
# Xi4 = boxspline(X,Y,4)
# pl.contourf(X, Y, Xi4)
# pl.scatter(X,Y,marker='.')
# pl.show(block=True)
# Xi10 = boxspline(X,Y,4)
# pl.contourf(X, Y, Xi10)
# pl.scatter(X,Y,marker='.')
# pl.show(block=True)



# xc   =  0.
# yc   =  0.
# sig  =  0.5
# maxval = 1.
# func_init = lambda x,y : maxval * np.exp(-0.5 * ((x-xc)**2 / sig**2
#                                                + (y-yc)**2 / sig**2))
# Zinit = func_init(X,Y)
# Z = func_init(X,Y)

# advec = 0.1
# nstep = 3
# dt = 0.1

# sommets1 = []
# sommets2 = []

# indx = np.where(Z == Z.max())[0][0]
# indy = np.where(Z == Z.max())[1][0]
# sommets1.append(X[indx,indy])
# sommets2.append(Y[indx,indy])


# pl.clf()
# pl.contourf(X, Y, Zinit)
# pl.plot(sommets1, sommets2, 'w+')
# pl.show(block=True)

# for tstep in range(nstep) :

#     Xnp1 = X - advec*tstep*dt
#     Ynp1 = Y - advec*tstep*dt

#     for j in range(n2) :
#         print "j = ", j
#         for i in range(n1) :
#             Z[i,j] = 0.
#             Chi = boxspline(Xnp1[i,j]-X, Ynp1[i,j]-Y, 4)
#             Chi2 = boxspline2(Xnp1[i,j]-X, Ynp1[i,j]-Y)
#             for k in range(n2) :
#                 for l in range(n1) :
#                     Z[i,j] = Z[i,j] + Zinit[k,l]*Chi[k,l]

#     # print (Zinit == Z)
#     Zinit = np.copy(Z)

#     indx = np.where(Z == Z.max())[0][0]
#     indy = np.where(Z == Z.max())[1][0]
#     sommets1.append(X[indx,indy])
#     sommets2.append(Y[indx,indy])


# pl.clf()
# pl.contourf(X, Y, Z)
# pl.plot(sommets1, sommets2, 'w+')
# pl.show(block=True)

# pl.clf()

# #pl.scatter(X,Y)
# #pl.scatter(Y,X)

# pl.contourf(X, Y, Z)
# pl.show(block=True)

