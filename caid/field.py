# -*- coding: UTF-8 -*-
import sys
import numpy as np
from numpy import array, linspace, zeros, zeros_like
from caid.cad_geometry import cad_geometry

try:
    from OpenGL.arrays import vbo
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
except:
    print('''ERROR: PyOpenGL not installed properly.''')

class field(object):
    def __init__(self, geometry=None, values=None, type='scalar'):
        """
        both geometry and values are cad_geometry objects
        geometry is needed to define the mapping
        while values is needed to store the B-splines/NURBS coefficients
        """
        self.geometry = geometry
        self.values   = values

        self._surface   = False
        self._show      = False
        self._type      = 'scalar'

    def set_geometry(self, geo):
        self.geometry = geo

    def set_values(self, values):
        self.values = values

    @property
    def fieldtype(self):
        return self._type

    @property
    def dim(self):
        return self.geometry.dim

    @property
    def coefficients(self):
        if self.values is not None:
            return [srf.points for srf in self.values]
        else:
            return None

    def get_vertex(self, id, ijk):
        pass

    def Draw(self):
        pass

    def set_surface(self, value):
        self._surface = value

    @property
    def surface(self):
        return self._surface

    def Show(self, value):
        self._show = value

    @property
    def show(self):
        return self._show

    def open(self, filename):
        from caid.cad_geometry import cad_geometry
        from caid.io import XML
        io = XML()

        from xml.dom.minidom import parse
        doc = parse(filename)
        rootElt = doc.documentElement

        # read attributs
        # get camera attributs
    #    eye = strtoArray(rootElt.getAttribute("eye"))
    #    self.viewer.lookAt.SetEye(eye)

        # geometry
        geoElt = rootElt.getElementsByTagName("geometry")[0]
        geo = cad_geometry()
        io.xmltogeo(geo, doc, geoElt)

        # ... values
        valuesElt = rootElt.getElementsByTagName("values")[0]
        values = cad_geometry()
        io.xmltogeo(values, doc, valuesElt)

        self.set_geometry(geo)
        self.set_values(values)

    def save(self, filename):
        # ... create xml doc
        from xml.dom.minidom import Document
        # Create the minidom document
        doc = Document()
        # Create the <caid> base element
        rootElt = doc.createElement("field")
        # set camera attributs
    #    eye = self.viewer.lookAt.GetEye()
    #    rootElt.setAttribute("eye", str(eye))

        doc.appendChild(rootElt)
        from caid.io import XML
        io = XML()
        # ... geometry
        geoElt = doc.createElement("geometry")
        geo = self.geometry
        doc = io.geotoxml(geo, doc, geoElt)
        rootElt.appendChild(geoElt)
        # ... geometry
        valuesElt = doc.createElement("values")
        values = self.values
        doc = io.geotoxml(values, doc, valuesElt)
        rootElt.appendChild(valuesElt)

        if filename is not None:
            f = open(filename, 'wr')
            s = doc.toprettyxml()
            f.write(s)
            f.close()
        else:
            print("No file was specified")

    def view(self, colormap=None, colorbar=None, n=None):
        V = viewer()
        if colormap is None:
            from caid.graphics.colormap import IceAndFire
            colormap = IceAndFire
        V.set_field(self)
        V.main(colormap=colormap, colorbar=colorbar, n=n)

    def VertexBuffer(self,n=None):
        if self.fieldtype == "scalar":
            return self.VertexBufferScalar(n=n)
        else:
            raise("Field type not yet used")

    def VertexBufferScalar(self,n=None):
        if self.dim == 1:
            return self.VertexBufferScalar_1d(n=n)
        if self.dim == 2:
            return self.VertexBufferScalar_2d(n=n)
        if self.dim == 3:
            return self.VertexBufferScalar_3d(n=n)

    def VertexBufferScalar_1d(self,n=None):
        list_arrays = []
        for id in range(0, self.geometry.npatchs):
            nrb = self.geometry[id]
            srf = self.values[id]
            if n is not None:
                nx = n[0]
            else:
                nx = nrb.shape
            ub = nrb.knots[0][0] ; ue = nrb.knots[0][-1]
            u = linspace(ub,ue,nx)

            array_vertex = zeros((2*(nx-1),4))
            P = nrb(u)
            A = srf(u)
            vertex_ID = 0
            for i in range(0,nx-1):
                x = P[i+1,0] ; y = P[i+1,1] ; z = P[i+1,2]
                a = A[i+1,0]
                array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                vertex_ID += 1

                x = P[i,0] ; y = P[i,1] ; z = P[i,2]
                a = A[i,0]
                array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                vertex_ID += 1
            if self.surface:
                array_vertex[:,2] = array_vertex[:,3]
            list_arrays.append(array_vertex)
        return list_arrays

    def VertexBufferScalar_2d(self,n=None):
        list_arrays = []
        for id in range(0, self.geometry.npatchs):
            nrb = self.geometry[id]
            srf = self.values[id]
            if n is not None:
                nx = n[0] ; ny = n[1]
            else:
                nx,ny = nrb.shape
            ub = nrb.knots[0][0] ; ue = nrb.knots[0][-1]
            u = linspace(ub,ue,nx)
            vb = nrb.knots[1][0] ; ve = nrb.knots[1][-1]
            v = linspace(vb,ve,ny)

            array_vertex = zeros((4*(nx-1)*(ny-1),4))
            P = nrb(u,v)
            A = srf(u,v)
            vertex_ID = 0
            for j in range(0,ny-1):
                for i in range(0,nx-1):
                    x = P[i+1,j,0] ; y = P[i+1,j,1] ; z = P[i+1,j,2]
                    a = A[i+1,j,0]
                    array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                    vertex_ID += 1

                    x = P[i+1,j+1,0] ; y = P[i+1,j+1,1] ; z = P[i+1,j+1,2]
                    a = A[i+1,j+1,0]
                    array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                    vertex_ID += 1

                    x = P[i,j+1,0] ; y = P[i,j+1,1] ; z = P[i,j+1,2]
                    a = A[i,j+1,0]
                    array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                    vertex_ID += 1

                    x = P[i,j,0] ; y = P[i,j,1] ; z = P[i,j,2]
                    a = A[i,j,0]
                    array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                    vertex_ID += 1
            if self.surface:
                array_vertex[:,2] = array_vertex[:,3]
            list_arrays.append(array_vertex)
        return list_arrays

    def VertexBufferScalar_3d(self,n=None):
        list_arrays = []
        for id in range(0, self.geometry.npatchs):
            nrb = self.geometry[id]
            srf = self.values[id]
            if n is not None:
                nx = n[0] ; ny = n[1] ; nz = n[2]
            else:
                nx,ny = nrb.shape
            ub = nrb.knots[0][0] ; ue = nrb.knots[0][-1]
            u = linspace(ub,ue,nx)
            vb = nrb.knots[1][0] ; ve = nrb.knots[1][-1]
            v = linspace(vb,ve,ny)
            wb = nrb.knots[2][0] ; we = nrb.knots[2][-1]
            w = linspace(wb,we,ny)

            array_vertex = zeros((8*(nx-1)*(ny-1)*(nz-1),4))
            P = nrb(u,v,w)
            A = srf(u,v,w)
            vertex_ID = 0
            for k in range(0,nz-1):
                for j in range(0,ny-1):
                    for i in range(0,nx-1):
                        # ... first face
                        x = P[i+1,j,k,0] ; y = P[i+1,j,k,1] ; z = P[i+1,j,k,2]
                        a = A[i+1,j,k,0]
                        array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                        vertex_ID += 1

                        x = P[i+1,j+1,k,0] ; y = P[i+1,j+1,k,1] ; z = P[i+1,j+1,k,2]
                        a = A[i+1,j+1,k,0]
                        array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                        vertex_ID += 1

                        x = P[i,j+1,k,0] ; y = P[i,j+1,k,1] ; z = P[i,j+1,k,2]
                        a = A[i,j+1,k,0]
                        array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                        vertex_ID += 1

                        x = P[i,j,k,0] ; y = P[i,j,k,1] ; z = P[i,j,k,2]
                        a = A[i,j,k,0]
                        array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                        vertex_ID += 1
                        # ...

                        # ... second face
                        x = P[i+1,j,k+1,0] ; y = P[i+1,j,k+1,1] ; z = P[i+1,j,k+1,2]
                        a = A[i+1,j,k+1,0]
                        array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                        vertex_ID += 1

                        x = P[i+1,j+1,k+1,0] ; y = P[i+1,j+1,k+1,1] ; z = P[i+1,j+1,k+1,2]
                        a = A[i+1,j+1,k+1,0]
                        array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                        vertex_ID += 1

                        x = P[i,j+1,k+1,0] ; y = P[i,j+1,k+1,1] ; z = P[i,j+1,k+1,2]
                        a = A[i,j+1,k+1,0]
                        array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                        vertex_ID += 1

                        x = P[i,j,k+1,0] ; y = P[i,j,k+1,1] ; z = P[i,j,k+1,2]
                        a = A[i,j,k+1,0]
                        array_vertex[vertex_ID,:] = np.array([x,y,z,a])
                        vertex_ID += 1
                        # ...

            if self.surface:
                array_vertex[:,2] = array_vertex[:,3]
            list_arrays.append(array_vertex)
        return list_arrays

