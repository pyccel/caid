# -*- coding: UTF-8 -*-

import wx
from wx.glcanvas import *
import wx
import wx.lib.scrolledpanel as scrolled
from geometry import geometry
from igakit.cad_geometry import cad_geometry
from numpy import pi, linspace

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

ESCAPE = '\033'

window = 0
Near    = 1.0
Far     = 20.0

def FloatToStr(x):
    return float("{0:.2f}".format(x))

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


class fieldsTree(wx.TreeCtrl):
    '''Our customized TreeCtrl class
    '''
    def __init__(self, fields, parent, id, position, size, style):
        """
        creates the fields Tree.
        Args:
            fields   : the fields object (created in the current workgroup)
            parent   : the Frame parent
        """
        wx.TreeCtrl.__init__(self, parent, id, position, size, style)
        self.inspector = fields
        root = self.AddRoot('fields')
        self.root = root
        self.parent = parent

        # ... fields
        menu_titles = [  "New Field"\
                       , "Show"\
                       , "Hide"\
                       , "2D mode"\
                       , "3D mode"\
                       , "Properties" ]

        self.menu_title_by_id = {}
        for title in menu_titles:
            self.menu_title_by_id[ wx.NewId() ] = title
        # ...

    def add_field(self, field):
        fieldItem = self.AppendItem(self.root, 'field', -1,
                                  -1,wx.TreeItemData(field) )

        geoItem  = self.AppendItem(fieldItem,'geometry', -1,
                                             -1,wx.TreeItemData(field.geometry))

        cItem  = self.AppendItem(fieldItem,'coefficients', -1,
                                             -1,wx.TreeItemData(field.coefficients))


    def GetItemText(self, item):
        obj = self.GetPyData( item )
        if obj.__class__.__name__=="field":
            txt = "field"
        elif obj.__class__.__name__=="field_scalar":
            txt = "field-scalar"
        else:
            txt = str(obj)
        return txt

    def SelectedField(self, item):
        obj = self.GetPyData( item )
        try:
#            Parent = self.GetItemParent(item)
            if (obj.__class__.__name__ in ["field", "field_scalar"]):
                return True
            else:
                return False
        except:
            return None, None


    def GetCurrentField(self, event):
        item = event.GetItem()
        obj = self.GetPyData( item )
        try:
#            Parent = self.GetItemParent(item)
            if (obj.__class__.__name__ in ["field","field_scalar"]):
                return obj, item
            else:
                return None, None
        except:
            return None, None

    def update(self):
        self.Refresh()

    def Refresh(self):
        self.DeleteChildren(self.root)
        wk = self.inspector.WorkGroup
        for V in wk.list_field:
            self.add_field(V)

    def OnSelChanged(self, event):
        '''Method called when selected item is changed
        '''
        # Get the selected item object
        item =  event.GetItem()
        # Display the selected item text in the text widget
        self.inspector.display.SetLabel(self.GetItemText(item))
