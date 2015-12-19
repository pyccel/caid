import wx
import numpy as np
from classActions import UndoModifyPatch

class viewTxtDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(viewTxtDialog, self).__init__(*args, **kw)

        self.ls_current_value = None
        self.value = None

        self.InitUI()
        self.SetSize((200, 100))


    def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.RadioButton(pnl, label='value'))

        self.txtCtrl = wx.TextCtrl(pnl)
        hbox1.Add(self.txtCtrl, flag=wx.LEFT, border=5)

        self.txtCtrl.SetValue("Bonjour")

        pnl.SetSizer(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnOk(self, event):
        self.Destroy()

    def OnClose(self, event):
        self.Destroy()


###########################################################################
## Class edtTxtDialog
###########################################################################

class edtTxtDialog( wx.Dialog ):

    def __init__( self, parent, title=wx.EmptyString, size = wx.DefaultSize ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY \
                            , title = title \
                            , pos = wx.DefaultPosition \
                            , size = size \
                            , style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString,
                                       wx.DefaultPosition, (-1,-1), 0 )
        bSizer2.Add( self.m_textCtrl3, 0, wx.ALL|wx.EXPAND, 5 )

        self.SetSizer( bSizer2 )
        self.Layout()
        bSizer2.Fit( self )

        self.Centre( wx.BOTH )
        self.SetSize(size)
        self.SetFocus()

        self.ID_CLOSE = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnClose, id=self.ID_CLOSE)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_NORMAL,  wx.WXK_ESCAPE, self.ID_CLOSE )])
        self.SetAcceleratorTable(accel_tbl)

    def OnClose(self, event):
        self.Close(True)

    def __del__( self ):
        pass

    # Virtual event handlers, overide them in your derived class
    def getValue(self):
        return self.m_textCtrl3.GetValue()

    def setValue(self, txt):
        try:
            self.m_textCtrl3.SetValue(txt)
        except:
            pass

class edtCoordinatesTxtDialog(wx.Dialog):

    def __init__(self, parent, title='', x=None,y=None,z=None,w=None):
        super(edtCoordinatesTxtDialog, self).__init__(None, title=title)

        self.x = x
        self.y = y
        self.z = z
        self.w = w

        self.InitUI()
        self.SetSize((240, 65))
        self.SetFocus()

        self.ID_CLOSE = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnClose, id=self.ID_CLOSE)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_NORMAL,  wx.WXK_ESCAPE, self.ID_CLOSE )])
        self.SetAcceleratorTable(accel_tbl)

    def OnClose(self, event):
        self.Close(True)

    def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        pnl.Bind(wx.EVT_TEXT, self.EvtText)

        self.txtCtrlxId = wx.NewId()
        self.txtCtrlx = wx.TextCtrl(pnl,self.txtCtrlxId,size = wx.Size(50, 30))
        if self.x is not None:
            self.txtCtrlx.SetValue(str(self.x))
        hbox1.Add(self.txtCtrlx, flag=wx.LEFT, border=5)

        pnl.SetSizer(hbox1)

        self.txtCtrlyId = wx.NewId()
        self.txtCtrly = wx.TextCtrl(pnl,self.txtCtrlyId,size = wx.Size(50, 30))
        if self.y is not None:
            self.txtCtrly.SetValue(str(self.y))
        hbox1.Add(self.txtCtrly, flag=wx.LEFT, border=5)

        pnl.SetSizer(hbox1)

        self.txtCtrlzId = wx.NewId()
        self.txtCtrlz = wx.TextCtrl(pnl,self.txtCtrlzId,size = wx.Size(50, 30))
        if self.z is not None:
            self.txtCtrlz.SetValue(str(self.z))
        hbox1.Add(self.txtCtrlz, flag=wx.LEFT, border=5)

        pnl.SetSizer(hbox1)

        self.txtCtrlwId = wx.NewId()
        self.txtCtrlw = wx.TextCtrl(pnl,self.txtCtrlwId,size = wx.Size(50, 30))
        if self.w is not None:
            self.txtCtrlw.SetValue(str(self.w))
        hbox1.Add(self.txtCtrlw, flag=wx.LEFT, border=5)

        pnl.SetSizer(hbox1)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)

        self.SetSizer(vbox)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlxId:
                self.x = float(event.GetString())
            if event.GetId() == self.txtCtrlyId:
                self.y = float(event.GetString())
            if event.GetId() == self.txtCtrlzId:
                self.z = float(event.GetString())
            if event.GetId() == self.txtCtrlwId:
                self.w = float(event.GetString())
        except:
            pass

    def getValue(self):
        return self.x, self.y, self.z, self.w


class radioDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(radioDialog, self).__init__(*args, **kw)
#    def __init__(self, parent, title, size=None, pos=(0,0)):
#        wx.Dialog.__init__( self, None,-1, title, size=size, pos=pos )

        self.valueID = 0
        self.value = None

#        self.InitUI()

    def InitUI(self, list_text):

        pnl = wx.PyScrolledWindow(self,-1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox1 = wx.BoxSizer(wx.VERTICAL)

        x = 20       # Magic numbers !?
        y = 20

        self.radioBtnList = []
        for text in list_text:
            self.radioBtnList.append(wx.RadioButton(pnl, label=text))

        for R in self.radioBtnList:
            w, h = R.GetSize()

            dy = h + 10     # calculate for next loop
            y += dy
            vbox1.Add(R)


        pnl.SetScrollbars( 0, dy,  0, y/dy+1 )
        pnl.SetScrollRate( 1, 1 )      # Pixels per scroll increment

        pnl.SetSizer(vbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnOk(self, event):
        list_state = []
        for R in self.radioBtnList:
            list_state.append(R.GetValue())

        index = -1
        for (i,v) in enumerate(list_state):
            if v :
                index = i
                break

        label = self.radioBtnList[index].GetLabel()
        self.value = str(label)
        self.valueID = index

        self.Destroy()

    def OnClose(self, event):
        self.Destroy()

    def GetValue(self):
        return self.value, self.valueID

class ZoomDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(ZoomDialog, self).__init__(*args, **kw)

        self.ls_current_value = None
        self.scale = 100.0

        self.InitUI()
        self.SetSize((200, 100))
        self.SetTitle("Change Zoom")


    def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.RadioButton(pnl, label='Scale'))
        pnl.Bind(wx.EVT_TEXT, self.EvtText)
        hbox1.Add(wx.TextCtrl(pnl), flag=wx.LEFT, border=5)

        pnl.SetSizer(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnOk(self, event):
        self.Destroy()

    def OnClose(self, event):
        self.Destroy()

    def EvtText(self, event):
        self.ls_current_value = event.GetString()

    def getValue(self):
        self.scale = float(self.ls_current_value)
        return 100.0 / self.scale

class hGridDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(hGridDialog, self).__init__(*args, **kw)

        self.ls_current_value = None
        self.value = 1.0

        self.InitUI()
        self.SetSize((200, 100))
        self.SetTitle("Change h-Grid")


    def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.RadioButton(pnl, label='Step'))
        pnl.Bind(wx.EVT_TEXT, self.EvtText)
        hbox1.Add(wx.TextCtrl(pnl), flag=wx.LEFT, border=5)

        pnl.SetSizer(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnOk(self, event):
        self.Destroy()

    def OnClose(self, event):
        self.Destroy()

    def EvtText(self, event):
        self.ls_current_value = event.GetString()

    def getValue(self):
        self.value = float(self.ls_current_value)
        return self.value

class TranslateViewerDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(TranslateViewerDialog, self).__init__(*args, **kw)

        self.ls_current_value = None
        self.value = None

        self.InitUI()
        self.SetSize((200, 100))
        self.SetTitle("Translate the Viewer")


    def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.RadioButton(pnl, label='Vector'))
        pnl.Bind(wx.EVT_TEXT, self.EvtText)
        hbox1.Add(wx.TextCtrl(pnl), flag=wx.LEFT, border=5)

        pnl.SetSizer(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnOk(self, event):
        self.Destroy()

    def OnClose(self, event):
        self.Destroy()

    def EvtText(self, event):
        self.ls_current_value = event.GetString()

    def getValue(self):
        txt = self.ls_current_value.split(',')
        self.value = [float(x) for x in txt]
        return self.value

class RotateViewerDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(RotateViewerDialog, self).__init__(*args, **kw)

        self.ls_current_value = None
        self.value = 1.0

        self.InitUI()
        self.SetSize((200, 100))
        self.SetTitle("Rotate the Viewer")


    def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.RadioButton(pnl, label='Degree'))
        pnl.Bind(wx.EVT_TEXT, self.EvtText)
        hbox1.Add(wx.TextCtrl(pnl), flag=wx.LEFT, border=5)

        pnl.SetSizer(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnOk(self, event):
        self.Destroy()

    def OnClose(self, event):
        self.Destroy()

    def EvtText(self, event):
        self.ls_current_value = event.GetString()

    def getValue(self):
        self.value = float(self.ls_current_value)
        return self.value

########################################################################
class Point(object):
    def __init__(self, ijk, P, w=1.):
        self.ijk = ijk
        self.x   = P[0]
        self.y   = P[1]
        self.z   = P[2]
        self.w   = w

    def __str__(self):
        return self.ijk + "  " \
                + self.x + "," \
                + self.y + "," \
                + self.z \
                + " weight = ", self.w

########################################################################
class edtControlPoints(wx.Dialog):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, workGroup):
        """Constructor"""
        wx.Dialog.__init__(self, None, wx.ID_ANY, "Control Points"\
              , size = (400,500))
        self.workGroup = workGroup

        wk          = self.workGroup
        patch       = wk.inspector.currentPatch
        patchItem   = wk.inspector.currentPatchItem
        geoItem     = wk.inspector.tree.GetItemParent(patchItem)
        geo         = wk.inspector.tree.GetPyData(geoItem)
        patch_id    = geo.index(patch)
        patchInfo   = geo.list_patchInfo[patch_id]
        patchInfo.showPoints = True
        # Refresh the viewer
        wk.Refresh()

        self.patch = patch
        self.patchInfo = patchInfo

        self._patchItem = patchItem
        self._geoItem   = geoItem
        self._geo       = geo

        from viewer import SelectedPoints
        self.selectedPoints = SelectedPoints(self.patch)

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.list_ctrl = wx.ListCtrl(pnl \
                              , style=wx.LC_REPORT|wx.EXPAND|wx.BORDER_SUNKEN)

        self.list_ctrl.InsertColumn(0, "Point")
        self.list_ctrl.InsertColumn(1, "x")
        self.list_ctrl.InsertColumn(2, "y")
        self.list_ctrl.InsertColumn(3, "z")
        self.list_ctrl.InsertColumn(4, "w")

        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)

        rows = []
        n = self.patch.shape
        # if 1D case
        if self.patch.dim == 1:
            for i in range(0,n[0]):
                P = self.patch.points[i,:]
                w = str(self.patch.weights[i])
                ijk   = "("+str(i)+")"
                Q = str(P[0]), str(P[1]), str(P[2])
                rows.append(Point(ijk,Q,w))
        # if 2D case
        if self.patch.dim == 2:
            for j in range(0,n[1]):
                for i in range(0,n[0]):
                    P = self.patch.points[i,j,:]
                    w = str(self.patch.weights[i,j])
                    ijk   = "("+str(i)+","+str(j)+")"
                    Q = str(P[0]), str(P[1]), str(P[2])
                    rows.append(Point(ijk,Q,w))
        # if 3D case
        if self.patch.dim == 3:
            for k in range(0,n[2]):
                for j in range(0,n[1]):
                    for i in range(0,n[0]):
                        P = self.patch.points[i,j,k,:]
                        w = str(self.patch.weights[i,j,k])
                        ijk   = "("+str(i)+","+str(j)+","+str(k)+")"
                        Q = str(P[0]), str(P[1]), str(P[2])
                        rows.append(Point(ijk,Q,w))
        self.rows = rows
        index = 0
        self.myRowDict = {}
        for row in self.rows:
            self.list_ctrl.InsertStringItem(index, row.ijk)
            self.list_ctrl.SetStringItem(index, 1, row.x)
            self.list_ctrl.SetStringItem(index, 2, row.y)
            self.list_ctrl.SetStringItem(index, 3, row.z)
            self.list_ctrl.SetStringItem(index, 4, row.w)
            self.myRowDict[index] = row
            index += 1

        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(self.list_ctrl, 1, wx.EXPAND, 5)
        pnl.SetSizer(hbox)

        vbox.Add(pnl, proportion=1, flag=wx.EXPAND, border=5)
        self.SetSizer(vbox)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        updateButton = wx.Button(self, label='Update')
        hbox2.Add(updateButton)

        vbox.Add(hbox2,flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.list_ctrl.Bind(wx.EVT_RIGHT_DOWN, self.OnRightMouseClick)
        updateButton.Bind(wx.EVT_BUTTON, self.OnUpdate)

        self.menu_titles = ["Edit", "Mark", "Select"]

        self.menu_title_by_id = {}
        for title in self.menu_titles:
            self.menu_title_by_id[ wx.NewId() ] = title

        self.SetFocus()

        self.ID_CLOSE = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnClose, id=self.ID_CLOSE)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_NORMAL,  wx.WXK_ESCAPE, self.ID_CLOSE )])
        self.SetAcceleratorTable(accel_tbl)

    def OnClose(self, event):
        self.Close(True)

    def OnUpdate(self, event):
        wk = self.workGroup
        self.updatePatch()
        self.patchInfo.showPoints = False
        self.selectedPoints.clean()
        # Refresh the viewer
        wk.Refresh(inspector=True)

    def updatePatch(self):
        C = np.zeros_like(self.patch.control)
        n = self.patch.shape

        patch_old = self.patch.copy()

        for key, row in list(self.myRowDict.items()):
            x = float(row.x)
            y = float(row.y)
            z = float(row.z)
            w = float(row.w)

            ijk = row.ijk
            # remove '(' and ')'
            ijk = ijk[1:-1]
            # split with respect to ','
            ijk = ijk.split(',')
            # convert to int
            ijk = [int(i) for i in ijk]

            # if 1D case
            if self.patch.dim == 1:
                i = ijk[0]
                C[i,:] = np.asarray([x,y,z,w])
            # if 2D case
            if self.patch.dim == 2:
                i = ijk[0] ; j = ijk[1]
                C[i,j,:] = np.asarray([x,y,z,w])
            # if 3D case
            if self.patch.dim == 3:
                i = ijk[0] ; j = ijk[1]; k = ijk[2]
                C[i,j,k,:] = np.asarray([x,y,z,w])


        # TODO add set_weights in igakit.nurbs
        self.patch._array = C
        self.patch.set_points(C[...,:3])

        # undo action
        wk = self.workGroup
        patch     = self.patch
        patchItem = self._patchItem
        geo       = self._geo
        geoItem   = self._geoItem
        old       = patch_old

        undo = UndoModifyPatch(wk, patchItem, patch, old, geo, geoItem)
        wk.appendAction(undo)

    def insertData(self):
        index = 0
        for row in self.rows:
            self.list_ctrl.InsertStringItem(index, row.ijk)
            self.list_ctrl.SetStringItem(index, 1, row.x)
            self.list_ctrl.SetStringItem(index, 2, row.y)
            self.list_ctrl.SetStringItem(index, 3, row.z)
            self.list_ctrl.SetStringItem(index, 4, row.w)
            index += 1

    def refreshList(self):
        self.list_ctrl.DeleteAllItems()
        self.insertData()

    def onItemSelected(self, event):
        wk = self.workGroup
        self.currentItem = event.m_itemIndex
        self.currentRow = self.myRowDict[self.currentItem]

        ijk = self.currentRow.ijk
        # remove '(' and ')'
        ijk = ijk[1:-1]
        # split with respect to ','
        ijk = ijk.split(',')
        # convert to int
        ijk = [int(i) for i in ijk]
        if self.patch.dim == 1:
            list_ijk = [ijk[0]]
        if self.patch.dim == 2:
            list_ijk = [[ijk[0]], [ijk[1]]]
        if self.patch.dim == 3:
            list_ijk = [[ijk[0]], [ijk[1]], [ijk[2]]]

        self.selectedPoints.clean()
        self.selectedPoints.addPointsByIndices(list_ijk)
        wk.viewer.AddSelectedPoints(self.selectedPoints)
        # Refresh the viewer
        wk.Refresh()

    def editPoint(self):
        wk = self.workGroup
        x = float(self.currentRow.x)
        y = float(self.currentRow.y)
        z = float(self.currentRow.z)
        w = float(self.currentRow.w)
        dlg = edtCoordinatesTxtDialog(None, title="Edit Point", x=x,y=y,z=z,w=w)
        dlg.ShowModal()
        xtxt, ytxt, ztxt, wtxt = dlg.getValue()
        try:
            xcenter, ycenter, zcenter = wk.viewer.lookAt.GetCenter()
            if xtxt is not None:
                x = float(xtxt)
            else:
                x = xcenter
            if ytxt is not None:
                y = float(ytxt)
            else:
                y = ycenter
            if ztxt is not None:
                z = float(ztxt)
            else:
                z = zcenter
            if wtxt is not None:
                w = float(wtxt)
            else:
                w = 1.0

            self.currentRow.x = str(x)
            self.currentRow.y = str(y)
            self.currentRow.z = str(z)
            self.currentRow.w = str(w)
        except:
            pass

        dlg.Destroy()

    def toSelectedPoint(self):
        wk = self.workGroup
        x = float(self.currentRow.x)
        y = float(self.currentRow.y)
        z = float(self.currentRow.z)
        w = float(self.currentRow.w)
        P = [x,y,z,w]

