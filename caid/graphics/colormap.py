#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2009-2010  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------
''' Colormap object.

    A Colormap object is a linear interpolation of a list of value/color where
    value is normalized between 0 and 1. over, under and bad value can be
    assigned special colors.

    Example:
    --------
      cmap = Colormap((0., (0.,0.,0.,1.)),
                      (1., (1.,1.,1.,1.)))
'''
import numpy
from color import Color

class Colormap:
    ''' '''

    def __init__(self, name, *args, **kwargs):
        ''' Build a new colormap from given (value,color) list.
        
        Parameters
        ----------
           name: str
               Colormap name

           args: [(value,Color),...]
               Value/color couples to build colormap from.
               Values must be normalized between 0 and 1
               
           bad: Color
               Color to be used for bad values.

           over: Color
               Color to be used for high out-of-range values.

           under: Color
               Color to be used for low out-of-range values.
        '''
        self.name = name
        self.vcolors = []
        self.LUT = {}
        self.LUT['rgb'] = None
        self.LUT['RGB'] = None
        self.LUT['rgba'] = None
        self.LUT['RGBA'] = None
        self.under = Color(0., 0., 1., 1.)
        self.over  = Color(1., 0., 0., 1.)
        self.bad   = Color(0., 1., 0., 1.)
        self.alpha = 1.0
        for value,color in args:
            self._append( value, Color(color) )
        self._update()
        self.under = kwargs.get('under', self.get_color(-1))
        self.over = kwargs.get('over', self.get_color(1))
        self.bad = kwargs.get('bad', self.bad)
        self._update()
    

    def set_alpha(self, alpha):
        ''' Set overall transparency. '''
        for i in range(len(self.vcolors)):
            value, color = self.vcolors[i]
            #self.vcolors[i].alpha = alpha
            color.alpha = alpha
        self._update()

    def set_under(self, *args):
        ''' Set color to be used for low out-of-range values. '''
        self.under = Color(*args)
        self._update()

    def set_over(self, *args):
        ''' Set color to be used for high out-of-range values. '''
        self.over = Color(*args)
        self._update()

    def set_bad(self, *args):
        ''' Set color to be used for bad (nan) values. '''
        self.bad = Color(*args)
        self._update()

    def _append( self, value, color ):
        ''' Append a new value/color '''
        self.vcolors.append( [value,color] )
        self.vcolors.sort( lambda x,y: int(x[0]-y[0]) )

    def _update(self):
        ''' Update internal representations '''
        
        n = 509
        self.LUT['RGB']  = [(0,0,0)]*(n+3)
        self.LUT['rgb']  = [(0.0,0.0,0.0)]*(n+3)
        self.LUT['RGBA'] = [(0,0,0,0)]*(n+3)
        self.LUT['rgba'] = [(0.0,0.0,0.0,0.0)]*(n+3)
        self.LUT['RGB'][0]  = self.bad.RGB
        self.LUT['RGB'][1]  = self.under.RGB
        self.LUT['RGB'][-1] = self.over.RGB
        self.LUT['RGBA'][0]  = self.bad.RGBA
        self.LUT['RGBA'][1]  = self.under.RGBA
        self.LUT['RGBA'][-1] = self.over.RGBA
        self.LUT['rgb'][0]  = self.bad.rgb
        self.LUT['rgb'][1]  = self.under.rgb
        self.LUT['rgb'][-1] = self.over.rgb
        self.LUT['rgba'][0]  = self.bad.rgba
        self.LUT['rgba'][1]  = self.under.rgba
        self.LUT['rgba'][-1] = self.over.rgba
        for i in range( n ):
            c = self.get_color( i/float(n-1) )
            self.LUT['RGB'][2+i] = c.RGB
            self.LUT['RGBA'][2+i] = c.RGBA
            self.LUT['rgb'][2+i] = c.rgb
            self.LUT['rgba'][2+i] = c.rgba
        self.LUT['RGB'] = numpy.array( self.LUT['RGB'],
                                       dtype=[('R',numpy.ubyte),
                                              ('G',numpy.ubyte),
                                              ('B',numpy.ubyte)])
        self.LUT['rgb'] = numpy.array( self.LUT['rgb'],
                                       dtype=[('r',numpy.float32),
                                              ('g',numpy.float32),
                                              ('b',numpy.float32)])
        self.LUT['RGBA'] = numpy.array( self.LUT['RGBA'],
                                        dtype=[('R',numpy.ubyte),
                                               ('G',numpy.ubyte),
                                               ('B',numpy.ubyte),
                                               ('A',numpy.ubyte)])
        self.LUT['rgba'] = numpy.array( self.LUT['rgba'],
                                        dtype=[('r',numpy.float32),
                                               ('g',numpy.float32),
                                               ('b',numpy.float32),
                                               ('a',numpy.float32)])
        self.size = n+3

    def get_color (self, value):
        ''' Get interpolated color from value '''

        if not len(self.vcolors):
            return Color(0.,0.,0.,self.alpha)
        elif len(self.vcolors) == 1:
            return self.vcolors[0][1]
        elif value < 0.0:
            return self.vcolors[0][1]
        elif value > 1.0:
            return self.vcolors[-1][1]
        sup_color = self.vcolors[0]
        inf_color = self.vcolors[-1]
        for i in range (len(self.vcolors)-1):
            if value < self.vcolors[i+1][0]:
                inf_color = self.vcolors[i]
                sup_color = self.vcolors[i+1]
                break
        r = (value-inf_color[0]) / (sup_color[0]-inf_color[0])
        return Color(sup_color[1].r*r + inf_color[1].r*(1-r),
                     sup_color[1].g*r + inf_color[1].g*(1-r),
                     sup_color[1].b*r + inf_color[1].b*(1-r),
                     sup_color[1].a*r + inf_color[1].a*(1-r))