#        if self.SelectedField(item):
#            self.inspector.ShowAction(self.inspector.fieldActions)
#        else:
#            self.inspector.HideAllActions()

        self.inspector.currentField, self.inspector.currentFieldItem =self.GetCurrentField(event)

        if self.inspector.currentField is not None:
            self.inspector.currentObject = self.inspector.currentField
            self.inspector.currentObjectItem = self.inspector.currentFieldItem

        self.selectionsItems = self.GetSelections()

        # Highlight and redraw the viewer
        self.inspector.WorkGroup.Refresh()

    def OnRightMouseClick(self, event):
        # get the current field
        field     = self.inspector.currentField
        if field is not None:
            self.OnRightMouseClickField(event, field)

    def OnRightMouseClickField(self, event, field):
        ### 2. Launcher creates wxMenu. ###
        menu = wx.Menu()
        for (id,title) in self.menu_title_by_id.items():
            ### 3. Launcher packs menu with Append. ###
            toAppend = True
            if field.show and (title=="Show"):
                toAppend = False
            if not field.show and (title=="Hide"):
                toAppend = False
            if not field.surface and (title=="2D mode"):
                toAppend = False
            if field.surface and (title=="3D mode"):
                toAppend = False
            if toAppend:
                menu.Append( id, title )
                ### 4. Launcher registers menu handlers with EVT_MENU, on the menu. ###
                wx.EVT_MENU( menu, id, self.MenuSelectionCbField)
        ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        self.parent.PopupMenu( menu, event.GetPoint() )
        menu.Destroy() # destroy to avoid mem leak

    def MenuSelectionCbField( self, event ):
        # do something
        operation = self.menu_title_by_id[ event.GetId() ]
        F     = self.inspector.currentField
        FItem = self.inspector.currentFieldItem
        wk = self.inspector.WorkGroup
        if operation == "Show":
            F.Show(True)
            F.set_surface(False)

            from igakit.graphics.colormap import Hot
            cmap = Hot
            F.view(colormap=cmap, n=[100,100])

        if operation == "Hide":
            F.Show(False)
            V = wk.fields_viewer
            V.Show(True)
            V.Refresh()
        if operation == "2D mode":
            F.set_surface(False)
            V = wk.fields_viewer
            V.Show(True)
            V.Refresh()
        if operation == "3D mode":
            F.set_surface(True)
            V = wk.fields_viewer
            V.Show(True)
            V.Refresh()

        if operation == "New Field":
            E = field()
            wk.add_field(E)
        wk.Refresh()

class Inspector(wx.Frame):
    '''Our customized window class
    '''
    def __init__(self, workgroup, parent, id, title\
                 , pos \
                 , size):
        '''Initialize our window
        '''
        wx.Frame.__init__(self, parent, id, title, pos, size)

        self.parent = parent
        self.WorkGroup = workgroup

        self.currentField        = None
        self.currentFieldItem    = None

        # Create a splitter window
        self.splitter = wx.SplitterWindow(self, -1)

        # Create the left panel
        self.leftPanel = wx.Panel(self.splitter, -1)
        # Create a box sizer that will contain the left panel contents
        self.leftBox = wx.BoxSizer(wx.VERTICAL)
        # Create our tree and put it into the left panel
        self.tree = fieldsTree(self, self.leftPanel, 1, wx.DefaultPosition, (-1, -1),
                           wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_MULTIPLE)
        # Add the tree to the box sizer
        self.leftBox.Add(self.tree, 1, wx.EXPAND)
        # Bind the OnSelChanged method to the tree
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.tree.OnSelChanged, id=1)
        # Set the size of the right panel to that required by the tree
        self.leftPanel.SetSizer(self.leftBox)

        # Create the right panel
        self.rightPanel  = scrolled.ScrolledPanel(self.splitter, -1)
        # Create the right box sizer that will contain the panel's contents
        self.displayBox = wx.BoxSizer(wx.VERTICAL)
        # Create a widget to display static text and store it in the right
        # panel
        self.display = wx.StaticText(self.rightPanel, -1, '', (10, 10),
                                     style=wx.ALIGN_LEFT)
        # Add the display widget to the right panel
        self.displayBox.Add(self.display, 1, wx.EXPAND)

        # the rightBox is a container for buttonFieldBox and displayBox
        self.rightBox = wx.BoxSizer(wx.HORIZONTAL)
        self.rightBox.Add(self.displayBox, 1, wx.EXPAND)

        self.actionsPanel = self.rightPanel
        self.actionsBox = self.rightBox

        self.list_actions = []
