import numpy as np
from numpy import array, asarray, pi, sin, cos
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

nm = 2
ni = 6

radius = 1.
angle = pi / 3.

center = array([0,0])
centers = [center]

points = []

def create_points(X, pts):
    for m in range(1, nm):
        for i in range(0, ni):
            P = m * radius * array([cos(i*angle)-X[0], sin(i*angle)-X[1]])
            pts.append(P)
    return pts

centers = create_points(center, centers)
for X in centers:
    points = create_points(X, points)

points = array(points)
tri = Delaunay(points)

barycenters = []
for T in tri.simplices:
    pts = points[T]
    A = array(pts[0,:]) ; B = array(pts[1,:]) ; C = array(pts[2,:])
    b = (A+B+C) / 3.
    barycenters.append(b)

barycenters = array(barycenters)

tri_b = Delaunay(barycenters)

plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
plt.plot(points[:,0], points[:,1], 'or')
plt.plot(barycenters[:,0], barycenters[:,1], 'ob')

xmin = points[:,0].min()  ;   xmax = points[:,0].max()
ymin = points[:,1].min()  ;   ymax = points[:,1].max()

plt.xlim([xmin-0.2, xmax+0.2])
plt.ylim([ymin-0.2, ymax+0.2])
plt.show()
