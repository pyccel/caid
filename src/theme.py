# -*- coding: UTF-8 -*-
import numpy as np
from caid.graphics.color import Color
from global_vars import strtoArray

def my_color(value):
    return list(Color(value).rgb)

def _singleton(cls):
    instances = {} # Line 2
    def getinstance():
        if cls not in instances:
            instances[cls] = cls() # Line 5
        return instances[cls]
    return getinstance

@_singleton
class theme():
    def __init__(self):
        self._alpha                             = None
        self._alpha_bg                          = None
        self._beta                              = None

        self._enable_blend                      = None
        self._enable_inspector_color            = None

        # RGB colors
        self._color_selected_geometry           = {}
        self._color_selected_geometry['mesh']   = None
        self._color_selected_geometry['nurbs']  = None
        self._color_selected_geometry['points'] = None

        # RGB colors
        self._color_selected_patch              = {}
        self._color_selected_patch['mesh']      = None
        self._color_selected_patch['nurbs']     = None
        self._color_selected_patch['points']    = None

        # RGB colors
        self._color_viewer                      = {}
        self._color_viewer['selection_points']  = None
        self._color_viewer['marker_points']     = None
        self._color_viewer['selection']         = None
        self._color_viewer['background']        = None
        self._color_viewer['grid']              = None
        self._color_viewer['default_geometry']  = None
        self._color_viewer['default_patch']     = None
        self._color_viewer['default_mesh']      = None
        self._color_viewer['default_points']    = None

        # RGB colors
        self._color_inspector                   = {}
        self._color_inspector['background']     = None
        self._color_inspector['hide_text']      = None
        self._color_inspector['show_text']      = None
        self._color_inspector['hide_background'] = None
        self._color_inspector['show_background'] = None

        # size
        self._size_points                       = {}
        self._size_points['selection_points']   = None
        self._size_points['marker_points']      = None
        self._size_points['geometry']           = None
        self._size_points['patch']              = None
        self._size_points['grid']               = None

        # default theme
#        self.set_theme("dark")
        self.set_theme("white")
