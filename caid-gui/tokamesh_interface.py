# -*- coding: UTF-8 -*-
import wx
import numpy as np

from theme import theme as Theme

theme = Theme()

ALPHA                   = theme.alpha
BETA                    = theme.beta
COLOR_GEOMETRY_MESH     = theme.color_selected_geometry('mesh')
COLOR_GEOMETRY_NURBS    = theme.color_selected_geometry('nurbs')
COLOR_GEOMETRY_POINTS   = theme.color_selected_geometry('points')
COLOR_PATCH_MESH        = theme.color_selected_patch('mesh')
COLOR_PATCH_NURBS       = theme.color_selected_patch('nurbs')
COLOR_PATCH_POINTS      = theme.color_selected_patch('points')
COLOR_DEFAULT_GEOMETRY  = theme.color_viewer('default_geometry')
COLOR_DEFAULT_PATCH     = theme.color_viewer('default_patch')
COLOR_DEFAULT_MESH      = theme.color_viewer('default_mesh')
COLOR_DEFAULT_POINTS    = theme.color_viewer('default_points')
SIZE_GEOMETRY_POINTS    = theme.size_points('geometry')
SIZE_PATCH_POINTS       = theme.size_points('patch')

class Page2DGrid(wx.Panel):
    def __init__(self, parent, viewer):
        wx.Panel.__init__(self, parent.nb)
        self.title = "2D Grid"
        pnl = self
        self.parent = parent
        self.viewer = viewer

        self.rowmin = None
        self.rowmax = None
        self.hx     = None
        self.colmin = None
        self.colmax = None
        self.hy     = None

        vbox = wx.BoxSizer(wx.VERTICAL)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Row-min", size=(190,20))
        self.txtCtrlRowMinId = wx.NewId()
        self.txtCtrlRowMin = wx.TextCtrl(pnl, self.txtCtrlRowMinId)

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlRowMin, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Row-max", size=(190,20))
        self.txtCtrlRowMaxId = wx.NewId()
        self.txtCtrlRowMax = wx.TextCtrl(pnl, self.txtCtrlRowMaxId)

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlRowMax, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "hx", size=(190,20))
        self.txtCtrlHxId = wx.NewId()
        self.txtCtrlHx = wx.TextCtrl(pnl, self.txtCtrlHxId)

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlHx, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Col-min", size=(190,20))
        self.txtCtrlColMinId = wx.NewId()
        self.txtCtrlColMin = wx.TextCtrl(pnl, self.txtCtrlColMinId)

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlColMin, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Col-max", size=(190,20))
        self.txtCtrlColMaxId = wx.NewId()
        self.txtCtrlColMax = wx.TextCtrl(pnl, self.txtCtrlColMaxId)

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlColMax, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "hy", size=(190,20))
        self.txtCtrlHyId = wx.NewId()
        self.txtCtrlHy = wx.TextCtrl(pnl, self.txtCtrlHyId)

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlHy, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox.Add(okButton)
        hbox.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        self.SetSizer(vbox)
        # ...

        self.Layout()

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        self.Bind(wx.EVT_TEXT, self.EvtText)

    def OnOk(self, event):
        self.viewer.set_rowmin(self.rowmin)
        self.viewer.set_rowmax(self.rowmax)
        self.viewer.set_hx(self.hx)
        self.viewer.set_colmin(self.colmin)
        self.viewer.set_colmax(self.colmax)
        self.viewer.set_hy(self.hy)

        self.viewer.Refresh()

    def OnClose(self, event):
        self.parent.Destroy()

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlRowMinId:
                self.rowmin = float(event.GetString())
            if event.GetId() == self.txtCtrlRowMaxId:
                self.rowmax = float(event.GetString())

            if event.GetId() == self.txtCtrlColMinId:
                self.colmin = float(event.GetString())
            if event.GetId() == self.txtCtrlColMaxId:
                self.colmax = float(event.GetString())

            if event.GetId() == self.txtCtrlHxId:
                self.hx = float(event.GetString())
            if event.GetId() == self.txtCtrlHyId:
                self.hy = float(event.GetString())
        except:
            pass

