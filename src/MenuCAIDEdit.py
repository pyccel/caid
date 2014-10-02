# -*- coding: UTF-8 -*-
import wx

class MenuCAIDEdit(wx.Menu):

    def __init__(self, parent):

        wx.Menu.__init__(self)
        self._geometry_menu = True
        self._show_mesh     = False
        self._enable_inspector_color = False

        self.parent = parent
        self.initGUI()

    def initGUI(self):

        # add New File in the menu
        self.m_undo = self.Append(wx.ID_UNDO, "U&ndo\tCtrl-Z", "Undo modification.")
        self.m_redo = self.Append(wx.ID_REDO, "R&edo\tCtrl-Y", "Redo modification.")
        self.AppendSeparator()

        self.m_cut = self.Append(wx.ID_CUT, "C&ut\tCtrl-X", "Cut Element.")
        self.m_copy = self.Append(wx.ID_COPY, "Co&py\tCtrl-C", "Copy Element.")
        self.m_paste = self.Append(wx.ID_PASTE, "P&aste\tCtrl-V", "paste Element.")
        self.AppendSeparator()

        self.m_refresh = self.Append(wx.ID_REFRESH, "Refresh\tF5", "Refresh.")
        self.m_selectAll = self.Append(wx.ID_SELECTALL, "Select A&ll", "Select All.")
        self.m_duplicate = self.Append(wx.ID_DUPLICATE, "Dupli&cate\tCtrl-D", "Duplicate.")
        self.m_delete = self.Append(wx.ID_DELETE, "D&elete\tDel", "Delete.")
        self.AppendSeparator()
        # ...

        # ...
        self.GeoMenuID   = wx.NewId()
        self.PatchMenuID = wx.NewId()

        self.m_geo_patch_menu   = self.Append(self.GeoMenuID  , "Geometry/Patch Menu\tF6", "Show Geometry/Patch Menu.")
        self.AppendSeparator()
        # ...

        # ...
        self.ShowMeshMenuID   = wx.NewId()
        self.HideMeshMenuID   = wx.NewId()

        self.m_showMesh_menu   = self.Append(self.ShowMeshMenuID  , "Show/Hide Mesh\tF7", "Show/Hide Mesh.")
        self.AppendSeparator()
        # ...

        # ...
        self.EnableInspectorColorMenuID = wx.NewId()
        self.DisableInspectorColorMenuID= wx.NewId()

        self.m_EnableInspectorColor_menu = self.Append(self.EnableInspectorColorMenuID, "Enable/Disable Inspector color \tF8", "Inspector color.")

        self.AppendSeparator()
        # ...

        # ...
        self.sm_theme = wx.Menu()
        self.ThemeID = wx.NewId()
        self.list_m_themes = []

        self.ThemeLoadID = wx.NewId()
        self.m_ThemeLoad = self.sm_theme.Append(self.ThemeLoadID, 'Load', kind=wx.ITEM_RADIO)
        self.list_m_themes.append(self.m_ThemeLoad)

        self.ThemeSaveID = wx.NewId()
        self.m_ThemeSave = self.sm_theme.Append(self.ThemeSaveID, 'Save', kind=wx.ITEM_RADIO)
        self.list_m_themes.append(self.m_ThemeSave)