#        self.set_theme("grey")
#        self.set_theme("django")

    @property
    def alpha(self):
        return self._alpha

    @property
    def alpha_bg(self):
        return self._alpha_bg

    @property
    def beta(self):
        return self._beta

    @property
    def enable_blend(self):
        return self._enable_blend

    @property
    def enable_inspector_color(self):
        return self._enable_inspector_color

    def color_selected_geometry(self, txt):
        return self._color_selected_geometry[txt]

    def color_selected_patch(self, txt):
        return self._color_selected_patch[txt]

    def color_viewer(self, txt):
        return self._color_viewer[txt]

    def color_inspector(self, txt):
        return self._color_inspector[txt]

    def size_points(self, txt):
        return self._size_points[txt]

    def set_alpha(self, value):
        self._alpha = value

    def set_alpha_bg(self, value):
        self._alpha_bg = value

    def set_beta(self, value):
        self._beta = value

    def set_enable_blend(self, value):
        self._enable_blend = value

    def set_enable_inspector_color(self, value):
        self._enable_inspector_color = value

    def set_color_selected_geometry(self, txt, value):
        self._color_selected_geometry[txt] = value

    def set_color_selected_patch(self, txt, value):
        self._color_selected_patch[txt] = value

    def set_color_viewer(self, txt, value):
        self._color_viewer[txt] = value

    def set_color_inspector(self, txt, value):
        self._color_inspector[txt] = value

    def set_size_points(self, txt, value):
        self._size_points[txt] = value

    def set_theme(self, value):
        if type(value) == str:
            if value == "grey":
                self.grey()
            if value == "dark":
                self.dark()
            if value == "white":
                self.white()
            if value == "django":
                self.django()
            if value == "joepass":
                self.joepass()

    def save(self, filename=None, doc=None):
        """
        saves the current theme in xml format in filename if specified.
        otherwise it returns the corresponding xml that can be inserted directly
        in workgroup.save
        """

        if (doc is None) and (filename is None):
            print("doc and filename can not be both None")
            raise

        if (doc is not None) and (filename is not None):
            print("doc and filename can not be both specified")
            raise

        if filename is not None:
            # ... create xml doc
            from xml.dom.minidom import Document
            # Create the minidom document
            doc = Document()

        # Create the <caid> base element
        rootElt = doc.createElement("theme")

        rootElt.setAttribute("alpha"\
                             , str(self.alpha))
        rootElt.setAttribute("beta"\
                             , str(self.beta))
        rootElt.setAttribute("alpha-background"\
                             , str(self.alpha_bg))
        rootElt.setAttribute("enable-blend"\
                             , str(self.enable_blend))

        rootElt.setAttribute("color-background"\
                             , str(self.color_viewer("background")))
        rootElt.setAttribute("color-grid"\
                             , str(self.color_viewer("grid")))
        rootElt.setAttribute("size-grid"\
                             , str(self.size_points("grid")))

        rootElt.setAttribute("color-selectedGeoMesh"\
                             , str(self.color_selected_geometry('mesh')))
        rootElt.setAttribute("color-selectedGeoNurbs"\
                             , str(self.color_selected_geometry('nurbs')))
        rootElt.setAttribute("color-selectedGeoPoints"\
                             , str(self.color_selected_geometry('points')))

        rootElt.setAttribute("color-selectedPatchMesh"\
                             , str(self.color_selected_patch('mesh')))
        rootElt.setAttribute("color-selectedPatchNurbs"\
                             , str(self.color_selected_patch('nurbs')))
        rootElt.setAttribute("color-selectedPatchPoints"\
                             , str(self.color_selected_patch('points')))

        rootElt.setAttribute("color-markerPoints"\
                             , str(self.color_viewer("marker_points")))
        rootElt.setAttribute("size-markerPoints"\
                             , str(self.size_points("marker_points")))

        rootElt.setAttribute("color-selectedPoints"\
                             , str(self.color_viewer("selection_points")))
        rootElt.setAttribute("size-selectedPoints"\
                             , str(self.size_points("selection_points")))


        rootElt.setAttribute("color-default_geometry"\
                             , str(self.color_viewer("default_geometry")))

        rootElt.setAttribute("color-default_patch"\
                             , str(self.color_viewer("default_patch")))

        rootElt.setAttribute("color-default_mesh"\
                             , str(self.color_viewer("default_mesh")))

        rootElt.setAttribute("color-default_points"\
                             , str(self.color_viewer("default_points")))

        rootElt.setAttribute("color-selection"\
                             , str(self.color_viewer("selection")))


        rootElt.setAttribute("size-geometryPoints"\
                             , str(self.size_points("geometry")))

        rootElt.setAttribute("size-patchPoints"\
                             , str(self.size_points("patch")))

        if filename is not None:
            doc.appendChild(rootElt)

            f = open(filename, 'wr')
            s = doc.toprettyxml()
            f.write(s)
            f.close()
        else:
            return rootElt, doc

    def load(self, filename=None, rootElt=None):
        """
        loads the current theme in xml format from filename if specified.
        """

        if (rootElt is None) and (filename is None):
            print("rootElt and filename can not be both None")
            raise

        if (rootElt is not None) and (filename is not None):
            print("rootElt and filename can not be both specified")
            raise

        if filename is not None:
            from xml.dom.minidom import parse
            doc = parse(filename)
            themeElt = doc.documentElement
        else:
            themeElt = rootElt.getElementsByTagName("theme")[0]


        # ...
        value = float(themeElt.getAttribute("alpha"))
        self.set_alpha(value)

        value = float(themeElt.getAttribute("beta"))
        self.set_beta(value)

        value = float(themeElt.getAttribute("alpha-background"))
        self.set_alpha_bg(value)

        txt = themeElt.getAttribute("enable-blend")
        if txt.lower() == "true":
            value = True
        if txt.lower() == "false":
            value = False
        self.set_enable_blend(value)
        # ...

        # RGB colors
        color = strtoArray(themeElt.getAttribute("color-selectedGeoMesh"))
        self.set_color_selected_geometry("mesh",color)

        color = strtoArray(themeElt.getAttribute("color-selectedGeoNurbs"))
        self.set_color_selected_geometry("nurbs",color)

        color = strtoArray(themeElt.getAttribute("color-selectedGeoPoints"))
        self.set_color_selected_geometry("points",color)

        # RGB colors
        color = strtoArray(themeElt.getAttribute("color-selectedPatchMesh"))
        self.set_color_selected_patch("mesh",color)

        color = strtoArray(themeElt.getAttribute("color-selectedPatchNurbs"))
        self.set_color_selected_patch("nurbs",color)

        color = strtoArray(themeElt.getAttribute("color-selectedPatchPoints"))
        self.set_color_selected_patch("points",color)

        # RGB colors
        color = strtoArray(themeElt.getAttribute("color-background"))
        self.set_color_viewer("background",color)

        color = strtoArray(themeElt.getAttribute("color-grid"))
        self.set_color_viewer("grid",color)

        value = float(themeElt.getAttribute("size-grid"))
        self.set_size_points("grid",value)


        color = strtoArray(themeElt.getAttribute("color-selectedPoints"))
        self.set_color_viewer("selection_points",color)

        value = float(themeElt.getAttribute("size-selectedPoints"))
        self.set_size_points("selection_points",value)


        color = strtoArray(themeElt.getAttribute("color-markerPoints"))
        self.set_color_viewer("marker_points",color)

        value = float(themeElt.getAttribute("size-markerPoints"))
        self.set_size_points("marker_points",value)


        color = strtoArray(themeElt.getAttribute("color-default_geometry"))
        self.set_color_viewer("default_geometry",color)

        color = strtoArray(themeElt.getAttribute("color-default_patch"))
        self.set_color_viewer("default_patch",color)

        color = strtoArray(themeElt.getAttribute("color-default_mesh"))
        self.set_color_viewer("default_mesh",color)

        color = strtoArray(themeElt.getAttribute("color-default_points"))
        self.set_color_viewer("default_points",color)

        color = strtoArray(themeElt.getAttribute("color-selection"))
        self.set_color_viewer("selection",color)


        value = float(themeElt.getAttribute("size-geometryPoints"))
        self.set_size_points("geometry",value)

        value = float(themeElt.getAttribute("size-patchPoints"))
        self.set_size_points("patch",value)



    def grey(self):
        self.set_alpha(1.)
        self.set_beta(1.)
        self.set_alpha_bg(0.)
        self.set_enable_blend(False)
        self.set_enable_inspector_color(False)

        # RGB colors
        self.set_color_selected_geometry("mesh",my_color("blue"))
        self.set_color_selected_geometry("nurbs",my_color("red"))
        self.set_color_selected_geometry("points",my_color("black"))

        # RGB colors
        self.set_color_selected_patch("mesh",my_color("lavender"))
        self.set_color_selected_patch("nurbs",my_color("black"))
        self.set_color_selected_patch("points",my_color("magenta"))

        # RGB colors
        self.set_color_viewer("selection_points",my_color("lightblue"))
        self.set_color_viewer("marker_points",my_color("blue"))
        self.set_color_viewer("selection",my_color("yellow"))
        self.set_color_viewer("background",my_color("lightgrey"))
        self.set_color_viewer("grid",my_color("lightgreen"))
        self.set_color_viewer("default_geometry",my_color("grey"))
        self.set_color_viewer("default_patch",my_color("grey"))
        self.set_color_viewer("default_mesh",my_color("white"))
        self.set_color_viewer("default_points",my_color("magenta"))

        self.set_size_points("selection_points",6.)
        self.set_size_points("marker_points",6.)
        self.set_size_points("geometry",6.)
        self.set_size_points("patch",6.)
        self.set_size_points("grid",2.)

        # RGB colors
        self.set_color_inspector("background",my_color("white"))
        self.set_color_inspector("show_text",my_color("black"))
        self.set_color_inspector("hide_text",my_color("red"))
        self.set_color_inspector("show_background",my_color("white"))
        self.set_color_inspector("hide_background",my_color("white"))


    def dark(self):
        self.set_alpha(1.)
        self.set_beta(1.)
        self.set_alpha_bg(1.)
        self.set_enable_blend(True)
        self.set_enable_inspector_color(False)

        # RGB colors
        self.set_color_selected_geometry("mesh",[0.2,0.1,0.57])
        self.set_color_selected_geometry("nurbs",[0.5,0.5,0.5])
        self.set_color_selected_geometry("points",[0.1,0.1,0.1])

        # RGB colors
        self.set_color_selected_patch("mesh",[0.65,0.65,0.65])
        self.set_color_selected_patch("nurbs",my_color("red"))
