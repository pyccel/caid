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
from global_vars import strtoArray
from theme import theme as Theme

theme = Theme()

class BoundaryConditions(object):
    def __init__(self, npatchs, dim):
        self.AllDirichlet = None
        self.dirichlet= None
        self.bc_dirichlet= None
        self.bc_neumann = None
        self.npatchs = npatchs
        self.dim = dim
        #-----------------------------------
        if self.dim == 1:
            self.f  = lambda x        : [ 0. ]
        if self.dim == 2:
            self.f  = lambda x,y      : [ 0. ]
        if self.dim == 3:
            self.f  = lambda x,y,z    : [ 0. ]
        #-----------------------------------

    def set_AllDirichlet(self):
        self.AllDirichlet = True

    def set_dirichlet_homogeneous(self, patch_id, face_id):
        if self.dirichlet is None:
            self.dirichlet = []
            for i in range(0,self.npatchs):
                self.dirichlet.append([])
        self.dirichlet[patch_id].append(face_id)

    def set_dirichlet_non_homogeneous(self, patch_id, face_id):
        if self.bc_dirichlet is None:
            self.bc_dirichlet = {}
        self.bc_dirichlet[patch_id, face_id] = self.f

    def set_neumann(self, patch_id, face_id):
        if self.bc_neumann is None:
            self.bc_neumann = {}
        self.bc_neumann[patch_id, face_id] = self.f

    def generate_testcase(self):
        testcase = {}
        if self.AllDirichlet is not None:
            testcase['AllDirichlet'] = True
            return testcase

        if self.dirichlet is not None:
            testcase['Dirichlet']    = self.dirichlet

        if self.bc_dirichlet is not None:
            testcase['bc_dirichlet'] = self.bc_dirichlet

        if self.bc_neumann is not None:
            testcase['bc_neumann']   = self.bc_neumann

        return testcase


class DragDropData(wx.CustomDataObject):
    def __init__(self):
        wx.CustomDataObject.__init__(self, wx.CustomDataFormat("MyDropData"))
        self.setObject(None)

    def setObject(self, obj):
        self.SetData(pickle.dumps(obj))

    def getObject(self):
        return pickle.loads(self.GetData())

class DragDropTarget(wx.DropTarget):
    def __init__(self, object):
        wx.DropTarget.__init__(self)
        self.object = object

    def OnDropText(self, x, y, data):
        self.object.InsertStringItem(0, data)

    def OnLeave(self):
        print("OnLeave!!")
        wx.DropTarget.OnLeave(self)

    def OnDragOver(self, x, y, result):
#        wx.DropTarget.OnDragOver(self, x,y,result)
        r = wx.DragLink
        print(r)
        return r


def showKnots(nrb):
    """
    returns a string that contains the list of knots
    """
    txt = ""
    for knots in nrb.knots:
        txt += str(knots)
        txt += "\n"
    return txt

def showConnectivity(geo):
    """
    returns a string that contains the list of clone/original patch/face
    """
    txt = ""
    for dic in geo.connectivity:
        txt += str(dic)
        txt += "\n"
    return txt

def showInternalFaces(geo):
    """
    returns a string that contains the list of internal faces
    """
    txt = ""
    for dic in geo.internal_faces:
        txt += str(dic)
        txt += "\n"
    return txt

def showExternalFaces(geo):
    """
    returns a string that contains the list of external faces
    """
    txt = ""
    for dic in geo.external_faces:
        txt += str(dic)
        txt += "\n"
    return txt

class inspectorTree(wx.TreeCtrl):
    '''Our customized TreeCtrl class
    '''
    def __init__(self, inspector, parent, id, position, size, style):
        '''Initialize our tree
        '''
        wx.TreeCtrl.__init__(self, parent, id, position, size, style)
        self.inspector = inspector
        root = self.AddRoot('caid')
        self.root = root
        self.parent = parent

        # index used and incremented when adding patchs
        self._patch_index = 0
        # index used and incremented when adding geometries
        self._geometry_index = 0

        # ... patchs and geometries
        menu_titles = [  "Show"\
                       , "Hide"\
                       , "Show Mesh"\
                       , "Hide Mesh"\
                       , "Show Control Points"\
                       , "Hide Control Points"\
                       , "Edit Control Points"\
                       , "Copy"\
                       , "Paste"\
                       , "Rename"\
                       , "Color"\
                       , "Mesh steps"\
                       , "Create Vectorial Space"\
                       , "Set Boundary Conditions"\
                       , "Save Boundary Conditions"\
                       , "Dirichlet Boundary Condition"\
                       , "Properties" ]

        self.menu_title_by_id = {}
        for title in menu_titles:
            self.menu_title_by_id[ wx.NewId() ] = title
        # ...

        # ... faces
        menu_titles = ["Extract" \
                       , "Stick-C1"\
                       , "Mark"\
                       , "Clone from Markers"\
                       , "Homogeneous Dirichlet"\
                       , "non Homogeneous Dirichlet"\
                       , "Neumann"]

        self.face_menu_title_by_id = {}
        for title in menu_titles:
            self.face_menu_title_by_id[ wx.NewId() ] = title
        # ...

