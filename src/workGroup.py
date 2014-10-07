# -*- coding: UTF-8 -*-
import wx
from directActions import *
from classActions import *
from time import localtime
from caid.field import field
from global_vars import strtoArray
from scripture import scripture
from PythonEditor import Editor as PythonEditor

class Preferences():
    def __init__(self, wk):
        self._wk = wk
        self._intersection  = {}
        self._coons         = {}

        # ... default initialization for intersection
        self.set_intersection("npts", 50)
        # ...

        # ... default initialization for coons
        self.set_coons("tol", 1.e-2)
        # ...

    @property
    def workgroup(self):
        return self._wk

    @property
    def intersection(self):
        return self._intersection

    def set_intersection(self, attribut, value):
        self._intersection[attribut] = value

    @property
    def coons(self):
        return self._coons

    def set_coons(self, attribut, value):
        self._coons[attribut] = value

class WorkGroup(wx.Frame):
    def __init__(self, parent, empty=False):
        self.parent = parent
        self._preferences = Preferences(self)
        self.list_geo   = []
        self.list_space = []
        self.list_field = []
        self.stockUndo = []
        self.stockRedo = []

        self.createInspector()
        self.createViewer()
#        self.createFields()
        self.initialize(empty=empty)
        self.directAct = directActions(self)
        # needed when saving the workgroup
        self.filename = None
        # needed for temporary save
        t = localtime()
        tmp_file = "session-"\
                +str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)\
                +"_"+str(t.tm_hour)+"h"+str(t.tm_min)+"min"\
                +".wkl"
        self.tmp_filename = tmp_file
        # auto save is activated by default
        self.auto_save = True

        self._macroRecording = False
        self._macro_script = scripture(self)

        self._pythonEditor = PythonEditor(self.parent, -1, '')
        self._pythonEditor.Show(False)

    @property
    def pythonEditor(self):
        return self._pythonEditor

    def set_pythonEditor(self, edt):
        self._pythonEditor = edt

    @property
    def preferences(self):
        return self._preferences

    def set_macroRecording(self, value):
        self._macroRecording = value

    @property
    def macroRecording(self):
        return self._macroRecording

    @property
    def macro_script(self):
        return self._macro_script

    def initialize(self, empty=False):
        """
        create an empty geometry object
        """
        if not empty:
            from geometry import geometry
            geo = geometry()
            self.add_geometry(geo)

    def createViewer(self):
        from viewer import Viewer
        self.viewer = Viewer(self, self.parent \
                                   , pos=(500,50) \
                                   , size=wx.Size(700,700))
        self.viewer.Show(True)

    def createInspector(self):
        from inspector import Inspector
        self.inspector = Inspector(self, self.parent, -1, 'Inspector' \
                                   , pos=(500,50) \
                                   , size=wx.Size(450,550))
        self.inspector.Show(True)

    def createSpaces(self):
        from spaces import Inspector
        self.spaces = Inspector(self, self.parent, -1, 'Spaces' \
                                   , pos=(500,300) \
                                   , size=wx.Size(450,550))
        self.spaces.Show(True)

    def createFields(self):
        from fields import Inspector
        self.fields = Inspector(self, self.parent, -1, 'Fields' \
                                   , pos=(500,300) \
                                   , size=wx.Size(450,550))
        self.fields.Show(True)

    def appendAction(self, undo):
        self.stockUndo.append( undo )
        if self.stockRedo:
            try:
                del self.stockRedo[:]
            except:
                print "problem occurs while deleting stockRedo"

    def add_geometry(self, geo, activeUndo=True):
        self.list_geo.append(geo)
        geoItem = self.inspector.add_geometry(geo)
        geo.set_treeItem(geoItem)

        # undo action
        if activeUndo:
            undo = UndoAddGeometry(self, geoItem, geo)
            self.appendAction(undo)

        self.Refresh()
        return geoItem

    def add_patch(self, geoItem, geo, patch, activeUndo=True):
        geo.append(patch)
        patchItem = self.inspector.add_patch(geoItem, geo, patch)

        # undo action
        if activeUndo:
            undo = UndoAddPatch(self, patchItem, patch, geo, geoItem)
            self.appendAction(undo)

        self.Refresh()
        return patchItem

    def add_space(self, geo, testcase=None):
        # create the Frame if list_space is empty
        if len(self.list_space) == 0:
            self.createSpaces()

        from pigasus.fem.basicPDE import basicPDE
        if testcase is None:
            testcase = {}
            testcase['AllDirichlet'] = True

        PDE = basicPDE(geometry=geo, testcase=testcase)
        V = PDE.space

        self.list_space.append(V)
        self.spaces.add_space(V)
        self.Refresh()

    def add_field(self, field):
        if len(self.list_field) == 0:
            self.createFields()
        self.list_field.append(field)
        self.fields.Show(True)
        self.fields.add_field(field)
        self.Refresh()

    def remove_geometry(self, geoItem, geo, activeUndo=True):
        # undo action
        if activeUndo:
            undo = UndoRemoveGeometry(self, geoItem, geo)
            self.appendAction(undo)

        # remove geo from the dictionary
        self.list_geo.remove(geo)
        # delete the corresponding item from the inspector
        self.inspector.remove_geometry(geoItem)
        self.inspector.reset_currentAll()

        # refresh the viewer
        self.Refresh()

    def remove_patch(self, patchItem, patch, geo=None, activeUndo=True):
        # remove patch from the dictionary
        if geo is None:
            geo = self.get_geometry_from_patch(patch)
        # undo action
        if activeUndo:
            geoItem = self.inspector.tree.GetItemParent(patchItem)
            undo = UndoRemovePatch(self, patchItem, patch, geo, geoItem)
            self.appendAction(undo)

        geo.remove_patch(patch)
        print "%"
        # delete the corresponding item from the inspector
        self.inspector.remove_patch(patchItem)
        print "%%"
        self.inspector.reset_currentAll()
        print "%%%"
        # refresh the viewer
        self.Refresh()

    def remove_field(self, fieldItem, field):
        # remove geo from the dictionary
        self.list_field.remove(field)
        # delete the corresponding item from the inspector
        self.fields.remove_field(fieldItem)
        self.fields.reset_currentAll()
        # refresh the viewer
        self.Refresh()

    def get_geometry_from_patch(self, patch):
        # remove patch from the dictionary
        print "looking for patch ", id(patch)
        for geo in self.list_geo:
            for nrb in geo:
                print id(nrb)
                if id(nrb) == id(patch):
                    print "found."
                    return geo
        print "Not found."

    def Refresh(self, inspector=False):
        if inspector:
            self.inspector.Refresh()
            # save in temp file
            if self.auto_save:
                self.save(filename=self.tmp_filename)

        self.viewer.drawWorld()
        self.viewer.Refresh()

    def message(self, txt):
        self.viewer.statusbar.SetStatusText(txt)

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        # this means that self.filename is also None
        if filename is None:
            # Create a save file dialog
            from global_vars import CAIDWorkGroupwildcard
            dialog = wx.FileDialog ( None\
                                    , style = wx.SAVE | wx.OVERWRITE_PROMPT\
                                    , wildcard=CAIDWorkGroupwildcard)
            # Show the dialog and get user input
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetPath()
                self.filename = filename
            # The user did not select anything
            else:
                print 'Nothing was selected.'
            # Destroy the dialog
            dialog.Destroy()

        # ... create xml doc
        from xml.dom.minidom import Document
        # Create the minidom document
        doc = Document()
        # Create the <theme> base element
        rootElt = self.viewer.theme.save(doc=doc)

        # Create the <caid> base element
        rootElt = doc.createElement("caid")
        # set camera attributs
        eye = self.viewer.lookAt.GetEye()
        rootElt.setAttribute("eye", str(eye))
        center = self.viewer.lookAt.GetCenter()
        rootElt.setAttribute("center", str(center))
        up = self.viewer.lookAt.GetUp()
        rootElt.setAttribute("up", str(up))

        doc.appendChild(rootElt)
        # ...

        # ...
        themeElt, doc = self.viewer.theme.save(doc=doc)
        rootElt.appendChild(themeElt)
        # ...

        # ...
        from caid.io import XML
        io = XML()
        for geo in self.list_geo:
            geo.save_attributs()
            geoElt = doc.createElement("geometry")
            doc = io.geotoxml(geo, doc, geoElt)
            rootElt.appendChild(geoElt)
        # ...

        if filename is not None:
            f = open(filename, 'wr')
            s = doc.toprettyxml()
            f.write(s)
            f.close()
        else:
            print "No file was specified"


    def open(self, filename=None):
        if filename is not None:
            self.filename = filename
        else:
            from global_vars import CAIDWorkGroupwildcard
            # Create an open file dialog
            dialog = wx.FileDialog(None\
                                   , style = wx.OPEN\
                                   , wildcard=CAIDWorkGroupwildcard)
            # Show the dialog and get user input
            if dialog.ShowModal() == wx.ID_OK:
                self.filename = dialog.GetPath()
            # The user did not select anything
            else:
                print 'Nothing was selected.'
            # Destroy the dialog
            dialog.Destroy()

        from caid.cad_geometry import cad_geometry
        from caid.io import XML
        from geometry import geometry
        io = XML()

        from xml.dom.minidom import parse
        doc = parse(self.filename)
        rootElt = doc.documentElement

        # read attributs
        # get camera attributs
        eye = strtoArray(rootElt.getAttribute("eye"))
        self.viewer.lookAt.SetEye(eye)
        center = strtoArray(rootElt.getAttribute("center"))
        self.viewer.lookAt.SetCenter(center)
        up = strtoArray(rootElt.getAttribute("up"))
        self.viewer.lookAt.SetUp(up)
        # get colors attributs

        # ...
        try:
            self.viewer.theme.load(rootElt=rootElt)
        except:
            print "Theme can not be loaded. Dark theme will be used."
            self.viewer.theme.set_theme("dark")
        # ...

        for geoElt in rootElt.getElementsByTagName("geometry"):
            geo = cad_geometry()
            io.xmltogeo(geo, doc, geoElt)
            _geo = geometry(geo)
            _geo.load_attributs()
            self.add_geometry(_geo)

        self.Refresh()

        # sets the temporary file for auto-save
        tmp = self.filename.split('/')[-1]
        basedir = self.filename.split(tmp)[0]
        self.tmp_filename = basedir+"~"+tmp

