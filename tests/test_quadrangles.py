# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from caid.quadrangles.quadrangles import Quadrangles

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
    # node,R,Z,u1,u2,v1,v2,w1,w2,boundary type,boundary index,color
    fmt_nodes = [int, float, float, float, float, float, float, float, float, int, int, int]
    nodes    = np.genfromtxt("jorekNodes.txt", comments="#")
#    print nodes.shape

    # element,vertex(1:4),color
    fmt_elements = [int, int, int, int, int, int]
    elements = np.genfromtxt("jorekElements.txt", comments="#")
    elements = np.array(elements, dtype=np.int32)
#    print elements.shape

    # extract quadrangles and use 0 based indexing
    quads = elements[:,1:-1] - 1
#    print quads

    R        = nodes[:,1]
    Z        = nodes[:,2]
    u        = nodes[:,3:5]
    v        = nodes[:,5:7]
    w        = nodes[:,7:9]
    bnd_type = np.array(nodes[:,9], dtype=np.int32)
    bnd_ind  = np.array(nodes[:,10], dtype=np.int32)
    color    = np.array(nodes[:,11], dtype=np.int32)

    quadrangles = Quadrangles(R,Z,quads=quads)
#    quadrangles.plot()
#    plt.show()

    triang = quadrangles.triang
    color_tri = color[quadrangles.ancestors]

    mask_1 = np.where(color[quadrangles.ancestors] == 1, 1, 0)
    mask_2 = np.where(color[quadrangles.ancestors] == 2, 1, 0)
    mask_3 = np.where(color[quadrangles.ancestors] == 3, 1, 0)
    mask_4 = np.where(color[quadrangles.ancestors] == 4, 1, 0)

#    masks = [mask_1, mask_2, mask_3, mask_4]
#    for mask, color in zip(masks, ["red", "blue", "green", "yellow"]):
#        triang.set_mask(mask)
#        plt.triplot(triang, '-', lw=0.75, color=color)
#        plt.show()

#    mask = mask_1 ; color = "blue"
#    triang.set_mask(mask)
#    plt.triplot(triang, '-', lw=0.75, color=color)
#    plt.show()




####################################
if __name__=="__main__":
#    test_1()
#    test_2()

#    nodes_filename    = "jorekNodes.txt"
#    elements_filename = "jorekElements.txt"

    nodes_filename    = "jorekNodes_ref.txt"
    elements_filename = "jorekElements_ref.txt"

    # node,R,Z,u1,u2,v1,v2,w1,w2,boundary type,boundary index,color
    fmt_nodes = [int, float, float, float, float, float, float, float, float, int, int, int]
    nodes    = np.genfromtxt(nodes_filename, comments="#")
    print nodes.shape

    # element,vertex(1:4),color
    fmt_elements = [int, int, int, int, int, int]
    elements = np.genfromtxt(elements_filename, comments="#")
    elements = np.array(elements, dtype=np.int32)
    color    = np.array(elements[:,-1], dtype=np.int32)
    print elements.shape

    # extract quadrangles and use 0 based indexing
    quads = elements[:,1:-1] - 1
#    print quads

    R        = nodes[:,1]
    Z        = nodes[:,2]
    u        = nodes[:,3:5]
    v        = nodes[:,5:7]
    w        = nodes[:,7:9]
    bnd_type = np.array(nodes[:,9], dtype=np.int32)
    bnd_ind  = np.array(nodes[:,10], dtype=np.int32)

    quadrangles = Quadrangles(R,Z,quads=quads)
#    quadrangles.plot()
#    plt.show()

    triang = quadrangles.triang
    color_tri = color[quadrangles.ancestors]

    ll_condition_1 = (color[quadrangles.ancestors] == 1)
    ll_condition_2 = (color[quadrangles.ancestors] == 2)
    ll_condition_3 = (color[quadrangles.ancestors] == 3)
    for my_color, col in zip([1,2,4], ["blue", "red", "green"]):
        ll_condition = (color[quadrangles.ancestors] == my_color)
        mask = np.where(ll_condition, 0, 1)

        triang.set_mask(mask)
        plt.triplot(triang, '-', lw=0.75, color=col)
    plt.show()
