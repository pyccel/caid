# -*- coding: UTF-8 -*-

#!/usr/bin/python

'''Spinning cube wxPython and PyOpenGL app'''

import wx
from wx.glcanvas import *

#import OpenGL
#from OpenGL import GLUT
#from OpenGL import GLU
#from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from MenuCAIDViewer import MenuCAIDViewer
from geometry import geometry, pointsToList
from caid.cad_geometry import cad_geometry, bilinear
import numpy as np
from numpy import zeros
from math import copysign
from theme import theme
from viewerPreferences import PreferencesDialog

from numpy import sin, cos, pi, abs, matrix, array, asarray

Near    = 1.0
Far     = 20.0

def FloatToStr(x):
    return float("{0:.2f}".format(x))

def findIndex(list_x,list_y, xmin, xmax, ymin, ymax):
    list_ind = []
    i = 0
    for x,y in zip(list_x,list_y):
        if xmin < x < xmax and ymin < y < ymax:
            list_ind.append(i)
        i += 1
    return np.asarray(list_ind)

def fromIndexToCoord(nrb,ind):
    if nrb.dim == 1:
        return ind
    if nrb.dim == 2:
        nx = nrb.shape[0] ; ny = nrb.shape[1]
        ix = ind / ny
        iy = ind - ny*ix
        return ix,iy

class LookAt():
    def __init__(self):
        self.eye    = [0.,0.,5.]
        self.center = [0.,0.,0.]
        self.up     = [0.,1.,0.]

    def SetEye(self, values):
        self.eye = values

    def SetCenter(self, values):
        self.center = values

    def SetUp(self, values):
        self.up = values

    def GetEye(self):
        return self.eye

    def GetCenter(self):
        return self.center

    def GetUp(self):
        return self.up

class SelectedPoints(object):
    def __init__(self, patch):
        # the selected patch
        self._patch = patch
        # index for each selected control point
        self.list_index = []
        # coordinates of each selected control point
        self.list_P     = []

    def addPointsByIndices(self, list_ijk):
        """
        insert new Control Points by giving their indices
        1D case : i
        2D case : i,j
        3D case : i,j,k
        """
        patch = self.patch

        if patch.dim == 1:
            for i in list_ijk:
                ijkP = [i]
                self.list_index.append(ijkP)
                P = patch.points[i,:3]
                self.list_P.append(P)
        if patch.dim == 2:
            list_i = list_ijk[0]
            list_j = list_ijk[1]
            for i,j in zip(list_i, list_j):
                ijkP = [i,j]
                self.list_index.append(ijkP)
                P = patch.points[i,j,:3]
                self.list_P.append(P)

    @property
    def points(self):
        return self.list_P

    @property
    def indices(self):
        return self.list_index

    @property
    def patch(self):
        return self._patch

    def clean(self):
        # index for each selected control point
        self.list_index = []
        # coordinates of each selected control point
        self.list_P     = []