class WorkGroupTree(wx.TreeCtrl):
    '''Our customized TreeCtrl class
    '''
    def __init__(self, parent, frame, id, position, size, style):
        '''Initialize our tree
        '''
        wx.TreeCtrl.__init__(self, parent, id, position, size, style)
        root = self.AddRoot('caid')
        self.root = root
#        self.parent = parent
        self.parent = frame
        self.dict_WorkGroup = {}
        self._currentWorkGroup = None
        self._lastWorkGroup = None

        self.menu_titles = [ "New Geometry"\
                            , "Import"\
                            , "Export"\
                            , "Save"\
                            , "Duplicate"\
                            , "New Scalar Field"\
                            , "Import Scalar Field"\
                            , "Delete" ]

        self.menu_title_by_id = {}
        for title in self.menu_titles:
            self.menu_title_by_id[ wx.NewId() ] = title

    @property
    def currentWorkGroup(self):
        if self._currentWorkGroup is None:
            self._currentWorkGroup = self._lastWorkGroup
        return self._currentWorkGroup

    def createWorkGroup(self, empty=False):
        wk = WorkGroup(self.parent, empty=empty)
        self.dict_WorkGroup[id(wk)] = wk
        TAG = "-" + str(len(self.dict_WorkGroup))

        wkItem = self.AppendItem(self.root, 'WorkGroup'+TAG, -1,
                                  -1,wx.TreeItemData(wk) )
        inspectorItem  = self.AppendItem(wkItem,'Inspector', -1,
                                             -1,wx.TreeItemData(wk))
        viewerItem  = self.AppendItem(wkItem,'Viewer', -1,
                                             -1,wx.TreeItemData(wk))
        spacesItem  = self.AppendItem(wkItem,'Spaces', -1,
                                             -1,wx.TreeItemData(wk))
        fieldsItem  = self.AppendItem(wkItem,'Fields', -1,
                                             -1,wx.TreeItemData(wk))


        return wk

    def SelectedViewer(self, item):
        obj = self.GetPyData( item )
        if obj.__class__.__name__ in ["Viewer"]:
            return True
        else:
            return False

    def SelectedInspector(self, item):
        obj = self.GetPyData( item )
        if obj.__class__.__name__ in ["Inspector"]:
            return True
        else:
            return False

    def GetCurrentWorkGroup(self, event):
        """
        return the current workgroup independtly from
        the selected item (viewer, inspector, workgroup)
        """
        item =  event.GetItem()
        obj = self.GetPyData(item)
        txt = self.GetItemText(item)
        tag = txt.split("-")[0]
        if tag in ["WorkGroup","Inspector","Viewer"]:
            return obj
        else:
            return None

    def OnSelChanged(self, event):
        '''Method called when selected item is changed
        '''
        # Get the selected item object
        item =  event.GetItem()
        self._currentWorkGroup = self.GetCurrentWorkGroup(event)
        if self._currentWorkGroup is not None:
            self._lastWorkGroup = self._currentWorkGroup

    def OnRightMouseClick(self, event):
        ### 2. Launcher creates wxMenu. ###
        menu = wx.Menu()
        for (id,title) in self.menu_title_by_id.items():
            ### 3. Launcher packs menu with Append. ###
            menu.Append( id, title )
            ### 4. Launcher registers menu handlers with EVT_MENU, on the menu. ###
            wx.EVT_MENU( menu, id, self.MenuSelectionCb )

        ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        self.parent.PopupMenu( menu, event.GetPoint() )
        menu.Destroy() # destroy to avoid mem leak

    def MenuSelectionCb( self, event ):
        # do something
        operation = self.menu_title_by_id[ event.GetId() ]
        if operation == "New Geometry":
            from geometry import geometry
            geo = geometry()

            wk = self.currentWorkGroup
            wk.add_geometry(geo)
        if operation == "Save":
            self.currentWorkGroup.save()
        if operation == "New Scalar Field":
            F = field()
            wk = self.currentWorkGroup
            wk.add_field(F)
        if operation == "Import Scalar Field":
            filename = None
            from global_vars import CAIDFieldWildcard
            # Create an open file dialog
            dialog = wx.FileDialog(None\
                                   , style = wx.OPEN\
                                   , wildcard=CAIDFieldWildcard)
            # Show the dialog and get user input
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetPath()
            # The user did not select anything
            else:
                print 'Nothing was selected.'
            # Destroy the dialog
            dialog.Destroy()

            if filename is not None:
                U = field()
                U.open(filename)
                wk = self.currentWorkGroup
                wk.add_field(U)
                wk.Refresh()
