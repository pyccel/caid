from matplotlib import pyplot as plt
from caid.cad_geometry import square
import numpy as np

# ... creates a unit square of degree (2,2) and 4 elements in each direction
geo = square(n=[3,3], p=[2,2])
# ...

# ... translate the geometry
displ = np.array([1.0, 2.0])
geo.translate(displ)
# ...

# ...
geo.plotMesh()
# ...

# ... define the matplotlib grid
nrb = geo[0]
xmin = nrb.points[...,0].min() - 0.1 ; xmax = nrb.points[...,0].max() + 0.1
ymin = nrb.points[...,1].min() - 0.1 ; ymax = nrb.points[...,1].max() + 0.1
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)

plt.savefig("transformation_ex1.png")
# ...
