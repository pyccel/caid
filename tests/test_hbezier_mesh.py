# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from caid.quadrangles.hermite_bezier import rectangle, square, circle

def test_rectangle():
    geo = rectangle(n=[25,25], origin=[5.,4.], lengths=[1.,2.])
    geo.save(label="rectangle")
    geo.plot()
    plt.title("Rectangular domain using Cubic hermite bezier elements")
    plt.show()

def test_square(n=4):
    geo = square(n=[n+1,n+1])
#    geo.save(label="square")
    geo.save(label="jorek")
#    geo.plot()
#    plt.title("Square domain using Cubic hermite bezier elements")
#    plt.show()

def test_circle():
    geo = circle(n=[25,25], center=[5.,4.], rmin=0.1, rmax=1.5)
    geo.save(label="circle")
#    geo.plot()
#    plt.title("Circular domain using Cubic hermite bezier elements")
#    plt.show()

########################################################################
if __name__ == "__main__":
    test_square(n=64)
#    test_circle()