#        self.MeshColor      = [1.,1.,1.]
#        self.NurbsColor     = [0.,0.,1.]
#        self.PointsColor    = [0.1,0.1,0.1]

    @property
    def enable_inspector_color(self):
        return theme.enable_inspector_color

    def set_enable_inspector_color(self, value):
        theme.set_enable_inspector_color(value)

    def add_geometry(self, geo):
        geo_name = geo.get_attribut("name")
        if geo_name is None:
            geo_name = "Geometry"
        geo_name = geo_name + " [id: " + str(self._geometry_index) + "]"

        geoItem = self.AppendItem(self.root, geo_name, -1,
                                  -1,wx.TreeItemData(geo) )

        if not geo.show:
            color = theme.color_inspector('hide_text')
            color = [int(255*c) for c in color]
            color = wx.Colour(color[0],color[1],color[2])
            self.SetItemTextColour(geoItem, color)

        if self.enable_inspector_color:
            if not geo.show:
                color = theme.color_inspector('hide_text')
                color = [int(255*c) for c in color]
                color = wx.Colour(color[0],color[1],color[2])
                self.SetItemTextColour(geoItem, color)

                color = theme.color_inspector('hide_background')
                color = [int(255*c) for c in color]
                color = wx.Colour(color[0],color[1],color[2])
                self.SetItemBackgroundColour(geoItem, color)
            else:
                color = theme.color_inspector('show_text')
                color = [int(255*c) for c in color]
                color = wx.Colour(color[0],color[1],color[2])
                self.SetItemTextColour(geoItem, color)

                color = geo.get_attribut("color-nurbs")
                if color is not None:
                    color = strtoArray(color)
                if color is None:
                    color = theme.color_viewer('default_geometry')

                color = [int(255*c) for c in color]
                color = wx.Colour(color[0],color[1],color[2])
                self.SetItemBackgroundColour(geoItem, color)

        self._geometry_index += 1

        self._patch_index = 0
        for i in range(0, geo.npatchs):
            nrb = geo[i]
            self.add_patch(geoItem, geo, nrb)
            self._patch_index += 1

        internalFacesItem  = self.AppendItem(geoItem,'Internal-Faces', -1,
                                             -1,wx.TreeItemData(showInternalFaces(geo)))
        externalFacesItem  = self.AppendItem(geoItem, 'External-Faces', -1,
                                             -1,wx.TreeItemData(showExternalFaces(geo)))
        connectivityItem  = self.AppendItem(geoItem, 'Connectivity', -1,
                                            -1,wx.TreeItemData(showConnectivity(geo)))

        return geoItem

    def add_patch(self, geoItem, geo, nrb):
        patch_id    = geo.index(nrb)
        patchInfo   = geo.list_patchInfo[patch_id]

        patch_name = nrb.get_attribut("name")
        if patch_name is None:
            patch_name = "Patch"

        patch_name = patch_name + " [id: " + str(self._patch_index) + "]"
        patchItem  = self.AppendItem(geoItem, patch_name \
                                     , -1, -1,wx.TreeItemData(nrb) )

        if not patchInfo.show:
            color = theme.color_inspector('hide_text')
            color = [int(255*c) for c in color]
            color = wx.Colour(color[0],color[1],color[2])
            self.SetItemTextColour(patchItem, color)

        if self.enable_inspector_color:
            if not patchInfo.show:
                color = theme.color_inspector('hide_text')
                color = [int(255*c) for c in color]
                color = wx.Colour(color[0],color[1],color[2])
                self.SetItemTextColour(patchItem, color)

                color = theme.color_inspector('hide_background')
                color = [int(255*c) for c in color]
                color = wx.Colour(color[0],color[1],color[2])
                self.SetItemBackgroundColour(patchItem, color)
            else:
                color = theme.color_inspector('show_text')
                color = [int(255*c) for c in color]
                color = wx.Colour(color[0],color[1],color[2])
                self.SetItemTextColour(patchItem, color)

                color = nrb.get_attribut("color-nurbs")
                if color is not None:
                    color = strtoArray(color)
                if color is None:
                    color = theme.color_viewer('default_patch')

                color = [int(255*c) for c in color]
                color = wx.Colour(color[0],color[1],color[2])
                self.SetItemBackgroundColour(patchItem, color)

        rationalItem = self.AppendItem(patchItem, 'rational', -1, -1,wx.TreeItemData(nrb.rational) )
        dimensionItem = self.AppendItem(patchItem, 'dimension' \
                                     , -1, -1,wx.TreeItemData(nrb.dim) )
        shapeItem = self.AppendItem(patchItem, 'shape' \
                                     , -1, -1,wx.TreeItemData(nrb.shape) )
        degreeItem = self.AppendItem(patchItem, 'degree' \
                                     , -1, -1,wx.TreeItemData(nrb.degree) )
        knotsItem  = self.AppendItem(patchItem, 'knots', -1,
                                     -1,wx.TreeItemData(showKnots(nrb)) )
        pointsItem  = self.AppendItem(patchItem, 'points', -1, -1,wx.TreeItemData(nrb.points) )
        weightsItem  = self.AppendItem(patchItem, 'weights', -1, -1,wx.TreeItemData(nrb.weights) )
        orientatinItem  = self.AppendItem(patchItem, 'orientation', -1, -1,wx.TreeItemData(nrb.orientation) )
        try:
            color = nrb.get_attributs("color")
            colorItem  = self.AppendItem(patchItem, 'color', -1, -1,wx.TreeItemData(color) )
        except:
            pass
        try:
            name = nrb.get_attributs("name")
            nameItem  = self.AppendItem(patchItem, 'name', -1,
                                        -1,wx.TreeItemData(name) )
        except:
            pass
        try:
            geoattr = nrb.get_attributs("geometry")
            geoattrItem  = self.AppendItem(patchItem, 'geometry', -1,
                                           -1,wx.TreeItemData(geoattr) )
        except:
            pass

        facesItem  = self.AppendItem(patchItem, 'faces', -1,
                                     -1,wx.TreeItemData(None) )

        if (nrb.dim > 1) and (nrb.__class__.__name__ in ["cad_nurbs"]):
            for face in range(0,nrb.nFaces):
                nrb_bnd = nrb.extract_face(face)
                geo_bnd = cad_geometry()
                geo_bnd.append(nrb_bnd)
                _geo = geometry(geo_bnd)
                _geo.face = face
                faceItem  = self.AppendItem(facesItem, 'Face' \
                                             , -1,
                                            -1,wx.TreeItemData(_geo) )

        return patchItem

    def GetItemText(self, item):
        obj = self.GetPyData( item )
        if obj.__class__.__name__=="geometry":
            txt = "cad_geometry"
        elif obj.__class__.__name__=="cad_nurbs":
            txt = "cad_nurbs"
        elif obj.__class__.__name__=="cad_op_nurbs":
            txt = "cad_op_nurbs"
        elif obj.__class__.__name__=="cad_grad_nurbs":
            txt = "cad_grad_nurbs"
        else:
            txt = str(obj)
        return txt

    def SelectedGeometry(self, item):
        obj = self.GetPyData( item )
        try:
            Parent = self.GetItemParent(item)
            if (not self.SelectedPatch(Parent)) \
               and (obj.__class__.__name__ in ["geometry"]):
                return True
            else:
                return False
        except:
            return False

    def SelectedPatch(self, item):
        obj = self.GetPyData( item )
        try:
            if obj.__class__.__name__ in ["cad_nurbs", "cad_op_nurbs", "cad_grad_nurbs"]:
                return True
            else:
                return False
        except:
            return False

    def SelectedFace(self, item):
        obj = self.GetPyData( item )
        try:
            Parent = self.GetItemParent(item)
            Ancestor = self.GetItemParent(Parent)
            if (self.SelectedPatch(Ancestor)) \
               and (obj.__class__.__name__ in ["geometry"]):
                return True
            else:
                return False
        except:
            return False

    def GetCurrentGeometry(self, event):
        item = event.GetItem()
        obj = self.GetPyData( item )
        try:
            Parent = self.GetItemParent(item)
            if (not self.SelectedPatch(Parent)) \
               and (obj.__class__.__name__ in ["geometry"]):
                return obj, item
            else:
                return None, None
        except:
            return None, None

    def GetCurrentPatch(self, event):
        item = event.GetItem()
        obj = self.GetPyData( item )
        try:
            if obj.__class__.__name__ in ["cad_nurbs", "cad_op_nurbs", "cad_grad_nurbs"]:
                return obj, item
            else:
                return None, None
        except:
            return None, None

    def GetCurrentFace(self, event):
        item = event.GetItem()
        obj = self.GetPyData( item )
        try:
            Parent = self.GetItemParent(item)
            Ancestor = self.GetItemParent(Parent)
            if (self.SelectedPatch(Ancestor)) \
               and (obj.__class__.__name__ in ["geometry"]):
                return obj, item
            else:
                return None, None
        except:
            return None, None

    def update(self):
        self.Refresh()

    def Refresh(self):
        self.DeleteChildren(self.root)
        self._geometry_index = 0
        self._patch_index    = 0
        wk = self.inspector.WorkGroup
        for geo in wk.list_geo:
            self.add_geometry(geo)

    def OnSelChanged(self, event):
        '''Method called when selected item is changed
        '''
        # Get the selected item object
        item =  event.GetItem()
        # Display the selected item text in the text widget
        self.inspector.display.SetLabel(self.GetItemText(item))
        # we must check if it is a face before geometry
        # because the face is also a geometry, but it has an ancestor which is a
        # patch
        if self.SelectedFace(item):
            self.inspector.ShowAction(self.inspector.geometryActions)
        elif self.SelectedGeometry(item):
            self.inspector.ShowAction(self.inspector.geometryActions)
        elif self.SelectedPatch(item):
            self.inspector.ShowAction(self.inspector.patchActions)
        else:
            self.inspector.HideAllActions()

        self.inspector.currentGeometry, self.inspector.currentGeometryItem =self.GetCurrentGeometry(event)
        self.inspector.currentPatch, self.inspector.currentPatchItem = self.GetCurrentPatch(event)
        self.inspector.currentFace, self.inspector.currentFaceItem =self.GetCurrentFace(event)

        if self.inspector.currentGeometry is not None:
            self.inspector.currentObject = self.inspector.currentGeometry
            self.inspector.currentObjectItem = self.inspector.currentGeometryItem
        if self.inspector.currentPatch is not None:
            self.inspector.currentObject = self.inspector.currentPatch
            self.inspector.currentObjectItem = self.inspector.currentPatchItem
        if self.inspector.currentFace is not None:
            self.inspector.currentObject = self.inspector.currentFace
            self.inspector.currentObjectItem = self.inspector.currentFaceItem
            self.inspector.currentGeometry      = None
            self.inspector.currentGeometryItem  = None

        self.selectionsItems = self.GetSelections()

        # Highlight and redraw the viewer
