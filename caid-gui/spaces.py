# -*- coding: UTF-8 -*-

import wx
import wx.lib.scrolledpanel as scrolled
from geometry import geometry
from caid.cad_geometry import cad_geometry
from viewer import Viewer
from numpy import pi, linspace
import numpy as np
import pickle as pickle
from objectActions import *
from geometryActions import *
from patchActions import *

class spacesTree(wx.TreeCtrl):
    '''Our customized TreeCtrl class
    '''
    def __init__(self, spaces, parent, id, position, size, style):
        """
        creates the spaces Tree.
        Args:
            spaces   : the spaces object (created in the current workgroup)
            parent   : the Frame parent
        """
        wx.TreeCtrl.__init__(self, parent, id, position, size, style)
        self.inspector = spaces
        root = self.AddRoot('spaces')
        self.root = root
        self.parent = parent

        # ... spaces
        menu_titles = [  "Add field"\
                       , "Properties" ]

        self.menu_title_by_id = {}
        for title in menu_titles:
            self.menu_title_by_id[ wx.NewId() ] = title
        # ...

        # ... connectivity
        menu_titles = [  "Export" ]

        self.connectivity_menu_title_by_id = {}
        for title in menu_titles:
            self.connectivity_menu_title_by_id[ wx.NewId() ] = title
        # ...

    def add_space(self, space):
        spaceItem = self.AppendItem(self.root, 'space', -1,
                                  -1,wx.TreeItemData(space) )

        geoItem  = self.AppendItem(spaceItem,'geometry', -1,
                                             -1,wx.TreeItemData(space.geometry))

        conItem  = self.AppendItem(spaceItem,'connectivity', -1,
                                             -1,wx.TreeItemData(space.connectivity))

        IDItem  = self.AppendItem(conItem,'ID', -1,
                                             -1,wx.TreeItemData(space.connectivity.ID))

        LMItem  = self.AppendItem(conItem,'LM', -1,
                                             -1,wx.TreeItemData(space.connectivity.LM))

#        self._patch_index = 0
#        for i in range(0, geo.npatchs):
#            nrb = geo[i]
#            self.add_patch(geoItem, nrb)
#            self._patch_index += 1


    def GetItemText(self, item):
        obj = self.GetItemData( item )
        if obj.__class__.__name__=="space":
            txt = "space"
        if obj.__class__.__name__.split('_')[0]=="connectivity":
            txt = "connectivity"
#        elif obj.__class__.__name__=="cad_nurbs":
#            txt = "cad_nurbs"
#        elif obj.__class__.__name__=="cad_op_nurbs":
#            txt = "cad_op_nurbs"
        else:
            txt = str(obj)
        return txt

    def SelectedSpace(self, item):
        obj = self.GetItemData( item )
        Parent = self.GetItemParent(item)
        if (obj.__class__.__name__ in ["space"]):
            return True
        else:
            return False

    def GetCurrentSpace(self, event):
        item = event.GetItem()
        obj = self.GetItemData( item )
        Parent = self.GetItemParent(item)
        if (obj.__class__.__name__ in ["space"]):
            return obj, item
        else:
            return None, None

    def SelectedConnectivity(self, item):
        obj = self.GetItemData( item )
        Parent = self.GetItemParent(item)
        if (obj.__class__.__name__.split('_')[0]=="connectivity"):
            return True
        else:
            return False

    def GetCurrentConnectivity(self, event):
        item = event.GetItem()
        obj = self.GetItemData( item )
        Parent = self.GetItemParent(item)
        if (obj.__class__.__name__.split('_')[0]=="connectivity"):
            return obj, item
        else:
            return None, None

    def update(self):
        self.Refresh()

    def Refresh(self):
        self.DeleteChildren(self.root)
        wk = self.inspector.WorkGroup
        for V in wk.list_space:
            self.add_space(V)

    def OnSelChanged(self, event):
        '''Method called when selected item is changed
        '''
        # Get the selected item object
        item =  event.GetItem()
        # Display the selected item text in the text widget
        self.inspector.display.SetLabel(self.GetItemText(item))
