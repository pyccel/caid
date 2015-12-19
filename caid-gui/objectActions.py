# -*- coding: UTF-8 -*-
import wx
from geometry import geometry
from caid.cad_geometry import cad_geometry, cad_nurbs
from viewer import Viewer
from numpy import pi, linspace, array, asarray
import numpy as np
from classActions import ObjectClassActions

class ObjectActionsCreateCircle(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.radius = 1.
        self.center = np.asarray([0.,0.,0.])

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "radius")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlRadiusId = wx.NewId()
        self.txtCtrlRadius = wx.TextCtrl(parentPanel, self.txtCtrlRadiusId, size=(50,25))
        self.txtCtrlRadius.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlRadius.SetValue(str(self.radius))
        hbox.Add(self.txtCtrlRadius, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "x")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlxId = wx.NewId()
        self.txtCtrlx = wx.TextCtrl(parentPanel, self.txtCtrlxId, size=(50,25))
        self.txtCtrlx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlx.SetValue(str(self.center[0]))
        hbox.Add(self.txtCtrlx, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "y")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlyId = wx.NewId()
        self.txtCtrly = wx.TextCtrl(parentPanel, self.txtCtrlyId, size=(50,25))
        self.txtCtrly.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrly.SetValue(str(self.center[1]))
        hbox.Add(self.txtCtrly, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "z")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlzId = wx.NewId()
        self.txtCtrlz = wx.TextCtrl(parentPanel, self.txtCtrlzId, size=(50,25))
        self.txtCtrlz.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlz.SetValue(str(self.center[2]))
        hbox.Add(self.txtCtrlz, border=5)

        self.Box.Add(hbox, border=5)
        # ...

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            from caid.cad_geometry import circle as domain
            _geo = domain(radius=self.radius, center=self.center)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... create object")
                macro_script.append("radius = "+str(self.radius))
                macro_script.append("center = "+str(list(self.center)))
            if self.patch:
                nrb = _geo[0]
                wk.add_patch(geoItem, geo, nrb)
                # macro recording
                if wk.macroRecording:
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("cad_nrb = circle(radius=radius, center=center)[0]")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)
            else:
                geo_new = geometry(_geo)
                geo_newItem = wk.add_geometry(geo_new)
                # macro recording
                if wk.macroRecording:
                    macro_script.append("_geo = circle(radius=radius, center=center)")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("# ...")

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlRadiusId:
                self.radius = float(event.GetString())
            if event.GetId() == self.txtCtrlxId:
                self.EvtCenterText(event, 0)
            if event.GetId() == self.txtCtrlyId:
                self.EvtCenterText(event, 1)
            if event.GetId() == self.txtCtrlzId:
                self.EvtCenterText(event, 2)
        except:
            pass

    def EvtCenterText(self, event, i):
        try :
            self.center[i] = float(event.GetString())
        except:
            pass

class ObjectActionsCreateQuartCircle(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.rmin = 0.5
        self.rmax = 1.
        self.center = np.asarray([0.,0.,0.])

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "rmin")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlRadiusMinId = wx.NewId()
        self.txtCtrlRadiusMin = wx.TextCtrl(parentPanel, self.txtCtrlRadiusMinId)
        self.txtCtrlRadiusMin.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlRadiusMin.SetValue(str(self.rmin))
        hbox.Add(self.txtCtrlRadiusMin, border=5)

        self.Box.Add(hbox, border=10)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(parentPanel, -1, "rmax")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlRadiusMaxId = wx.NewId()
        self.txtCtrlRadiusMax = wx.TextCtrl(parentPanel, self.txtCtrlRadiusMaxId)
        self.txtCtrlRadiusMax.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlRadiusMax.SetValue(str(self.rmax))
        hbox.Add(self.txtCtrlRadiusMax, border=5)

        self.Box.Add(hbox, border=10)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "x")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlxId = wx.NewId()
        self.txtCtrlx = wx.TextCtrl(parentPanel, self.txtCtrlxId, size=(50,25))
        self.txtCtrlx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlx.SetValue(str(self.center[0]))
        hbox.Add(self.txtCtrlx, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "y")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlyId = wx.NewId()
        self.txtCtrly = wx.TextCtrl(parentPanel, self.txtCtrlyId, size=(50,25))
        self.txtCtrly.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrly.SetValue(str(self.center[1]))
        hbox.Add(self.txtCtrly, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "z")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlzId = wx.NewId()
        self.txtCtrlz = wx.TextCtrl(parentPanel, self.txtCtrlzId, size=(50,25))
        self.txtCtrlz.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlz.SetValue(str(self.center[2]))
        hbox.Add(self.txtCtrlz, border=5)

        self.Box.Add(hbox, border=5)
        # ...

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            from caid.cad_geometry import quart_circle as domain
            _geo = domain(rmin=self.rmin, rmax=self.rmax, center=self.center)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... create object")
                macro_script.append("rmin = "+str(self.rmin))
                macro_script.append("rmax = "+str(self.rmax))
                macro_script.append("center = "+str(list(self.center)))
            if self.patch:
                nrb = _geo[0]
                wk.add_patch(geoItem, geo, nrb)
                # macro recording
                if wk.macroRecording:
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("cad_nrb = quart_circle(rmin=rmin, rmax=rmax, center=center)[0]")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)
            else:
                geo_new = geometry(_geo)
                geo_newItem = wk.add_geometry(geo_new)
                # macro recording
                if wk.macroRecording:
                    macro_script.append("_geo = quart_circle(rmin=rmin, rmax=rmax, center=center)")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("# ...")

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlRadiusMinId:
                self.rmin = float(event.GetString())
            if event.GetId() == self.txtCtrlRadiusMaxId:
                self.rmax= float(event.GetString())
            if event.GetId() == self.txtCtrlEpsilonId:
                self.epsilon= float(event.GetString())
            if event.GetId() == self.txtCtrlxId:
                self.EvtCenterText(event, 0)
            if event.GetId() == self.txtCtrlyId:
                self.EvtCenterText(event, 1)
            if event.GetId() == self.txtCtrlzId:
                self.EvtCenterText(event, 2)
        except:
            pass

    def EvtCenterText(self, event, i):
        try :
            self.center[i] = float(event.GetString())
        except:
            pass