#        self.set_color_selected_patch("nurbs",[0.2,0.8,0.57])
        self.set_color_selected_patch("points",[0.2,0.2,0.2])

        # RGB colors
        self.set_color_viewer("selection_points",[1.,0.,0.])
        self.set_color_viewer("marker_points",[0.25,0.25,0.95])
        self.set_color_viewer("selection",[0.1,0.1,0.1])
        self.set_color_viewer("background",[0.0, 0.0, 0.0])
        self.set_color_viewer("grid",[1.0, 1.0, 1.0])
        self.set_color_viewer("default_geometry",[0.,0.,1.])
        self.set_color_viewer("default_patch",[0.,0.,1.])
        self.set_color_viewer("default_mesh",[1.,1.,1.])
        self.set_color_viewer("default_points",[0.1,0.1,0.1])

        self.set_size_points("selection_points",6.)
        self.set_size_points("marker_points",6.)
        self.set_size_points("geometry",6.)
        self.set_size_points("patch",6.)
        self.set_size_points("grid",2.)

        # RGB colors
        self.set_color_inspector("background",my_color("white"))
        self.set_color_inspector("show_text",my_color("black"))
        self.set_color_inspector("hide_text",my_color("red"))
        self.set_color_inspector("show_background",my_color("white"))
        self.set_color_inspector("hide_background",my_color("white"))


    def white(self):
        self.set_alpha(1.)
        self.set_beta(1.)
        self.set_alpha_bg(0.)
        self.set_enable_blend(False)
        self.set_enable_inspector_color(False)

        # RGB colors
        self.set_color_selected_geometry("mesh",my_color("blue"))
        self.set_color_selected_geometry("nurbs",my_color("red"))
        self.set_color_selected_geometry("points",my_color("black"))

        # RGB colors
        self.set_color_selected_patch("mesh",my_color("lavender"))
        self.set_color_selected_patch("nurbs",my_color("blue"))
        self.set_color_selected_patch("points",my_color("magenta"))

        # RGB colors
        self.set_color_viewer("selection_points",my_color("lightblue"))
        self.set_color_viewer("marker_points",my_color("blue"))
        self.set_color_viewer("selection",my_color("yellow"))
        self.set_color_viewer("background",my_color("white"))
        self.set_color_viewer("grid",my_color("lightgreen"))
        self.set_color_viewer("default_geometry",my_color("grey"))
        self.set_color_viewer("default_patch",my_color("grey"))
        self.set_color_viewer("default_mesh",my_color("white"))
        self.set_color_viewer("default_points",my_color("magenta"))

        self.set_size_points("selection_points",6.)
        self.set_size_points("marker_points",6.)
        self.set_size_points("geometry",6.)
        self.set_size_points("patch",6.)
        self.set_size_points("grid",2.)

        # RGB colors
        self.set_color_inspector("background",my_color("white"))
        self.set_color_inspector("show_text",my_color("black"))
        self.set_color_inspector("hide_text",my_color("red"))
        self.set_color_inspector("show_background",my_color("white"))
        self.set_color_inspector("hide_background",my_color("white"))

    def django(self):
        self.set_alpha(1.)
        self.set_beta(1.)
        self.set_alpha_bg(0.)
        self.set_enable_blend(False)
        self.set_enable_inspector_color(False)

        # RGB colors
        self.set_color_selected_geometry("mesh",my_color("#FCC059"))
        self.set_color_selected_geometry("nurbs",my_color("#D1D2D5")) # #E14B3B #EC1559
        self.set_color_selected_geometry("points",my_color("#FF93CC"))

        # RGB colors
        self.set_color_selected_patch("mesh",my_color("#EDAA4E"))
        self.set_color_selected_patch("nurbs",my_color("#1C8B98"))
        self.set_color_selected_patch("points",my_color("#D9007E"))

        # RGB colors
        self.set_color_viewer("selection_points",my_color("#006699"))
        self.set_color_viewer("marker_points",my_color("#339798"))
        self.set_color_viewer("selection",my_color("#CCCC99"))
        self.set_color_viewer("background",my_color("#10C8CD"))
        self.set_color_viewer("grid",my_color("lightgreen"))
        self.set_color_viewer("default_geometry",my_color("#983265"))
        self.set_color_viewer("default_patch",my_color("#983265"))
        self.set_color_viewer("default_mesh",my_color("white"))
        self.set_color_viewer("default_points",my_color("magenta"))

        self.set_size_points("selection_points",6.)
        self.set_size_points("marker_points",6.)
        self.set_size_points("geometry",6.)
        self.set_size_points("patch",6.)
        self.set_size_points("grid",2.)

        # RGB colors
        self.set_color_inspector("background",my_color("white"))
        self.set_color_inspector("show_text",my_color("black"))
        self.set_color_inspector("hide_text",my_color("red"))
        self.set_color_inspector("show_background",my_color("white"))
        self.set_color_inspector("hide_background",my_color("white"))

    def joepass(self):
        self.set_alpha(1.)
        self.set_beta(1.)
        self.set_alpha_bg(1.)
        self.set_enable_blend(True)
        self.set_enable_inspector_color(False)

        # RGB colors
        self.set_color_selected_geometry("mesh",[0.2,0.1,0.57])
        self.set_color_selected_geometry("nurbs",[0.5,0.5,0.5])
        self.set_color_selected_geometry("points",[0.1,0.1,0.1])

        # RGB colors
        self.set_color_selected_patch("mesh",[0.65,0.65,0.65])
        self.set_color_selected_patch("nurbs",my_color("red"))
        self.set_color_selected_patch("points",[0.2,0.2,0.2])

        # RGB colors
        self.set_color_viewer("selection_points",[1.,0.,0.])
        self.set_color_viewer("marker_points",[0.25,0.25,0.95])
        self.set_color_viewer("selection",[0.1,0.1,0.1])
        self.set_color_viewer("background",[0.0, 0.0, 0.0])
        self.set_color_viewer("grid",[1.0, 1.0, 1.0])
        self.set_color_viewer("default_geometry",[0.1,0.3,0.2])
        self.set_color_viewer("default_patch",[0.1,0.3,0.2])
        self.set_color_viewer("default_mesh",[1.,1.,1.])
        self.set_color_viewer("default_points",[0.1,0.1,0.1])

        self.set_size_points("selection_points",6.)
        self.set_size_points("marker_points",6.)
        self.set_size_points("geometry",6.)
        self.set_size_points("patch",6.)
        self.set_size_points("grid",2.)

        # RGB colors
        self.set_color_inspector("background",my_color("white"))
        self.set_color_inspector("show_text",my_color("black"))
        self.set_color_inspector("hide_text",my_color("red"))
        self.set_color_inspector("show_background",my_color("white"))
        self.set_color_inspector("hide_background",my_color("white"))