#        if self.SelectedSpace(item):
#            self.inspector.ShowAction(self.inspector.spaceActions)
#        else:
#            self.inspector.HideAllActions()

        self.inspector.currentSpace, self.inspector.currentSpaceItem =self.GetCurrentSpace(event)
        self.inspector.currentConnectivity, self.inspector.currentConnectivityItem=self.GetCurrentConnectivity(event)

        if self.inspector.currentSpace is not None:
            self.inspector.currentObject = self.inspector.currentSpace
            self.inspector.currentObjectItem = self.inspector.currentSpaceItem
        if self.inspector.currentConnectivity is not None:
            self.inspector.currentObject = self.inspector.currentConnectivity
            self.inspector.currentObjectItem = self.inspector.currentConnectivityItem

        self.selectionsItems = self.GetSelections()

        # Highlight and redraw the viewer
        self.inspector.WorkGroup.Refresh()

    def OnRightMouseClick(self, event):
        # get the current space
        space     = self.inspector.currentSpace
        if space is not None:
            self.OnRightMouseClickSpace(event, space)
        # get the connectivity
        connectivity = self.inspector.currentConnectivity
        if connectivity is not None:
            conItem     = self.inspector.currentConnectivityItem
            spaceItem   = self.inspector.tree.GetItemParent(conItem)
            space       = self.inspector.tree.GetItemData(spaceItem)
            self.OnRightMouseClickConnectivity(event, space)

    def OnRightMouseClickConnectivity(self, event, face):
        wk = self.inspector.WorkGroup
        ### 2. Launcher creates wxMenu. ###
        menu = wx.Menu()
        for (id,title) in list(self.connectivity_menu_title_by_id.items()):
            ### 3. Launcher packs menu with Append. ###
            toAppend = True
            if toAppend:
                ### 4. Launcher registers menu handlers with EVT_MENU, on the menu. ###
                title_id = menu.Append( id, title )
                menu.Bind( wx.EVT_MENU, self.MenuSelectionCbConnectivity, title_id )

        ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        self.parent.PopupMenu( menu, event.GetPoint() )
        menu.Destroy() # destroy to avoid mem leak

    def MenuSelectionCbConnectivity( self, event ):
        # do something
        operation = self.connectivity_menu_title_by_id[ event.GetId() ]
        con       = self.inspector.currentConnectivity
        conItem   = self.inspector.currentConnectivityItem
        if operation == "Export":
            filename = None
            # Create a save file dialog
            from global_vars import CAIDConnectivityWildcard
            dialog = wx.FileDialog ( None\
                                    , style = wx.SAVE | wx.OVERWRITE_PROMPT\
                                    , wildcard=CAIDConnectivityWildcard)
            # Show the dialog and get user input
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetPath()
            # Destroy the dialog
            dialog.Destroy()
            if filename is not None:
                name    = filename.split('.')[0]
                ext     = filename.split('.')[-1]
                if ext=="zip":
                    con.save(name=name, fmt=ext)
                else:
                    print("Wrong Extension")
#        # Refresh the viewer
#        self.inspector.WorkGroup.Refresh()

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

        self.currentSpace        = None
        self.currentSpaceItem    = None

        # Create a splitter window
        self.splitter = wx.SplitterWindow(self, -1)

        # Create the left panel
        self.leftPanel = wx.Panel(self.splitter, -1)
        # Create a box sizer that will contain the left panel contents
        self.leftBox = wx.BoxSizer(wx.VERTICAL)
        # Create our tree and put it into the left panel
        self.tree = spacesTree(self, self.leftPanel, 1, wx.DefaultPosition, (-1, -1),
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

        # the rightBox is a container for buttonSpaceBox and displayBox
        self.rightBox = wx.BoxSizer(wx.HORIZONTAL)
        self.rightBox.Add(self.displayBox, 1, wx.EXPAND)

        self.actionsPanel = self.rightPanel
        self.actionsBox = self.rightBox

        self.list_actions = []
#        self.spaceActions    = SpaceActions(self, self.actionsPanel, self.actionsBox)
#        self.list_actions.append(self.spaceActions)

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
        self.currentSpace        = None
        self.currentSpaceItem    = None

    def add_space(self, V):
        self.tree.add_space(V)

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
        print("Left")
#        y = evt.GetPosition()
#        self.st.SetLabel(str(y))

    def OnClick(self, event):
        print("OnClick")
        ID = event.GetId()
        if ID == GEO_TRS_ID:
            self.OnTranslateSpace(event)

    def onKeyPressUp(self, event):
        wk = self.WorkGroup
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE:
            wk.directAct.removeObject()

class MyApp(wx.App):
    '''Our application class
    '''
    def OnInit(self):
        '''Initialize by creating the split window with the tree
        '''
        frame = Inspector(None, -1, 'Inspector')
        frame.Show(True)
        self.SetTopWindow(frame)
        self.frame = frame

        return True

if __name__ == '__main__':
    app = MyApp(0)
    frame = app.frame
    tree = frame.tree
    from caid.cad_geometry import circle_5mp, square
    s1 = circle_5mp()
    s2 = square()
    geo1 = geometry(s1)
    geo2 = geometry(s2)
    tree.add_geometry(geo1)
    tree.add_geometry(geo2)
    app.MainLoop()