class Viewer (GLCanvas):
    '''Actual OpenGL scene'''
    #
    def __init__ (self, workgroup, parent, attribs = None, id = wx.ID_ANY \
                  , pos=wx.DefaultPosition, size=wx.Size(400,400) \
                 , theme=theme()):
        if not attribs:
            attribs = [WX_GL_RGBA, WX_GL_DOUBLEBUFFER, WX_GL_DEPTH_SIZE, 24]
        frame = wx.Frame(parent = parent, id = wx.ID_ANY,
                    title="Viewer",
                    pos = pos, size = size)
        GLCanvas.__init__(self, frame, id, attribList = attribs)
        self.context = GLContext(self)
        self.frame = frame
        self.WorkGroup = workgroup
        self.init   = False
        self.width  = 0
        self.height = 0
        self._theme = theme
        # Display event handlers
        self.Bind(wx.EVT_PAINT      , self.OnPaint)
        self.Bind(wx.EVT_SIZE       , self.OnSize)
        # Mouse handlers
        self.Bind(wx.EVT_MOUSEWHEEL , self.OnMouseWheel)
        self.Bind(wx.EVT_LEFT_DOWN  , self.OnMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP    , self.OnMouseLeftUp)
        self.Bind(wx.EVT_MOTION     , self.OnMouseMotion)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightMouseClick)
        # keyboard handlers
        self.Bind(wx.EVT_CHAR       , self.key)
        self.Bind(wx.EVT_KEY_DOWN   , self.onKeyPressDown)
        self.Bind(wx.EVT_KEY_UP     , self.onKeyPressUp)

        # viewer 2D or 3D mode
        self.active2D = True
        # show/hide  grid
        self.showGrid = False
        # the grid can be drawn as lines or points
        self.showGridLines = True

        # steps used for mesh Evaluator
        self.evaluator_steps            = [2,2,2]

        # Wheel sensitivity used for Zoom
        self.WheelSensitivity = 0.5
        # TODO must be updated when zooming
        self.unit = 3.

        # cutCurveFreq used for the frequency sampling when moving the cursor
        self.cutCurveFreq   = 5
        self.CutCurvePoints = []

        # handles viewer eye/...
        self.lookAt = LookAt()

        # initial mouse position
        self.lastx = self.x = 30
        self.lasty = self.y = 30

        # used for the 2D grid
        self.rowmin = -5. ; self.rowmax = 5.
        self.colmin = -5. ; self.colmax = 5.
        self.hx = 1.; self.hy = 1.

        # used for selection mode
        self.cornerx = None
        self.cornery = None

        # Data Selection
        self.EnabledSelectionMode = False
        # Look At => define a viewing transformation
        self.EnabledLookAtMode = False
        # Marker points
        self.EnabledMarkerMode = False
        # EnabledLookAtModeID = 0 ==> update center position
        # EnabledLookAtModeID = 1 ==> update the up vector
        # Otherwise ==> nothing to do
        self.EnabledLookAtModeID = -1

        # cut Curve Mode
        self.EnabledCutCurveMode = False

        # contains the list of marker points, picked directly on the viewer
        # TODO use numpy array rather than a list
        self.MarkerPoints = []
        self.fixMarkers = False
        # contains the list of selected points, picked directly on the viewer
        # list_SelectedPoints is a list of SelectedPoints class
        self.list_SelectedPoints = []

        self.SetFocus()

        self.statusbar = self.frame.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        self.menu_titles = ["2D view", "3D view" \
                            , "Show Grid", "Hide Grid"\
                            , "Grid as Points", "Grid as Lines"\
                            , "Clear Markers", "Clear Selected Points" \
                            , "Fixed Markers", "Floating Markers"\
                            , "Add Marker"\
                            , "Import Markers"\
                            , "Export Markers"\
                            , "Print", "Preferences" ]

        self.menu_title_by_id = {}
        for title in self.menu_titles:
            self.menu_title_by_id[ wx.NewId() ] = title

    @property
    def theme(self):
        return self._theme

    def set_theme(self, value):
        self._theme.set_theme(value)

    # ...
    @property
    def alpha(self):
        return self.theme.alpha

    def set_alpha(self, alpha):
        self.theme.set_alpha(alpha)
    # ...

    # ...
    @property
    def beta(self):
        return self.theme.beta

    def set_beta(self, beta):
        self.theme.set_beta(beta)
    # ...

    # ...
    @property
    def alpha_bg(self):
        return self.theme.alpha_bg

    def set_alpha_bg(self, alpha):
        self.theme.set_alpha_bg(alpha)
    # ...

    # ...
    @property
    def enableBlend(self):
        return self.theme.enable_blend

    def set_enableBlend(self, value):
        self.theme.set_enable_blend(value)
    # ...

    # ...
    @property
    def color_background(self):
        return self.theme.color_viewer("background")

    def set_color_background(self, value=None):
        if value is not None:
            self.theme.set_color_viewer("background", value)
    # ...

    # ...
    @property
    def color_grid(self):
        return self.theme.color_viewer("grid")

    def set_color_grid(self, value=None):
        if value is not None:
            self.theme.set_color_viewer("grid", value)
    # ...

    # ...
    @property
    def size_GridPoints(self):
        return self.theme.size_points('grid')

    def set_size_GridPoints(self, value=None):
        if value is not None:
            self.theme.set_size_points('grid', value)
    # ...

    # ...
    @property
    def color_selectedPoints(self):
        return self.theme.color_viewer("selection_points")

    def set_color_selectedPoints(self, color, alpha=None):
        if alpha is None:
            alpha = self.alpha
        if color is None:
            print("Warning Selected Points Color is None")
        else:
            if len(color) == 3:
                color.append(alpha)
        self.theme.set_color_viewer("selection_points", color)
    # ...

    # ...
    @property
    def color_markerPoints(self):
        return self.theme.color_viewer("marker_points")

    def set_color_markerPoints(self, color, alpha=None):
        if alpha is None:
            alpha = self.alpha
        if color is None:
            print("Warning Marker Points Color is None")
        else:
            if len(color) == 3:
                color.append(alpha)
        self.theme.set_color_viewer("marker_points", color)
    # ...

    # ...
    @property
    def color_selectedGeoMesh(self):
        return self.theme.color_selected_geometry('mesh')

    def set_color_selectedGeoMesh(self, value=None):
        if value is not None:
            self.theme.set_color_selected_geometry('mesh', value)
    # ...

    # ...
    @property
    def color_selectedGeoNurbs(self):
        return self.theme.color_selected_geometry('nurbs')

    def set_color_selectedGeoNurbs(self, value=None):
        if value is not None:
            self.theme.set_color_selected_geometry('nurbs', value)
    # ...

    # ...
    @property
    def color_selectedGeoPoints(self):
        return self.theme.color_selected_geometry('points')

    def set_color_selectedGeoPoints(self, value=None):
        if value is not None:
            self.theme.set_color_selected_geometry('points', value)
    # ...

    # ...
    @property
    def color_selectedPatchMesh(self):
        return self.theme.color_selected_patch('mesh')

    def set_color_selectedPatchMesh(self, value=None):
        if value is not None:
            self.theme.set_color_selected_patch('mesh', value)
    # ...

    # ...
    @property
    def color_selectedPatchNurbs(self):
        return self.theme.color_selected_patch('nurbs')

    def set_color_selectedPatchNurbs(self, value=None):
        if value is not None:
            self.theme.set_color_selected_patch('nurbs', value)
    # ...

    # ...
    @property
    def color_selectedPatchPoints(self):
        return self.theme.color_selected_patch('points')

    def set_color_selectedPatchPoints(self, value=None):
        if value is not None:
            self.theme.set_color_selected_patch('points', value)
    # ...

    # ...
    @property
    def size_MarkerPoints(self):
        return self.theme.size_points('marker_points')

    def set_size_MarkerPoints(self, value=None):
        if value is not None:
            self.theme.set_size_points('marker_points', value)
    # ...

    # ...
    @property
    def size_SelectedPoints(self):
        return self.theme.size_points('selection_points')

    def set_size_SelectedPoints(self, value=None):
        if value is not None:
            self.theme.set_size_points('selection_points',value)
    # ...

    # ...
    def AddMarkerPoint(self, P):
        self.MarkerPoints.append(P)
        self.statusbar.SetStatusText("Add a new Marker")

    def SetMarkerPoints(self, list_markers):
        self.MarkerPoints = list_markers
        self.statusbar.SetStatusText("Set a new Markers list")

    def CleanMarkerPoints(self):
        self.MarkerPoints = []
        self.statusbar.SetStatusText("Cleaning Marker Points")

    @property
    def nMarkerPoints(self):
        return len(self.MarkerPoints)

    def FindMarkerPoint(self, P):
        # returns the index of a marker point
        return self.MarkerPoints.index(P)
    # ...

    # ...
    def AddSelectedPoints(self, selectedPoints):
        self.list_SelectedPoints.append(selectedPoints)
        self.statusbar.SetStatusText("Add new Selected Points")

    def CleanSelectedPoints(self):
        self.list_SelectedPoints = []
        self.statusbar.SetStatusText("Cleaning Selected Points")
    # ...

    # ...
    def AddCutCurvePoint(self, P):
        self.CutCurvePoints.append(P)

    def CleanCutCurvePoints(self):
        self.CutCurvePoints = []
    # ...

    # ...
    def Show(self,value):
        self.frame.Show(value)

    def Set2DMode(self):
        self.active2D = True
        self.statusbar.SetStatusText("2D mode enabled")

    def Set3DMode(self):
        self.active2D = False
        self.statusbar.SetStatusText("3D mode enabled")

    def ShowGrid(self):
        self.showGrid = True
        self.statusbar.SetStatusText("Show Grid")

    def HideGrid(self):
        self.showGrid = False
        self.statusbar.SetStatusText("Hide Grid")

    def GetEnabledSelectionMode(self):
        return self.EnabledSelectionMode

    def SetEnabledSelectionMode(self, value):
        self.EnabledSelectionMode =  value

    def GetEnabledLookAtMode(self):
        return self.EnabledLookAtMode

    def SetEnabledLookAtMode(self, value):
        self.EnabledLookAtMode =  value

    def GetEnabledMarkerMode(self):
        return self.EnabledMarkerMode

    def SetEnabledMarkerMode(self, value):
        self.EnabledMarkerMode =  value

    def GetEnabledCutCurveMode(self):
        return self.EnabledCutCurveMode

    def SetEnabledCutCurveMode(self, value):
        self.EnabledCutCurveMode =  value

    def get_rowmin(self):
        return self.rowmin

    def set_rowmin(self, value=None):
        if value is not None:
            self.rowmin = value

    def get_rowmax(self):
        return self.rowmax

    def set_rowmax(self, value=None):
        if value is not None:
            self.rowmax = value

    def get_colmin(self):
        return self.colmin

    def set_colmin(self, value=None):
        if value is not None:
            self.colmin = value

    def get_colmax(self):
        return self.colmax

    def set_colmax(self, value=None):
        if value is not None:
            self.colmax = value

    def get_hx(self):
        return self.hx

    def set_hx(self, value=None):
        if value is not None:
            self.hx = value

    def get_hy(self):
        return self.hy

    def set_hy(self, value=None):
        if value is not None:
            self.hy = value

    def get_wheelSensitivity(self):
        return self.WheelSensitivity

    def set_wheelSensitivity(self, value=None):
        if value is not None:
            self.WheelSensitivity = value

    def set_showGridLines(self, value):
        self.showGridLines = value
    #
    def OnPaint (self, event):
        self.OnDraw()

    def OnDraw(self, clear=True):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.initGL()
        if clear:
            self.clear()
        self.setProjection()
        self.setViewpoint()
        self.drawWorld()
        self.SwapBuffers()
    #
    def OnSize (self, event):
        # Note these are ints, not floats, for glViewport
        self.width, self.height = self.GetSizeTuple()
    #
    def initGL (self):
        colorBg = list(self.color_background) + [self.alpha_bg]
        glClearColor(*colorBg)
        self.init = True