class ObjectActionsCreateAnnulus(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.rmin = 0.5
        self.rmax = 1.
        self.center = np.asarray([0.,0.,0.])

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "rmin")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlRadiusMinId = wx.NewId()
        self.txtCtrlRadiusMin = wx.TextCtrl(parentPanel, self.txtCtrlRadiusMinId)
        self.txtCtrlRadiusMin.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlRadiusMin.SetValue(str(self.rmin))
        hbox.Add(self.txtCtrlRadiusMin, border=5)

        self.Box.Add(hbox, border=10)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(parentPanel, -1, "rmax")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlRadiusMaxId = wx.NewId()
        self.txtCtrlRadiusMax = wx.TextCtrl(parentPanel, self.txtCtrlRadiusMaxId)
        self.txtCtrlRadiusMax.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlRadiusMax.SetValue(str(self.rmax))
        hbox.Add(self.txtCtrlRadiusMax, border=5)

        self.Box.Add(hbox, border=10)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "x")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlxId = wx.NewId()
        self.txtCtrlx = wx.TextCtrl(parentPanel, self.txtCtrlxId, size=(50,25))
        self.txtCtrlx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlx.SetValue(str(self.center[0]))
        hbox.Add(self.txtCtrlx, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "y")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlyId = wx.NewId()
        self.txtCtrly = wx.TextCtrl(parentPanel, self.txtCtrlyId, size=(50,25))
        self.txtCtrly.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrly.SetValue(str(self.center[1]))
        hbox.Add(self.txtCtrly, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "z")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlzId = wx.NewId()
        self.txtCtrlz = wx.TextCtrl(parentPanel, self.txtCtrlzId, size=(50,25))
        self.txtCtrlz.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlz.SetValue(str(self.center[2]))
        hbox.Add(self.txtCtrlz, border=5)

        self.Box.Add(hbox, border=5)
        # ...

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            from caid.cad_geometry import annulus as domain
            _geo = domain(rmin=self.rmin, rmax=self.rmax, center=self.center)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... create object")
                macro_script.append("rmin = "+str(self.rmin))
                macro_script.append("rmax = "+str(self.rmax))
                macro_script.append("center = "+str(list(self.center)))
            if self.patch:
                nrb = _geo[0]
                wk.add_patch(geoItem, geo, nrb)
                # macro recording
                if wk.macroRecording:
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("cad_nrb = annulus(rmin=rmin, rmax=rmax, center=center)[0]")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)
            else:
                geo_new = geometry(_geo)
                geo_newItem = wk.add_geometry(geo_new)
                # macro recording
                if wk.macroRecording:
                    macro_script.append("_geo = annulus(rmin=rmin, rmax=rmax, center=center)")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("# ...")

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlRadiusMinId:
                self.rmin = float(event.GetString())
            if event.GetId() == self.txtCtrlRadiusMaxId:
                self.rmax= float(event.GetString())
            if event.GetId() == self.txtCtrlxId:
                self.EvtCenterText(event, 0)
            if event.GetId() == self.txtCtrlyId:
                self.EvtCenterText(event, 1)
            if event.GetId() == self.txtCtrlzId:
                self.EvtCenterText(event, 2)
        except:
            pass

    def EvtCenterText(self, event, i):
        try :
            self.center[i] = float(event.GetString())
        except:
            pass