#        self.inspector.WorkGroup.viewer.Refresh()
        self.inspector.WorkGroup.Refresh()

    def OnBeginDrag(self, event):
        item = event.GetItem()
        tree = event.GetEventObject()

        if item != tree.GetRootItem(): # prevent dragging root item
            def DoDrag():
                print("Drag'n'Drop still in dev!")
##                wk = self.inspector.WorkGroup
##                patch = wk.inspector.currentObject
##                patchItem = wk.inspector.currentPatchItem
##                geoItem = wk.inspector.tree.GetItemParent(patchItem)
##                geo = wk.inspector.tree.GetPyData(geoItem)
##                print "Starting drag'n'drop with %s..." % repr(id(patch))
##                geo = cad_geometry()
##                geo.append(patch)
##                geo = geometry(geo)
##                dd = DragDropData()
##                dd.setObject(geo)
##
##                comp = wx.DataObjectComposite()
##                comp.Add(dd)
##                dropSource = wx.DropSource(self)
##                dropSource.SetData(comp)
##                result = dropSource.DoDragDrop(wx.Drag_AllowMove)
##                wk.add_geometry(geo)
##                wk.Refresh()
##                print "drag'n'drop finished with:", result, "\n"

#                txt = tree.GetItemText(item)
#                print "Starting Drag with %s..." % repr(txt)
#                dd = DragDropData()
#                dd.setObject(txt)
#
#                comp = wx.DataObjectComposite()
#                comp.Add(dd)
#                tds = wx.DropSource(self)
#                tds.SetData(comp)
#                tds.DoDragDrop(True)

            wx.CallAfter(DoDrag) # can't call dropSource.DoDrag here..

    def OnDragInit(self, event):
        item = event.GetItem()
        tree = event.GetEventObject()
        txt = tree.GetItemText(item)

        dd = DragDropData()
        dd.setObject(txt)
        tdo = wx.DataObjectComposite()
        tdo.Add(dd)

        tds = wx.DropSource(tree)
        tds.SetData(tdo)
        tds.DoDragDrop(True)

    def OnRightMouseClick(self, event):
        # get the current geometry
        geo     = self.inspector.currentGeometry
        if geo is not None:
            self.OnRightMouseClickGeometry(event, geo)
        # get the current Patch
        patch = self.inspector.currentPatch
        if patch is not None:
            patchItem   = self.inspector.currentPatchItem
            geoItem     = self.inspector.tree.GetItemParent(patchItem)
            geo         = self.inspector.tree.GetPyData(geoItem)
            patch_id    = geo.index(patch)
            patchInfo   = geo.list_patchInfo[patch_id]
            self.OnRightMouseClickPatch(event, patchInfo)
        # get the current Face
        face     = self.inspector.currentFace
        if face is not None:
            self.OnRightMouseClickFace(event, face)

    def OnRightMouseClickGeometry(self, event, geo):
        ### 2. Launcher creates wxMenu. ###
        menu = wx.Menu()
        for (id,title) in list(self.menu_title_by_id.items()):
            ### 3. Launcher packs menu with Append. ###
            if not self.inspector.GetEnabledBoundaryConditions():
                toAppend = True
                if geo.show and (title=="Show"):
                    toAppend = False
                if not geo.show and (title=="Hide"):
                    toAppend = False
                if geo.showPoints and (title=="Show Control Points"):
                    toAppend = False
                if not geo.showPoints and (title=="Hide Control Points"):
                    toAppend = False
                if geo.showMesh and (title=="Show Mesh"):
                    toAppend = False
                if not geo.showMesh and (title=="Hide Mesh"):
                    toAppend = False
                if (len(self.inspector.list_copyPatchs) == 0) \
                   and (title=="Paste"):
                    toAppend = False
                if (title=="Save Boundary Conditions"):
                    toAppend = False
                if (title=="Dirichlet Boundary Condition"):
                    toAppend = False
                # Only available for patchs
                if title in ["Edit Control Points", "Copy"]:
                    toAppend = False
            else:
                toAppend = False
                if (title=="Save Boundary Conditions"):
                    toAppend = True
                if (title=="Dirichlet Boundary Condition"):
                    toAppend = True
            if toAppend:
                menu.Append( id, title )
                ### 4. Launcher registers menu handlers with EVT_MENU, on the menu. ###
                wx.EVT_MENU( menu, id, self.MenuSelectionCbGeometry )
        ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        self.parent.PopupMenu( menu, event.GetPoint() )
        menu.Destroy() # destroy to avoid mem leak

    def OnRightMouseClickPatch(self, event, nrbInfo):
        # deactivate if HideAll
        if self.inspector.GetEnabledHideAll():
            return
        ### 2. Launcher creates wxMenu. ###
        menu = wx.Menu()
        for (id,title) in list(self.menu_title_by_id.items()):
            ### 3. Launcher packs menu with Append. ###
            toAppend = True
            if nrbInfo.show and (title=="Show"):
                toAppend = False
            if not nrbInfo.show and (title=="Hide"):
                toAppend = False
            if nrbInfo.showPoints and (title=="Show Control Points"):
                toAppend = False
            if not nrbInfo.showPoints and (title=="Hide Control Points"):
                toAppend = False
            if nrbInfo.showMesh and (title=="Show Mesh"):
                toAppend = False
            if not nrbInfo.showMesh and (title=="Hide Mesh"):
                toAppend = False
            # Only available for geometries
            if title in ["Paste"\
                         , "Set Boundary Conditions"\
                         , "Save Boundary Conditions"\
                         , "Dirichlet Boundary Conditions"\
                         , "Create Vectorial Space"]:
                toAppend = False
            if toAppend:
                menu.Append( id, title )
                ### 4. Launcher registers menu handlers with EVT_MENU, on the menu. ###
                wx.EVT_MENU( menu, id, self.MenuSelectionCbPatch )
        ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        self.parent.PopupMenu( menu, event.GetPoint() )
        menu.Destroy() # destroy to avoid mem leak

    def OnRightMouseClickFace(self, event, face):
        # deactivate if HideAll
        if self.inspector.GetEnabledHideAll() \
           and not self.inspector.GetEnabledBoundaryConditions():
            return
        wk = self.inspector.WorkGroup
        ### 2. Launcher creates wxMenu. ###
        menu = wx.Menu()
        for (id,title) in list(self.face_menu_title_by_id.items()):
            ### 3. Launcher packs menu with Append. ###
            toAppend = True
            if (len(wk.viewer.MarkerPoints) == 0) \
               and (title=="Clone from Markers"):
                toAppend = False
            if (self.inspector.GetEnabledBoundaryConditions()) \
               and (title in ["Extract"\
                              , "Stick-C1"\
                              , "Mark"\
                             , "Clone from Markers"]):
                toAppend = False
            if (not self.inspector.GetEnabledBoundaryConditions()) \
               and (title in ["Homogeneous Dirichlet"\
                             , "non Homogeneous Dirichlet"\
                             , "Neumann"]):
                toAppend = False
            if toAppend:
                menu.Append( id, title )
                ### 4. Launcher registers menu handlers with EVT_MENU, on the menu. ###
                wx.EVT_MENU( menu, id, self.MenuSelectionCbFace)
        ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        self.parent.PopupMenu( menu, event.GetPoint() )
        menu.Destroy() # destroy to avoid mem leak

    def MenuSelectionCbGeometry( self, event ):
        # do something
        operation = self.menu_title_by_id[ event.GetId() ]
        geo     = self.inspector.currentGeometry
        geoItem = self.inspector.currentGeometryItem
        if operation == "Show":
