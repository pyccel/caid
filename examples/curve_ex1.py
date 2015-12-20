import numpy as np
from caid.cad_geometry import cad_nurbs
from matplotlib import pyplot as plt
from numpy import pi, array

# ... create a 3D curve
def make_curve():
    T = np.array([0., 0., 0., 0.5, 0.75, 0.75, 1., 1., 1.])
    C = [[ 6.0, 0.0, 6.0],
         [-5.5, 0.2, 5.5],
         [-5.0, 1.3,-5.0],
         [ 4.5, 2.,-4.5],
         [ 4.0, 2.5, 4.0],
         [-3.5, 2.75, 3.5],]

    crv = cad_nurbs([T], C)
    return crv
# ...

# ... custom plot curve
def curve_plot(crv, text="P", color="r" \
               , xmin=None, xmax=None \
               , ymin=None, ymax=None \
               , n_points=100):

    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)
    frame1.set_frame_on(False)

    if (xmin is not None) and (xmax is not None):
        plt.xlim(xmin, xmax)

    if (ymin is not None) and (ymax is not None):
        plt.ylim(ymin, ymax)

    t = np.linspace(0.0,1.0,n_points)
    C = crv.points
    P = crv(t)
    x = P[:,0]
    y = P[:,1]

    plt.plot(x,y, color)

    i = 0
    for [xc,yc,zc] in C:
        label = "$"+text+"_{%s}$" % (str(i+1))
        plt.text(xc-0.05,yc+0.05, label, fontsize=14, color="k")
        plt.plot(xc,yc, "ok")
        i += 1
    # control polygon
    plt.plot(C[...,0], C[...,1], "-.k")
# ...


# ... create a 3D curve
crv0 = make_curve()
crv1 = make_curve()
# ...

# ... refine the curve by inserting the knot 0.5
crv1.refine(0, [0.5])
# ...

# ... raising the spline degree
crv1.elevate(0,1)
# ...

# ... define the matplotlib grid
xmin = -6.5 ; xmax = 7.
ymin = -0.5 ; ymax = 3.25
# ...

curve_plot(crv0, text="P", color="b")
plt.savefig("curve_ex1_original.png")
plt.clf()

curve_plot(crv1, text="Q", color="r")
plt.savefig("curve_ex1_refined.png")
plt.clf()
