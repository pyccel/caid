# -*- coding: UTF-8 -*-
import sys
import numpy as np
from numpy import array, linspace, zeros, zeros_like
from igakit.cad_geometry import cad_geometry
#from igakit.graphics import glFreeType

try:
    from OpenGL.arrays import vbo
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
except:
    print '''ERROR: PyOpenGL not installed properly.'''

from igakit.field import field

class colorbar(field):
    def __init__(self, C, xmax=0., xmin=0., ymax=0., ymin=0., zmax=0., zmin=0., colormap=None, side='right'):
        self._colormap = colormap
        self._C = C
        self._side = side
        print "> create colorbar with ", len(C), " side ", side

        if side == 'right':
            scale = [0.25, 2.]
            displ = [xmax+2.,0.]
            n = [0,len(C)-2]
        if side == 'left':
            scale = [0.25, 2.]
            displ = [xmin-1.,0.]
            n = [0,len(C)-2]
        if side == 'bottom':
            scale = [2., 0.25]
            displ = [0.,ymin-2.]
            n = [len(C)-2,0]
        if side == 'top':
            scale = [2., 0.25]
            displ = [0.,ymax+2.]
            n = [len(C)-2,0]

        from igakit.cad_geometry import square
        geometry = square()
        values   = square(n=n)

        for geo in [geometry, values]:
            for axis in range(0, 2):
                geo.scale(scale[axis], axis=axis)
            geo.translate(displ)

        patch_id = 0
        nrb = values[patch_id]
        P = zeros_like(nrb.points)
        if side == 'right':
            P[0,:,0] = C
            P[1,:,0] = C
        if side == 'left':
            P[0,:,0] = C
            P[1,:,0] = C
        if side == 'bottom':
            P[:,0,0] = C
            P[:,1,0] = C
        if side == 'top':
            P[:,0,0] = C
            P[:,1,0] = C
        nrb.set_points(P)
        field.__init__(self, geometry=geometry, values=values, type='scalar')