#            geo.Show()
            for Item in self.selectionsItems:
                if self.SelectedGeometry(Item):
                    geo = self.GetPyData(Item)
                    geo.Show()
            self.Refresh()
        if operation == "Hide":
#            geo.Hide()
            for Item in self.selectionsItems:
                if self.SelectedGeometry(Item):
                    geo = self.GetPyData(Item)
                    geo.Hide()
            self.Refresh()
        if operation == "Show Control Points":
            for Item in self.selectionsItems:
                if self.SelectedGeometry(Item):
                    geo = self.GetPyData(Item)
                    geo.showPoints = True
        if operation == "Hide Control Points":
            for Item in self.selectionsItems:
                if self.SelectedGeometry(Item):
                    geo = self.GetPyData(Item)
                    geo.showPoints = False
        if operation == "Show Mesh":
            for Item in self.selectionsItems:
                if self.SelectedGeometry(Item):
                    geo = self.GetPyData(Item)
                    geo.showMesh = True
        if operation == "Hide Mesh":
            for Item in self.selectionsItems:
                if self.SelectedGeometry(Item):
                    geo = self.GetPyData(Item)
                    geo.showMesh = False
        if operation == "Mesh steps":
            for Item in self.selectionsItems:
                if self.SelectedGeometry(Item):
                    geo = self.GetPyData(Item)
                    self.ChooseMeshStepsGeometry(event)
        if operation == "Paste":
            self.inspector.pastePatchs()
        if operation == "Color":
            self.ChooseColorGeometry(event)
        if operation == "Rename":
            from customDialogs import edtTxtDialog
            dlg = edtTxtDialog(None, title="Rename Geometry", size=(200,75))
            dlg.setValue(geo.get_attribut("name"))
            dlg.ShowModal()
            ls_text = dlg.getValue()
            try:
                name = str(ls_text)
            except:
                name = None
            dlg.Destroy()
            if name is not None:
                geo.set_attribut("name",name)
            self.update()
            self.inspector.reset_currentAll()
        if operation == "Create Vectorial Space":
            wk = self.inspector.WorkGroup
            testcase = self.inspector.boundaryConditions.generate_testcase()
            wk.add_space(geo, testcase=testcase)
            self.inspector.boundaryConditions = None
            wk.Refresh()
        if operation == "Set Boundary Conditions":
            wk = self.inspector.WorkGroup
            wk.inspector.SetEnabledBoundaryConditions(True)
            wk.inspector.SetEnabledHideAll(True)
            self.inspector.boundaryConditions = BoundaryConditions(geo.npatchs, geo.dim)
        if operation == "Save Boundary Conditions":
            wk = self.inspector.WorkGroup
            wk.inspector.SetEnabledBoundaryConditions(False)
            wk.inspector.SetEnabledHideAll(False)
            print("===========================")
            print("Boundary Conditions ")
            print((self.inspector.boundaryConditions.AllDirichlet))
            print((self.inspector.boundaryConditions.dirichlet))
            print((self.inspector.boundaryConditions.bc_dirichlet))
            print((self.inspector.boundaryConditions.bc_neumann))
            print("===========================")
        if operation == "Dirichlet Boundary Condition":
            self.inspector.boundaryConditions.set_AllDirichlet()
            wk = self.inspector.WorkGroup
            wk.inspector.SetEnabledBoundaryConditions(False)
            wk.inspector.SetEnabledHideAll(False)
            print("===========================")
            print("Boundary Conditions ")
            print((self.inspector.boundaryConditions.AllDirichlet))
            print((self.inspector.boundaryConditions.dirichlet))
            print((self.inspector.boundaryConditions.bc_dirichlet))
            print((self.inspector.boundaryConditions.bc_neumann))
            print("===========================")
        # Refresh the viewer
