# -*- coding: UTF-8 -*-
from pigasus.utils.manager import context



def run(geo, AllDirichlet=True, f=None):
    with context():
        from pigasus.gallery.poisson import poisson
        import numpy as np
        import matplotlib.pyplot as plt
        PDE = poisson(geo, AllDirichlet=True)
        if f is None:
            sin = np.sin ; pi = np.pi ; kx = 2. * pi ; ky = 2. * pi
            f = lambda x,y : [( kx**2 + ky**2 ) * sin ( kx * x ) * sin ( ky * y )]
        PDE.assembly(f=f)
        PDE.solve()
        PDE.plot()
        plt.colorbar(); plt.show()
        PDE.free()