#        self.selectedPoints.addPointsByIndices(list_ijk)
#        wk.viewer.AddSelectedPoints(self.selectedPoints)
#
#        ijk = self.currentRow.ijk
#
#        selectedPoints = SelectedPoints(self.patch)
#        X,Y,Z = pointsToList(self.patch.points)
#        list_ind = findIndex(X,Y,xmin,xmax,ymin,ymax)
#        list_ijk = fromIndexToCoord(patch, list_ind)
#        selectedPoints.addPointsByIndices(list_ijk)
#        self.AddSelectedPoints(selectedPoints)
#
#        wk.viewer.AddSelectedPoints(P)
#        wk.Refresh()

    def toMarkerPoint(self):
        wk = self.workGroup
        x = float(self.currentRow.x)
        y = float(self.currentRow.y)
        z = float(self.currentRow.z)
        w = float(self.currentRow.w)
        P = [x,y,z,w]
        wk.viewer.AddMarkerPoint(P)
        wk.Refresh()

    def OnRightMouseClick(self, event):
        ### 2. Launcher creates wxMenu. ###
        menu = wx.Menu()
        for (id,title) in list(self.menu_title_by_id.items()):
            ### 3. Launcher packs menu with Append. ###
            toAppend = True
            menu.Append( id, title )
            ### 4. Launcher registers menu handlers with EVT_MENU, on the menu. ###
            wx.EVT_MENU( menu, id, self.MenuSelectionCb)
        ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        self.PopupMenu( menu)
        menu.Destroy() # destroy to avoid mem leak

    def MenuSelectionCb( self, event ):
        # do something
        operation = self.menu_title_by_id[ event.GetId() ]
        if operation == "Edit":
            self.editPoint()
            self.refreshList()
        if operation == "Select":
            self.toSelectedPoint()
            self.refreshList()
        if operation == "Mark":
            self.toMarkerPoint()
            self.refreshList()

########################################################################

