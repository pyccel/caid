# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from caid.quadrangles.hermite_bezier import rectangle, square, circle

geo = rectangle(n=[25,25], origin=[5.,4.], lengths=[1.,2.])
geo.plot()
plt.title("Rectangular domain using Cubic hermite bezier elements")
plt.show()

geo = square(n=[25,25])
geo.plot()
plt.title("Square domain using Cubic hermite bezier elements")
plt.show()

geo = circle(n=[25,25], center=[5.,4.], rmin=0.1, rmax=1.5)
geo.plot()
plt.title("Circular domain using Cubic hermite bezier elements")
plt.show()