class PageColors(wx.Panel):
    def __init__(self, parent, viewer):
        wx.Panel.__init__(self, parent.nb)
        self.title = "Colors"
        pnl = self
        self.parent = parent
        self.viewer = viewer

        self.background = None
        self.grid = None
        self.selectedGeoMesh = None
        self.selectedGeoNurbs = None
        self.selectedGeoPoints = None
        self.selectedPatchMesh = None
        self.selectedPatchNurbs = None
        self.selectedPatchPoints = None
        self.markerPoints = None
        self.alpha        = self.viewer.alpha
        self.beta         = self.viewer.beta

        vbox = wx.BoxSizer(wx.VERTICAL)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "BackGround", size=(190,20))
        self.pnlBackGround = wx.Panel(self, -1, size=(190,25))
        color = [c*255 for c in self.viewer.color_background]
        color = color[::-1]
        self.pnlBackGround.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnBackGroundId = wx.NewId()
        btnBackGround = wx.BitmapButton(self, id=self.btnBackGroundId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlBackGround, 0, wx.EXPAND, border=5)
        hbox.Add(btnBackGround, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Alpha", size=(190,20))
        self.txtCtrlAlphaId = wx.NewId()
        self.txtCtrlAlpha = wx.TextCtrl(pnl, self.txtCtrlAlphaId)
        self.txtCtrlAlpha.SetValue(str(self.alpha))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlAlpha, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Beta", size=(190,20))
        self.txtCtrlBetaId = wx.NewId()
        self.txtCtrlBeta = wx.TextCtrl(pnl, self.txtCtrlBetaId)
        self.txtCtrlBeta.SetValue(str(self.beta))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlBeta, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Grid", size=(190,20))
        self.pnlGrid = wx.Panel(self, -1, size=(190,25))
        self.pnlGrid.SetBackgroundColour(wx.Colour(*self.viewer.color_grid))
        color = [c*255 for c in self.viewer.color_grid]
        color = color[::-1]
        self.pnlGrid.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnGridId = wx.NewId()
        btnGrid = wx.BitmapButton(self, id=self.btnGridId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlGrid, 0, wx.EXPAND, border=5)
        hbox.Add(btnGrid, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Marker-Points", size=(190,20))
        self.pnlMarkerPoints = wx.Panel(self, -1, size=(190,25))
        color = [c*255 for c in self.viewer.color_selectedPatchPoints]
        color = color[::-1]
        self.pnlMarkerPoints.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnMarkerPointsId = wx.NewId()
        btnMarkerPoints = wx.BitmapButton(self, id=self.btnMarkerPointsId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlMarkerPoints, 0, wx.EXPAND, border=5)
        hbox.Add(btnMarkerPoints, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Geometry-Mesh", size=(190,20))
        self.pnlSelGeoMesh = wx.Panel(self, -1, size=(190,25))
        color = [c*255 for c in self.viewer.color_selectedGeoMesh]
        color = color[::-1]
        self.pnlSelGeoMesh.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelGeoMeshId = wx.NewId()
        btnSelGeoMesh = wx.BitmapButton(self, id=self.btnSelGeoMeshId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelGeoMesh, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelGeoMesh, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Gometry-Nurbs", size=(190,20))
        self.pnlSelGeoNurbs = wx.Panel(self, -1, size=(190,25))
        color = [c*255 for c in self.viewer.color_selectedGeoNurbs]
        color = color[::-1]
        self.pnlSelGeoNurbs.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelGeoNurbsId = wx.NewId()
        btnSelGeoNurbs = wx.BitmapButton(self, id=self.btnSelGeoNurbsId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelGeoNurbs, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelGeoNurbs, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Geometry-Points", size=(190,20))
        self.pnlSelGeoPoints = wx.Panel(self, -1, size=(190,25))
        color = [c*255 for c in self.viewer.color_selectedGeoPoints]
        color = color[::-1]
        self.pnlSelGeoPoints.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelGeoPointsId = wx.NewId()
        btnSelGeoPoints = wx.BitmapButton(self, id=self.btnSelGeoPointsId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelGeoPoints, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelGeoPoints, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Patch-Mesh", size=(190,20))
        self.pnlSelPatchMesh = wx.Panel(self, -1, size=(190,25))
        color = [c*255 for c in self.viewer.color_selectedPatchMesh]
        color = color[::-1]
        self.pnlSelPatchMesh.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelPatchMeshId = wx.NewId()
        btnSelPatchMesh = wx.BitmapButton(self, id=self.btnSelPatchMeshId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelPatchMesh, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelPatchMesh, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Patch-Nurbs", size=(190,20))
        self.pnlSelPatchNurbs = wx.Panel(self, -1, size=(190,25))
        color = [c*255 for c in self.viewer.color_selectedPatchNurbs]
        color = color[::-1]
        self.pnlSelPatchNurbs.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelPatchNurbsId = wx.NewId()
        btnSelPatchNurbs = wx.BitmapButton(self, id=self.btnSelPatchNurbsId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelPatchNurbs, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelPatchNurbs, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Patch-Points", size=(190,20))
        self.pnlSelPatchPoints = wx.Panel(self, -1, size=(190,25))
        color = [c*255 for c in self.viewer.color_selectedPatchPoints]
        color = color[::-1]
        self.pnlSelPatchPoints.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelPatchPointsId = wx.NewId()
        btnSelPatchPoints = wx.BitmapButton(self, id=self.btnSelPatchPointsId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelPatchPoints, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelPatchPoints, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox.Add(okButton)
        hbox.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        self.SetSizer(vbox)
        # ...

        self.Layout()

        btnBackGround.Bind(wx.EVT_BUTTON, self.ChooseColor)
        btnGrid.Bind(wx.EVT_BUTTON, self.ChooseColor)

        btnMarkerPoints.Bind(wx.EVT_BUTTON, self.ChooseColor)

        btnSelGeoMesh.Bind(wx.EVT_BUTTON, self.ChooseColor)
        btnSelGeoNurbs.Bind(wx.EVT_BUTTON, self.ChooseColor)
        btnSelGeoPoints.Bind(wx.EVT_BUTTON, self.ChooseColor)

        btnSelPatchMesh.Bind(wx.EVT_BUTTON, self.ChooseColor)
        btnSelPatchNurbs.Bind(wx.EVT_BUTTON, self.ChooseColor)
        btnSelPatchPoints.Bind(wx.EVT_BUTTON, self.ChooseColor)

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        self.Bind(wx.EVT_TEXT, self.EvtText)

    def ChooseColor(self, event):
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            _values = data.GetColour().Get()
#            values = np.asarray(_values) * 1./255.
            values = []
            for i in range(0,3):
                x = _values[i]
                values.append(x * 1. / 255.)
            values = values[::-1]
        if event.GetId() == self.btnBackGroundId:
            self.background = values
            self.pnlBackGround.SetBackgroundColour(wx.Colour(*values))
        if event.GetId() == self.btnGridId:
            self.grid = values
            self.pnlGrid.SetBackgroundColour(wx.Colour(*values))
        if event.GetId() == self.btnSelGeoMeshId:
            self.selectedGeoMesh = values
            self.pnlSelGeoMesh.SetBackgroundColour(wx.Colour(*values))
        if event.GetId() == self.btnSelGeoNurbsId:
            self.selectedGeoNurbs = values
            self.pnlSelGeoNurbs.SetBackgroundColour(wx.Colour(*values))
        if event.GetId() == self.btnSelGeoPointsId:
            self.selectedGeoPoints = values
            self.pnlSelGeoPoints.SetBackgroundColour(wx.Colour(*values))
        if event.GetId() == self.btnSelPatchMeshId:
            self.selectedPatchMesh = values
            self.pnlSelPatchMesh.SetBackgroundColour(wx.Colour(*values))
        if event.GetId() == self.btnSelPatchNurbsId:
            self.selectedPatchNurbs = values
            self.pnlSelPatchNurbs.SetBackgroundColour(wx.Colour(*values))
        if event.GetId() == self.btnSelPatchPointsId:
            self.selectedPatchPoints = values
            self.pnlSelPatchPoints.SetBackgroundColour(wx.Colour(*values))
        if event.GetId() == self.btnMarkerPointsId:
            self.markerPoints= values
            self.pnlMarkerPoints.SetBackgroundColour(wx.Colour(*values))

        dlg.Destroy()

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAlphaId:
                self.alpha = float(event.GetString())
            if event.GetId() == self.txtCtrlBetaId:
                self.beta = float(event.GetString())
        except:
            pass

    def OnOk(self, event):
        self.viewer.set_color_background(self.background)
        self.viewer.set_color_grid(self.grid)
        self.viewer.set_color_selectedGeoMesh(self.selectedGeoMesh)
        self.viewer.set_color_selectedGeoNurbs(self.selectedGeoNurbs)
        self.viewer.set_color_selectedGeoPoints(self.selectedGeoPoints)
        self.viewer.set_color_selectedPatchMesh(self.selectedPatchMesh)
        self.viewer.set_color_selectedPatchNurbs(self.selectedPatchNurbs)
        self.viewer.set_color_selectedPatchPoints(self.selectedPatchPoints)
        self.viewer.set_color_markerPoints(self.markerPoints)
        self.viewer.set_alpha(self.alpha)
        self.viewer.set_beta(self.beta)

        self.viewer.Refresh()

    def OnClose(self, event):
        self.parent.Destroy()

class PageViewer(wx.Panel):
    def __init__(self, parent, viewer):
        wx.Panel.__init__(self, parent.nb)
        self.title = "Viewer"
        pnl = self
        self.parent = parent
        self.viewer = viewer

        self.WheelSensitivity = None
        self.rowmax = None
        self.hx     = None
        self.colmin = None
        self.colmax = None
        self.hy     = None

        vbox = wx.BoxSizer(wx.VERTICAL)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Wheel Sensitivity", size=(190,20))
        self.txtCtrlWheelId = wx.NewId()
        self.txtCtrlWheel = wx.TextCtrl(pnl, self.txtCtrlWheelId)

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlWheel, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Row-max", size=(190,20))
        self.txtCtrlRowMaxId = wx.NewId()
        self.txtCtrlRowMax = wx.TextCtrl(pnl, self.txtCtrlRowMaxId)

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlRowMax, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "hx", size=(190,20))
        self.txtCtrlHxId = wx.NewId()
        self.txtCtrlHx = wx.TextCtrl(pnl, self.txtCtrlHxId)

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlHx, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Col-min", size=(190,20))
        self.txtCtrlColMinId = wx.NewId()
        self.txtCtrlColMin = wx.TextCtrl(pnl, self.txtCtrlColMinId)

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlColMin, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Col-max", size=(190,20))
        self.txtCtrlColMaxId = wx.NewId()
        self.txtCtrlColMax = wx.TextCtrl(pnl, self.txtCtrlColMaxId)

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlColMax, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "hy", size=(190,20))
        self.txtCtrlHyId = wx.NewId()
        self.txtCtrlHy = wx.TextCtrl(pnl, self.txtCtrlHyId)

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlHy, 0, wx.EXPAND|wx.RIGHT, border=5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox.Add(okButton)
        hbox.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        self.SetSizer(vbox)
        # ...

        self.Layout()

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        self.Bind(wx.EVT_TEXT, self.EvtText)

    def OnOk(self, event):
        self.viewer.set_wheelSensitivity(self.WheelSensitivity)
        self.viewer.set_rowmax(self.rowmax)
        self.viewer.set_hx(self.hx)
        self.viewer.set_colmin(self.colmin)
        self.viewer.set_colmax(self.colmax)
        self.viewer.set_hy(self.hy)

        self.viewer.Refresh()

    def OnClose(self, event):
        self.parent.Destroy()

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlWheelId:
                self.WheelSensitivity = float(event.GetString())
            if event.GetId() == self.txtCtrlRowMaxId:
                self.rowmax = float(event.GetString())

            if event.GetId() == self.txtCtrlColMinId:
                self.colmin = float(event.GetString())
            if event.GetId() == self.txtCtrlColMaxId:
                self.colmax = float(event.GetString())

            if event.GetId() == self.txtCtrlHxId:
                self.hx = float(event.GetString())
            if event.GetId() == self.txtCtrlHyId:
                self.hy = float(event.GetString())
        except:
            pass


class PreferencesDialog(wx.Dialog):

    def __init__(self, parent, viewer, title):
        super(PreferencesDialog, self).__init__(parent)
        self.parent = parent
        self.viewer = viewer

        self.ls_current_value = None
        self.value = None

        self.InitUI()
        self.SetSize((520, 550))
        self.SetTitle("Viewer Preferences")

    def InitUI(self):

        self.pnl = wx.Panel(self)
        self.nb = wx.Listbook(self.pnl)

        # create the page windows as children of the notebook
        page_2dgrid  = Page2DGrid(self, self.viewer)
        page_colors  = PageColors(self, self.viewer)
        page_viewer  = PageViewer(self, self.viewer)

        # add the pages to the notebook with the label to show on the tab
        self.nb.AddPage(page_2dgrid, page_2dgrid.title)
        self.nb.AddPage(page_colors, page_colors.title)
        self.nb.AddPage(page_viewer, page_viewer.title)

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.pnl.SetSizer(sizer)
