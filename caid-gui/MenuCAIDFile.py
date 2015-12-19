from ExportDialog import ExportDialog
from global_vars import N_RECENT_FILES
import wx

class MenuCAIDFile(wx.Menu):

    def __init__(self, parent):

        wx.Menu.__init__(self)
        self.parent = parent
        self.initGUI()

        self.currentFile = None
        self.recentFiles = []
        self.nRecentFiles = N_RECENT_FILES

    def initGUI(self):

        # add New File in the menu
        self.m_newfile = self.Append(wx.ID_NEW, "N&ew\tCtrl-N", "New File.")
        self.m_openfile = self.Append(wx.ID_OPEN, "O&pen\tCtrl-O", "Open File.")
        self.AppendSeparator()

        self.m_savefile = self.Append(wx.ID_SAVE, "S&ave\tCtrl-S", "Save File.")
        self.m_saveAsfile = self.Append(wx.ID_SAVEAS, "Save A&s", "Save File As.")
        self.AppendSeparator()

        self.recentFilesID = wx.NewId()
        self.m_recentFiles = self.Append(self.recentFilesID, "R&ecent Files", "Open Recent Files.")
        self.AppendSeparator()

        self.m_exit = self.Append(wx.ID_EXIT, "E&xit\tCtrl-X", "Close window and exit program.")

        # ... deactivate items
        self.m_recentFiles.Enable(False)
        # ...

    def OnNewFile(self, event):
        self.parent.tree.createWorkGroup()


    def OnOpenFile(self, event):
        wk = self.parent.tree.createWorkGroup(empty=True)
        wk.open()

    def OnSaveAsFile(self, event):
        filename = None
        # Create a save file dialog
        from global_vars import CAIDWorkGroupwildcard
        dialog = wx.FileDialog ( None\
                                , style = wx.SAVE | wx.OVERWRITE_PROMPT\
                                , wildcard=CAIDWorkGroupwildcard)
        # Show the dialog and get user input
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
        # The user did not select anything
        else:
            print('Nothing was selected.')
        # Destroy the dialog
        dialog.Destroy()

        if filename is not None:
            wk = self.parent.tree.currentWorkGroup
            wk.save(filename = filename)

    def OnSaveFile(self, event):
        wk = self.parent.tree.currentWorkGroup
        wk.save()

    def OnRecentFiles(self, event):
        print("OnRecentFiles")

    def UpdateRecentFiles(self):
        print("UpdateRecentFiles")
#        if self.currentFile not in self.recentFiles:
#            if len(self.recentFiles) == self.nRecentFiles :
#                self.recentFiles.pop(0)
#            self.recentFiles.append(self.currentFile)