#        self.fieldActions    = FieldActions(self, self.actionsPanel, self.actionsBox)
#        self.list_actions.append(self.fieldActions)

        self.actionsPanel.SetSizer(self.actionsBox)
        self.rightPanel.SetSizer(self.rightBox)
        self.rightPanel.SetupScrolling()

        # Set the size of the right panel to that required by the
        # display widget
        # Put the left and right panes into the split window
        self.splitter.SplitVertically(self.leftPanel, self.rightPanel,
                                      sashPosition=160)
        # Create the window in the centre of the screen
        self.Centre()

        # Hide all actions
        self.HideAllActions()

        # keyboard handlers
        self.Bind(wx.EVT_KEY_UP     , self.onKeyPressUp)
        # Bind the right mouse click
        self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.tree.OnRightMouseClick, id=1)


    def reset_currentAll(self):
        self.currentField        = None
        self.currentFieldItem    = None

    def add_field(self, V):
        self.tree.add_field(V)

    def remove_field(self, Item):
        self.tree.Delete(Item)

    def HideAllActions(self):
        for action in self.list_actions:
            action.Hide()
        self.rightBox.Layout()

    def ShowAction(self, act):
        self.HideAllActions()
        act.Show()
        self.rightBox.Layout()
        # activate the scroll when changing to patch actions for example
        size = self.rightPanel.GetSize()
        self.rightPanel.SetSize(size)

    def Refresh(self):
        self.reset_currentAll()
        self.tree.Refresh()

    def OnScroll(self, evt):
        print "Left"
#        y = evt.GetPosition()
#        self.st.SetLabel(str(y))

    def OnClick(self, event):
        print "OnClick"
        ID = event.GetId()

    def onKeyPressUp(self, event):
        wk = self.WorkGroup
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE:
            wk.directAct.removeObject()
        if keycode == wx.WXK_ESCAPE:
            self.Show(False)