#        self.ThemeID = wx.NewId()
#        self.m_Theme = self.sm_theme.Append(self.ThemeID, '', kind=wx.ITEM_RADIO)
#        self.list_m_themes.append(self.m_Theme)

        self.ThemeGreyID = wx.NewId()
        self.m_ThemeGrey = self.sm_theme.Append(self.ThemeGreyID, 'Grey', kind=wx.ITEM_RADIO)
        self.list_m_themes.append(self.m_ThemeGrey)

        self.ThemeDarkID = wx.NewId()
        self.m_ThemeDark = self.sm_theme.Append(self.ThemeDarkID, 'Dark', kind=wx.ITEM_RADIO)
        self.list_m_themes.append(self.m_ThemeDark)

        self.ThemeWhiteID = wx.NewId()
        self.m_ThemeWhite = self.sm_theme.Append(self.ThemeWhiteID, 'White', kind=wx.ITEM_RADIO)
        self.list_m_themes.append(self.m_ThemeWhite)

        self.ThemeDjangoID = wx.NewId()
        self.m_ThemeDjango = self.sm_theme.Append(self.ThemeDjangoID, 'Django', kind=wx.ITEM_RADIO)
        self.list_m_themes.append(self.m_ThemeDjango)

        self.ThemePassID = wx.NewId()
        self.m_ThemePass = self.sm_theme.Append(self.ThemePassID, 'Joe Pass', kind=wx.ITEM_RADIO)
        self.list_m_themes.append(self.m_ThemePass)
        # ...

        # ...
        self.sm_intersection = wx.Menu()
        self.IntersectionID = wx.NewId()
        self.list_m_intersection = []

        self.IntersectionNptsID = wx.NewId()
        self.m_IntersectionNpts = self.sm_intersection.Append(self.IntersectionNptsID, 'Resolution', kind=wx.ITEM_RADIO)
        self.list_m_intersection.append(self.m_IntersectionNpts)
        # ...

        # ...
        self.sm_coons = wx.Menu()
        self.CoonsID = wx.NewId()
        self.list_m_coons = []

        self.CoonsTolID = wx.NewId()
        self.m_CoonsTol = self.sm_coons.Append(self.CoonsTolID, 'Tolerance', kind=wx.ITEM_RADIO)
        self.list_m_coons.append(self.m_CoonsTol)
        # ...


        # ...
        self.sm_preferences = wx.Menu()
        self.PreferencesID = wx.NewId()
        self.sm_preferences.AppendMenu(self.PreferencesID, 'Theme', self.sm_theme)
        self.sm_preferences.AppendMenu(self.PreferencesID, 'Intersection', self.sm_intersection)
        self.sm_preferences.AppendMenu(self.PreferencesID, 'Coons', self.sm_coons)

        self.AppendMenu(self.PreferencesID, 'Preferences', self.sm_preferences)
        # ...

        # ... deactivate items
#        self.m_undo.Enable(False)
#        self.m_redo.Enable(False)
        self.m_cut.Enable(False)
        self.m_copy.Enable(False)
        self.m_paste.Enable(False)
        self.m_selectAll.Enable(False)
        self.m_duplicate.Enable(False)
        self.m_delete.Enable(False)
        # ...

    def OnUndo( self, event ):
        print "OnUndo: Begin"

        wk = self.parent.tree.currentWorkGroup
        if wk is None:
            return

        if len( wk.stockUndo ) == 0:
                return

        a = wk.stockUndo.pop()
#        if len( stockUndo ) == 0:
#                self.toolbar1.EnableTool( 808, False )
        a.undo()
        wk.stockRedo.append( a )
#        self.toolbar1.EnableTool( 809, True )

        print "done."

    def OnRedo( self, event ):
        print "OnRedo: Begin"

        wk = self.parent.tree.currentWorkGroup
        if wk is None:
            return

        if len( wk.stockRedo ) == 0:
                return
        a = wk.stockRedo.pop()

#        if len( stockRedo ) == 0:
#                self.toolbar1.EnableTool( 809, False )
        a.redo()
        wk.stockUndo.append( a )
#        self.toolbar1.EnableTool( 808, True )

        print "done."

    def OnClosePage(self, event):
        print "OnClosePage TODO"

    def OnCut(self, event):
        print "OnCut TODO"

    def OnCopy(self, event):
        print "OnCopy TODO"

    def OnPaste(self, event):
        print "OnPaste TODO"

    def OnRefresh(self, event):
        wk = self.parent.tree.currentWorkGroup
        if wk is None:
            return

        wk.Refresh(inspector=True)

    def OnSelectAll(self, event):
        print "OnSelectAll"
#        OnSelectAll(self.parent.editor)

    def OnDelete(self, event):
        print "OnDelete "
#        OnErase(self.parent.editor)

    def OnDuplicate(self, event):
        print "OnDuplicate"
#        OnDuplicate(self.parent.editor)

    def OnPreferences(self, event):
        print "OnPreferences TODO"
