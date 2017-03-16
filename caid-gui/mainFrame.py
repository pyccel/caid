from aboutBox import *
from MenuCAIDFile import MenuCAIDFile
from MenuCAIDEdit import MenuCAIDEdit
from MenuCAIDTools import MenuCAIDTools
from workGroup import *
from caid.field import field
import sys
import os
from glob import glob
import wx
import wx.html
import wxversion
#wxversion.select("2.9")

class Frame(wx.Frame):
    def __init__(self, title, filenames=[]):
        wx.Frame.__init__(self, None, title=title, pos=(50,50), size=(450,150))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        menuBar = wx.MenuBar()

        # ...
        # creation of menu File
        # ...
        menuFile = MenuCAIDFile(self)

        self.Bind(wx.EVT_MENU, menuFile.OnNewFile, menuFile.m_newfile)
        self.Bind(wx.EVT_MENU, menuFile.OnOpenFile, menuFile.m_openfile)

        self.Bind(wx.EVT_MENU, menuFile.OnSaveFile, menuFile.m_savefile)
        self.Bind(wx.EVT_MENU, menuFile.OnSaveAsFile, menuFile.m_saveAsfile)

        self.Bind(wx.EVT_MENU, menuFile.OnRecentFiles, menuFile.m_recentFiles)

        self.Bind(wx.EVT_MENU, self.OnClose, menuFile.m_exit)

        menuBar.Append(menuFile, "&File")
        # ...

        # ...
        # creation of menu Edit
        # ...
        menuEdit = MenuCAIDEdit(self)

        self.Bind(wx.EVT_MENU, menuEdit.OnUndo, menuEdit.m_undo)
        self.Bind(wx.EVT_MENU, menuEdit.OnRedo, menuEdit.m_redo)

        self.Bind(wx.EVT_MENU, menuEdit.OnCut, menuEdit.m_cut)
        self.Bind(wx.EVT_MENU, menuEdit.OnCopy, menuEdit.m_copy)
        self.Bind(wx.EVT_MENU, menuEdit.OnPaste, menuEdit.m_paste)

        self.Bind(wx.EVT_MENU, menuEdit.OnRefresh, menuEdit.m_refresh)
        self.Bind(wx.EVT_MENU, menuEdit.OnSelectAll, menuEdit.m_selectAll)
        self.Bind(wx.EVT_MENU, menuEdit.OnDuplicate, menuEdit.m_duplicate)
        self.Bind(wx.EVT_MENU, menuEdit.OnDelete, menuEdit.m_delete)

        self.Bind(wx.EVT_MENU, menuEdit.OnShowGeometryPatchMenu, menuEdit.m_geo_patch_menu)

        self.Bind(wx.EVT_MENU, menuEdit.OnShowMeshMenu, menuEdit.m_showMesh_menu)

        self.Bind(wx.EVT_MENU, menuEdit.OnEnableInspectorColor, menuEdit.m_EnableInspectorColor_menu)

        for m in menuEdit.list_m_themes:
            self.Bind(wx.EVT_MENU, menuEdit.OnTheme, m)

        for m in menuEdit.list_m_intersection:
            self.Bind(wx.EVT_MENU, menuEdit.OnIntersection, m)

        for m in menuEdit.list_m_coons:
            self.Bind(wx.EVT_MENU, menuEdit.OnCoons, m)

        menuBar.Append(menuEdit, "&Edit")
        # ...

        # ...
        # creation of menu Tools
        # ...
        menuTools = MenuCAIDTools(self)

        self.Bind(wx.EVT_MENU, menuTools.OnCommandLine, menuTools.m_CommandLine)
        self.Bind(wx.EVT_MENU, menuTools.OnPythonEditor, menuTools.m_PythonEditor)
        self.Bind(wx.EVT_MENU, menuTools.OnEditParameters, menuTools.m_EditParameters)

        self.Bind(wx.EVT_MENU, menuTools.OnMacroRecording, menuTools.m_MacroRecording)
        self.Bind(wx.EVT_MENU, menuTools.OnClearMacroRecording, menuTools.m_ClearMacroRecording)
        self.Bind(wx.EVT_MENU, menuTools.OnMacroMetric, menuTools.m_MacroMetric)
        self.Bind(wx.EVT_MENU, menuTools.OnMacroTokaMesh, menuTools.m_MacroTokaMesh)
        self.Bind(wx.EVT_MENU, menuTools.OnMacroConnectivity, menuTools.m_MacroConnectivity)
        self.Bind(wx.EVT_MENU, menuTools.OnExecuteEditor, menuTools.m_ExecuteEditor)

        self.Bind(wx.EVT_MENU, menuTools.OnCustomize, menuTools.m_Customize)

        menuBar.Append(menuTools, "&Tools")
        # ...

        # ...
        # creation of menu Help
        # ...
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menuBar.Append(menu, "&Help")
        # ...

        self.SetMenuBar(menuBar)
        self.statusbar = self.CreateStatusBar()

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('#ededed') #4f5049

        self.vBox = wx.BoxSizer(wx.VERTICAL)

        # Create our tree and put it into the left panel
        self.tree = WorkGroupTree(self.panel, self, 1 \
                                  , wx.DefaultPosition, (-1, -1) \
                                  , wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        # Add the tree to the box sizer
        self.vBox.Add(self.tree, 1, wx.EXPAND)
        # Bind the OnSelChanged method to the tree
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.tree.OnSelChanged, id=1)
        # Bind the right mouse click
        self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.tree.OnRightMouseClick, id=1)
        # Set the size of the right panel to that required by the tree
        self.panel.SetSizer(self.vBox)


        # keyboard handlers
        self.Bind(wx.EVT_CHAR       , self.key)
        self.Bind(wx.EVT_KEY_DOWN   , self.onKeyPressDown)
        self.Bind(wx.EVT_KEY_UP     , self.onKeyPressUp)

        # open a workgroup if filename is given
        print(("filenames=", filenames))
        if len(filenames) == 0:
            wk = self.tree.createWorkGroup(empty=False)
        else:
            wk = self.tree.createWorkGroup(empty=True)

        wk.inspector.ShowAction(wk.inspector.geometryActions)

        for filename in filenames:
            if filename is not None:
                ext = filename.split('.')[-1]
                print(("Extension ", ext))
                if ext == "pfl":
                    wk.viewer.Show(False)
                    wk.inspector.Show(False)
                    U = field()
                    U.open(filename)
                    wk.add_field(U)
                    wk.Refresh()
                    U.Show(False)
    #                V = wk.fields_viewer
    #                V.Show(True)

                if ext in  ["xml", "nml"]:
                    print(filename)
                    print((os.path.isfile(filename)))
                    if os.path.isfile(filename):
                        geo = cad_geometry(filename)
                        _geo = geometry(geo)
                        _geo.load_attributs()
                        wk.add_geometry(_geo)
                    else:
                        print("Invalid filename : ")
                        raise

                if ext == "wkl":
                    wk.open(filename=filename)

                if os.path.isdir(filename):
                    dirname = filename
                    names = glob(dirname+"/*")
                    names.sort()
                    directories = [dirname]
                    for name in names:
                        if os.path.isdir(name):
                            directories.append(name)

                    for dname in directories:
                        print((">> dname ", dname))
                        files = glob(dname+"/*")
                        files.sort()
                        for f in files:
                            fname = os.path.basename(f)
                            ext = os.path.splitext(fname)[-1]
                            if ext == ".xml":
                                _file = os.path.join(dname, fname)
                                print(("reading ", _file))
                                geo = cad_geometry(_file)
                                _geo = geometry(geo)
                                _geo.load_attributs()
                                wk.add_geometry(_geo)

#                files = glob(dirname+"/*")
#                files.sort()
#                for f in files:
#                    fname = os.path.basename(f)
#                    print "reading ", fname
#                    ext = os.path.splitext(fname)[-1]
#                    if ext == ".xml":
#                        _file = os.path.join(dirname, fname)
#                        geo = cad_geometry(_file)
#                        _geo = geometry(geo)
#                        _geo.load_attributs()
#                        wk.add_geometry(_geo)

    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()

    def OnClose(self, event):
        dlg = wx.MessageDialog(self,
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            try:
                self.designer.Destroy()
            except :
                pass
            self.Destroy()

    def key (self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.GetParent().Close()

    def onKeyPressDown(self, event):
#        print "onKeyPressDown"
        keycode = event.GetKeyCode()
#        print "keycode =", keycode

    def onKeyPressUp(self, event):
#        print "onKeyPressUp"
        keycode = event.GetKeyCode()
#        print "keycode =", keycode
