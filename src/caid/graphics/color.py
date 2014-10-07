#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2009-2010  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------
''' Color object.

    A Color object represents a color using standard red, green, blue & alpha
    channels internally. It can be built in many different ways::

      white = Color(255)             # L : luminance
      white = Color(255,255)         # LA : luminance, alpha
      white = Color(255,255,255)     # RGB : red,green, blue
      white = Color(255,255,255,255) # RGBA : red, green, blue, alpha
      white = Color(1.)              # l: normalized luminance
      white = Color(1.,1.)           # la : normalized luminance + alpha
      white = Color(1.,1.,1.)        # rgb : normalized rgb + alpha
      white = Color(1.,1.,1.,1.)     # rgba : normalized red, green, blue, alpha
      white = Color('#FF')           # L : luminance
      white = Color('#FFFF')         # LA : luminance + alpha
      white = Color('#FFFFFF')       # RGB : red, green, blue
      white = Color('#FFFFFFFF')     # RGBA : red, green, blue, alpha
      white = Color('white')         # Normalized web color name
'''

class Color(object):
    
    def __init__(self, *args, **kwargs):
        ''' Create a color from given parameters.

        Parameters
        ----------
        l: float
           normalized luminance value
        r: float
           normalized red value
        g: float
           normalized green value
        b: float
           normalized blue value
        a: float
           normalized alpha value
        '''

        if len(args) > 1:
            color = args
        else:
            color = args[0]
        r = g = b = a = 1.0
        if type(color) == Color:
            r = color.r
            g = color.g
            b = color.b
            a = color.a
        elif type(color) == int:
            r = g = b = color/255.
            a = 1.0
        elif type(color) == float:
            r = g = b = color
            a = 1.0
        elif type(color) == str:
            if color[0] == '#':
                color = color[1:]
                if len(color) == 2:
                    r, g, b, a = color[:2], color[:2], color[:2], 1.
                    r, g, b = [int(n,16)/255. for n in (r, g, b)]
                elif len(color) == 4:
                    r, g, b, a = color[:2], color[:2], color[2:], color[2:4]
                    r, g, b, a = [int(n,16)/255. for n in (r, g, b, a)]
                elif len(color) == 6:
                    r, g, b, a = color[:2], color[2:4], color[4:], 1.
                    r, g, b = [int(n,16)/255. for n in (r, g, b)]
                elif len(color) == 8:
                    r, g, b, a = color[:2], color[2:4], color[4:6], color[6:],
                    r, g, b, a = [int(n,16)/255. for n in (r, g, b, a)]
                else:
                    raise ValueError, "%s does not correspond to a known color" % color
            elif color in self._colors.keys():
                c = self._colors[color][1:]
                r, g, b = c[:2], c[2:4], c[4:]
                r, g, b = [int(n, 16)/255. for n in (r, g, b)]
                a = 1.0
            else:
                raise ValueError, "%s does not correspond to a known color" % color
        elif type(color) in[tuple, list]:
            if len(color) == 1:
                if type(color[0]) == int:
                    r = g = b = color[0]/255.
                else:
                    r = g = b = color[0]
                a = 1.0
            elif len(color) == 2:
                if type(color[0]) == int:
                    r = g = b = color[0]/255.
                else:
                    r = g = b = color[0]
                if type(color[1]) == int:
                    a = color[1]/255.
                else:
                    a = color[1]
            elif len(color) >= 3:
                if type(color[0]) == int:
                    r = color[0]/255.
                else:
                    r = color[0]
                if type(color[1]) == int:
                    g = color[1]/255.
                else:
                    g = color[1]
                if type(color[2]) == int:
                    b = color[2]/255.
                else:
                    b = color[2]
                a = 1.0
            if len(color) == 4:
                if type(color[0]) == int:
                    r = color[0]/255.
                else:
                    r = color[0]
                if type(color[1]) == int:
                    g = color[1]/255.
                else:
                    g = color[1]
                if type(color[2]) == int:
                    b = color[2]/255.
                else:
                    b = color[2]
                if type(color[3]) == int:
                    a = color[3]/255.
                else:
                    a = color[3]
        else:
            raise ValueError, "%s does not correspond to a known  color" % color
        if 'alpha' in kwargs:
            a = kwargs['alpha']
        self.color = [float(r),float(g),float(b),float(a)]


    def __eq__(self, other):
        ''' Test if two color are equals '''
        return (self.r == other.r and self.g == other.g and
                self.b == other.b and self.a == other.a)


    def _get_l (self):
        return 0.3*self.r + 0.59*self.g + 0.11*self.b
    def _set_l (self, luminance):
        self.r = self.g = self.b = luminance
    l = property(_get_l, _set_l,
                         doc="Normalized luminance")

    def _get_L (self):
        return int(0.3*self.R + 0.59*self.G + 0.11*self.B)
    def _set_L (self, luminance):
        self.R = self.G = self.B = luminance
    L = property(_get_L, _set_L,
                 doc="Luminance")


    def _get_rgb(self):
        return (self.color[0],
                self.color[1],
                self.color[2])
    def _set_rgb(self, rgb):
        self._set_r(rgb[0])
        self._set_g(rgb[1])
        self._set_b(rgb[2])
    rgb = property(_get_rgb, _set_rgb,
                   doc="3-tuple of normalized RGB channels")

    def _get_RGB(self):
        return (int(self.color[0]*255),
                int(self.color[1]*255),
                int(self.color[2]*255))
    def _set_RGB(self, RGB):
        self._set_R(RGB[0])
        self._set_G(RGB[1])
        self._set_B(RGB[2])
    RGB = property(_get_RGB, _set_RGB,
                   doc="3-tuple of RGB channels")

    def _get_rgba(self):
        return (self.color[0],
                self.color[1],
                self.color[2],
                self.color[3])
    def _set_rgba(self, rgba):
        self._set_r(rgba[0])
        self._set_g(rgba[1])
        self._set_b(rgba[2])
        self._set_a(rgba[3])        
    rgba = property(_get_rgba, _set_rgba,
                    doc="4-tuple of normalized RGBA channels")

    def _get_RGBA(self):
        return (int(self.color[0]*255),
                int(self.color[1]*255),
                int(self.color[2]*255),
                int(self.color[3]*255))
    def _set_RGBA(self, RGBA):
        self._set_R(RGBA[0])
        self._set_G(RGBA[1])
        self._set_B(RGBA[2])
        self._set_A(RGBA[3])        
    RGBA = property(_get_RGBA, _set_RGBA,
                    doc="4-tuple of RGBA channels")

    def _get_r(self):
        return self.color[0]
    def _set_r(self, r):
        self.color[0] = max(0.0,min(1.0,r))
    r = property(_get_r, _set_r,
                 doc="Normalized red channel")

    def _get_g(self):
        return self.color[1]
    def _set_g(self, g):
        self.color[1] = max(0.0,min(1.0,g))
    g = property(_get_g, _set_g,
                 doc="Normalized green channel")

    def _get_b(self):
        return self.color[2]
    def _set_b(self, b):
        self.color[2] = max(0.0,min(1.0,g))
    b = property(_get_b, _set_b,
                 doc="Normalized blue channel")

    def _get_a(self):
        return self.color[3]
    def _set_a(self, a):
        self.color[3] = max(0.0,min(1.0,a))
    a = property(_get_a, _set_a,
                 doc="Normalized alpha channel")

    def _get_R(self):
        return int(self.color[0]*255)
    def _set_R(self, R):
        self.color[0] = max(0.0,min(1.0,round(R/255.,2)))
    R = property(_get_R, _set_R,
                 doc="Red channel (0-255)")

    def _get_G(self):
        return int(self.color[1]*255)
    def _set_G(self, G):
        self.color[1] = max(0.0,min(1.0,round(G/255.,2)))
    G = property(_get_G, _set_G,
                 doc="Green channel (0-255)")

    def _get_B(self):
        return int(self.color[2]*255)
    def _set_B(self, B):
        self.color[2] = max(0.0,min(1.0,round(B/255.,2)))
    B = property(_get_B, _set_B,
                 doc="Blue channel (0-255)")

    def _get_A(self):
        return int(self.color[3]*255)
    def _set_A(self, A):
        self.color[3] = max(0.0,min(1.0,round(A/255.,2)))
    A = property(_get_A, _set_A,
                 doc="Alpha channel (0-255)")

    def __repr__(self):
        return repr(self.RGBA)

    def name(self):
        for color in self._colors.keys():
            if Color(color) == self:
                return "Color('%s')" % color
        else:
            return "Color('#%x%x%x%x')" % (self.R,self.G,self.B,self.A)

    _colors = {
        'aliceblue' : '#f0f8ff',
        'antiquewhite' : '#faebd7',
        'aqua' : '#00ffff',
        'aquamarine' : '#7fffd4',
        'azure' : '#f0ffff',
        'beige' : '#f5f5dc',
        'bisque' : '#ffe4c4',
        'black' : '#000000',
        'blanchedalmond' : '#ffebcd',
        'blue' : '#0000ff',
        'blueviolet' : '#8a2be2',
        'brown' : '#a52a2a',
        'burlywood' : '#deb887',
        'cadetblue' : '#5f9ea0',
        'chartreuse' : '#7fff00',
        'chocolate' : '#d2691e',
        'coral' : '#ff7f50',
        'cornflowerblue' : '#6495ed',
        'cornsilk': '#fff8dc',
        'crimson' : '#dc143c',
        'cyan' : '#00ffff',
        'darkblue' : '#00008b',
        'darkcyan' : '#008b8b',
        'darkgoldenrod' : '#b8860b',
        'darkgray' : '#a9a9a9',
        'darkgrey' : '#a9a9a9',
        'darkgreen' : '#006400',
        'darkkhaki' : '#bdb76b',
        'darkmagenta' : '#8b008b',
        'darkolivegreen' : '#556b2f',
        'darkorange' : '#ff8c00',
        'darkorchid' : '#9932cc',
        'darkred' : '#8b0000',
        'darksalmon' : '#e9967a',
        'darkseagreen' : '#8fbc8f',
        'darkslateblue' : '#483d8b',
        'darkslategray' : '#2f4f4f',
        'darkslategrey' : '#2f4f4f',
        'darkturquoise' : '#00ced1',
        'darkviolet' : '#9400d3',
        'deeppink' : '#ff1493',
        'deepskyblue' : '#00bfff',
        'dimgray' : '#696969',
        'dimgrey' : '#696969',
        'dodgerblue' : '#1e90ff',
        'firebrick' : '#b22222',
        'floralwhite' : '#fffaf0',
        'forestgreen' : '#228b22',
        'fuchsia' : '#ff00ff',
        'gainsboro' : '#dcdcdc',
        'ghostwhite' : '#f8f8ff',
        'gold' : '#ffd700',
        'goldenrod' : '#daa520',
        'gray' : '#808080',
        'grey' : '#808080',
        'green' : '#008000',
        'greenyellow' : '#adff2f',
        'honeydew' : '#f0fff0',
        'hotpink' : '#ff69b4',
        'indianred ' : '#cd5c5c',
        'indigo ' : '#4b0082',
        'ivory' : '#fffff0',
        'khaki' : '#f0e68c',
        'lavender' : '#e6e6fa',
        'lavenderblush' : '#fff0f5',
        'lawngreen' : '#7cfc00',
        'lemonchiffon' : '#fffacd',
        'lightblue' : '#add8e6',
        'lightcoral' : '#f08080',
        'lightcyan' : '#e0ffff',
        'lightgoldenrodyellow' : '#fafad2',
        'lightgrey' : '#d3d3d3',
        'lightgreen' : '#90ee90',
        'lightpink' : '#ffb6c1',
        'lightsalmon' : '#ffa07a',
        'lightseagreen' : '#20b2aa',
        'lightskyblue' : '#87cefa',
        'lightslategray' : '#778899',
        'lightslategrey' : '#778899',
        'lightsteelblue' : '#b0c4de',
        'lightyellow' : '#ffffe0',
        'lime' : '#00ff00',
        'limegreen' : '#32cd32',
        'linen' : '#faf0e6',
        'magenta' : '#ff00ff',
        'maroon' : '#800000',
        'mediumaquamarine' : '#66cdaa',
        'mediumblue' : '#0000cd',
        'mediumorchid' : '#ba55d3',
        'mediumpurple' : '#9370d8',
        'mediumseagreen' : '#3cb371',
        'mediumslateblue' : '#7b68ee',
        'mediumspringgreen' : '#00fa9a',
        'mediumturquoise' : '#48d1cc',
        'mediumvioletred' : '#c71585',
        'midnightblue' : '#191970',
        'mintcream' : '#f5fffa',
        'mistyrose' : '#ffe4e1',
        'moccasin' : '#ffe4b5',
        'navajowhite' : '#ffdead',
        'navy' : '#000080',
        'oldlace' : '#fdf5e6',
        'olive' : '#808000',
        'olivedrab' : '#6b8e23',
        'orange' : '#ffa500',
        'orangered' : '#ff4500',
        'orchid' : '#da70d6',
        'palegoldenrod' : '#eee8aa',
        'palegreen' : '#98fb98',
        'paleturquoise' : '#afeeee',
        'palevioletred' : '#d87093',
        'papayawhip' : '#ffefd5',
        'peachpuff' : '#ffdab9',
        'peru' : '#cd853f',
        'pink' : '#ffc0cb',
        'plum' : '#dda0dd',
        'powderblue' : '#b0e0e6',
        'purple' : '#800080',
        'red' : '#ff0000',
        'rosybrown' : '#bc8f8f',
        'royalblue' : '#4169e1',
        'saddlebrown' : '#8b4513',
        'salmon' : '#fa8072',
        'sandybrown' : '#f4a460',
        'seagreen' : '#2e8b57',
        'seashell' : '#fff5ee',
        'sienna' : '#a0522d',
        'silver' : '#c0c0c0',
        'skyblue' : '#87ceeb',
        'slateblue' : '#6a5acd',
        'slategray' : '#708090',
        'slategrey' : '#708090',
        'snow' : '#fffafa',
        'springgreen' : '#00ff7f',
        'steelblue' : '#4682b4',
        'tan' : '#d2b48c',
        'teal' : '#008080',
        'thistle' : '#d8bfd8',
        'tomato' : '#ff6347',
        'turquoise' : '#40e0d0',
        'violet' : '#ee82ee',
        'wheat' : '#f5deb3',
        'white' : '#ffffff',
        'whitesmoke' : '#f5f5f5',
        'yellow' : '#ffff00',
        'yellowgreen' : '#9acd32'}


if __name__ == '__main__':
    colors = ['Color(255)',             # L : luminance
              'Color(255,255)',         # LA : luminance, alpha
              'Color(255,255,255)',     # RGB : red,green, blue
              'Color(255,255,255,255)', # RGBA : red, green, blue, alpha
              'Color(1.)',              # l: normalized luminance
              'Color(1.,1.)',           # la : normalized luminance + alpha
              'Color(1.,1.,1.)',        # rgb : normalized rgb + alpha
              'Color(1.,1.,1.,1.)',     # rgba : normalized red, green, blue, alpha
              "Color('#FF')",           # L : luminance
              "Color('#FFFF')",         # LA : lumnance, alpha
              "Color('#FFFFFF')",       # RGB : red, green, blue
              "Color('#FFFFFFFF')",     # RGBA : red, green, blue, alpha
              "Color('white')"]         # Normalized web color name
    for color in colors:
        c = eval(color)
        print '%s : %s' %(color, c.rgba)
    print 'Color(1.) = %s ' % Color(1.).name()
