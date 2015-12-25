from matplotlib import pyplot as plt
from caid.cad_geometry import square
from caid.cad_geometry import circle
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

plt.savefig("transformations_2d_translate.png") ; plt.clf()
# ...

# ... creates a unit square of degree (2,2) and 4 elements in each direction
geo = square(n=[3,3], p=[2,2])
# ...

# ... rotate the geometry
geo.rotate(np.pi/4, axis=2)
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

plt.savefig("transformations_2d_rotate.png") ; plt.clf()
# ...

# ... creates a unit circle of degree (2,2) and 4 elements in each direction
geo = circle(n=[3,3], p=[2,2])
# ...

# ... scaling with (2,4) in each direction
geo.scale(2., axis=0)
geo.scale(4., axis=1)
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

plt.axis("equal")

plt.savefig("transformations_2d_scale.png") ; plt.clf()
# ...