#        dlg = PreferencesDialog(self.parent, title="Preferences")
#        dlg.ShowModal()
#        dlg.Destroy()

    def OnTheme(self, event):
        wk = self.parent.tree.currentWorkGroup
        if wk is None:
            return

        if event.GetId() == self.ThemeLoadID:
            filename = "theme.xml"
            # Create a save file dialog
            from global_vars import CAIDThemewildcard
            dialog = wx.FileDialog(None\
                                   , style = wx.OPEN\
                                   , wildcard=CAIDThemewildcard)
            # Show the dialog and get user input
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetPath()
            # The user did not select anything
            else:
                print 'Nothing was selected.'
                print 'current filename : ', filename
            # Destroy the dialog
            dialog.Destroy()
            wk.viewer.theme.load(filename=filename)

        if event.GetId() == self.ThemeSaveID:
            filename = "theme.xml"
            # Create a save file dialog
            from global_vars import CAIDThemewildcard
            dialog = wx.FileDialog ( None\
                                    , style = wx.SAVE | wx.OVERWRITE_PROMPT\
                                    , wildcard=CAIDThemewildcard)
            # Show the dialog and get user input
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetPath()
            # The user did not select anything
            else:
                print 'Nothing was selected.'
                print 'current filename : ', filename
            # Destroy the dialog
            dialog.Destroy()
            wk.viewer.theme.save(filename=filename)

        if event.GetId() == self.ThemeGreyID:
            wk.viewer.set_theme("grey")
        if event.GetId() == self.ThemeDarkID:
            wk.viewer.set_theme("dark")
        if event.GetId() == self.ThemeWhiteID:
            wk.viewer.set_theme("white")
        if event.GetId() == self.ThemeDjangoID:
            wk.viewer.set_theme("django")
        if event.GetId() == self.ThemePassID:
            wk.viewer.set_theme("joepass")

#        if event.GetId() == self.ThemeID:
#            wk.viewer.set_theme("")

    def OnIntersection(self, event):
        wk = self.parent.tree.currentWorkGroup
        if wk is None:
            return

        if event.GetId() == self.IntersectionNptsID:
            npts = wk.preferences.intersection["npts"]

            from customDialogs import edtTxtDialog
            dlg = edtTxtDialog(None, title="Edit Resolution", size=(200,75) )
            dlg.setValue(str(npts))
            dlg.ShowModal()
            try:
                value = int(dlg.getValue())
            except:
                value = npts
            wk.preferences.set_intersection("npts", value)
            dlg.Destroy()


    def OnCoons(self, event):
        wk = self.parent.tree.currentWorkGroup
        if wk is None:
            return

        if event.GetId() == self.CoonsTolID:
            tol = wk.preferences.coons["tol"]

            from customDialogs import edtTxtDialog
            dlg = edtTxtDialog(None, title="Edit Tolerance", size=(200,75) )
            dlg.setValue(str(tol))
            dlg.ShowModal()
            try:
                value = float(dlg.getValue())
            except:
                value = tol
            wk.preferences.set_coons("tol", value)
            dlg.Destroy()

    def OnShowGeometryPatchMenu(self, event):
        wk = self.parent.tree.currentWorkGroup
        if wk is None:
            return

        self._geometry_menu = not self._geometry_menu

        if event.GetId() == self.GeoMenuID:
            if self._geometry_menu:
                wk.inspector.ShowAction(wk.inspector.geometryActions)
            else:
                wk.inspector.ShowAction(wk.inspector.patchActions)

    def OnShowMeshMenu(self, event):
        wk = self.parent.tree.currentWorkGroup
        if wk is None:
            return

        self._show_mesh     = not self._show_mesh

        if event.GetId() == self.ShowMeshMenuID:
            for geo in wk.list_geo:
                geo.showMesh = self._show_mesh

        wk.Refresh()

    def OnEnableInspectorColor(self, event):
        wk = self.parent.tree.currentWorkGroup
        if wk is None:
            return

        self._enable_inspector_color = not self._enable_inspector_color

        if event.GetId() == self.EnableInspectorColorMenuID:
            wk.inspector.tree.set_enable_inspector_color(self._enable_inspector_color)
            wk.Refresh(inspector=True)