#class Viewer (GLCanvas):
#    '''Actual OpenGL scene'''
#    #
#    def __init__ (self, workgroup, parent, attribs = None, id = wx.ID_ANY):
#        if not attribs:
#            attribs = [WX_GL_RGBA, WX_GL_DOUBLEBUFFER, WX_GL_DEPTH_SIZE, 24]
#        frame = wx.Frame(parent = parent, id = wx.ID_ANY,
#                    title="Viewer",
#                    pos = wx.DefaultPosition, size = (800, 800))
#        GLCanvas.__init__(self, frame, id, attribList = attribs)
#        self.context = GLContext(self)
#        self.frame = frame
#        self.WorkGroup = workgroup
#        self.init   = False
#        self.width  = 400
#        self.height = 400
#        # Display event handlers
#        self.Bind(wx.EVT_PAINT      , self.OnPaint)
#        self.Bind(wx.EVT_SIZE       , self.OnSize)
##        # Mouse handlers
##        self.Bind(wx.EVT_MOUSEWHEEL , self.OnMouseWheel)
##        self.Bind(wx.EVT_LEFT_DOWN  , self.OnMouseLeftDown)
##        self.Bind(wx.EVT_LEFT_UP    , self.OnMouseLeftUp)
##        self.Bind(wx.EVT_MOTION     , self.OnMouseMotion)
##        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightMouseClick)
##        # keyboard handlers
##        self.Bind(wx.EVT_CHAR       , self.key)
##        self.Bind(wx.EVT_KEY_DOWN   , self.onKeyPressDown)
##        self.Bind(wx.EVT_KEY_UP     , self.onKeyPressUp)
#
#        self.list_field = []
#
#        # viewer 2D or 3D mode
#        self.active2D = True
#        # show/hide  grid
#        self.showGrid = False
#        # the grid can be drawn as lines or points
#        self.showGridLines = True
#
#        # background color
#        self.color_background = [0.0, 0.0, 0.0]
#
#        # Wheel sensitivity used for Zoom
#        self.WheelSensitivity = 0.5
#        # TODO must be updated when zooming
#        self.unit = 3.
#
#        # cutCurveFreq used for the frequency sampling when moving the cursor
#        self.cutCurveFreq   = 5
#        self.CutCurvePoints = []
#
#        # handles viewer eye/...
#        self.lookAt = LookAt()
#
#        # initial mouse position
#        self.lastx = self.x = 30
#        self.lasty = self.y = 30
#
#        # used for the 2D grid
#        self.rowmin = -5. ; self.rowmax = 5.
#        self.colmin = -5. ; self.colmax = 5.
#        self.hx = 1.; self.hy = 1.
#
#        # used for selection mode
#        self.cornerx = None
#        self.cornery = None
#
#        # Data Selection
#        self.EnabledSelectionMode = False
#        # Look At => define a viewing transformation
#        self.EnabledLookAtMode = False
#        # Marker points
#        self.EnabledMarkerMode = False
#        # EnabledLookAtModeID = 0 ==> update center position
#        # EnabledLookAtModeID = 1 ==> update the up vector
#        # Otherwise ==> nothing to do
#        self.EnabledLookAtModeID = -1
#
#        # cut Curve Mode
#        self.EnabledCutCurveMode = False
#
#        # contains the list of marker points, picked directly on the viewer
#        self.MarkerPoints = []
#        self.fixMarkers = False
#        # contains the list of selected points, picked directly on the viewer
#        # list_SelectedPoints is a list of SelectedPoints class
#        self.list_SelectedPoints = []
#
#        self.SetFocus()
#
#        self.statusbar = self.frame.CreateStatusBar()
#        self.statusbar.SetStatusText('Ready')
#
#    def append(self, field):
#        self.list_field.append(field)
#
#    def clear_fields(self):
#        self.list_field = []
#    #
#    def OnPaint (self, event):
#        self.OnDraw()
#
#    def OnDraw(self, clear=True):
#        dc = wx.PaintDC(self)
#        self.SetCurrent(self.context)
#        if not self.init:
#            self.initGL()
#        if clear:
#            self.clear()
#        self.setProjection()
#        self.setViewpoint()
#        self.drawWorld()
#        self.SwapBuffers()
#    #
#    def OnSize (self, event):
#        # Note these are ints, not floats, for glViewport
#        self.width, self.height = self.GetSizeTuple()
#    #
#    def initGL (self):
##        colorBg = list(self.getColor_background()) + [1.0]
#        colorBg = list([1.,1.,1.]) + [1.0]
#        glClearColor(*colorBg)
#        self.init = True
##        glutInitDisplayMode(GLUT_RGB)
#    #
#    def clear (self):
#        glViewport(0, 0, self.width, self.height)
#        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#    #
#    def setProjection (self):
#        glMatrixMode(GL_PROJECTION)
#        glLoadIdentity()
#        gluPerspective(60.0, float(self.width) / float(self.height), Near, Far)
#        glMatrixMode(GL_MODELVIEW)
#    #
#    def setViewpoint (self):
#        glLoadIdentity()
#        xeye,yeye,zeye = self.lookAt.GetEye()
#        xcenter,ycenter,zcenter = self.lookAt.GetCenter()
#        xup,yup,zup = self.lookAt.GetUp()
#        gluLookAt(xeye,yeye,zeye   \
#                  ,xcenter,ycenter,zcenter  \
#                  ,xup,yup,zup  )
#        txt = [FloatToStr(x) for x in self.lookAt.GetCenter()]
##        self.statusbar.SetStatusText('View Point has been changed to ' +
##                                     str(txt) )
#
#
#    def drawWorld (self):
##        colorBg = list(self.getColor_background()) + [1.0]
#        colorBg = list([1.,1.,1.]) + [1.0]
#
#        glClearColor(*colorBg)
#        for F in self.list_field:
#            F.Draw()
#
##        glPushMatrix()
##        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
##        # glEnable(GL_CULL_FACE)
##        # draw all cad objetcs
##        for geo in self.WorkGroup.list_geo:
##            geo.Draw()
##        self.DrawMarkerPoints()
##        self.DrawSelectedPoints()
##        glPopMatrix()
#
#
