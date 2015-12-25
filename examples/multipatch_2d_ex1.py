import numpy as np
from caid.cad_geometry import cad_geometry, square, quart_circle, circle
from matplotlib import pyplot as plt
from numpy import pi, array

# ...
def plotGeo(geo, MeshResolution=3, color='k' \
            , list_label=None \
            , list_facecolors=None):
    for patch_id in range(0, geo.npatchs):
        if list_facecolors is not None:
            facecolor = list_facecolors[patch_id]
            nrb = geo[patch_id]
            list_t = []
            for axis in range(0, nrb.dim):
                t = np.linspace(nrb.knots[axis][0],nrb.knots[axis][-1],MeshResolution)
                list_t.append(t)
            P = nrb(*list_t)
            x = P[...,0]
            y = P[...,1]
            z = np.ones_like(x)
#            plt.pcolor(x,y,z,vmin=1.,vmax=1.)
            plt.contourf(x,y,z, colors=facecolor)

        if list_label is not None:
            C = geo[patch_id].points
            xm = C[...,0].mean()
            ym = C[...,1].mean()
            txt = ("$%s$") % list_label[patch_id]
            plt.text(xm, ym, txt, fontsize=16, color=color)

#        nrb = geo[patch_id]
#        t1 = np.linspace(nrb.knots[0][0],nrb.knots[0][-1],100)
#        t2 = np.linspace(nrb.knots[1][0],nrb.knots[1][-1],100)
#
#        list_faces  = [0, 1, 2, 3]
#        list_colors = ['k']*4
##        list_colors = ['r', 'g', 'b', 'k']
#        for (face, color) in zip(list_faces, list_colors):
#            nrb_bnd = nrb.extract_face(face)
#            plot_crv(nrb_bnd, t1, t2, tangent=False, normal=False, color=color,
#                     label='Face '+str(face))
# ...


nx = 3 ; ny = 3
px = 2 ; py = 2

# ... Import the square domain
geo_1 = square(n=[nx,ny],p=[px,py])

# ... Import the square domain
geo_2 = square(n=[nx,ny],p=[px,py])
geo_2[0].translate(1.0, axis=0)

# ... Import the square domain
geo_3 = square(n=[nx,ny],p=[px,py])
geo_3[0].translate(1.0, axis=1)

# ... Import the square domain
geo_4 = square(n=[nx,ny],p=[px,py])
geo_4[0].translate(1.0, axis=0)
geo_4[0].translate(1.0, axis=1)

geo_12 = geo_1.merge(geo_2)
geo_34 = geo_3.merge(geo_4)
geo    = geo_12.merge(geo_34)

for i in range(0, geo.npatchs):
    geo[i].scale(0.5, axis=0)
    geo[i].scale(0.5, axis=1)

geo.save("square_4mp.xml")

plotGeo(geo, MeshResolution=3 \
        , list_label=["A", "B", "C", "D"] \
       , list_facecolors=["green", "pink", "white", "red"])

plt.savefig("multipatch_2d_ex1_square_4mp.png")
plt.clf()
