# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from caid.quadrangles.quadrangles import Quadrangles, CubicHermiteBezier

def test_1():
    """
    A02 -- A12 -- A22
     |      |      |
    A01 -- A11 -- A21
     |      |      |
    A00 -- A10 -- A20
    """
    points = np.zeros((9,2))
    # A00
    points[0,:] = np.array([0.,0.])
    # A01
    points[1,:] = np.array([0.,.5])
    # A02
    points[2,:] = np.array([0.,1.])
    # A10
    points[3,:] = np.array([.5,0.])
    # A11
    points[4,:] = np.array([.5,.5])
    # A12
    points[5,:] = np.array([.5,1.])
    # A20
    points[6,:] = np.array([1.,0.])
    # A21
    points[7,:] = np.array([1.,.5])
    # A22
    points[8,:] = np.array([1.,1.])

    quads = [ [0,3,4,1] \
            , [3,6,7,4] \
            , [1,4,5,2] \
            , [4,7,8,5] \
            ]

    quad = Quadrangles(points[:,0],points[:,1],quads=quads)

    plt.triplot(quad.triang, '-', lw=0.75, color="red")
    plt.show()

def test_2():
#    nodes_filename    = "jorekNodes.txt"
#    elements_filename = "jorekElements.txt"

    nodes_filename    = "jorekNodes_ref.txt"
    elements_filename = "jorekElements_ref.txt"

    quadrangles = CubicHermiteBezier(nodes_filename, elements_filename)
#    quadrangles.plot()
#    plt.show()

    triang = quadrangles.triang
    for my_color, col in zip([1,2,4], ["blue", "red", "green"]):
        ll_condition = (quadrangles.colors[quadrangles.ancestors] == my_color)
        mask = np.where(ll_condition, 0, 1)

        triang.set_mask(mask)
        plt.triplot(triang, '-', lw=0.75, color=col)


    my_color = 2
    ll_condition = (quadrangles.colors[quadrangles.ancestors] == my_color)
    mask = np.where(ll_condition)

    for i in range(0, quadrangles.quads.shape[0]):
        if quadrangles.elements_bnd_patchs[i] > 1 and quadrangles.colors[i]==2:
            plt.plot(quadrangles.x[quadrangles.quads[i]], quadrangles.y[quadrangles.quads[i]], "or")

    plt.show()



####################################
if __name__=="__main__":
#    test_1()
    test_2()