#        self.inspector.WorkGroup.viewer.Refresh()
        self.inspector.WorkGroup.Refresh()

    def MenuSelectionCbPatch( self, event ):
        # do something
        wk = self.inspector.WorkGroup
        patch       = self.inspector.currentPatch
        patchItem   = self.inspector.currentPatchItem
        geoItem     = self.inspector.tree.GetItemParent(patchItem)
        geo         = self.inspector.tree.GetPyData(geoItem)
        patch_id    = geo.index(patch)
        patchInfo   = geo.list_patchInfo[patch_id]
        operation   = self.menu_title_by_id[ event.GetId() ]
        if operation == "Show":
            for Item in self.selectionsItems:
                if self.SelectedPatch(Item):
                    patch = self.GetPyData(Item)
                    patchItem = Item
                    geoItem     = self.inspector.tree.GetItemParent(patchItem)
                    geo         = self.inspector.tree.GetPyData(geoItem)
                    patch_id    = geo.index(patch)
                    patchInfo   = geo.list_patchInfo[patch_id]

                    patchInfo.show = True
        if operation == "Hide":
            for Item in self.selectionsItems:
                if self.SelectedPatch(Item):
                    patch = self.GetPyData(Item)
                    patchItem = Item
                    geoItem     = self.inspector.tree.GetItemParent(patchItem)
                    geo         = self.inspector.tree.GetPyData(geoItem)
                    patch_id    = geo.index(patch)
                    patchInfo   = geo.list_patchInfo[patch_id]

                    patchInfo.show = False
        if operation == "Show Control Points":
            for Item in self.selectionsItems:
                if self.SelectedPatch(Item):
                    patch = self.GetPyData(Item)
                    patchItem = Item
                    geoItem     = self.inspector.tree.GetItemParent(patchItem)
                    geo         = self.inspector.tree.GetPyData(geoItem)
                    patch_id    = geo.index(patch)
                    patchInfo   = geo.list_patchInfo[patch_id]

                    patchInfo.showPoints = True
        if operation == "Hide Control Points":
            for Item in self.selectionsItems:
                if self.SelectedPatch(Item):
                    patch = self.GetPyData(Item)
                    patchItem = Item
                    geoItem     = self.inspector.tree.GetItemParent(patchItem)
                    geo         = self.inspector.tree.GetPyData(geoItem)
                    patch_id    = geo.index(patch)
                    patchInfo   = geo.list_patchInfo[patch_id]

                    patchInfo.showPoints = False
        if operation == "Show Mesh":
            for Item in self.selectionsItems:
                if self.SelectedPatch(Item):
                    patch = self.GetPyData(Item)
                    patchItem = Item
                    geoItem     = self.inspector.tree.GetItemParent(patchItem)
                    geo         = self.inspector.tree.GetPyData(geoItem)
                    patch_id    = geo.index(patch)
                    patchInfo   = geo.list_patchInfo[patch_id]

                    patchInfo.showMesh = True
        if operation == "Hide Mesh":
            for Item in self.selectionsItems:
                if self.SelectedPatch(Item):
                    patch = self.GetPyData(Item)
                    patchItem = Item
                    geoItem     = self.inspector.tree.GetItemParent(patchItem)
                    geo         = self.inspector.tree.GetPyData(geoItem)
                    patch_id    = geo.index(patch)
                    patchInfo   = geo.list_patchInfo[patch_id]

                    patchInfo.showMesh = False
        if operation == "Copy":
            self.inspector.copyPatch()
        if operation == "Color":
            self.ChooseColorPatch(event)
        if operation == "Mesh steps":
            self.ChooseMeshStepsPatch(event)
        if operation == "Rename":
            from customDialogs import edtTxtDialog
            dlg = edtTxtDialog(None, title="Rename Patch", size=(200,75) )
            dlg.setValue(patch.get_attribut("name"))
            dlg.ShowModal()
            ls_text = dlg.getValue()
            try:
                name = str(ls_text)
            except:
                name = None
            dlg.Destroy()
            if name is not None:
                patchInfo.set_name(name)
            self.update()
            self.inspector.reset_currentAll()

        if operation == "Edit Control Points":
            from customDialogs import edtControlPoints
            xyzCenter = wk.viewer.lookAt.GetCenter()
            dlg = edtControlPoints(wk)
            dlg.ShowModal()
            dlg.patchInfo.showPoints = False
            dlg.Destroy()
            wk.viewer.CleanSelectedPoints()
        # Refresh the viewer
        wk.Refresh()

    def MenuSelectionCbFace( self, event ):
        # do something
        operation = self.face_menu_title_by_id[ event.GetId() ]
        face     = self.inspector.currentFace
        faceItem = self.inspector.currentFaceItem
        if operation == "Extract":
            wk = self.inspector.WorkGroup
            patchItem = self.GetItemParent(self.GetItemParent(faceItem))
            patch     = self.GetPyData(patchItem)
            face_id = face.face
            nrb = patch.extract_face(face_id)
            geoItem = self.inspector.tree.GetItemParent(patchItem)
            geo = self.inspector.tree.GetPyData(geoItem)
            wk.add_patch(geoItem, geo, nrb)
            wk.Refresh()
        if operation == "Stick-C1":
            self.inspector.ShowAction(self.inspector.patchActionsStickC1)
        if operation == "Mark":
            wk = self.inspector.WorkGroup
            patchItem = self.GetItemParent(self.GetItemParent(faceItem))
            patch     = self.GetPyData(patchItem)
            face_id = face.face
            nrb = patch.extract_face(face_id)
            from geometry import controlToList
            X,Y,Z,W = controlToList(nrb.control)
            for x,y,z,w in zip(X,Y,Z,W):
                P = [x,y,z,w]
                wk.viewer.AddMarkerPoint(P)
            wk.Refresh()
        if operation == "Clone from Markers":
            wk = self.inspector.WorkGroup
            patchItem = self.GetItemParent(self.GetItemParent(faceItem))
            patch     = self.GetPyData(patchItem)
            face_id = face.face

            n = len(wk.viewer.MarkerPoints)
            # TODO copy weights
            P = np.zeros((n,4))
            for i in range(0,n):
                P[i,:] = wk.viewer.MarkerPoints[i]

            control = patch.control
            if patch.dim == 2:
                if face_id == 0:
                    control[:,0,:]  = P[:,:]
                if face_id == 1:
                    control[0,:,:]  = P[:,:]
                if face_id == 2:
                    control[:,-1,:] = P[:,:]
                if face_id == 3:
                    control[-1,:,:] = P[:,:]

            wk.viewer.CleanMarkerPoints()
            # TODO add set_weights in igakit.nurbs
            patch._array = control
            patch.set_points(control[...,:3])
            wk.Refresh(inspector=True)
        if operation == "Homogeneous Dirichlet":
            wk = self.inspector.WorkGroup
            patchItem = self.GetItemParent(self.GetItemParent(faceItem))
            patch     = self.GetPyData(patchItem)
            geoItem = self.inspector.tree.GetItemParent(patchItem)
            geo = self.inspector.tree.GetPyData(geoItem)
            patch_id = geo.index(patch)
            face_id = face.face
            self.inspector.boundaryConditions.set_dirichlet_homogeneous(patch_id,face_id)
        if operation == "non Homogeneous Dirichlet":
            wk = self.inspector.WorkGroup
            patchItem = self.GetItemParent(self.GetItemParent(faceItem))
            patch     = self.GetPyData(patchItem)
            geoItem = self.inspector.tree.GetItemParent(patchItem)
            geo = self.inspector.tree.GetPyData(geoItem)
            patch_id = geo.index(patch)
            face_id = face.face
            self.inspector.boundaryConditions.set_dirichlet_non_homogeneous(patch_id,face_id)
        if operation == "Neumann":
            wk = self.inspector.WorkGroup
            patchItem = self.GetItemParent(self.GetItemParent(faceItem))
            patch     = self.GetPyData(patchItem)
            geoItem = self.inspector.tree.GetItemParent(patchItem)
            geo = self.inspector.tree.GetPyData(geoItem)
            patch_id = geo.index(patch)
            face_id = face.face
            self.inspector.boundaryConditions.set_neumann(patch_id,face_id)
        # Refresh the viewer
        self.inspector.WorkGroup.Refresh()

    def ChooseColorGeometry(self, event):
        geo     = self.inspector.currentGeometry
        if geo.NurbsColor is None:
            colors = theme.color_viewer("default_geometry") # [100, 130, 45]
            values = [int(255*x) for x in colors]
        else:
            values = [int(255*x) for x in geo.NurbsColor]
        colorData = wx.ColourData()
        colorData.SetColour(wx.Colour(*values))

        dlg = wx.ColourDialog(self, colorData)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            values = data.GetColour().Get()
            values = np.asarray(values) * 1./255.
        dlg.Destroy()

        for Item in self.selectionsItems:
            if self.SelectedGeometry(Item):
                geo = self.GetPyData(Item)
                geo.set_nurbsColor(values)

        self.Refresh()
        self.inspector.WorkGroup.Refresh()

    def ChooseColorPatch(self, event):
        patch       = self.inspector.currentPatch
        patchItem   = self.inspector.currentPatchItem
        geoItem     = self.inspector.tree.GetItemParent(patchItem)
        geo         = self.inspector.tree.GetPyData(geoItem)
        patch_id    = geo.index(patch)
        patchInfo   = geo.list_patchInfo[patch_id]

        if patchInfo.NurbsColor is not None:
            values = [int(255*x) for x in patchInfo.NurbsColor]
        elif geo.NurbsColor is not None:
            values = [int(255*x) for x in geo.NurbsColor]
        else:
            colors = theme.color_viewer("default_patch") # patchInfo.NurbsColor
            values = [int(255*x) for x in colors]

        colorData = wx.ColourData()
        colorData.SetColour(wx.Colour(*values))
        dlg = wx.ColourDialog(self, colorData)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            values = data.GetColour().Get()
            values = np.asarray(values) * 1./255.
        dlg.Destroy()

        for Item in self.selectionsItems:
            if self.SelectedPatch(Item):
                patch = self.GetPyData(Item)
                patchItem = Item
                geoItem     = self.inspector.tree.GetItemParent(patchItem)
                geo         = self.inspector.tree.GetPyData(geoItem)
                patch_id    = geo.index(patch)
                patchInfo   = geo.list_patchInfo[patch_id]
                patchInfo.set_nurbsColor(values)

        patchInfo.set_nurbsColor(values)
        self.Refresh()
        self.inspector.WorkGroup.Refresh()

    def ChooseMeshStepsGeometry(self, event):
        geo         = self.inspector.currentGeometry
        geoItem     = self.inspector.currentGeometryItem

        from customDialogs import edtTxtDialog
        dlg = edtTxtDialog(None, title="Edit Mesh step", size=(200,75) )
        patchInfo = geo.list_patchInfo[0]
        if patchInfo.steps is not None:
            dlg.setValue(str(patchInfo.steps[0]))
        dlg.ShowModal()
        ls_text = dlg.getValue()
        try:
            step = int(ls_text)
        except:
            step = 5
        dlg.Destroy()

        for patchInfo in geo.list_patchInfo:
            patchInfo.set_steps([step,step,step])
        self.inspector.WorkGroup.Refresh()

    def ChooseMeshStepsPatch(self, event):
        patch       = self.inspector.currentPatch
        patchItem   = self.inspector.currentPatchItem
        geoItem     = self.inspector.tree.GetItemParent(patchItem)
        geo         = self.inspector.tree.GetPyData(geoItem)
        patch_id    = geo.index(patch)
        patchInfo   = geo.list_patchInfo[patch_id]

        from customDialogs import edtTxtDialog
        dlg = edtTxtDialog(None, title="Edit Mesh step" , size=(200,75))
        if patchInfo.steps is not None:
            dlg.setValue(str(patchInfo.steps[0]))
        dlg.ShowModal()
        ls_text = dlg.getValue()
        try:
            step = int(ls_text)
        except:
            step = 5
        dlg.Destroy()

        patchInfo.set_steps([step,step,step])
        self.inspector.WorkGroup.Refresh()