class ObjectActionsCreateCircle_5mp(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.rmin = 0.5
        self.rmax = 1.
        self.center = np.asarray([0.,0.,0.])

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "rmin")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlRadiusMinId = wx.NewId()
        self.txtCtrlRadiusMin = wx.TextCtrl(parentPanel, self.txtCtrlRadiusMinId)
        self.txtCtrlRadiusMin.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlRadiusMin.SetValue(str(self.rmin))
        hbox.Add(self.txtCtrlRadiusMin, border=5)

        self.Box.Add(hbox, border=10)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(parentPanel, -1, "rmax")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlRadiusMaxId = wx.NewId()
        self.txtCtrlRadiusMax = wx.TextCtrl(parentPanel, self.txtCtrlRadiusMaxId)
        self.txtCtrlRadiusMax.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlRadiusMax.SetValue(str(self.rmax))
        hbox.Add(self.txtCtrlRadiusMax, border=5)

        self.Box.Add(hbox, border=10)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "x")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlxId = wx.NewId()
        self.txtCtrlx = wx.TextCtrl(parentPanel, self.txtCtrlxId, size=(50,25))
        self.txtCtrlx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlx.SetValue(str(self.center[0]))
        hbox.Add(self.txtCtrlx, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "y")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlyId = wx.NewId()
        self.txtCtrly = wx.TextCtrl(parentPanel, self.txtCtrlyId, size=(50,25))
        self.txtCtrly.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrly.SetValue(str(self.center[1]))
        hbox.Add(self.txtCtrly, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "z")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlzId = wx.NewId()
        self.txtCtrlz = wx.TextCtrl(parentPanel, self.txtCtrlzId, size=(50,25))
        self.txtCtrlz.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlz.SetValue(str(self.center[2]))
        hbox.Add(self.txtCtrlz, border=5)

        self.Box.Add(hbox, border=5)
        # ...

                
    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            from caid.cad_geometry import circle_5mp as domain
            _geo = domain(rmin=self.rmin, rmax=self.rmax, center=self.center)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... create object")
                macro_script.append("rmin = "+str(self.rmin))
                macro_script.append("rmax = "+str(self.rmax))
                macro_script.append("center = "+str(list(self.center)))
            if self.patch:
                for nrb in _geo:
                    wk.add_patch(geoItem, geo, nrb)
                # macro recording
                if wk.macroRecording:
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("_geo = circle_5mp(rmin=rmin, rmax=rmax, center=center)")
                    macro_script.append("for nrb in _geo:")
                    macro_script.append("\twk.add_patch(geoItem, geo, nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)
            else:
                geo_new = geometry(_geo)
                geo_newItem = wk.add_geometry(geo_new)
                # macro recording
                if wk.macroRecording:
                    macro_script.append("_geo = circle_5mp(rmin=rmin, rmax=rmax, center=center)")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("# ...")

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlRadiusMinId:
                self.rmin = float(event.GetString())
            if event.GetId() == self.txtCtrlRadiusMaxId:
                self.rmax= float(event.GetString())
            if event.GetId() == self.txtCtrlxId:
                self.EvtCenterText(event, 0)
            if event.GetId() == self.txtCtrlyId:
                self.EvtCenterText(event, 1)
            if event.GetId() == self.txtCtrlzId:
                self.EvtCenterText(event, 2)
        except:
            pass

    def EvtCenterText(self, event, i):
        try :
            self.center[i] = float(event.GetString())
        except:
            pass

class ObjectActionsCreatePinched_Circle_5mp(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.rmin = 0.5
        self.rmax = 1.
        self.center = np.asarray([0.,0.,0.])
        self.epsilon = 0.5

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "rmin")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlRadiusMinId = wx.NewId()
        self.txtCtrlRadiusMin = wx.TextCtrl(parentPanel, self.txtCtrlRadiusMinId)
        self.txtCtrlRadiusMin.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlRadiusMin.SetValue(str(self.rmin))
        hbox.Add(self.txtCtrlRadiusMin, border=5)

        self.Box.Add(hbox, border=10)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(parentPanel, -1, "rmax")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlRadiusMaxId = wx.NewId()
        self.txtCtrlRadiusMax = wx.TextCtrl(parentPanel, self.txtCtrlRadiusMaxId)
        self.txtCtrlRadiusMax.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlRadiusMax.SetValue(str(self.rmax))
        hbox.Add(self.txtCtrlRadiusMax, border=5)

        self.Box.Add(hbox, border=10)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(parentPanel, -1, "epsilon")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlEpsilonId = wx.NewId()
        self.txtCtrlEpsilon = wx.TextCtrl(parentPanel, self.txtCtrlEpsilonId)
        self.txtCtrlEpsilon.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlEpsilon.SetValue(str(self.epsilon))
        hbox.Add(self.txtCtrlEpsilon, border=5)

        self.Box.Add(hbox, border=10)
        # ...

        
        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "x")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlxId = wx.NewId()
        self.txtCtrlx = wx.TextCtrl(parentPanel, self.txtCtrlxId, size=(50,25))
        self.txtCtrlx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlx.SetValue(str(self.center[0]))
        hbox.Add(self.txtCtrlx, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "y")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlyId = wx.NewId()
        self.txtCtrly = wx.TextCtrl(parentPanel, self.txtCtrlyId, size=(50,25))
        self.txtCtrly.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrly.SetValue(str(self.center[1]))
        hbox.Add(self.txtCtrly, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "z")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlzId = wx.NewId()
        self.txtCtrlz = wx.TextCtrl(parentPanel, self.txtCtrlzId, size=(50,25))
        self.txtCtrlz.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlz.SetValue(str(self.center[2]))
        hbox.Add(self.txtCtrlz, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        
    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            from caid.cad_geometry import pinched_circle_5mp as domain
            _geo = domain(rmin=self.rmin, rmax=self.rmax, epsilon=self.epsilon, center=self.center)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... create object")
                macro_script.append("rmin = "+str(self.rmin))
                macro_script.append("rmax = "+str(self.rmax))
                macro_script.append("epsilon = "+str(self.epsilon))
                macro_script.append("center = "+str(list(self.center)))
            if self.patch:
                for nrb in _geo:
                    wk.add_patch(geoItem, geo, nrb)
                # macro recording
                if wk.macroRecording:
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("_geo = pinched_circle_5mp(rmin=rmin, rmax=rmax, epsilon=epsilon, center=center)")
                    macro_script.append("for nrb in _geo:")
                    macro_script.append("\twk.add_patch(geoItem, geo, nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)
            else:
                geo_new = geometry(_geo)
                geo_newItem = wk.add_geometry(geo_new)
                # macro recording
                if wk.macroRecording:
                    macro_script.append("_geo = pinched_circle_5mp(rmin=rmin, rmax=rmax, epsilon=epsilon, center=center)")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("# ...")

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlRadiusMinId:
                self.rmin = float(event.GetString())
            if event.GetId() == self.txtCtrlRadiusMaxId:
                self.rmax= float(event.GetString())
            if event.GetId() == self.txtCtrlEpsilonId:
                self.epsilon= float(event.GetString())
            if event.GetId() == self.txtCtrlxId:
                self.EvtCenterText(event, 0)
            if event.GetId() == self.txtCtrlyId:
                self.EvtCenterText(event, 1)
            if event.GetId() == self.txtCtrlzId:
                self.EvtCenterText(event, 2)
        except:
            pass

    def EvtCenterText(self, event, i):
        try :
            self.center[i] = float(event.GetString())
        except:
            pass

class ObjectActionsTranslate(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "x")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlxId = wx.NewId()
        self.txtCtrlx = wx.TextCtrl(parentPanel, self.txtCtrlxId, size=(50,25))
        self.txtCtrlx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlx.SetValue(str(0))
        hbox.Add(self.txtCtrlx, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "y")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlyId = wx.NewId()
        self.txtCtrly = wx.TextCtrl(parentPanel, self.txtCtrlyId, size=(50,25))
        self.txtCtrly.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrly.SetValue(str(0))
        hbox.Add(self.txtCtrly, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "z")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlzId = wx.NewId()
        self.txtCtrlz = wx.TextCtrl(parentPanel, self.txtCtrlzId, size=(50,25))
        self.txtCtrlz.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlz.SetValue(str(0))
        hbox.Add(self.txtCtrlz, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        self.v = np.asarray([0.,0.,0.])

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            if self.patch:
                patch = wk.inspector.currentObject
                patch.translate(self.v)

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... translate object")

                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("v = "+str(list(self.v)))
                    macro_script.append("patch.translate(v)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)

            else:
                geo = wk.inspector.currentObject
                geo.translate(self.v)

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... translate object")
                    geo_id = wk.list_geo.index(geo)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("v = "+str(list(self.v)))
                    macro_script.append("geo.translate(v)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlxId:
                self.EvtvText(event, 0)
            if event.GetId() == self.txtCtrlyId:
                self.EvtvText(event, 1)
            if event.GetId() == self.txtCtrlzId:
                self.EvtvText(event, 2)
        except:
            pass

    def EvtvText(self, event, i):
        try :
            self.v[i] = float(event.GetString())
        except:
            pass


class ObjectActionsRotate(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "angle")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAngleId = wx.NewId()
        self.txtCtrlAngle = wx.TextCtrl(parentPanel, self.txtCtrlAngleId, size=(50,25))
        self.txtCtrlAngle.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAngle.SetValue(str(0))
        hbox.Add(self.txtCtrlAngle, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxisId = wx.NewId()
        self.txtCtrlAxis = wx.TextCtrl(parentPanel, self.txtCtrlAxisId, size=(50,25))
        self.txtCtrlAxis.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAxis.SetValue(str(2))
        hbox.Add(self.txtCtrlAxis, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        self.angle = 0.
        self.axis  = 2

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            if self.patch:
                patch = wk.inspector.currentObject
                patch.rotate(self.angle * pi / 180, axis=self.axis)

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... rotate object")

                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("angle = "+str(self.angle))
                    macro_script.append("axis = "+str(self.axis))
                    macro_script.append("patch.rotate(angle * pi / 180, axis=axis)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)

            else:
                geo = wk.inspector.currentObject
                geo.rotate(self.angle * pi / 180, axis=self.axis)

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... rotate object")
                    geo_id = wk.list_geo.index(geo)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("angle = "+str(self.angle))
                    macro_script.append("axis = "+str(self.axis))
                    macro_script.append("geo.rotate(angle * pi / 180, axis=axis)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAngleId:
                self.angle = float(event.GetString())
            if event.GetId() == self.txtCtrlAxisId:
                self.axis = int(event.GetString())
        except:
            pass

class ObjectActionsScale(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.scale = 1.
        self.axis  = None

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "scale")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlScaleId = wx.NewId()
        self.txtCtrlScale = wx.TextCtrl(parentPanel, self.txtCtrlScaleId)
        self.txtCtrlScale.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlScale.SetValue(str(self.scale))
        hbox.Add(self.txtCtrlScale, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxisId = wx.NewId()
        self.txtCtrlAxis = wx.TextCtrl(parentPanel, self.txtCtrlAxisId)
        self.txtCtrlAxis.Bind(wx.EVT_TEXT, self.EvtText)
#        self.txtCtrlAxis.SetValue(str(2))
        hbox.Add(self.txtCtrlAxis, border=5)

        self.Box.Add(hbox, border=5)
        # ...


    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            if self.patch:
                patch = wk.inspector.currentObject
                patch.scale(self.scale, axis=self.axis)

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... scale object")

                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("scale = "+str(self.scale))
                    macro_script.append("axis = "+str(self.axis))
                    macro_script.append("patch.scale(scale=scale, axis=axis)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)
            else:
                geo = wk.inspector.currentObject
                geo.scale(self.scale, axis=self.axis)
                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... scale object")
                    geo_id = wk.list_geo.index(geo)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("scale = "+str(self.scale))
                    macro_script.append("axis = "+str(self.axis))
                    macro_script.append("geo.scale(scale=scale, axis=axis)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)

            self.axis = None

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlScaleId:
                self.scale = float(event.GetString())
            if event.GetId() == self.txtCtrlAxisId:
                self.axis = int(event.GetString())
        except:
            pass

class ObjectActionsCreateLinear(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.points = np.zeros((2,2), dtype='d')
        self.points[0,0] = -0.5
        self.points[1,0] = +0.5

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "A")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxId = wx.NewId()
        self.txtCtrlAx = wx.TextCtrl(parentPanel, self.txtCtrlAxId, size=(50,25))
        self.txtCtrlAx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAx.SetValue(str(self.points[0,0]))
        hbox.Add(self.txtCtrlAx, border=5)

        self.txtCtrlAyId = wx.NewId()
        self.txtCtrlAy = wx.TextCtrl(parentPanel, self.txtCtrlAyId, size=(50,25))
        self.txtCtrlAy.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAy.SetValue(str(self.points[0,1]))
        hbox.Add(self.txtCtrlAy, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "B")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlBxId = wx.NewId()
        self.txtCtrlBx = wx.TextCtrl(parentPanel, self.txtCtrlBxId, size=(50,25))
        self.txtCtrlBx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlBx.SetValue(str(self.points[1,0]))
        hbox.Add(self.txtCtrlBx, border=5)

        self.txtCtrlById = wx.NewId()
        self.txtCtrlBy = wx.TextCtrl(parentPanel, self.txtCtrlById, size=(50,25))
        self.txtCtrlBy.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlBy.SetValue(str(self.points[1,1]))
        hbox.Add(self.txtCtrlBy, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            from caid.cad_geometry import linear as domain
            _geo = domain(points=self.points)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... create object")
                macro_script.append("points = "+str(list(self.points)))
            if self.patch:
                nrb = _geo[0]
                wk.add_patch(geoItem, geo, nrb)
                # macro recording
                if wk.macroRecording:
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("cad_nrb = linear(points=points)[0]")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)
            else:
                wk.add_geometry(geometry(_geo))
                # macro recording
                if wk.macroRecording:
                    macro_script.append("_geo = linear(points=points)")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("# ...")

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAxId:
                self.points[0,0] = float(event.GetString())
            if event.GetId() == self.txtCtrlAyId:
                self.points[0,1] = float(event.GetString())
            if event.GetId() == self.txtCtrlBxId:
                self.points[1,0] = float(event.GetString())
            if event.GetId() == self.txtCtrlById:
                self.points[1,1] = float(event.GetString())
        except:
            pass

class ObjectActionsCreateBilinear(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        s = slice(-0.5, +0.5, 2j)
        x, y = np.ogrid[s, s]
        points = np.zeros((2,2,2), dtype='d')
        points[...,0] = x
        points[...,1] = y
        self.points = points

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "A")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxId = wx.NewId()
        self.txtCtrlAx = wx.TextCtrl(parentPanel, self.txtCtrlAxId, size=(50,25))
        self.txtCtrlAx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAx.SetValue(str(self.points[0,0,0]))
        hbox.Add(self.txtCtrlAx, border=5)

        self.txtCtrlAyId = wx.NewId()
        self.txtCtrlAy = wx.TextCtrl(parentPanel, self.txtCtrlAyId, size=(50,25))
        self.txtCtrlAy.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAy.SetValue(str(self.points[0,0,1]))
        hbox.Add(self.txtCtrlAy, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "B")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlBxId = wx.NewId()
        self.txtCtrlBx = wx.TextCtrl(parentPanel, self.txtCtrlBxId, size=(50,25))
        self.txtCtrlBx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlBx.SetValue(str(self.points[1,0,0]))
        hbox.Add(self.txtCtrlBx, border=5)

        self.txtCtrlById = wx.NewId()
        self.txtCtrlBy = wx.TextCtrl(parentPanel, self.txtCtrlById, size=(50,25))
        self.txtCtrlBy.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlBy.SetValue(str(self.points[1,0,1]))
        hbox.Add(self.txtCtrlBy, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "C")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlCxId = wx.NewId()
        self.txtCtrlCx = wx.TextCtrl(parentPanel, self.txtCtrlCxId, size=(50,25))
        self.txtCtrlCx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlCx.SetValue(str(self.points[0,1,0]))
        hbox.Add(self.txtCtrlCx, border=5)

        self.txtCtrlCyId = wx.NewId()
        self.txtCtrlCy = wx.TextCtrl(parentPanel, self.txtCtrlCyId, size=(50,25))
        self.txtCtrlCy.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlCy.SetValue(str(self.points[0,1,1]))
        hbox.Add(self.txtCtrlCy, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "D")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlDxId = wx.NewId()
        self.txtCtrlDx = wx.TextCtrl(parentPanel, self.txtCtrlDxId, size=(50,25))
        self.txtCtrlDx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlDx.SetValue(str(self.points[1,1,0]))
        hbox.Add(self.txtCtrlDx, border=5)

        self.txtCtrlDyId = wx.NewId()
        self.txtCtrlDy = wx.TextCtrl(parentPanel, self.txtCtrlDyId, size=(50,25))
        self.txtCtrlDy.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlDy.SetValue(str(self.points[1,1,1]))
        hbox.Add(self.txtCtrlDy, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            from caid.cad_geometry import bilinear as domain
            _geo = domain(points=self.points)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... create object")
                macro_script.append("points = "+str(list(self.points)))
            if self.patch:
                nrb = _geo[0]
                wk.add_patch(geoItem, geo, nrb)
                # macro recording
                if wk.macroRecording:
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("cad_nrb = bilinear(points=points)[0]")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)
            else:
                wk.add_geometry(geometry(_geo))
                # macro recording
                if wk.macroRecording:
                    macro_script.append("_geo = bilinear(points=points)")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("# ...")

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAxId:
                self.points[0,0,0] = float(event.GetString())
            if event.GetId() == self.txtCtrlAyId:
                self.points[0,0,1] = float(event.GetString())
            if event.GetId() == self.txtCtrlBxId:
                self.points[1,0,0] = float(event.GetString())
            if event.GetId() == self.txtCtrlById:
                self.points[1,0,1] = float(event.GetString())

            if event.GetId() == self.txtCtrlCxId:
                self.points[0,1,0] = float(event.GetString())
            if event.GetId() == self.txtCtrlCyId:
                self.points[0,1,1] = float(event.GetString())
            if event.GetId() == self.txtCtrlDxId:
                self.points[1,1,0] = float(event.GetString())
            if event.GetId() == self.txtCtrlDyId:
                self.points[1,1,1] = float(event.GetString())

        except:
            pass

class ObjectActionsCreateTriangle(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.profile = 0
        self.A = [0.,0.]
        self.B = [0.,1.]
        self.C = [1.,0.]

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "A")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxId = wx.NewId()
        self.txtCtrlAx = wx.TextCtrl(parentPanel, self.txtCtrlAxId, size=(50,25))
        self.txtCtrlAx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAx.SetValue(str(self.A[0]))
        hbox.Add(self.txtCtrlAx, border=5)

        self.txtCtrlAyId = wx.NewId()
        self.txtCtrlAy = wx.TextCtrl(parentPanel, self.txtCtrlAyId, size=(50,25))
        self.txtCtrlAy.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAy.SetValue(str(self.A[1]))
        hbox.Add(self.txtCtrlAy, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "B")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlBxId = wx.NewId()
        self.txtCtrlBx = wx.TextCtrl(parentPanel, self.txtCtrlBxId, size=(50,25))
        self.txtCtrlBx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlBx.SetValue(str(self.B[0]))
        hbox.Add(self.txtCtrlBx, border=5)

        self.txtCtrlById = wx.NewId()
        self.txtCtrlBy = wx.TextCtrl(parentPanel, self.txtCtrlById, size=(50,25))
        self.txtCtrlBy.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlBy.SetValue(str(self.B[1]))
        hbox.Add(self.txtCtrlBy, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "C")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlCxId = wx.NewId()
        self.txtCtrlCx = wx.TextCtrl(parentPanel, self.txtCtrlCxId, size=(50,25))
        self.txtCtrlCx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlCx.SetValue(str(self.C[0]))
        hbox.Add(self.txtCtrlCx, border=5)

        self.txtCtrlCyId = wx.NewId()
        self.txtCtrlCy = wx.TextCtrl(parentPanel, self.txtCtrlCyId, size=(50,25))
        self.txtCtrlCy.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlCy.SetValue(str(self.C[1]))
        hbox.Add(self.txtCtrlCy, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "Profile")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlProfileId = wx.NewId()
        self.txtCtrlProfile = wx.TextCtrl(parentPanel, self.txtCtrlProfileId, size=(50,25))
        self.txtCtrlProfile.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlProfile.SetValue(str(self.profile))
        hbox.Add(self.txtCtrlProfile, border=5)

        self.Box.Add(hbox, border=5)
        # ...

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            from caid.cad_geometry import triangle as domain
            points = [self.A, self.B, self.C]
            _geo = domain(points=points, profile=self.profile)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... create object")
                macro_script.append("profile = "+str(self.profile))
                macro_script.append("points = "+str(list(points)))
            if self.patch:
                nrb = _geo[0]
                wk.add_patch(geoItem, geo, nrb)
                # macro recording
                if wk.macroRecording:
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("cad_nrb = triangle(points=points, profile=profile)[0]")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)
            else:
                wk.add_geometry(geometry(_geo))
                # macro recording
                if wk.macroRecording:
                    macro_script.append("_geo = triangle(points=points, profile=profile)")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("# ...")

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAxId:
                self.A[0] = float(event.GetString())
            if event.GetId() == self.txtCtrlAyId:
                self.A[1] = float(event.GetString())
            if event.GetId() == self.txtCtrlBxId:
                self.B[0] = float(event.GetString())
            if event.GetId() == self.txtCtrlById:
                self.B[1] = float(event.GetString())
            if event.GetId() == self.txtCtrlCxId:
                self.C[0] = float(event.GetString())
            if event.GetId() == self.txtCtrlCyId:
                self.C[1] = float(event.GetString())

            if event.GetId() == self.txtCtrlProfileId:
                self.profile = int(event.GetString())
        except:
            pass

class ObjectActionsCreateArc(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.angle  = 90.
        self.radius = 1.
        self.center = np.asarray([0.,0.,0.])

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "angle")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAngleId = wx.NewId()
        self.txtCtrlAngle = wx.TextCtrl(parentPanel, self.txtCtrlAngleId, size=(50,25))
        self.txtCtrlAngle.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAngle.SetValue(str(self.angle))
        hbox.Add(self.txtCtrlAngle, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "radius")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlRadiusId = wx.NewId()
        self.txtCtrlRadius = wx.TextCtrl(parentPanel, self.txtCtrlRadiusId, size=(50,25))
        self.txtCtrlRadius.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlRadius.SetValue(str(self.radius))
        hbox.Add(self.txtCtrlRadius, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "x")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlxId = wx.NewId()
        self.txtCtrlx = wx.TextCtrl(parentPanel, self.txtCtrlxId, size=(50,25))
        self.txtCtrlx.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlx.SetValue(str(self.center[0]))
        hbox.Add(self.txtCtrlx, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "y")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlyId = wx.NewId()
        self.txtCtrly = wx.TextCtrl(parentPanel, self.txtCtrlyId, size=(50,25))
        self.txtCtrly.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrly.SetValue(str(self.center[1]))
        hbox.Add(self.txtCtrly, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "z")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlzId = wx.NewId()
        self.txtCtrlz = wx.TextCtrl(parentPanel, self.txtCtrlzId, size=(50,25))
        self.txtCtrlz.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlz.SetValue(str(self.center[2]))
        hbox.Add(self.txtCtrlz, border=5)

        self.Box.Add(hbox, border=5)
        # ...

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            from caid.cad_geometry import arc as domain
            angle = self.angle * pi / 180
            _geo = domain(angle=angle, radius=self.radius,center=self.center)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... create object")
                macro_script.append("angle = "+str(self.angle))
                macro_script.append("radius = "+str(self.radius))
                macro_script.append("center = "+str(list(self.center)))
            if self.patch:
                nrb = _geo[0]
                wk.add_patch(geoItem, geo, nrb)
                # macro recording
                if wk.macroRecording:
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("cad_nrb = arc(angle=angle, radius=radius, center=center)[0]")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)
            else:
                wk.add_geometry(geometry(_geo))
                # macro recording
                if wk.macroRecording:
                    macro_script.append("_geo = arc(angle=angle, radius=radius, center=center)")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("# ...")

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAngleId:
                self.angle = float(event.GetString())
            if event.GetId() == self.txtCtrlRadiusId:
                self.radius = float(event.GetString())
            if event.GetId() == self.txtCtrlxId:
                self.EvtCenterText(event, 0)
            if event.GetId() == self.txtCtrlyId:
                self.EvtCenterText(event, 1)
            if event.GetId() == self.txtCtrlzId:
                self.EvtCenterText(event, 2)
        except:
            pass

    def EvtCenterText(self, event, i):
        try :
            self.center[i] = float(event.GetString())
        except:
            pass

class ObjectActionsPolarExtrude(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.scale = 0.
        self.xcenter = None
        self.ycenter = None
        self.zcenter = None

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "scale")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlScaleId = wx.NewId()
        self.txtCtrlScale = wx.TextCtrl(parentPanel, self.txtCtrlScaleId)
        self.txtCtrlScale.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlScale.SetValue(str(self.scale))
        hbox.Add(self.txtCtrlScale, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "x")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlxId = wx.NewId()
        self.txtCtrlx = wx.TextCtrl(parentPanel, self.txtCtrlxId, size=(50,25))
        self.txtCtrlx.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlx, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "y")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlyId = wx.NewId()
        self.txtCtrly = wx.TextCtrl(parentPanel, self.txtCtrlyId, size=(50,25))
        self.txtCtrly.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrly, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "z")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlzId = wx.NewId()
        self.txtCtrlz = wx.TextCtrl(parentPanel, self.txtCtrlzId, size=(50,25))
        self.txtCtrlz.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlz, border=5)

        self.Box.Add(hbox, border=5)
        # ...

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            xyzc = None
            if (self.xcenter is not None) \
               and (self.ycenter is not None) \
               and (self.zcenter is not None):
                xyzc = [self.xcenter, self.ycenter, self.zcenter]
            # inspector = self.parent
            wk = self.parent.WorkGroup
            from caid.cad_geometry import cad_geometry
            if self.patch:
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentPatchItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo = wk.inspector.tree.GetPyData(geoItem)

                geo_t = cad_geometry()
                geo_t.append(patch)
                _geo = geo_t.polarExtrude(t=self.scale,xyzc=xyzc)
                nrb = _geo[0]
                wk.add_patch(geoItem, geo, nrb)

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... polar-extrude patch")

                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("_geo = cad_geometry()")
                    macro_script.append("_geo.append(patch)")
                    macro_script.append("scale = "+str(self.scale))
                    if xyzc is None:
                        macro_script.append("xyzc = None")
                    else:
                        macro_script.append("xyzc = "+str(list(xyzc)))
                    macro_script.append("cad_nrb = _geo.polarExtrude(t=scale,xyzc=xyzc)[0]")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")
                wk.Refresh(inspector=True)

            else:
                geo = wk.inspector.currentGeometry
                geoItem = wk.inspector.currentGeometryItem
                _geo = geo.polarExtrude(t=self.scale,xyzc=xyzc)
                wk.add_geometry(geometry(_geo))

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... polar-extrude geometry")
                    geo_id = wk.list_geo.index(geo)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("scale = "+str(self.scale))
                    if xyzc is None:
                        macro_script.append("xyzc = None")
                    else:
                        macro_script.append("xyzc = "+str(list(xyzc)))
                    macro_script.append("_geo = geo.polarExtrude(t=scale,xyzc=xyzc)")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("# ...")

            self.center = None

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlScaleId:
                self.scale = float(event.GetString())
            if event.GetId() == self.txtCtrlxId:
                self.xcenter = float(event.GetString())
            if event.GetId() == self.txtCtrlyId:
                self.zcenter = float(event.GetString())
            if event.GetId() == self.txtCtrlzId:
                self.ycenter = float(event.GetString())
        except:
            pass

class ObjectActionsCurve(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"
        # add button to import points
        self.IMPORT_ID = wx.NewId() ; IMPORT_TAG = "Import"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        list_buttonsInfo.append([self.IMPORT_ID, IMPORT_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.degree = 2
        self.s = 0.1

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.cbInterpolateID = wx.NewId()
        self.cbInterpolate = wx.CheckBox(parentPanel, self.cbInterpolateID,'Interpolate', (10, 10))
        self.cbInterpolate.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cbInterpolate.SetValue(True)

        hbox.Add(self.cbInterpolate, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.cbApproximateID = wx.NewId()
        self.cbApproximate = wx.CheckBox(parentPanel,
                                           self.cbApproximateID,'Approximate', (10, 10))
        self.cbApproximate.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cbApproximate.SetValue(False)

        hbox.Add(self.cbApproximate, border=5)

        self.Box.Add(hbox, border=5)
        # ...


        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.cbLinesID = wx.NewId()
        self.cbLines = wx.CheckBox(parentPanel,
                                           self.cbLinesID,'Lines', (10, 10))
        self.cbLines.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cbLines.SetValue(False)

        hbox.Add(self.cbLines, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "Degree")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlDegreeId = wx.NewId()
        self.txtCtrlDegree = wx.TextCtrl(parentPanel, self.txtCtrlDegreeId, size=(50,25))
        self.txtCtrlDegree.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlDegree.SetValue(str(self.degree))
        hbox.Add(self.txtCtrlDegree, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "Smooth")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlSmoothId = wx.NewId()
        self.txtCtrlSmooth = wx.TextCtrl(parentPanel, self.txtCtrlSmoothId, size=(50,25))
        self.txtCtrlSmooth.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlSmooth.SetValue(str(self.s))
        hbox.Add(self.txtCtrlSmooth, border=5)

        self.Box.Add(hbox, border=5)
        # ...

    def EvtCheckBox(self, event):
        if event.GetId() == self.cbInterpolateID:
            self.cbApproximate.SetValue(False)
            self.cbLines.SetValue(False)
        if event.GetId() == self.cbApproximateID:
            self.cbInterpolate.SetValue(False)
            self.cbLines.SetValue(False)
        if event.GetId() == self.cbLinesID:
            self.cbInterpolate.SetValue(False)
            self.cbApproximate.SetValue(False)
            self.degree = 1
            self.txtCtrlDegree.SetValue(str(self.degree))

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlDegreeId:
                self.degree = int(event.GetString())
            if event.GetId() == self.txtCtrlSmoothId:
                self.s      = float(event.GetString())
        except:
            pass

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.IMPORT_ID:
            # Create an open file dialog
            dialog = wx.FileDialog(None, style = wx.OPEN)
            # Show the dialog and get user input
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetPath()
                a = np.genfromtxt(filename)
                # inspector = self.parent
                wk = self.parent.WorkGroup
                wk.viewer.CleanMarkerPoints()
                for i in range(0, a.shape[0]):
                    xyz = list(a[i,:])
                    if len(xyz) == 2:
                        xyz += [0.]
                    # add weight = 1.
                    xyz += [1.]
                    P = np.asarray(xyz)
                    wk.viewer.AddMarkerPoint(P)
                wk.Refresh()
            # Destroy the dialog
            dialog.Destroy()
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            list_P = wk.viewer.MarkerPoints
            x = []; y = []
            for P in list_P:
                x.append(P[0])
                y.append(P[1])
            if self.cbInterpolate.GetValue():
                from scipy import interpolate
                tck,u = interpolate.splprep([x,y],s=0, k=self.degree)
                knots = tck[0]
                Px = tck[1][0]
                Py = tck[1][1]
                C  = np.zeros((len(Px),3))
                C[:,0] = array(Px)
                C[:,1] = array(Py)
                nrb = cad_nurbs([knots], C)
            if self.cbApproximate.GetValue():
                from scipy import interpolate
                tck,u = interpolate.splprep([x,y],s=self.s, k=self.degree)
                knots = tck[0]
                Px = tck[1][0]
                Py = tck[1][1]
                C  = np.zeros((len(Px),3))
                C[:,0] = array(Px)
                C[:,1] = array(Py)
                nrb = cad_nurbs([knots], C)
            if self.cbLines.GetValue():
                from caid.cad_geometry import linear
                from igakit.cad import join
                list_crv = []
                for P,Q in zip(list_P[:-1], list_P[1:]):
                    points = np.zeros((2,2))
                    points[0,0] = P[0] ; points[0,1] = P[1]
                    points[1,0] = Q[0] ; points[1,1] = Q[1]
                    crv = linear(points = points)[0]
                    list_crv.append(crv)
                nrb = list_crv[0]
                axis = 0
                for crv in list_crv[1:]:
                    nrb = join(nrb, crv, axis)

            wk.viewer.CleanMarkerPoints()
            geo = cad_geometry()
            geo.append(nrb)
            wk.add_geometry(geometry(geo))
            wk.Refresh()

class ObjectActionsJoin(ObjectClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ObjectClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.axis  = 0

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxisId = wx.NewId()
        self.txtCtrlAxis = wx.TextCtrl(parentPanel, self.txtCtrlAxisId, size=(50,25))
        self.txtCtrlAxis.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAxis.SetValue(str(self.axis))
        hbox.Add(self.txtCtrlAxis, border=5)

        self.Box.Add(hbox, border=5)
        # ...


    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            from igakit.cad import join
            list_patchs = []
            for item in wk.inspector.tree.selectionsItems:
                patch = wk.inspector.tree.GetPyData(item)
                list_patchs.append(patch)

            nrb_new = list_patchs[0]
            for nrb in list_patchs[1:]:
                nrb_new = join(nrb_new, nrb,self.axis)
            geo = cad_geometry()
            geo.append(nrb_new)
            wk.add_geometry(geometry(geo))

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... join algorithm")
                list_gp = []
                for item in wk.inspector.tree.selectionsItems:
                    patch   = wk.inspector.tree.GetPyData(item)
                    geoItem = wk.inspector.tree.GetItemParent(item)
                    geo     = wk.inspector.tree.GetPyData(geoItem)
                    list_gp.append([geo, patch])

                macro_script.append("list_patchs = []")
                for i,gp in enumerate(list_gp):
                    geo = gp[0] ; patch = gp[1]
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("list_patchs.append(patch)")

                macro_script.append("axis = "+str(self.axis))
                macro_script.append("nrb_new = list_patchs[0]")
                macro_script.append("for nrb in list_patchs[1:]:")
                macro_script.append("\tnrb_new = join(nrb_new, nrb,axis)")
                macro_script.append("_geo = cad_geometry()")
                macro_script.append("_geo.append(nrb_new)")
                macro_script.append("wk.add_geometry(geometry(_geo))")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")

            wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAxisId:
                self.axis = int(event.GetString())
        except:
            pass
