import random
import wx

########################################################################
class TabPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self, parent, page, list_btns, sizeBtn=10):
        """"""
        wx.Panel.__init__(self, parent=parent)
        self.page = page
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.BCK_ID = wx.NewId()
        self.NXT_ID = wx.NewId()

        # Back button
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_OTHER, (16,16))
        self.BackBtn = wx.BitmapButton(self, id=self.BCK_ID, bitmap=bmp \
                                  , size=(bmp.GetWidth()+10,
                                          bmp.GetHeight()+10))
        self.BackBtn.Bind(wx.EVT_BUTTON, self.onChangeSelection)
        sizer.Add(self.BackBtn, 0, wx.EXPAND, 2)
        if page == 0:
            self.BackBtn.Disable()

        # Next button
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_OTHER, (16,16))
        self.NextBtn = wx.BitmapButton(self, id=self.NXT_ID, bitmap=bmp \
                                  , size=(bmp.GetWidth()+10,
                                          bmp.GetHeight()+10))
        self.NextBtn.Bind(wx.EVT_BUTTON, self.onChangeSelection)
        sizer.Add(self.NextBtn, 0, wx.EXPAND, 2)
        if page == len(list_btns)/sizeBtn-1:
            self.NextBtn.Disable()

        for info in list_btns[page*sizeBtn:(page+1)*sizeBtn]:
            idBtn = info[0]
            labelBtn = info[1]
            btn = wx.Button(self, id=idBtn, label=labelBtn)
            btn.Bind(wx.EVT_BUTTON, self.buttonClick)
            sizer.Add(btn, 0, wx.EXPAND, 2)

        self.SetSizer(sizer)

    #----------------------------------------------------------------------
    def onChangeSelection(self, event):
        """
        Change the page!
        """
        notebook = self.GetParent()
        ID = event.GetId()
        if ID == self.BCK_ID:
            notebook.SetSelection(self.page-1)
        if ID == self.NXT_ID:
            notebook.SetSelection(self.page+1)

    def buttonClick(self,event):
        print "OK"
########################################################################
class InspectorActionsFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "",
                          size=(200,400)
                          )
        panel = wx.Panel(self)
        sizeBtn = 10

        list_btns = []
        for i in range(0,30):
            list_btns.append([wx.NewId(), "Button"+str(i)])

        notebook = wx.Notebook(panel)

        nPages = len(list_btns)/sizeBtn
        if len(list_btns) % sizeBtn > 0:
            nPages += 1

        for ipage in range(0, nPages):
            itab = TabPanel(notebook, ipage, list_btns, sizeBtn=10)
            notebook.AddPage(itab, "Act")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()

        self.Show()


#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = InspectorActionsFrame()
    app.MainLoop()