class Inspector(wx.Frame):
    '''Our customized window class
    '''
    def __init__(self, workgroup, parent, id, title \
                 , pos \
                 , size):
        '''Initialize our window
        '''
        wx.Frame.__init__(self, parent, id, title, pos=pos, size=size)

        self.parent = parent
        self.WorkGroup = workgroup

        self.currentGeometry        = None
        self.currentGeometryItem    = None
        self.currentPatch           = None
        self.currentPatchItem       = None
        self.currentFace            = None
        self.currentFaceItem        = None
        self.currentObject          = None
        self.currentObjectItem      = None

        # if true activate boundary conditions selection mode
        self.EnabledBoundaryConditions = False
        self.boundaryConditions     = None

        # needed to hide all actions if boundary conditions mode is activated
        self.EnabledHideAll = False

        # used whenever we right-click and copy a patch
        # when right-click on paste, we append the elements of this list
        # into the selected geometry
        self.list_copyPatchs        = []

        # Create a splitter window
        self.splitter = wx.SplitterWindow(self, -1)

        # Create the left panel
        self.leftPanel = wx.Panel(self.splitter, -1)
#        self.leftPanel = wx.ScrolledWindow(self.splitter, -1)
        # Create a box sizer that will contain the left panel contents
        self.leftBox = wx.BoxSizer(wx.VERTICAL)
        # Create our tree and put it into the left panel
        self.tree = inspectorTree(self, self.leftPanel, 1, wx.DefaultPosition, (-1, -1),
                           wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_MULTIPLE)
        # Add the tree to the box sizer
        self.leftBox.Add(self.tree, 1, wx.EXPAND)
        # Bind the OnSelChanged method to the tree
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.tree.OnSelChanged, id=1)
        # Bind the right mouse click
        self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.tree.OnRightMouseClick, id=1)
        # Bind Drag And Drop capability