# Default colormaps
# ------------------------------------------------------------------------------
IceAndFire = Colormap("IceAndFire",
                      (0.00, (0.0, 0.0, 1.0)),
                      (0.25, (0.0, 0.5, 1.0)),
                      (0.50, (1.0, 1.0, 1.0)),
                      (0.75, (1.0, 1.0, 0.0)),
                      (1.00, (1.0, 0.0, 0.0)))
Ice = Colormap("Ice",
               (0.00, (0.0, 0.0, 1.0)),
               (0.50, (0.5, 0.5, 1.0)),
               (1.00, (1.0, 1.0, 1.0)))
Fire = Colormap("Fire",
                (0.00, (1.0, 1.0, 1.0)),
                (0.50, (1.0, 1.0, 0.0)),
                (1.00, (1.0, 0.0, 0.0)))
Hot = Colormap("Hot",
               (0.00, (0.0, 0.0, 0.0)),
               (0.33, (1.0, 0.0, 0.0)),
               (0.66, (1.0, 1.0, 0.0)),
               (1.00, (1.0, 1.0, 1.0)))
Grey       = Colormap("Grey", (0., (0.,0.,0.)), (1., (1.,1.,1.)))
Grey_r     = Colormap("Grey_r", (0., (1.,1.,1.)), (1., (0.,0.,0.)))
DarkRed    = Colormap("DarkRed", (0., (0.,0.,0.)), (1., (1.,0.,0.)))
DarkGreen  = Colormap("DarkGreen",(0., (0.,0.,0.)), (1., (0.,1.,0.)))
DarkBlue   = Colormap("DarkBlue", (0., (0.,0.,0.)), (1., (0.,0.,1.)))
LightRed   = Colormap("LightRed", (0., (1.,1.,1.)), (1., (1.,0.,0.)))
LightGreen = Colormap("LightGreen", (0., (1.,1.,1.)), (1., (0.,1.,0.)))
LightBlue  = Colormap("LightBlue", (0., (1.,1.,1.)), (1., (0.,0.,1.)))


if __name__ == '__main__':
    cmap = Grey
    cmap.set_under(1.,0.,0.,1.)
    cmap.set_over(0.,0.,1.,1.)
    cmap.set_bad(1.,0.,1.,0.)
    LUT = cmap.LUT['RGBA']
    Z = numpy.array([0,.5,1,-1, 2, numpy.NaN])
    zmin, zmax = 0.0, 1.0

    # LUT.size = bad + under + actual # colors + over
    Zn = (Z-zmin)
    Zn *= (LUT.size-3-1)/float(zmax-zmin)
    Zi = Zn.astype(numpy.int)

    # Zn holds unranged indices of colors
    # At this stage, they can be negative or superior to LUT.size-3

    # Set negative indices to become 'under' color (1)
    #  and increment others by 2 to skip bad and under colors
    Zi = numpy.maximum (Zi+2, 1)

    # Set out-of-range indices to be 'over' color (LUT.size-1)
    Zi = numpy.minimum (Zi, LUT.size-1)

    # Replace too high indices with 'over' color index ( = 1)
 
    # Replace bad indices with 'bad' color
    Zi = numpy.multiply(Zi, 1-numpy.isnan(Z))

    I = LUT.take(Zi,mode='clip').view((numpy.ubyte,4))
    print I