#        glutInitDisplayMode(GLUT_RGB)
    #
    def clear (self):
        glViewport(0, 0, self.width, self.height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #
    def setProjection (self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, float(self.width) / float(self.height), Near, Far)
        glMatrixMode(GL_MODELVIEW)
    #
    def setViewpoint (self):
        glLoadIdentity()
        xeye,yeye,zeye = self.lookAt.GetEye()
        xcenter,ycenter,zcenter = self.lookAt.GetCenter()
        xup,yup,zup = self.lookAt.GetUp()
        gluLookAt(xeye,yeye,zeye   \
                  ,xcenter,ycenter,zcenter  \
                  ,xup,yup,zup  )
        txt = [FloatToStr(x) for x in self.lookAt.GetCenter()]
#        self.statusbar.SetStatusText('View Point has been changed to ' +
#                                     str(txt) )

    #
    def highLightSelection(self):
        wk = self.WorkGroup
        # Highlight geometry
        geo = wk.inspector.currentGeometry
        if geo is not None:
            MeshColorGeo    = self.color_selectedGeoMesh
            NurbsColorGeo   = self.color_selectedGeoNurbs
            PointsColorGeo  = self.color_selectedGeoPoints

            geo.Draw(MeshColor=MeshColorGeo \
                     , NurbsColor=NurbsColorGeo \
                     ,PointsColor=PointsColorGeo \
                    , alpha=self.beta\
                    , blend=self.enableBlend)
        # highlight patch
        patch = wk.inspector.currentPatch
        if patch is not None:
            patchItem = wk.inspector.currentPatchItem
            geoItem = wk.inspector.tree.GetItemParent(patchItem)
            geo = wk.inspector.tree.GetPyData(geoItem)

            # Redraw the geometry
            MeshColorGeo    = self.color_selectedGeoMesh
            NurbsColorGeo   = self.color_selectedGeoNurbs
            PointsColorGeo  = self.color_selectedGeoPoints

#            print ">>>>>>>>>>>>>>"
#            print MeshColorGeo
#            print NurbsColorGeo
#            print PointsColorGeo

            geo.Draw(MeshColor=MeshColorGeo \
                     , NurbsColor=NurbsColorGeo \
                     ,PointsColor=PointsColorGeo \
                    , alpha=self.beta \
                    , blend=self.enableBlend)

            # Redraw the patch
            MeshColorNrb    = self.color_selectedPatchMesh
            NurbsColorNrb   = self.color_selectedPatchNurbs
            PointsColorNrb  = self.color_selectedPatchPoints

#            print "+++++++++++++++"
#            print MeshColorNrb
#            print NurbsColorNrb
#            print PointsColorNrb

            geo.Draw(nrb=patch \
                     , MeshColor=MeshColorNrb \
                     , NurbsColor=NurbsColorNrb \
                     , PointsColor=PointsColorNrb \
                     , alpha=self.beta\
                    , blend=self.enableBlend)

        # Highlight face: face is also a geometry object
        face = wk.inspector.currentFace
        if face is not None:
            MeshColorGeo    = self.color_selectedGeoMesh
            NurbsColorGeo   = self.color_selectedGeoNurbs
            PointsColorGeo  = self.color_selectedGeoPoints

            face.Draw(MeshColor=MeshColorGeo \
                     , NurbsColor=NurbsColorGeo \
                     ,PointsColor=PointsColorGeo \
                    , alpha=self.beta\
                    , blend=self.enableBlend)

    def drawWorld (self):
        colorBg = list(self.color_background) + [self.alpha_bg]
        glClearColor(*colorBg)

        glPushMatrix()
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # glEnable(GL_CULL_FACE)
        # draw all cad objetcs
        for geo in self.WorkGroup.list_geo:
            geo.Draw(alpha=self.beta\
                    , blend=self.enableBlend)
        # Draw selection
        self.highLightSelection()
#        # Draw Color Maps
#        self.OnDrawColorMap()
        # Draw 2D grid if acrive2D is true
        if self.active2D:
            rowmin = self.get_rowmin(); rowmax = self.get_rowmax()
            colmin = self.get_colmin(); colmax = self.get_colmax()
            hx     = self.get_hx()    ; hy     = self.get_hy()
            xcenter,ycenter,zcenter = self.lookAt.GetCenter()
            rowmin += ycenter
            rowmax += ycenter
            colmin += xcenter
            colmax += xcenter

            self.DrawGrid(rowmin, rowmax, colmin, colmax, hx, hy)
        self.DrawMarkerPoints()
        self.DrawSelectedPoints()
        glPopMatrix()
    #

    def key (self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.GetParent().Close()

    def onKeyPressDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SHIFT:
            self.SetEnabledSelectionMode(True)
        if keycode == wx.WXK_CONTROL:
            self.SetEnabledLookAtMode(True)
        if keycode == wx.WXK_SPACE:
            self.SetEnabledMarkerMode(True)
        # press 's' or 'S'
        if keycode == 83:
            self.SetEnabledCutCurveMode(True)

    def onKeyPressUp(self, event):
        wk = self.WorkGroup
        keycode = event.GetKeyCode()
        print(("key ", keycode))
        if keycode == wx.WXK_SHIFT:
            self.SetEnabledSelectionMode(False)
        if keycode == wx.WXK_CONTROL:
            self.SetEnabledLookAtMode(False)
        if keycode == wx.WXK_SPACE:
            self.SetEnabledMarkerMode(False)
        if keycode == wx.WXK_DELETE:
            wk.directAct.removeObject()
        # press 'a' or 'A'
        if keycode == 65:
            wk.directAct.createArc()
        # press 'l' or 'L'
        if keycode == 76:
            wk.directAct.createLines()
        # press 'b' or 'B'
        if keycode == 66:
            wk.directAct.createBilinear()
        # press 'm' or 'M'
        if keycode == 77:
            wk.directAct.SelectedToMarkersPoints()
        # press 'c' or 'C'
        if keycode == 67:
            wk.directAct.CloneSelectedPoints()
        # press 's' or 'S'
        if keycode == 83:
            wk.directAct.cutCurve()
            self.SetEnabledCutCurveMode(False)
            self.CleanCutCurvePoints()


    def OnMouseWheel(self, evt):
        if self.GetEnabledLookAtMode():
            print("Look at mode activated: OnMouseWheel")
        else:
            wheelSensitivity = self.get_wheelSensitivity()
            xeye,yeye,zeye = self.lookAt.GetEye()
            zeye += - 1.0 * wheelSensitivity * copysign (1.0, evt.GetWheelRotation())
            self.unit += -0.5 * wheelSensitivity * copysign (1.0, evt.GetWheelRotation())
            self.lookAt.SetEye([xeye,yeye,zeye])
            self.setViewpoint()
            self.Refresh()

    def OnMouseLeftDown(self, evt):
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
        pos = self.ToPhysicalPosition((self.x, self.y))
        [self.cornerx, self.cornery] = pos
        txt = [FloatToStr(x) for x in pos]
        self.statusbar.SetStatusText('Current position : ' + str(txt))

    def OnMouseLeftUp(self, evt):
        print("OnMouseLeftUp")

        self.x, self.y = evt.GetPosition()
        pos = self.ToPhysicalPosition((self.x, self.y))
        lastpos = self.ToPhysicalPosition((self.lastx, self.lasty))

        if self.GetEnabledSelectionMode():
            wk = self.WorkGroup
            patch = wk.inspector.currentPatch
            # add here any other condition that enables the selection
            # for the moment, selection only valide for patch
            activateSelection = (patch is not None)
            if activateSelection:
                [x1, y1] = [self.cornerx, self.cornery]
                [x2, y2] = self.ToPhysicalPosition((self.x, self.y))

                xmin = min([x1,x2]) ; xmax = max([x1,x2])
                ymin = min([y1,y2]) ; ymax = max([y1,y2])

                print("Enter")
                self.OnDrawSelectionRectangle(x1, y1, x2, y2)
                self.OnDraw(clear=False)

            if patch is not None:
                selectedPoints = SelectedPoints(patch)
                X,Y,Z = pointsToList(patch.points)
                list_ind = findIndex(X,Y,xmin,xmax,ymin,ymax)
                list_ijk = fromIndexToCoord(patch, list_ind)
                selectedPoints.addPointsByIndices(list_ijk)
                self.AddSelectedPoints(selectedPoints)

        elif self.GetEnabledLookAtMode():
            self.Set3DMode()
            v = np.asarray(list(pos)) - np.asarray(list(lastpos))
            xeye,yeye,zeye = self.lookAt.GetEye()
            xeye -= v[0]
            yeye -= v[1]
            self.lookAt.SetEye([xeye,yeye,zeye])
            self.setViewpoint()
        elif self.GetEnabledMarkerMode():
            # floating markers
            if not self.fixMarkers:
                P = [pos[0],pos[1],self.lookAt.GetCenter()[-1],1.]
            # fixed markers
            else:
                try:
                    rowmin = self.get_rowmin(); rowmax = self.get_rowmax()
                    colmin = self.get_colmin(); colmax = self.get_colmax()
                    xcenter,ycenter,zcenter = self.lookAt.GetCenter()
                    rowmin += ycenter ; rowmax += ycenter
                    colmin += xcenter ; colmax += xcenter
                    hx     = self.get_hx()    ; hy     = self.get_hy()
                    rows    = np.arange( rowmin, rowmax, hx )
                    columns = np.arange( colmin, colmax, hy )

                    x,y,z = [pos[0],pos[1],zcenter]
                    i = np.argmin((columns-x)**2)
                    j = np.argmin((rows-y)**2)
                    x = columns[i]
                    y = rows[j]
                    P = [x,y,z,1.]
                except:
                    P = [pos[0],pos[1],self.lookAt.GetCenter()[-1],1.]

            self.AddMarkerPoint(P)
        else:
            v = np.asarray(list(pos)) - np.asarray(list(lastpos))
            xcenter,ycenter,zcenter = self.lookAt.GetCenter()
            xcenter -= v[0]
            ycenter -= v[1]
            self.lookAt.SetCenter([xcenter,ycenter,zcenter])
            if self.active2D:
                xeye,yeye,zeye = self.lookAt.GetEye()
                self.lookAt.SetEye([xcenter,ycenter,zeye])

            pos = self.ToPhysicalPosition((self.x, self.y))
            txt = [FloatToStr(x) for x in pos]
            self.statusbar.SetStatusText('Current position : ' + str(txt))
        self.Refresh()

    def OnMouseMotion(self, evt):
        pos = evt.GetPosition()
        x,y = self.ToPhysicalPosition(pos)
        P = [x, y, 0.]
        self.statusbar.SetStatusText("Current Position : "\
                                     + str ([FloatToStr(x) for x in P]))

        if self.GetEnabledSelectionMode():
            if evt.Dragging() and evt.LeftIsDown() :
                self.lastx, self.lasty = self.x, self.y
                self.x, self.y = evt.GetPosition()

                [x1, y1] = [self.cornerx, self.cornery]
                [x2, y2] = self.ToPhysicalPosition((self.x, self.y))

                self.OnDrawSelectionRectangle(x1, y1, x2, y2)
                self.OnDraw(clear=False)
        if self.GetEnabledCutCurveMode():
            self.AddCutCurvePoint(P)
        self.Refresh()

    def OnRightMouseClick(self, event):
        ### 2. Launcher creates wxMenu. ###
        menu = wx.Menu()
        for (id,title) in list(self.menu_title_by_id.items()):
            ### 3. Launcher packs menu with Append. ###
            toAppend = True
            if self.active2D \
               and (title=="2D view"):
                toAppend = False
            if (not self.active2D) \
               and (title=="3D view"):
                toAppend = False
            if self.showGrid \
               and (title=="Show Grid"):
                toAppend = False
            if not self.showGrid \
               and (title=="Hide Grid"):
                toAppend = False
            if self.showGridLines \
               and (title=="Grid as Lines"):
                toAppend = False
            if not self.showGridLines \
               and (title=="Grid as Points"):
                toAppend = False
            if not self.fixMarkers \
               and (title=="Floating Markers"):
                toAppend = False
            if self.fixMarkers \
               and (title=="Fixed Markers"):
                toAppend = False
            if (len(self.MarkerPoints) == 0) \
               and (title=="Clear Markers"):
                toAppend = False
            if (len(self.list_SelectedPoints) == 0) \
               and (title=="Clear Selected Points"):
                toAppend = False
            if toAppend:
                menu.Append( id, title )
                ### 4. Launcher registers menu handlers with EVT_MENU, on the menu. ###
                wx.EVT_MENU( menu, id, self.MenuSelectionCb)
        ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        self.frame.PopupMenu( menu)
        menu.Destroy() # destroy to avoid mem leak

    def MenuSelectionCb( self, event ):
        # do something
        operation = self.menu_title_by_id[ event.GetId() ]
        if operation == "2D view":
            self.Set2DMode()
            xcenter,ycenter,zcenter = self.lookAt.GetCenter()
            xeye,yeye,zeye = self.lookAt.GetEye()
            self.lookAt.SetEye([xcenter,ycenter,zeye])
            self.Refresh()
        if operation == "3D view":
            self.Set3DMode()
        if operation == "Show Grid":
            self.ShowGrid()
            self.Refresh()
        if operation == "Hide Grid":
            self.HideGrid()
            self.Refresh()
        if operation == "Grid as Lines":
            self.set_showGridLines(True)
            self.Refresh()
        if operation == "Grid as Points":
            self.set_showGridLines(False)
            self.Refresh()
        if operation == "Fixed Markers":
            self.fixMarkers = True
        if operation == "Floating Markers":
            self.fixMarkers = False
        if operation == "Clear Markers":
            self.CleanMarkerPoints()
            self.Refresh()
        if operation == "Clear Selected Points":
            self.CleanSelectedPoints()
            self.Refresh()
        if operation == "Print":
            self.printViewer()
        if operation == "Add Marker":
            from customDialogs import edtCoordinatesTxtDialog
            dlg = edtCoordinatesTxtDialog(None, title="Add Marker")
            dlg.ShowModal()
            xtxt, ytxt, ztxt, wtxt = dlg.getValue()
            try:
                xcenter, ycenter, zcenter = self.lookAt.GetCenter()
                if xtxt is not None:
                    x = float(xtxt)
                else:
                    x = xcenter
                if ytxt is not None:
                    y = float(ytxt)
                else:
                    y = ycenter
                if ztxt is not None:
                    z = float(ztxt)
                else:
                    z = zcenter
                if wtxt is not None:
                    w = float(wtxt)
                else:
                    w = 1.0

                self.AddMarkerPoint([x,y,z,w])
                self.Refresh()
            except:
                print("Warning: problem occured while reading values")
                pass
            dlg.Destroy()
        if operation == "Import Markers":
            filename = None
            # Create a save file dialog
            from global_vars import CAIDMarkerswildcard
            dialog = wx.FileDialog ( None\
                                    , style = wx.OPEN\
                                    , wildcard=CAIDMarkerswildcard)
            # Show the dialog and get user input
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetPath()
            # The user did not select anything
            else:
                print('Nothing was selected.')
            # Destroy the dialog
            dialog.Destroy()

            if filename is not None:
                # text files
                if filename.split('.')[-1] == "txt":
                    _markers_array = np.genfromtxt(filename)
                    n = _markers_array.shape
                    markers_array = zeros((n[0],4))
                    markers_array[:,-1] = 1.
                    markers_array[:,:n[1]] = _markers_array

#                    self.SetMarkerPoints(list(markers_array))
                    for i in range(0, n[0]):
                        x,y,z,a = markers_array[i,:]
                        self.AddMarkerPoint([x,y,z,a])

        if operation == "Export Markers":
            filename = None
            # Create a save file dialog
            from global_vars import CAIDMarkerswildcard
            dialog = wx.FileDialog ( None\
                                    , style = wx.SAVE | wx.OVERWRITE_PROMPT\
                                    , wildcard=CAIDMarkerswildcard)
            # Show the dialog and get user input
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetPath()
            # The user did not select anything
            else:
                print('Nothing was selected.')
            # Destroy the dialog
            dialog.Destroy()

            if filename is not None:
                # text files
                if filename.split('.')[-1] == "txt":
                    n = self.nMarkerPoints
                    markers_array = zeros((n,4))
                    for i in range(0, n):
                        markers_array[i,:] = self.MarkerPoints[i]
                    np.savetxt(filename, markers_array)

        if operation == "Preferences":
            dlg = PreferencesDialog(self.frame, self, title="Viewer Preferences")
            dlg.ShowModal()
            dlg.Destroy()

#    def compute_pos(self, x, y, z):
#        '''
#        Compute the 3d opengl coordinates for 3 coordinates.
#        @param x,y: coordinates from canvas taken with mouse position
#        @param z: coordinate for z-axis
#        @return; (gl_x, gl_y, gl_z) tuple corresponding to coordinates in OpenGL context
#        '''
#        modelview = matrix(glGetDoublev(GL_MODELVIEW_MATRIX))
#        projection = matrix(glGetDoublev(GL_PROJECTION_MATRIX))
#        viewport = glGetIntegerv(GL_VIEWPORT)
#
#        winX = float(x)
#        winY = float(viewport[3] - float(y))
#        winZ = z
#        return gluUnProject(winX, winY, winZ, modelview, projection, viewport)

    def ToPhysicalPosition(self, coord):
        xcenter,ycenter,zcenter = self.lookAt.GetCenter()
        xeye   ,yeye   ,zeye    = self.lookAt.GetEye()
        size =  self.GetSize()
        hx = 0.5 * (size[0] - 0.)
        hy = 0.5 * (size[1] - 0.)
        xh = (1.0 / hx ) * (coord[0] - 0.0) - 1.0
        yh = (1.0 / hy ) * (coord[1] - 0.0) - 1.0
        xh *= self.unit
        xh += xcenter #* zeye * 3./ 6.
        yh *= - self.unit
        yh += ycenter #* zeye * 3./ 6.
        return [xh,yh]

    def OnDrawSelectionRectangle(self, x1, y1, x2, y2):
#        glClear(GL_COLOR_BUFFER_BIT)
#        glBegin(GL_QUADS)
#        col = self.theme.color_viewer("selection") + [self.theme.alpha]
#        glColor4f(*col)
#        glVertex2f(x1, y1)
#        glVertex2f(x2, y1)
#        glVertex2f(x2, y2)
#        glVertex2f(x1, y2)
#        glEnd()

        points = np.asarray([[[x1,y1],[x1,y2]],[[x2,y1],[x2,y2]]])
        geo_selection = geometry(bilinear(points=points))
        col = self.theme.color_viewer("selection")
        geo_selection.Draw(alpha=self.beta, blend=self.enableBlend, NurbsColor=col)

#    def OnDrawColorMap(self):
#        nx = 100
#        ny = 100
##        colorMap = np.random.random((nx,ny,3))
#        colorMap = 25*np.ones((nx,ny,3), dtype=np.int)
#
#        glClear(GL_COLOR_BUFFER_BIT)
#        glBegin (GL_POINTS)
#        for i in range (len(colorMap)): #iterate over each pixel and draw it.
#            for j in range (len(colorMap)):
#                glColor3ub (colorMap[i][j][0], colorMap[i][j][1], colorMap[i][j][2])
#                glVertex2i (i, j)
#        glEnd()

    def DrawGrid(self, rowmin, rowmax, colmin, colmax, hx, hy):
        if not self.showGrid:
            return

        rows    = np.arange( rowmin, rowmax, hx )
        columns = np.arange( colmin, colmax, hy )
        prof = 0.0

        nrows = len(rows)
        ncolumns = len(columns)

        # Draw the grid as Lines
        if self.showGridLines:
            glBegin(GL_LINES)
#            glColor(*self.color_grid())
            col = self.color_grid + [self.alpha]
            glColor4f(*col)
            for i in range(0,nrows):
                glVertex(columns[0] ,rows[i],prof)
                glVertex(columns[-1],rows[i],prof)

            for i in range(0,ncolumns):
                glVertex(columns[i], rows[0],prof)
                glVertex(columns[i],rows[-1],prof)
            glEnd()
        # Draw the grid as points
        else:
            glPointSize(self.size_GridPoints)
            glBegin(GL_POINTS)
#            glColor(self.color_grid)
            col = self.color_grid + [self.alpha]
            glColor4f(*col)
            for i in range(0,ncolumns):
                for j in range(0,nrows):
                    P = [columns[i], rows[j], prof]
                    glVertex(P[0],P[1],P[2])
            glEnd()

    def DrawMarkerPoints(self):
        if len(self.MarkerPoints) == 0 :
            return
        # ...
        # draw Points
        # ...
        glPointSize(self.size_MarkerPoints)
        glBegin(GL_POINTS)
        col = self.color_markerPoints+ [self.alpha]
        glColor4f(*col)
        for P in self.MarkerPoints:
            glVertex(P[0],P[1],P[2])
        glEnd()
        # ...

    def DrawSelectedPoints(self):
        if len(self.list_SelectedPoints) == 0 :
            return
        list_Q = []
        for selectedPoints in self.list_SelectedPoints:
            list_Q += selectedPoints.points
        if len(list_Q) == 0:
            return
        # ...
        # draw Points
        # ...
        glPointSize(self.size_SelectedPoints)
        glBegin(GL_POINTS)
        col = self.color_selectedPoints + [self.alpha]
        glColor4f(*col)
        for P in list_Q:
            glVertex(P[0],P[1],P[2])
        glEnd()
        # ...


    def printViewer(self):
        """Save current buffer to filename in format"""
        from global_vars import CAIDViewerWildcard
        # Create a save file dialog
        dialog = wx.FileDialog ( None, style = wx.SAVE | wx.OVERWRITE_PROMPT
                               , wildcard=CAIDViewerWildcard)
        # Show the dialog and get user input
        if dialog.ShowModal() == wx.ID_OK:
            filename="test.jpeg"
            try:
                filename = dialog.GetPath()
            except:
                pass
            ext = filename.split('.')[-1]
            if ext == "jpeg":
                fmt="JPEG"
            if ext == "png":
                fmt="PNG"

            import Image # get PIL's functionality...
            import os
            x,y,width,height = glGetDoublev(GL_VIEWPORT)
            width = int(width)
            height = int(height)
            glPixelStorei(GL_PACK_ALIGNMENT, 1)
            data = glReadPixels(x, y, width, height, GL_RGB, GL_UNSIGNED_BYTE)
#            image = Image.fromstring( "RGB", (width, height), data )
            image = Image.frombytes( "RGB", (width, height), data )
            image = image.transpose( Image.FLIP_TOP_BOTTOM)
            image.save( filename, fmt )
            self.statusbar.SetStatusText("Image has been saved in " + filename)

        # Destroy the dialog
        dialog.Destroy()
