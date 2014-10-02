# -*- coding: UTF-8 -*-
import wx
import numpy as np

from theme import theme as Theme

theme = Theme()

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

#        font_section = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        font_section = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # -------------------------------------------------------------------
        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "BackGround", size=(190,20))
        self.pnlBackGround = wx.Panel(self, -1, size=(190,25))
        color = [c*255 for c in theme.color_viewer('background')]
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
        staticTxt = wx.StaticText(pnl, -1, "Grid", size=(190,20))
        self.pnlGrid = wx.Panel(self, -1, size=(190,25))
        self.pnlGrid.SetBackgroundColour(wx.Colour(*self.viewer.color_grid))
        color = [c*255 for c in theme.color_viewer('grid')]
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
        # -------------------------------------------------------------------

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # -------------------------------------------------------------------
        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Alpha", size=(70,20))
        self.txtCtrlAlphaId = wx.NewId()
        self.txtCtrlAlpha = wx.TextCtrl(pnl, self.txtCtrlAlphaId)
        self.txtCtrlAlpha.SetValue(str(theme.alpha))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlAlpha, 0, wx.EXPAND|wx.RIGHT, border=50)
        # ...

        # ...
        staticTxt = wx.StaticText(pnl, -1, "Beta", size=(70,20))
        self.txtCtrlBetaId = wx.NewId()
        self.txtCtrlBeta = wx.TextCtrl(pnl, self.txtCtrlBetaId)
        self.txtCtrlBeta.SetValue(str(theme.beta))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlBeta, 0, wx.EXPAND|wx.RIGHT, border=50)
        # ...

        # ...
        staticTxt = wx.StaticText(pnl, -1, "Alpha-background", size=(140,20))
        self.txtCtrlAlpha_BgId = wx.NewId()
        self.txtCtrlAlpha_Bg = wx.TextCtrl(pnl, self.txtCtrlAlpha_BgId)
        self.txtCtrlAlpha_Bg.SetValue(str(theme.alpha_bg))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlAlpha_Bg, 0, wx.EXPAND|wx.RIGHT, border=50)
        # ...

        # ...
        self.cb_blendID = wx.NewId()
        self.cb_blend = wx.CheckBox(pnl, self.cb_blendID ,'Blend', (15, 30))
        self.cb_blend.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cb_blend.SetValue(theme.enable_blend)

        hbox.Add(self.cb_blend, 0, wx.ALL, 5)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...
        # -------------------------------------------------------------------

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # -------------------------------------------------------------------
        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Selected Geometry", size=(400,20))
        staticTxt.SetFont(font_section)
        hbox.Add(staticTxt, 0, wx.ALL, 5)
        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "mesh", size=(70,20))
        self.pnlSelGeoMesh = wx.Panel(self, -1, size=(90,25))
        color = [c*255 for c in theme.color_selected_geometry('mesh')]
        self.pnlSelGeoMesh.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelGeoMeshId = wx.NewId()
        btnSelGeoMesh = wx.BitmapButton(self, id=self.btnSelGeoMeshId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelGeoMesh, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelGeoMesh, 0, wx.EXPAND|wx.RIGHT, border=70)
        # ...

        # ...
        staticTxt = wx.StaticText(pnl, -1, "nurbs", size=(70,20))
        self.pnlSelGeoNurbs = wx.Panel(self, -1, size=(90,25))
        color = [c*255 for c in theme.color_selected_geometry('nurbs')]
        self.pnlSelGeoNurbs.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelGeoNurbsId = wx.NewId()
        btnSelGeoNurbs = wx.BitmapButton(self, id=self.btnSelGeoNurbsId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelGeoNurbs, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelGeoNurbs, 0, wx.EXPAND|wx.RIGHT, border=70)
        # ...

        # ...
        staticTxt = wx.StaticText(pnl, -1, "points", size=(70,20))
        self.pnlSelGeoPoints = wx.Panel(self, -1, size=(90,25))
        color = [c*255 for c in theme.color_selected_geometry('points')]
        self.pnlSelGeoPoints.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelGeoPointsId = wx.NewId()
        btnSelGeoPoints = wx.BitmapButton(self, id=self.btnSelGeoPointsId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelGeoPoints, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelGeoPoints, 0, wx.EXPAND|wx.RIGHT, border=70)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...
        # -------------------------------------------------------------------

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # -------------------------------------------------------------------
        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Selected Patch", size=(400,20))
        staticTxt.SetFont(font_section)
        hbox.Add(staticTxt, 0, wx.ALL, 5)
        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "mesh", size=(70,20))
        self.pnlSelPatchMesh = wx.Panel(self, -1, size=(90,25))
        color = [c*255 for c in theme.color_selected_patch('mesh')]
        self.pnlSelPatchMesh.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelPatchMeshId = wx.NewId()
        btnSelPatchMesh = wx.BitmapButton(self, id=self.btnSelPatchMeshId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelPatchMesh, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelPatchMesh, 0, wx.EXPAND|wx.RIGHT, border=70)
        # ...

        # ...
        staticTxt = wx.StaticText(pnl, -1, "nurbs", size=(70,20))
        self.pnlSelPatchNurbs = wx.Panel(self, -1, size=(90,25))
        color = [c*255 for c in theme.color_selected_patch('nurbs')]
        self.pnlSelPatchNurbs.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelPatchNurbsId = wx.NewId()
        btnSelPatchNurbs = wx.BitmapButton(self, id=self.btnSelPatchNurbsId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelPatchNurbs, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelPatchNurbs, 0, wx.EXPAND|wx.RIGHT, border=70)
        # ...

        # ...
        staticTxt = wx.StaticText(pnl, -1, "points", size=(70,20))
        self.pnlSelPatchPoints = wx.Panel(self, -1, size=(90,25))
        color = [c*255 for c in theme.color_selected_patch('points')]
        self.pnlSelPatchPoints.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelPatchPointsId = wx.NewId()
        btnSelPatchPoints = wx.BitmapButton(self, id=self.btnSelPatchPointsId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelPatchPoints, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelPatchPoints, 0, wx.EXPAND|wx.RIGHT, border=70)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...
        # -------------------------------------------------------------------

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # -------------------------------------------------------------------
        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Default", size=(400,20))
        staticTxt.SetFont(font_section)
        hbox.Add(staticTxt, 0, wx.ALL, 5)
        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "geometry", size=(70,20))
        self.pnlDefaultGeometry = wx.Panel(self, -1, size=(90,25))
        color = [c*255 for c in theme.color_viewer('default_geometry')]
        self.pnlDefaultGeometry.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnDefaultGeometryId = wx.NewId()
        btnDefaultGeometry = wx.BitmapButton(self, id=self.btnDefaultGeometryId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlDefaultGeometry, 0, wx.EXPAND, border=5)
        hbox.Add(btnDefaultGeometry, 0, wx.EXPAND|wx.RIGHT, border=70)
        # ...

        # ...
        staticTxt = wx.StaticText(pnl, -1, "patch", size=(70,20))
        self.pnlDefaultPatch= wx.Panel(self, -1, size=(90,25))
        color = [c*255 for c in theme.color_viewer('default_patch')]
        self.pnlDefaultPatch.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnDefaultPatchId = wx.NewId()
        btnDefaultPatch= wx.BitmapButton(self, id=self.btnDefaultPatchId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlDefaultPatch, 0, wx.EXPAND, border=5)
        hbox.Add(btnDefaultPatch, 0, wx.EXPAND|wx.RIGHT, border=70)
        # ...

        vbox.Add(hbox, 0, wx.ALL, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # ...
        staticTxt = wx.StaticText(pnl, -1, "mesh", size=(70,20))
        self.pnlDefaultMesh= wx.Panel(self, -1, size=(90,25))
        color = [c*255 for c in theme.color_viewer('default_mesh')]
        self.pnlDefaultMesh.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnDefaultMeshId = wx.NewId()
        btnDefaultMesh= wx.BitmapButton(self, id=self.btnDefaultMeshId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlDefaultMesh, 0, wx.EXPAND, border=5)
        hbox.Add(btnDefaultMesh, 0, wx.EXPAND|wx.RIGHT, border=70)
        # ...

        # ...
        staticTxt = wx.StaticText(pnl, -1, "points", size=(70,20))
        self.pnlDefaultPoints= wx.Panel(self, -1, size=(90,25))
        color = [c*255 for c in theme.color_viewer('default_points')]
        self.pnlDefaultPoints.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnDefaultPointsId = wx.NewId()
        btnDefaultPoints= wx.BitmapButton(self, id=self.btnDefaultPointsId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlDefaultPoints, 0, wx.EXPAND, border=5)
        hbox.Add(btnDefaultPoints, 0, wx.EXPAND|wx.RIGHT, border=70)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...
        # -------------------------------------------------------------------

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # -------------------------------------------------------------------
        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Points", size=(400,20))
        staticTxt.SetFont(font_section)
        hbox.Add(staticTxt, 0, wx.ALL, 5)
        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Marker", size=(70,20))
        self.pnlMarkerPoints = wx.Panel(self, -1, size=(90,25))
        color = [c*255 for c in theme.color_viewer('marker_points')]
        self.pnlMarkerPoints.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnMarkerPointsId = wx.NewId()
        btnMarkerPoints = wx.BitmapButton(self, id=self.btnMarkerPointsId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlMarkerPoints, 0, wx.EXPAND, border=5)
        hbox.Add(btnMarkerPoints, 0, wx.EXPAND|wx.RIGHT, border=70)
        # ...

        # ...
        staticTxt = wx.StaticText(pnl, -1, "Selected", size=(70,20))
        self.pnlSelectedPoints = wx.Panel(self, -1, size=(90,25))
        color = [c*255 for c in theme.color_viewer('selection_points')]
        self.pnlSelectedPoints.SetBackgroundColour(wx.Colour(*color))
        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))
        self.btnSelectedPointsId = wx.NewId()
        btnSelectedPoints = wx.BitmapButton(self, id=self.btnSelectedPointsId \
                                             , bitmap=imageOpenDir \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.pnlSelectedPoints, 0, wx.EXPAND, border=5)
        hbox.Add(btnSelectedPoints, 0, wx.EXPAND|wx.RIGHT, border=70)

        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...
        # -------------------------------------------------------------------

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # -------------------------------------------------------------------
        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "Size Points", size=(400,20))
        staticTxt.SetFont(font_section)
        hbox.Add(staticTxt, 0, wx.ALL, 5)
        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "marker", size=(70,20))
        self.txtCtrlSizeMarkerId = wx.NewId()
        self.txtCtrlSizeMarker= wx.TextCtrl(pnl, self.txtCtrlSizeMarkerId)
        self.txtCtrlSizeMarker.SetValue(str(theme.size_points('marker_points')))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlSizeMarker, 0, wx.EXPAND|wx.RIGHT, border=50)
        # ...

        # ...
        staticTxt = wx.StaticText(pnl, -1, "selected", size=(70,20))
        self.txtCtrlSizeSelectedPointsId = wx.NewId()
        self.txtCtrlSizeSelectedPoints= wx.TextCtrl(pnl, self.txtCtrlSizeSelectedPointsId)
        self.txtCtrlSizeSelectedPoints.SetValue(str(theme.size_points('selection_points')))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlSizeSelectedPoints, 0, wx.EXPAND|wx.RIGHT, border=50)
        # ...

        # ...
        staticTxt = wx.StaticText(pnl, -1, "grid", size=(70,20))
        self.txtCtrlSizeGridId = wx.NewId()
        self.txtCtrlSizeGrid= wx.TextCtrl(pnl, self.txtCtrlSizeGridId)
        self.txtCtrlSizeGrid.SetValue(str(theme.size_points('grid')))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlSizeGrid, 0, wx.EXPAND|wx.RIGHT, border=50)
        # ...

        vbox.Add(hbox, 0, wx.ALL, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # ...
        staticTxt = wx.StaticText(pnl, -1, "geometry", size=(70,20))
        self.txtCtrlSizeGeometryId = wx.NewId()
        self.txtCtrlSizeGeometry= wx.TextCtrl(pnl, self.txtCtrlSizeGeometryId)
        self.txtCtrlSizeGeometry.SetValue(str(theme.size_points('geometry')))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlSizeGeometry, 0, wx.EXPAND|wx.RIGHT, border=50)
        # ...

        # ...
        staticTxt = wx.StaticText(pnl, -1, "patch", size=(70,20))
        self.txtCtrlSizePatchId = wx.NewId()
        self.txtCtrlSizePatch= wx.TextCtrl(pnl, self.txtCtrlSizePatchId)
        self.txtCtrlSizePatch.SetValue(str(theme.size_points('patch')))

        hbox.Add(staticTxt, 0, wx.ALL, 5)
        hbox.Add(self.txtCtrlSizePatch, 0, wx.EXPAND|wx.RIGHT, border=50)
        # ...

        # ...
        vbox.Add(hbox, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...
        # -------------------------------------------------------------------

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Refresh')
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

        btnDefaultGeometry.Bind(wx.EVT_BUTTON, self.ChooseColor)
        btnDefaultPatch.Bind(wx.EVT_BUTTON, self.ChooseColor)
        btnDefaultMesh.Bind(wx.EVT_BUTTON, self.ChooseColor)
        btnDefaultPoints.Bind(wx.EVT_BUTTON, self.ChooseColor)

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        self.Bind(wx.EVT_TEXT, self.EvtText)


    def EvtCheckBox(self, event):
        if event.GetId() == self.cb_blendID:
            theme.set_enable_blend(self.cb_blend.GetValue())

    def ChooseColor(self, event):
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            _values = data.GetColour().Get()
            values = [x/255. for x in _values]

        if event.GetId() == self.btnBackGroundId:
            theme.set_color_viewer('background', values)
            self.pnlBackGround.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()
        if event.GetId() == self.btnGridId:
            theme.set_color_viewer('grid', values)
            self.pnlGrid.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()

        if event.GetId() == self.btnSelGeoMeshId:
            theme.set_color_selected_geometry ('mesh', values)
            self.pnlSelGeoMesh.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()
        if event.GetId() == self.btnSelGeoNurbsId:
            theme.set_color_selected_geometry ('nurbs', values)
            self.pnlSelGeoNurbs.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()
        if event.GetId() == self.btnSelGeoPointsId:
            theme.set_color_selected_geometry ('points', values)
            self.pnlSelGeoPoints.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()

        if event.GetId() == self.btnSelPatchMeshId:
            theme.set_color_selected_patch ('mesh', values)
            self.pnlSelPatchMesh.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()
        if event.GetId() == self.btnSelPatchNurbsId:
            theme.set_color_selected_patch ('nurbs', values)
            self.pnlSelPatchNurbs.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()
        if event.GetId() == self.btnSelPatchPointsId:
            theme.set_color_selected_patch ('points', values)
            self.pnlSelPatchPoints.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()

        if event.GetId() == self.btnDefaultGeometryId:
            theme.set_color_viewer ('default_geometry', values)
            self.pnlDefaultGeometry.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()
        if event.GetId() == self.btnDefaultPatchId:
            theme.set_color_viewer ('default_patch', values)
            self.pnlDefaultPatch.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()
        if event.GetId() == self.btnDefaultMeshId:
            theme.set_color_viewer ('default_mesh', values)
            self.pnlDefaultMesh.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()
        if event.GetId() == self.btnDefaultPointsId:
            theme.set_color_viewer ('default_points', values)
            self.pnlDefaultPoints.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()

        if event.GetId() == self.btnMarkerPointsId:
            theme.set_color_viewer('marker_points', values)
            self.pnlMarkerPoints.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()
        if event.GetId() == self.btnSelectedPointsId:
            theme.set_color_viewer('selection_points', values)
            self.pnlMarkerPoints.SetBackgroundColour(wx.Colour(*_values))
            self.viewer.Refresh()

        dlg.Destroy()

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAlphaId:
                value = float(event.GetString())
                theme.set_alpha(value)
            if event.GetId() == self.txtCtrlBetaId:
                value = float(event.GetString())
                theme.set_beta(value)
            if event.GetId() == self.txtCtrlAlpha_BgId:
                value = float(event.GetString())
                theme.set_alpha_bg(value)

            if event.GetId() == self.txtCtrlSizeMarkerId:
                value = float(event.GetString())
                theme.set_size_points('marker_points',value)
            if event.GetId() == self.txtCtrlSizeSelectedPointsId:
                value = float(event.GetString())
                theme.set_size_points('selection_points',value)
            if event.GetId() == self.txtCtrlSizeGridId:
                value = float(event.GetString())
                theme.set_size_points('grid',value)
            if event.GetId() == self.txtCtrlSizeGeometryId:
                value = float(event.GetString())
                theme.set_size_points('geometry',value)
            if event.GetId() == self.txtCtrlSizePatchId:
                value = float(event.GetString())
                theme.set_size_points('patch',value)
        except:
            pass

        self.viewer.Refresh()

    def OnOk(self, event):
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
        self.SetSize((920, 750))
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
