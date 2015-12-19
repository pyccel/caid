# -*- coding: UTF-8 -*-
import wx
from geometry import geometry
from caid.cad_geometry import cad_geometry
from viewer import Viewer
from numpy import pi, linspace
import numpy as np

class ClassActions(object):
    # parent is the inspector
    # parentPanel is rightPanel of inspector
    # parentBox is rightBox
    def __init__(self, parent, parentPanel, parentBox, list_buttonsInfo,
                 backButton=False):
        self.parent     = parent
        self.parentPanel= parentPanel
        self.parentBox  = parentBox

        if backButton:
            self.BCK_ID = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_OTHER, (16,16))
            self.BackBtn = wx.BitmapButton(parentPanel, id=self.BCK_ID, bitmap=bmp \
                                      , size=(bmp.GetWidth()+10,
                                              bmp.GetHeight()+10))

            self.BackBtn.Bind(wx.EVT_BUTTON, self.OnClick)

        # Button box for actions
        self.Box = wx.BoxSizer(wx.VERTICAL)
        self.Buttons = []

        # add back button
        if backButton:
            self.Buttons.append(self.BackBtn)
            self.Box.Add(self.Buttons[-1], 0, wx.EXPAND, 2)
        for info in list_buttonsInfo:
            btnID  = info[0]
            btnTAG = info[1]
            self.Buttons.append(wx.Button(parentPanel, btnID, btnTAG))
            self.Buttons[-1].Bind(wx.EVT_BUTTON, self.OnClick)
            self.Box.Add(self.Buttons[-1], 0, wx.EXPAND, 2)

        self.parentBox.Add(self.Box, 0, wx.EXPAND)

    def Hide(self):
        self.parentBox.Hide(self.Box)

    def Show(self):
        self.parentBox.Show(self.Box)

    def OnClick(self, event):
        pass

class ObjectClassActions(ClassActions):
    def __init__(self, *args, **kwargs):
        ClassActions.__init__(self, *args, **kwargs)
        self.patch = True

    def asPatch(self):
        self.patch = True

    def asGeometry(self):
        self.patch = False

class UndoAction(object):
    def __init__(self, wk, Item, new \
                 , old=None \
                , parent=None \
                 , parentItem=None):
        self._wk  = wk
        self._new = new
        self._Item = Item
        self._old = old
        self._parent = parent
        self._parentItem = parentItem

    @property
    def wk(self):
        return self._wk

    @property
    def new(self):
        return self._new

    @property
    def old(self):
        return self._old

    @property
    def Item(self):
        return self._Item

    @property
    def parent(self):
        return self._parent

    @property
    def parentItem(self):
        return self._parentItem

    def undo(self):
        pass

    def redo(self):
        pass

class UndoAddGeometry(UndoAction):
    def __init__(self, wk, Item, new):
        UndoAction.__init__(self, wk, Item, new)
        self._index = wk.list_geo.index(new)

    @property
    def index(self):
        return self._index

    def undo(self):
        self.wk.remove_geometry(self.Item, self.new, activeUndo=False)

    def redo(self):
        self.wk.add_geometry(self.new, activeUndo=False)

class UndoRemoveGeometry(UndoAction):
    def __init__(self, wk, Item, new):
        UndoAction.__init__(self, wk, Item, new)
        self._index = wk.list_geo.index(new)

    @property
    def index(self):
        return self._index

    def undo(self):
        self._Item = self.wk.add_geometry(self.new, activeUndo=False)

    def redo(self):
        self.wk.remove_geometry(self.Item, self.new, activeUndo=False)

#class UndoRemoveGeometry(UndoAction):
#    def __init__(self, wk, Item, new, old=None):
#        UndoAction.__init__(self, wk, Item, new, old=old)
#        self._index = wk.list_geo.index(new)
#
#    @property
#    def index(self):
#        return self._index
#
#    def undo(self):
#        if self.old is None:
#            self.wk.remove_geometry(self.Item, self.new)
#        else:
#            self.wk.list_geo[self.index] = self.old
#
#    def redo(self):
#        self.wk.add_geometry(self.new)

class UndoAddPatch(UndoAction):
    def __init__(self, wk, Item, new, geo, geoItem):
        UndoAction.__init__(self, wk, Item, new, parent=geo, parentItem=geoItem)

    def undo(self):
        self.wk.remove_patch(self.Item, self.new, geo=self.parent, activeUndo=False)

    def redo(self):
        patchItem = self.wk.add_patch(self.parentItem, self.parent, self.new, activeUndo=False)
        self._Item = patchItem

class UndoRemovePatch(UndoAction):
    def __init__(self, wk, Item, new, geo, geoItem):
        UndoAction.__init__(self, wk, Item, new, parent=geo, parentItem=geoItem)

    def undo(self):
        patchItem = self.wk.add_patch(self.parentItem, self.parent, self.new, activeUndo=False)
        self._Item = patchItem

    def redo(self):
        self.wk.remove_patch(self.Item, self.new, geo=self.parent, activeUndo=False)

class UndoModifyPatch(UndoAction):
    def __init__(self, wk, Item, new, old, geo, geoItem):
        UndoAction.__init__(self, wk, Item, new, parent=geo, parentItem=geoItem, old=old)

        self._ini_new = new.copy()
        self._ini_old = old.copy()

    def undo(self):
        self.new.set_points(self._ini_old._array[...,:3])
        self.wk.Refresh(inspector=True)

    def redo(self):
        self.new.set_points(self._ini_new._array[...,:3])
        self.wk.Refresh(inspector=True)
