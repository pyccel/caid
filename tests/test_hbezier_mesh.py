# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from caid.quadrangles.hermite_bezier import circle, CubicHermiteBezier

geo = circle(n=[25,25], center=[5.,4.], rmin=0.1, rmax=1.5)
geo.plot()
plt.show()