# Vertex Shader
str_VS = """
varying vec4 vertex_color;
void main()
{
gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
vertex_color = gl_Color;
}
"""

# Fragment Shader
str_FS = """
varying vec4 vertex_color;
void main()
{
gl_FragColor = vertex_color;
}
"""

from caid.graphics.viewer import viewer as basic_viewer
from caid.graphics.viewer import Action, Menu
class viewer(basic_viewer):
    def __init__(self, colormap=None, field=None, colorbar=None, title="", size=(100,100) \
                , backGroundColor=(1.0, 1.0, 1.0, 0.0)):

        self._colormap = colormap
        self._field = field
        self._colorbar = colorbar
        self._show_colorbar = True
        self._side_colorbar = 'left'

        self._resolution = array([10,10,10])

        my_menu = self.create_menu()

        # ------------------------------------------
        basic_viewer.__init__(self, title=title, size=size \
                 , str_VS=str_VS, str_FS=str_FS, vertex_shader=GL_QUADS\
                , backGroundColor=backGroundColor \
                , vbo  = None \
                , menu = my_menu)
        # ------------------------------------------

    def menu_colormap_Ice(self):
        from caid.graphics.colormap import Ice as cmap
        self.update(colormap=cmap, force=True)
        self.Refresh()

    def menu_colormap_Hot(self):
        from caid.graphics.colormap import Hot as cmap
        self.update(colormap=cmap, force=True)
        self.Refresh()

    def menu_colormap_IceAndFire(self):
        from caid.graphics.colormap import IceAndFire as cmap
        self.update(colormap=cmap, force=True)
        self.Refresh()

    def menu_colormap_Fire(self):
        from caid.graphics.colormap import Fire as cmap
        self.update(colormap=cmap, force=True)
        self.Refresh()

    def menu_colormap_Grey(self):
        from caid.graphics.colormap import Grey as cmap
        self.update(colormap=cmap, force=True)
        self.Refresh()

    def menu_colormap_Grey_r(self):
        from caid.graphics.colormap import Grey_r as cmap
        self.update(colormap=cmap, force=True)
        self.Refresh()

    def menu_colormap_DarkRed(self):
        from caid.graphics.colormap import DarkRed as cmap
        self.update(colormap=cmap, force=True)
        self.Refresh()

    def menu_colormap_DarkGreen(self):
        from caid.graphics.colormap import DarkGreen as cmap
        self.update(colormap=cmap, force=True)
        self.Refresh()

    def menu_colormap_DarkBlue(self):
        from caid.graphics.colormap import DarkBlue as cmap
        self.update(colormap=cmap, force=True)
        self.Refresh()

    def menu_colormap_LightRed(self):
        from caid.graphics.colormap import LightRed as cmap
        self.update(colormap=cmap, force=True)
        self.Refresh()

    def menu_colormap_LightGreen(self):
        from caid.graphics.colormap import LightGreen as cmap
        self.update(colormap=cmap, force=True)
        self.Refresh()

    def menu_colormap_LightBlue(self):
        from caid.graphics.colormap import LightBlue as cmap
        self.update(colormap=cmap, force=True)
        self.Refresh()

    def menu_elevate(self):
        self.field.set_surface(True)
        if self.colorbar is not None:
            self.colorbar.set_surface(True)
        self.Clean()
        self.update(force=True)
        self.Refresh()

    def menu_reduce(self):
        self.field.set_surface(False)
        if self.colorbar is not None:
            self.colorbar.set_surface(False)
        self.resetView()
        self.Clean()
        self.update(force=True)
        self.Refresh()

    def menu_save(self):
        print("Save TODO")

    def menu_resolution(self):
        print("Resolution TODO")

    def menu_reset(self):
        self.resetView()
        self.Clean()
        self.update(force=True)
        self.Refresh()

    def menu_colorbar_show(self):
        show_colorbar = self.show_colorbar
        self.set_show_colorbar(not show_colorbar)
        self.Clean()
        self.update(force=True)
        self.Refresh()

    def menu_colorbar_left(self):
        self.set_show_colorbar(True)
        self.set_side_colorbar('left')
        self.Clean()
        self.update(force=True)
        self.Refresh()

    def menu_colorbar_right(self):
        self.set_show_colorbar(True)
        self.set_side_colorbar('right')
        self.Clean()
        self.update(force=True)
        self.Refresh()

    def menu_colorbar_top(self):
        self.set_show_colorbar(True)
        self.set_side_colorbar('top')
        self.Clean()
        self.update(force=True)
        self.Refresh()

    def menu_colorbar_bottom(self):
        self.set_show_colorbar(True)
        self.set_side_colorbar('bottom')
        self.Clean()
        self.update(force=True)
        self.Refresh()

    def create_menu(self):

        list_actions_menu = []
        list_actions_menu.append(Action(self.menu_elevate, "Elevate"))
        list_actions_menu.append(Action(self.menu_reduce, "Reduce"))
        list_actions_menu.append(Action(self.menu_save, "Save"))
        list_actions_menu.append(Action(self.menu_reduce, "Resolution"))
        list_actions_menu.append(Action(self.menu_reset, "Reset"))

        list_actions_colormap = []
        list_actions_colormap.append(Action(self.menu_colormap_Ice, "Ice"))
        list_actions_colormap.append(Action(self.menu_colormap_Hot, "Hot"))
        list_actions_colormap.append(Action(self.menu_colormap_IceAndFire, "IceAndFire"))
        list_actions_colormap.append(Action(self.menu_colormap_Fire, "Fire"))
        list_actions_colormap.append(Action(self.menu_colormap_Grey, "Grey"))
        list_actions_colormap.append(Action(self.menu_colormap_Grey_r, "Grey_r"))
        list_actions_colormap.append(Action(self.menu_colormap_DarkRed, "DarkRed"))
        list_actions_colormap.append(Action(self.menu_colormap_DarkGreen, "DarkGreen"))
        list_actions_colormap.append(Action(self.menu_colormap_DarkBlue, "DarkBlue"))
        list_actions_colormap.append(Action(self.menu_colormap_LightRed, "LightRed"))
        list_actions_colormap.append(Action(self.menu_colormap_LightGreen, "LightGreen"))
        list_actions_colormap.append(Action(self.menu_colormap_LightBlue, "LightBlue"))

        list_actions_colorbar = []
        list_actions_colorbar.append(Action(self.menu_colorbar_show, "Show"))
        list_actions_colorbar.append(Action(self.menu_colorbar_left, "Left"))
        list_actions_colorbar.append(Action(self.menu_colorbar_right, "Right"))
        list_actions_colorbar.append(Action(self.menu_colorbar_top, "Top"))
        list_actions_colorbar.append(Action(self.menu_colorbar_bottom, "Bottom"))

        my_menu = Menu()
        my_menu.append(list_actions_menu, label="Menu")
        my_menu.append(list_actions_colormap, label="ColorMap")
        my_menu.append(list_actions_colorbar, label="ColorBar")

        return my_menu

    @property
    def field(self):
        return self._field

    @property
    def vbo(self):
        return self._vbo

    @property
    def colormap(self):
        return self._colormap

    def setColotMap(self, colormap):
        self._colormap = colormap

    @property
    def colorbar(self):
        return self._colorbar

    def setColotBar(self, colorbar):
        self._colorbar = colorbar

    def set_show_colorbar(self, value):
        self._show_colorbar = value

    @property
    def show_colorbar(self):
        return self._show_colorbar

    def setColotMap(self, colormap):
        self._colormap = colormap

    def set_field(self, field):
        self._field = field

    @property
    def resolution(self):
        return self._resolution

    def set_resolution(self, n):
        self._resolution = n

    def set_side_colorbar(self, side, nvalues=10):
        from caid.graphics.colorbar import colorbar as cbar
        # Create a colorbar array...
        C = np.linspace(self.vmin,self.vmax,nvalues).astype(np.float32)
        colorbar = cbar(C, colormap=self.colormap, side=side)
        self._colorbar = colorbar
        self._side_colorbar = side

    def main(self, colormap=None, colorbar=None, field=None, clean=False, n=None, force=False):
        self.update(colormap=colormap, colorbar=colorbar, field=field, clean=clean, n=n, force=force)

        glutMainLoop()

    def update(self, colormap=None, colorbar=None, field=None, clean=False, n=None, force=False):
        if colormap is not None:
            self._colormap = colormap
            force = True
        if colorbar is not None:
            self._colorbar = colorbar
            force = True
        if field is not None:
            self._field = field
            force = True

        print("show_colorbar ", self.show_colorbar)
        self.updateVertexBuffer(colormap=colormap, field=field, n=n, force=force)

        if self.show_colorbar:
            if self.colorbar is None:
                from caid.graphics.colorbar import colorbar as cbar
                # Create a colorbar array...
                nvalues = 10
                C = np.linspace(self.vmin,self.vmax,nvalues).astype(np.float32)
                colorbar = cbar(C, colormap=colormap, side='left'\
                               , xmin = self.xmin \
                               , ymin = self.ymin \
                               , zmin = self.zmin \
                               , xmax = self.xmax \
                               , ymax = self.ymax \
                               , zmax = self.zmax \
                               )
                self._colorbar = colorbar
            print(">>> Enter colorbar VB")
            self.updateVertexBuffer(  colormap=colormap \
                                    , field=self.colorbar \
                                    , n=[10,10] \
                                    , force=force)

        self.finalizeVertexBuffer(colormap=colormap, field=self.colorbar, n=n, force=force)

    def updateVertexBuffer(self, colormap=None, field=None, n=None, force=False):
        if colormap is None:
            colormap = self.colormap

        if field is None:
            field = self.field

        print("force ", force)

        if not force:
            return

        # .....................................
        V = field.VertexBuffer(n=n)[0].astype(np.float32)
        basic_viewer.updateVertexBuffer(self, V)

    def finalizeVertexBuffer(self, colormap=None, field=None, n=None, force=False):
        cmap = self.colormap
        F    = field

        LUT = cmap.LUT['rgb']

        Z = self.v_array[:,3]
        zmin = np.min(Z)
        zmax = np.max(Z)

        if np.abs(zmax-zmin) < 1.e-7:
            return

        # LUT.size = bad + under + actual # colors + over
        Zn = (Z-zmin)
        Zn *= (LUT.size-3-1)/float(zmax-zmin)
        Zi = Zn.astype(np.int)

        ## Zn holds unranged indices of colors
        ## At this stage, they can be negative or superior to LUT.size-3
        #
        ## Set negative indices to become 'under' color (1)
        ##  and increment others by 2 to skip bad and under colors
        #Zi = np.maximum (Zi+2, 1)
        #
        ## Set out-of-range indices to be 'over' color (LUT.size-1)
        #Zi = np.minimum (Zi, LUT.size-1)
        #
        ## Replace too high indices with 'over' color index ( = 1)
        #
        ## Replace bad indices with 'bad' color
        #Zi = np.multiply(Zi, 1-np.isnan(Z))

        I = LUT.take(Zi,mode='clip').view((np.float32,3))
        # .....................................

        self.v_array[:,3:] = I

# ------------------------------------------
if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        filename = "U.pfl"

    F = field()
    F.open(filename)
    F.Show(True)
    F.set_surface(False)

    from caid.graphics.colormap import *
    list_cmap = [  IceAndFire, Ice, Fire \
                 , Hot, Grey, Grey_r \
                 , DarkRed, DarkGreen, DarkBlue \
                 , LightRed, LightGreen, LightBlue]

    cmap = Hot

#    cmap.set_under(0.,0.,0.,0.)
#    cmap.set_over(0.,0.,0.,0.)
#    cmap.set_under(1.,1.,1.,0.)
#    cmap.set_bad(1.,0.,1.,0.)


#    V = viewer()
#    V.main(colormap=list_cmap[0], field=F, n=[100,100])

    F.view(colormap=cmap, n=[100,100])

