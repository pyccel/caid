from global_vars import DIM_PROJECT, MODELS_DIRECTORY
import numpy as np
import wx

class PageDefaultExport(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent.nb)
        self.title = "Default Export"
        pnl = self
        self.parent = parent
        currentDim = DIM_PROJECT

        self.radioBtnList = []

        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))

#        self.SetBackgroundColour("White")

        # ...
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "File", size=(160,30))
        self.txtCtrlWorkDirId = wx.NewId()
        self.txtCtrlWorkDir = wx.TextCtrl(pnl, self.txtCtrlWorkDirId, size=(190,30), pos=(60, 20))
        self.buttonOpenDir = wx.BitmapButton(pnl, id=-1, bitmap=imageOpenDir \
#                                       , pos=(10, 20) \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox1.Add(staticTxt, 0, wx.ALL, 5)
        hbox1.Add(self.txtCtrlWorkDir, border=5)
        hbox1.Add(self.buttonOpenDir, flag=wx.LEFT, border=5)

        vbox.Add(hbox1, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # ...
        hbox100 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox100.Add(okButton)
        hbox100.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(hbox100, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        self.SetSizer(vbox)
        # ...

        self.Layout()

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        self.Bind(wx.EVT_TEXT, self.EvtText)
        self.buttonOpenDir.Bind(wx.EVT_BUTTON, self.Action)

    def Action(self, event):
#        print "OnOpenDir"
        # Create a save file dialog
        dialog = wx.FileDialog ( None, style = wx.SAVE | wx.OVERWRITE_PROMPT )
        # Show the dialog and get user input
        if dialog.ShowModal() == wx.ID_OK:
            ls_file = dialog.GetPath()
#            print 'Selected:', ls_file
            import pigasus.geometry.cad_geometry as cg

            lo_geo = cg.cad_geometry()
            for elt in self.parent.parent.list_elements:
                if elt.EligibleElement:
                    lo_geo.add_patch(elt.geo.list[0])
                lo_geo.add_patch(elt.geo.list[0])
            lo_geo.save(ls_file)
        # The user did not select anything
        else:
            print('Nothing was selected.')
        # Destroy the dialog
        dialog.Destroy()

    def OnOk(self, event):
        self.parent.Destroy()

    def OnClose(self, event):
        self.parent.Destroy()

    def EvtText(self, event):
        if event.GetId() == self.txtCtrlWorkDirId:
            self.txtCtrlWorkDir.SetValue(event.GetString())

class PageBezierFormat(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent.nb)
        self.title = "Bezier Format"
        pnl = self
        self.parent = parent
        currentDim = DIM_PROJECT

        self.file = MODELS_DIRECTORY + "/tmp.txt"

        self.radioBtnList = []

        imageOpenDir = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (24,24))

#        self.SetBackgroundColour("White")

        # ...
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        staticTxt = wx.StaticText(pnl, -1, "File", size=(160,30))
        self.txtCtrlWorkDirId = wx.NewId()
        self.txtCtrlWorkDir = wx.TextCtrl(pnl, self.txtCtrlWorkDirId, size=(190,30), pos=(60, 20))
        self.buttonOpenDir = wx.BitmapButton(pnl, id=-1, bitmap=imageOpenDir \
#                                       , pos=(10, 20) \
                                       , size = (imageOpenDir.GetWidth()+5 \
                                                             , imageOpenDir.GetHeight()+5))

        hbox1.Add(staticTxt, 0, wx.ALL, 5)
        hbox1.Add(self.txtCtrlWorkDir, border=5)
        hbox1.Add(self.buttonOpenDir, flag=wx.LEFT, border=5)

        vbox.Add(hbox1, 0, wx.ALL, 5)
        pnl.SetSizer(vbox)
        # ...

        staticline = wx.StaticLine(self, -1, (25, 260), (300,1))
        vbox.Add(staticline, 0, wx.ALL, 5)

        # ...
        hbox100 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox100.Add(okButton)
        hbox100.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(hbox100, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        self.SetSizer(vbox)
        # ...

        self.Layout()

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        self.Bind(wx.EVT_TEXT, self.EvtText)
        self.buttonOpenDir.Bind(wx.EVT_BUTTON, self.Action)

    def Action(self, event):
#        print "OnOpenDir"
        # Create a save file dialog
        dialog = wx.FileDialog ( None, style = wx.SAVE | wx.OVERWRITE_PROMPT )
        # Show the dialog and get user input
        if dialog.ShowModal() == wx.ID_OK:
            self.file = dialog.GetPath()
#            print 'Selected:', self.file

        # The user did not select anything
        else:
            print('Nothing was selected.')
        # Destroy the dialog
        dialog.Destroy()

    def OnOk(self, event):
        list_Nodes = []
        list_elementData = []
        list_elementInfo = []
        for elt in self.parent.parent.list_elements:
            if elt.EligibleElement:
                currentNodes, currentData, currentInfo = elt.geo.ToBezierPatch(ai_patch_id=0)
                for data in currentNodes:
                    list_Nodes.append(data)
                for data in currentData:
                    list_elementData.append(data)
                for data in currentInfo:
                    list_elementInfo.append(data)

#        print "list_elementData = ",list_elementData
        list_info = [len(list_Nodes), len(list_elementData)]

        ls_file = self.file.split('.')[0]
        np.savetxt(ls_file+"_Info"+".txt", list_info)

        np.savetxt(ls_file+"_Nodes"+".txt", list_Nodes)
        np.savetxt(ls_file+"_ElementData"+".txt", list_elementData)
        np.savetxt(ls_file+"_ElementInfo"+".txt", list_elementInfo)

        self.parent.Destroy()

    def OnClose(self, event):
        self.parent.Destroy()

    def EvtText(self, event):
        if event.GetId() == self.txtCtrlWorkDirId:
            self.txtCtrlWorkDir.SetValue(event.GetString())

class ExportDialog(wx.Dialog):

    def __init__(self, parent, title):
        super(ExportDialog, self).__init__(parent)
        self.parent = parent

        self.ls_current_value = None
        self.value = None

        self.InitUI()
        self.SetSize((450, 400))
#        self.SetTitle("Change Zoom")

    def InitUI(self):

        self.pnl = wx.Panel(self)
        self.nb = wx.Notebook(self.pnl)

        # create the page windows as children of the notebook
        page_DefaultExport = PageDefaultExport(self)
        page_BezierFormat = PageBezierFormat(self)

        # add the pages to the notebook with the label to show on the tab
        self.nb.AddPage(page_DefaultExport, page_DefaultExport.title)
        self.nb.AddPage(page_BezierFormat, page_BezierFormat.title)

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.pnl.SetSizer(sizer)

    def SetPageDefaultExport(self):
        self.nb.SetSelection(0)

    def SetPageBezierFormat(self):
        self.nb.SetSelection(1)
