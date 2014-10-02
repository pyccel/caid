import wx

class MenuCAIDViewer(wx.Menu):

    def __init__(self, parent):

        wx.Menu.__init__(self)
        self.parent = parent
        self.initGUI()

    def initGUI(self):
        self.actionZoomID = wx.NewId()
        self.m_actionZoom = self.Append(self.actionZoomID, '&Zoom', 'Zoom on the viewer')
        self.AppendSeparator()

        self.actionhGridID = wx.NewId()
        self.m_actionhGrid = self.Append(self.actionhGridID, '&Set hGrid',  'Set the grid s step of the viewer')
        self.AppendSeparator()

        self.actionTranslateID = wx.NewId()
        self.m_actionTranslate = self.Append(self.actionTranslateID, '&Translate', 'Translate the viewer')
        self.actionRotateID = wx.NewId()
        self.m_actionRotate = self.Append(self.actionRotateID, '&Rotate', 'Rotate the viewer')
        self.AppendSeparator()

        self.CleanMarkSelectedPtsID = wx.NewId()
        self.m_CleanMarkSelectedPts = self.Append(self.CleanMarkSelectedPtsID \
                                                  , '&Clean Mark Selected Points' \
                                                  , 'Clean Mark Selected Points')

        self.CleanMarkerPtsID = wx.NewId()
        self.m_CleanMarkerPts = self.Append(self.CleanMarkerPtsID \
                                                  , '&Clean Marker Points' \
                                                  , 'Clean Marker Points')

        # ... deactivate items
#        self.m_actionZoom.Enable(False)
        self.m_actionhGrid.Enable(False)
        self.m_actionTranslate.Enable(False)
        self.m_actionRotate.Enable(False)
        self.m_CleanMarkSelectedPts.Enable(False)
        self.m_CleanMarkerPts.Enable(False)
        # ...

    def OnZoom(self, event):
        print "OnZoom"
#        import common_obj as _com
#        com = _com.common_obj()
#        com.designer.OnZoom(event)

    def OnhGrid(self, event):
        print "OnhGrid"
#        import common_obj as _com
#        com = _com.common_obj()
#        com.designer.OnhGrid(event)

    def OnTranslate(self, event):
        print "OnTranslate"
#        import common_obj as _com
#        com = _com.common_obj()
#        com.designer.OnTranslate(event)

    def OnRotate(self, event):
        print "OnRotate"
#        import common_obj as _com
#        com = _com.common_obj()
#        com.designer.OnRotate(event)

    def OnCleanMarkSelectedPts(self, event):
        print "OnCleanMarkSelectedPts"
#        import common_obj as _com
#        com = _com.common_obj()
#        com.designer.ClearMarkedSelection ()

    def OnCleanMarkerPts(self, event):
        print "OnCleanMarkerPts"
#        import common_obj as _com
#        com = _com.common_obj()
#        com.designer.CleanMarkerPoints ()
