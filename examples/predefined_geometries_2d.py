from matplotlib import pyplot as plt
import numpy as np

# ... creates a unit square of degree (2,2) and 4 elements in each direction
from caid.cad_geometry import square
geo = square(n=[3,3], p=[2,2])
geo.plotMesh(MeshResolution=10)
plt.savefig("predefined_geometries_2d_square.png")
# ...

plt.clf()

# ... creates a unit circle of degree (2,2) and (8,4) elements in each direction
from caid.cad_geometry import circle
geo = circle(n=[7,3], p=[2,2])
geo.plotMesh(MeshResolution=10)
plt.savefig("predefined_geometries_2d_circle.png")
# ...

plt.clf()

# ... creates a unit quart_circle of degree (2,2) and 4 elements in each direction
from caid.cad_geometry import quart_circle
geo = quart_circle(n=[3,3], p=[2,2])
geo.plotMesh(MeshResolution=10)
plt.savefig("predefined_geometries_2d_quart_circle.png")
# ...

plt.clf()

# ... creates a unit annulus of degree (2,2) and 4 elements in each direction
from caid.cad_geometry import annulus
geo = annulus(n=[7,7], p=[2,2])
geo.plotMesh(MeshResolution=10)
plt.savefig("predefined_geometries_2d_annulus.png")
# ...

plt.clf()

# ... creates a unit circle with 5 patchs, of degree (2,2) and (4,4) elements in each direction
from caid.cad_geometry import circle_5mp as circle
geo = circle(n=[7,7], p=[2,2])
geo.plotMesh(MeshResolution=10)
plt.savefig("predefined_geometries_2d_circle_5mp.png")
# ...