#        self.tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self.tree.OnBeginDrag)
#        dt = DragDropTarget(self.tree)
#        self.tree.SetDropTarget(dt)
        self.tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self.tree.OnDragInit)
        # Set the size of the right panel to that required by the tree
        self.leftPanel.SetSizer(self.leftBox)

        # Create the right panel
#        self.rightPanel  = wx.Panel(self.splitter, -1)
        self.rightPanel  = scrolled.ScrolledPanel(self.splitter, -1)
#        self.rightPanel = wx.ScrolledWindow(self.splitter, -1)
#        self.rightPanel.EnableScrolling(False, True)
#        self.rightPanel.SetAutoLayout(True)
        # Create the right box sizer that will contain the panel's contents
        self.displayBox = wx.BoxSizer(wx.VERTICAL)
        # Create a widget to display static text and store it in the right
        # panel
        self.display = wx.StaticText(self.rightPanel, -1, '', (10, 10),
                                     style=wx.ALIGN_LEFT)
        # Add the display widget to the right panel
        self.displayBox.Add(self.display, 1, wx.EXPAND)

        # the rightBox is a container for buttonGeometryBox and displayBox
        self.rightBox = wx.BoxSizer(wx.HORIZONTAL)
        self.rightBox.Add(self.displayBox, 1, wx.EXPAND)

        self.actionsPanel = self.rightPanel
        self.actionsBox = self.rightBox

        self.list_actions = []
        self.geometryActions    = GeometryActions(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.geometryActions)
        self.geometryActionsNew = GeometryActionsNew(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.geometryActionsNew)
        self.geometryActionsAdd = GeometryActionsAdd(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.geometryActionsAdd)
        self.geometryActionsRefine = GeometryActionsRefine(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.geometryActionsRefine)

        self.patchActionsRefine = PatchActionsRefine(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsRefine)
        self.patchActionsElevate = PatchActionsElevate(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsElevate)
        self.patchActionsSwap = PatchActionsSwap(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsSwap)
        self.patchActionsReverse = PatchActionsReverse(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsReverse)
        self.patchActionsExtract = PatchActionsExtract(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsExtract)
        self.patchActionsExtrude = PatchActionsExtrude(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsExtrude)
        self.patchActions       = PatchActions(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActions)
        self.patchActionsSplit = PatchActionsSplit(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsSplit)
        self.patchActionsClonePoints = PatchActionsClonePoints(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsClonePoints)
        self.patchActionsTCoons = PatchActionsTCoons(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsTCoons)
        self.patchActionsApproximate = PatchActionsApproximate(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsApproximate)
        self.patchActionsStickC1 = PatchActionsStickC1(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsStickC1)
        self.patchActionsInsert = PatchActionsInsert(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsInsert)
        self.patchActionsRemap = PatchActionsRemap(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsRemap)
        self.patchActionsRemove = PatchActionsRemove(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsRemove)
        self.patchActionsSlice = PatchActionsSlice(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsSlice)
        self.patchActionsClamp = PatchActionsClamp(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsClamp)
        self.patchActionsUnclamp = PatchActionsUnclamp(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsUnclamp)
        self.patchActionsRevolve = PatchActionsRevolve(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.patchActionsRevolve)

        self.objectActionsTranslate = ObjectActionsTranslate(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsTranslate)
        self.objectActionsRotate = ObjectActionsRotate(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsRotate)
        self.objectActionsScale = ObjectActionsScale(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsScale)
        self.objectActionsCreateArc = ObjectActionsCreateArc(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsCreateArc)
        self.objectActionsCreateLinear = ObjectActionsCreateLinear(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsCreateLinear)
        self.objectActionsCreateBilinear = ObjectActionsCreateBilinear(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsCreateBilinear)
        self.objectActionsCreateCircle = ObjectActionsCreateCircle(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsCreateCircle)
        self.objectActionsCreateQuartCircle = ObjectActionsCreateQuartCircle(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsCreateQuartCircle)
        self.objectActionsCreateAnnulus = ObjectActionsCreateAnnulus(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsCreateAnnulus)
        self.objectActionsCreateCircle_5mp = ObjectActionsCreateCircle_5mp(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsCreateCircle_5mp)
        self.objectActionsCreateTriangle = ObjectActionsCreateTriangle(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsCreateTriangle)
        self.objectActionsPolarExtrude = ObjectActionsPolarExtrude(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsPolarExtrude)
        self.objectActionsCurve = ObjectActionsCurve(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsCurve)
        self.objectActionsJoin = ObjectActionsJoin(self, self.actionsPanel, self.actionsBox)
        self.list_actions.append(self.objectActionsJoin)


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
#        self.Bind(wx.EVT_CHAR       , self.key)
#        self.Bind(wx.EVT_KEY_DOWN   , self.onKeyPressDown)
        self.Bind(wx.EVT_KEY_UP     , self.onKeyPressUp)

    def reset_currentAll(self):
        self.currentGeometry        = None
        self.currentGeometryItem    = None
        self.currentPatch           = None
        self.currentPatchItem       = None
        self.currentObject          = None
        self.currentObjectItem      = None

    def GetEnabledBoundaryConditions(self):
        return self.EnabledBoundaryConditions

    def SetEnabledBoundaryConditions(self, value):
        self.EnabledBoundaryConditions =  value

    def GetEnabledHideAll(self):
        return self.EnabledHideAll

    def SetEnabledHideAll(self, value):
        self.EnabledHideAll =  value
        if value:
            self.HideAllActions()

    def copyPatch(self):
        # Multiple selection is possible
        wk = self.WorkGroup
        for Item in self.tree.selectionsItems:
            if self.tree.SelectedPatch(Item):
                patch = self.tree.GetPyData(Item)
                self.list_copyPatchs.append(patch)

        # macro recording
        if wk.macroRecording:
            macro_script = wk.macro_script
            macro_script.new_line()
            macro_script.append("# ... copy selected patchs")
            list_gp = []
            for item in wk.inspector.tree.selectionsItems:
                patch   = wk.inspector.tree.GetPyData(item)
                geoItem = wk.inspector.tree.GetItemParent(item)
                geo     = wk.inspector.tree.GetPyData(geoItem)
                list_gp.append([geo, patch])

            macro_script.append("list_copyPatchs = []")
            for i,gp in enumerate(list_gp):
                geo = gp[0] ; patch = gp[1]
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("list_copyPatchs.append(patch)")

            macro_script.append("# ...")


    def pastePatchs(self):
        wk = self.WorkGroup
        geo     = self.currentGeometry
        geoItem = self.currentGeometryItem
        # add all copy patchs
        for patch in self.list_copyPatchs:
            nrb = patch.copy()
            wk.add_patch(geoItem, geo, nrb)

        # macro recording
        if wk.macroRecording:
            macro_script = wk.macro_script
            macro_script.new_line()
            macro_script.append("# ... paste selected patchs")
            geo_id = wk.list_geo.index(geo)
            macro_script.append("geo_id = "+str(geo_id))
            macro_script.append("geo = geometries[geo_id]")
            macro_script.append("geoItem = geo.treeItem")
            macro_script.append("for patch in list_copyPatchs:")
            macro_script.append("\tcad_nrb = patch.copy()")
            macro_script.append("\twk.add_patch(geoItem, geo, cad_nrb)")
            macro_script.append("wk.Refresh(inspector=True)")
            macro_script.append("# ...")

        # clean the list copy patchs
        self.cleanCopyPatchs()

    def cleanCopyPatchs(self):
        self.list_copyPatchs = []
        wk = self.WorkGroup
        # macro recording
        if wk.macroRecording:
            macro_script = wk.macro_script
            macro_script.new_line()
            macro_script.append("# ... clean Copy Patchs")
            macro_script.append("list_copyPatchs = []")
            macro_script.append("# ...")

    def add_geometry(self, geo):
        geoItem = self.tree.add_geometry(geo)
        return geoItem

    def add_patch(self, geoItem, geo, nrb):
        return self.tree.add_patch(geoItem, geo, nrb)

    def remove_geometry(self, geoItem):
        self.tree.Delete(geoItem)

    def remove_patch(self, patchItem):
        self.tree.Delete(patchItem)

    def HideAllActions(self):
        for action in self.list_actions:
            action.Hide()
        self.rightBox.Layout()

    def ShowAction(self, act):
        if self.GetEnabledHideAll():
            return
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
            self.OnTranslateGeometry(event)

    def onKeyPressUp(self, event):
        wk = self.WorkGroup
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE:
            wk.directAct.removeObject()
        if keycode == wx.WXK_F2:
            wk.directAct.renameObject()

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
