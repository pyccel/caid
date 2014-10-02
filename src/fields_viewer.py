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
from igakit.cad_geometry import cad_geometry
import numpy as np
from math import copysign
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
        self.eye    = [0.,0.,3.]
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


class Viewer (GLCanvas):
    '''Actual OpenGL scene'''
    #
    def __init__ (self, workgroup, parent, attribs = None, id = wx.ID_ANY):
        if not attribs:
            attribs = [WX_GL_RGBA, WX_GL_DOUBLEBUFFER, WX_GL_DEPTH_SIZE, 24]
        frame = wx.Frame(parent = parent, id = wx.ID_ANY,
                    title="Fields Viewer",
                    pos = wx.DefaultPosition, size = (400, 400))
        GLCanvas.__init__(self, frame, id, attribList = attribs)
        self.context = GLContext(self)
        self.frame = frame
        self.WorkGroup = workgroup
        self.init   = False
        self.width  = 0
        self.height = 0
        # Display event handlers
        self.Bind(wx.EVT_PAINT      , self.OnPaint)
        self.Bind(wx.EVT_SIZE       , self.OnSize)
        # Mouse handlers
        self.Bind(wx.EVT_MOUSEWHEEL , self.OnMouseWheel)
        self.Bind(wx.EVT_LEFT_DOWN  , self.OnMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP    , self.OnMouseLeftUp)
#        self.Bind(wx.EVT_MOTION     , self.OnMouseMotion)
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

        # background color
        self.color_background = [0., 0., 0.]

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

        # Look At => define a viewing transformation
        self.EnabledLookAtMode = False

        self.SetFocus()

        self.statusbar = self.frame.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        self.menu_titles = ["2D view", "3D view" \
                            , "Print", "Preferences" ]

        self.menu_title_by_id = {}
        for title in self.menu_titles:
            self.menu_title_by_id[ wx.NewId() ] = title

    def Show(self,value):
        self.frame.Show(value)

    def Set2DMode(self):
        self.active2D = True
        self.statusbar.SetStatusText("2D mode enabled")

    def Set3DMode(self):
        self.active2D = False
        self.statusbar.SetStatusText("3D mode enabled")

    def get_wheelSensitivity(self):
        return self.WheelSensitivity

    def set_wheelSensitivity(self, value=None):
        if value is not None:
            self.WheelSensitivity = value

    def getColor_background(self):
        return self.color_background

    def setColor_background(self, value=None):
        if value is not None:
            self.color_background = value

    def GetEnabledLookAtMode(self):
        return self.EnabledLookAtMode

    def SetEnabledLookAtMode(self, value):
        self.EnabledLookAtMode =  value

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
        colorBg = list(self.getColor_background()) + [1.0]
        glClearColor(*colorBg)
        self.init = True

        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)

#        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#        glViewport(0, 0, self.width, self.height)
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

    def drawWorld (self):
        colorBg = list(self.getColor_background()) + [1.0]
        glClearColor(*colorBg)

        glPushMatrix()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        for F in self.WorkGroup.list_field:
            F.Draw()
        glPopMatrix()
    #

    def key (self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.GetParent().Close()

    def onKeyPressDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_CONTROL:
            self.SetEnabledLookAtMode(True)

    def onKeyPressUp(self, event):
        wk = self.WorkGroup
        keycode = event.GetKeyCode()
        print "key ", keycode
        if keycode == wx.WXK_ESCAPE:
            self.Show(False)
        if keycode == wx.WXK_CONTROL:
            self.SetEnabledLookAtMode(False)
        if keycode == wx.WXK_DELETE:
            wk.directAct.removeObject()


    def OnMouseWheel(self, evt):
        if self.GetEnabledLookAtMode():
            print "Look at mode activated: OnMouseWheel"
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
        self.x, self.y = evt.GetPosition()
        pos = self.ToPhysicalPosition((self.x, self.y))
        lastpos = self.ToPhysicalPosition((self.lastx, self.lasty))

        if self.GetEnabledLookAtMode():
            self.Set3DMode()
            v = np.asarray(list(pos)) - np.asarray(list(lastpos))
            xeye,yeye,zeye = self.lookAt.GetEye()
            xeye -= v[0]
            yeye -= v[1]
            self.lookAt.SetEye([xeye,yeye,zeye])
            self.setViewpoint()
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
        self.Refresh()

    def OnRightMouseClick(self, event):
        ### 2. Launcher creates wxMenu. ###
        menu = wx.Menu()
        for (id,title) in self.menu_title_by_id.items():
            ### 3. Launcher packs menu with Append. ###
            toAppend = True
            if self.active2D \
               and (title=="2D view"):
                toAppend = False
            if (not self.active2D) \
               and (title=="3D view"):
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
        if operation == "Print":
            self.printViewer()
        if operation == "Preferences":
            dlg = PreferencesDialog(self.frame, self, title="Viewer Preferences")
            dlg.ShowModal()
            dlg.Destroy()


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
            image = Image.fromstring( "RGB", (width, height), data )
            image = image.transpose( Image.FLIP_TOP_BOTTOM)
            image.save( filename, fmt )
            self.statusbar.SetStatusText("Image has been saved in " + filename)

        # Destroy the dialog
        dialog.Destroy()
