# -*- coding: UTF-8 -*-
import wx
import os
from geometry import geometry
from caid.cad_geometry import cad_geometry
from viewer import Viewer
from numpy import pi, linspace
import numpy as np
from classActions import *
from objectActions import *

class GeometryActions(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        # ...
        self.NEW_ID = wx.NewId() ; NEW_TAG = "New"
        self.DEL_ID = wx.NewId() ; DEL_TAG = "Delete"
        self.DUP_ID = wx.NewId() ; DUP_TAG = "Duplicate"
        self.ADD_ID = wx.NewId() ; ADD_TAG = "Add Patch"
        self.PLJ_ID = wx.NewId() ; PLJ_TAG = "Plot Jacobian"
        self.PLM_ID = wx.NewId() ; PLM_TAG = "Plot Mesh"
        self.PEX_ID = wx.NewId() ; PEX_TAG = "Polar Extrude"
        self.EDT_ID = wx.NewId() ; EDT_TAG = "Edit"
        self.TRS_ID = wx.NewId() ; TRS_TAG = "Translate"
        self.ROT_ID = wx.NewId() ; ROT_TAG = "Rotate"
        self.SCL_ID = wx.NewId() ; SCL_TAG = "Scale"
        self.REF_ID = wx.NewId() ; REF_TAG = "Refine"
        self.IMP_ID = wx.NewId() ; IMP_TAG = "Import"
        self.EXP_ID = wx.NewId() ; EXP_TAG = "Export"
        self.EXD_ID = wx.NewId() ; EXD_TAG = "Expand"
        self.T5P_ID = wx.NewId() ; T5P_TAG = "To 5 Patchs"
        self.REI_ID = wx.NewId() ; REI_TAG = "Reset Info"
        self.UPI_ID = wx.NewId() ; UPI_TAG = "Update Info"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.NEW_ID, NEW_TAG])
        list_buttonsInfo.append([self.DEL_ID, DEL_TAG])
        list_buttonsInfo.append([self.DUP_ID, DUP_TAG])
        list_buttonsInfo.append([self.ADD_ID, ADD_TAG])
        list_buttonsInfo.append([self.PLJ_ID, PLJ_TAG])
        list_buttonsInfo.append([self.PLM_ID, PLM_TAG])
        list_buttonsInfo.append([self.PEX_ID, PEX_TAG])
        list_buttonsInfo.append([self.EDT_ID, EDT_TAG])
        list_buttonsInfo.append([self.TRS_ID, TRS_TAG])
        list_buttonsInfo.append([self.ROT_ID, ROT_TAG])
        list_buttonsInfo.append([self.SCL_ID, SCL_TAG])
        list_buttonsInfo.append([self.REF_ID, REF_TAG])
        list_buttonsInfo.append([self.IMP_ID, IMP_TAG])
        list_buttonsInfo.append([self.EXP_ID, EXP_TAG])
        list_buttonsInfo.append([self.EXD_ID, EXD_TAG])
        list_buttonsInfo.append([self.T5P_ID, T5P_TAG])
        list_buttonsInfo.append([self.REI_ID, REI_TAG])
        list_buttonsInfo.append([self.UPI_ID, UPI_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox, list_buttonsInfo)

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.NEW_ID:
            self.parent.ShowAction(self.parent.geometryActionsNew)
        if ID == self.ADD_ID:
            self.parent.ShowAction(self.parent.geometryActionsAdd)
        if ID == self.DEL_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            geo_id = wk.list_geo.index(geo)
            wk.remove_geometry(geoItem, geo)

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... delete geometry")
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("geoItem = geo.treeItem")
                macro_script.append("wk.remove_geometry(geoItem, geo)")
                macro_script.append("# ...")

        if ID == self.DUP_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup

            geo = wk.inspector.currentGeometry
            geo_new = wk.inspector.currentGeometry.copy()
            geo_newItem = wk.add_geometry(geo_new)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... copy geometry")
                geo_id = wk.list_geo.index(geo)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("_geo = geo.copy()")
                macro_script.append("wk.add_geometry(geometry(_geo))")
                macro_script.append("# ...")

        if ID == self.PLJ_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            import matplotlib.pyplot as plt
            try:
                MeshResolution = geo.list_patchInfo[0].steps[0]
            except:
                MeshResolution = 10
            geo.plotJacobians(MeshResolution=MeshResolution)
            plt.colorbar()
            plt.show()
        if ID == self.PLM_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            import matplotlib.pyplot as plt
            MeshResolution = geo.list_patchInfo[0].steps[0]
            geo.plotMesh(MeshResolution=MeshResolution)
            plt.show()
        if ID == self.EXP_ID:
            from global_vars import CAIDwildcard
            # Create a save file dialog
            dialog = wx.FileDialog ( None, style = wx.SAVE | wx.OVERWRITE_PROMPT
                                   , wildcard=CAIDwildcard)
            # Show the dialog and get user input
            if dialog.ShowModal() == wx.ID_OK:
                ls_file = dialog.GetPath()
                wk = self.parent.WorkGroup
                geo = wk.inspector.currentGeometry
                geo.save(ls_file)

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... export geometry")
                    geo_id = wk.list_geo.index(geo)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("filename = \""+ls_file+"\"")
                    macro_script.append("geo.save(filename)")
                    macro_script.append("# ...")

            # Destroy the dialog
            dialog.Destroy()
        if ID == self.EDT_ID:
            from Editor import Editor
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            edt = Editor(wk.parent, -1, 'Editor')
            filename = edt.DoOpenGeometryAsFile(geo)
            # wait until the editor is closed
            createNewGeo = False
            while edt:
                if edt.modify:
                    createNewGeo = True
                wx.MilliSleep(10)
                wx.GetApp().Yield()
            if createNewGeo:
                newgeo = cad_geometry(filename)
                geo_new = geometry(newgeo)
                geo_newItem = wk.add_geometry(geo_new)
            try:
                os.remove(filename)
            except:
                pass
        if ID == self.TRS_ID:
            self.parent.objectActionsTranslate.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsTranslate)
        if ID == self.ROT_ID:
            self.parent.objectActionsRotate.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsRotate)
        if ID == self.SCL_ID:
            self.parent.objectActionsScale.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsScale)
        if ID == self.REF_ID:
            self.parent.ShowAction(self.parent.geometryActionsRefine)
        if ID == self.PEX_ID:
            self.parent.objectActionsPolarExtrude.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsPolarExtrude)
        if ID == self.EXD_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            list_geo = geo.expand()
            for _geo in list_geo:
                geo_new = geometry(_geo)
                geo_newItem = wk.add_geometry(geo_new)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... expand geometry")
                geo_id = wk.list_geo.index(geo)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("list_geo = geo.expand()")
                macro_script.append("for _geo in list_geo:")
                macro_script.append("\twk.add_geometry(geometry(_geo))")
                macro_script.append("# ...")

        if ID == self.IMP_ID:
            # Create an open file dialog
            dialog = wx.FileDialog(None, style = wx.OPEN)
            # Show the dialog and get user input
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetPath()
                # TODO update recent files
#                self.UpdateRecentFiles(filename)
                geo = cad_geometry(filename)
                wk = self.parent.WorkGroup
                wk.add_geometry(geometry(geo))
                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... import geometry")
                    macro_script.append("filename = \""+filename+"\"")
                    macro_script.append("_geo = cad_geometry(filename)")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("# ...")
            # Destroy the dialog
            dialog.Destroy()
        if ID == self.REI_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            geo.initialize_info()
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... initialize info geometry")
                geo_id = wk.list_geo.index(geo)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("geo.initialize_info()")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")
            wk.Refresh(inspector=True)
        if ID == self.UPI_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            geo.update()
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... update geometry")
                geo_id = wk.list_geo.index(geo)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("geo.update()")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")
            wk.Refresh(inspector=True)
        if ID == self.T5P_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            item = wk.inspector.tree.GetSelection()
            geo_bnd = wk.inspector.tree.GetItemData(item)
            face = geo_bnd.face
            faceItem = wk.inspector.tree.GetItemParent(item)
            patchItem = wk.inspector.tree.GetItemParent(faceItem)
            geoItem = wk.inspector.tree.GetItemParent(patchItem)
            geo = wk.inspector.tree.GetItemData(geoItem)
            _geo = cad_geometry()
            _geo.append(geo[0])
            geo_new = geometry(_geo.to5patchs(face))
            geo_newItem = wk.add_geometry(geo_new)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... to-5-patchs geometry")
                geo_id = wk.list_geo.index(geo)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("_geo = cad_geometry()")
                macro_script.append("_geo.append(geo[0])")
                macro_script.append("face = "+str(face))
                macro_script.append("_geo = _geo.to5patchs(face)")
                macro_script.append("wk.add_geometry(geometry(_geo))")
                macro_script.append("wk.Refresh()")
                macro_script.append("# ...")
            wk.Refresh()

class GeometryActionsNew(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.EMP_ID = wx.NewId() ; EMP_TAG = "Empty"
        self.LIN_ID = wx.NewId() ; LIN_TAG = "Line"
        self.LNR_ID = wx.NewId() ; LNR_TAG = "Linear"
        self.ARC_ID = wx.NewId() ; ARC_TAG = "Arc"
        self.CRV_ID = wx.NewId() ; CRV_TAG = "Curve"
        self.SQR_ID = wx.NewId() ; SQR_TAG = "Square"
        self.BIL_ID = wx.NewId() ; BIL_TAG = "Bilinear"
        self.CRC_ID = wx.NewId() ; CRC_TAG = "Circle"
        self.QCR_ID = wx.NewId() ; QCR_TAG = "Quart-Circle"
        self.ANL_ID = wx.NewId() ; ANL_TAG = "Annulus"
        self.CR5_ID = wx.NewId() ; CR5_TAG = "Circle 5 patchs"
        self.PC5_ID = wx.NewId() ; PC5_TAG = "Pinched Circle 5 patchs"
        self.TRL_ID = wx.NewId() ; TRL_TAG = "Triangle"
        self.CUB_ID = wx.NewId() ; CUB_TAG = "Cube"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.EMP_ID, EMP_TAG])
        list_buttonsInfo.append([self.LIN_ID, LIN_TAG])
        list_buttonsInfo.append([self.LNR_ID, LNR_TAG])
        list_buttonsInfo.append([self.ARC_ID, ARC_TAG])
        list_buttonsInfo.append([self.CRV_ID, CRV_TAG])
        list_buttonsInfo.append([self.SQR_ID, SQR_TAG])
        list_buttonsInfo.append([self.BIL_ID, BIL_TAG])
        list_buttonsInfo.append([self.CRC_ID, CRC_TAG])
        list_buttonsInfo.append([self.QCR_ID, QCR_TAG])
        list_buttonsInfo.append([self.ANL_ID, ANL_TAG])
        list_buttonsInfo.append([self.CR5_ID, CR5_TAG])
        list_buttonsInfo.append([self.PC5_ID, PC5_TAG])
        list_buttonsInfo.append([self.TRL_ID, TRL_TAG])
        list_buttonsInfo.append([self.CUB_ID, CUB_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

    def OnClick(self, event):
        # inspector = self.parent
        wk = self.parent.WorkGroup

        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.EMP_ID:
            geo = cad_geometry()
            wk.add_geometry(geometry(geo))
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... create object")
                macro_script.append("_geo = cad_geometry()")
                macro_script.append("wk.add_geometry(geometry(_geo))")
                macro_script.append("# ...")
        if ID == self.LIN_ID:
            from caid.cad_geometry import line as domain
            geo = domain()
            wk.add_geometry(geometry(geo))
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... create object")
                macro_script.append("_geo = line()")
                macro_script.append("wk.add_geometry(geometry(_geo))")
                macro_script.append("# ...")
        if ID == self.LNR_ID:
            self.parent.objectActionsCreateLinear.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsCreateLinear)
        if ID == self.ARC_ID:
            self.parent.objectActionsCreateArc.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsCreateArc)
        if ID == self.CRV_ID:
            self.parent.objectActionsCurve.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsCurve)
        if ID == self.SQR_ID:
            from caid.cad_geometry import square as domain
            geo = domain()
            wk.add_geometry(geometry(geo))
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... create object")
                macro_script.append("_geo = square()")
                macro_script.append("wk.add_geometry(geometry(_geo))")
                macro_script.append("# ...")
        if ID == self.BIL_ID:
            self.parent.objectActionsCreateBilinear.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsCreateBilinear)
        if ID == self.CRC_ID:
            self.parent.objectActionsCreateCircle.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsCreateCircle)
        if ID == self.QCR_ID:
            self.parent.objectActionsCreateQuartCircle.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsCreateQuartCircle)
        if ID == self.ANL_ID:
            self.parent.objectActionsCreateAnnulus.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsCreateAnnulus)
        if ID == self.CR5_ID:
            self.parent.objectActionsCreateCircle_5mp.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsCreateCircle_5mp)
        if ID == self.PC5_ID:
            self.parent.objectActionsCreatePinched_Circle_5mp.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsCreatePinched_Circle_5mp)
        if ID == self.TRL_ID:
            self.parent.objectActionsCreateTriangle.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsCreateTriangle)
        if ID == self.CUB_ID:
#            from caid.cad_geometry import cube as domain
            from caid.cad_geometry import trilinear as domain
            geo = domain()
            wk.add_geometry(geometry(geo))

class GeometryActionsAdd(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.LIN_ID = wx.NewId() ; LIN_TAG = "Line"
        self.LNR_ID = wx.NewId() ; LNR_TAG = "Linear"
        self.ARC_ID = wx.NewId() ; ARC_TAG = "Arc"
        self.CRV_ID = wx.NewId() ; CRV_TAG = "Curve"
        self.SQR_ID = wx.NewId() ; SQR_TAG = "Square"
        self.BIL_ID = wx.NewId() ; BIL_TAG = "Bilinear"
        self.CRC_ID = wx.NewId() ; CRC_TAG = "Circle"
        self.QCR_ID = wx.NewId() ; QCR_TAG = "Quart-Circle"
        self.ANL_ID = wx.NewId() ; ANL_TAG = "Annulus"
        self.CR5_ID = wx.NewId() ; CR5_TAG = "Circle 5 patchs"
        self.PC5_ID = wx.NewId() ; PC5_TAG = "Pinched Circle 5 patchs"
        self.TRL_ID = wx.NewId() ; TRL_TAG = "Triangle"
        self.CUB_ID = wx.NewId() ; CUB_TAG = "Cube"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.LIN_ID, LIN_TAG])
        list_buttonsInfo.append([self.LNR_ID, LNR_TAG])
        list_buttonsInfo.append([self.ARC_ID, ARC_TAG])
        list_buttonsInfo.append([self.CRV_ID, CRV_TAG])
        list_buttonsInfo.append([self.SQR_ID, SQR_TAG])
        list_buttonsInfo.append([self.BIL_ID, BIL_TAG])
        list_buttonsInfo.append([self.CRC_ID, CRC_TAG])
        list_buttonsInfo.append([self.QCR_ID, QCR_TAG])
        list_buttonsInfo.append([self.ANL_ID, ANL_TAG])
        list_buttonsInfo.append([self.CR5_ID, CR5_TAG])
        list_buttonsInfo.append([self.PC5_ID, PC5_TAG])
        list_buttonsInfo.append([self.TRL_ID, TRL_TAG])
        list_buttonsInfo.append([self.CUB_ID, CUB_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox, list_buttonsInfo, backButton=True)

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)

        if ID == self.LNR_ID:
            self.parent.objectActionsCreateLinear.asPatch()
            self.parent.ShowAction(self.parent.objectActionsCreateLinear)
        if ID == self.ARC_ID:
            self.parent.objectActionsCreateArc.asPatch()
            self.parent.ShowAction(self.parent.objectActionsCreateArc)
        if ID == self.CRV_ID:
            self.parent.objectActionsCurve.asPatch()
            self.parent.ShowAction(self.parent.objectActionsCurve)
        if ID == self.BIL_ID:
            self.parent.objectActionsCreateBilinear.asPatch()
            self.parent.ShowAction(self.parent.objectActionsCreateBilinear)
        if ID == self.CRC_ID:
            self.parent.objectActionsCreateCircle.asPatch()
            self.parent.ShowAction(self.parent.objectActionsCreateCircle)
        if ID == self.QCR_ID:
            self.parent.objectActionsCreateQuartCircle.asPatch()
            self.parent.ShowAction(self.parent.objectActionsCreateQuartCircle)
        if ID == self.ANL_ID:
            self.parent.objectActionsCreateAnnulus.asPatch()
            self.parent.ShowAction(self.parent.objectActionsCreateAnnulus)
        if ID == self.CR5_ID:
            self.parent.objectActionsCreateCircle_5mp.asPatch()
            self.parent.ShowAction(self.parent.objectActionsCreateCircle_5mp)
        if ID == self.PC5_ID:
            self.parent.objectActionsCreatePinched_Circle_5mp.asPatch()
            self.parent.ShowAction(self.parent.objectActionsCreatePinched_Circle_5mp)
        if ID == self.TRL_ID:
            self.parent.objectActionsCreateTriangle.asGeometry()
            self.parent.ShowAction(self.parent.objectActionsCreateTriangle)

        if ID == self.LIN_ID:
            from caid.cad_geometry import line as domain
            nrb = domain()[0]
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            wk.add_patch(geoItem, geo, nrb)

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... add line patch")
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentPatchItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo = wk.inspector.tree.GetItemData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("cad_nrb = line()[0]")
                macro_script.append("geoItem = geo.treeItem")
                macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")

            wk.Refresh(inspector=True)

        if ID == self.SQR_ID:
            from caid.cad_geometry import square as domain
            nrb = domain()[0]
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            wk.add_patch(geoItem, geo, nrb)

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... add line patch")
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentPatchItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo = wk.inspector.tree.GetItemData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("cad_nrb = square()[0]")
                macro_script.append("geoItem = geo.treeItem")
                macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")

        if ID == self.CUB_ID:
#            from caid.cad_geometry import cube as domain
            from caid.cad_geometry import trilinear as domain
            nrb = domain()[0]
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            wk.add_patch(geoItem, geo, nrb)

            wk.Refresh(inspector=True)

class GeometryActionsRefine(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        # if True => create arc as patch
        # if False => create arc as geometry
        self.patch = True

        self.n  =  np.zeros(3,dtype=np.int)
        self.p  =  np.zeros(3,dtype=np.int)
        self.m  =  np.ones(3,dtype=np.int)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "n")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrln1Id = wx.NewId()
        self.txtCtrln1 = wx.TextCtrl(parentPanel, self.txtCtrln1Id, size=(50,25))
        self.txtCtrln1.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrln1.SetValue(str(self.n[0]))
        hbox.Add(self.txtCtrln1, border=5)

        self.spinn1Id = wx.NewId()
        self.spinn1 = wx.SpinButton(parentPanel, self.spinn1Id, style=wx.SP_VERTICAL)
        self.spinn1.Bind(wx.EVT_SPIN, self.OnSpin)
        self.spinn1.SetRange(0, 512)
        self.spinn1.SetValue(0)
        hbox.Add(self.spinn1, border=5)

        self.txtCtrln2Id = wx.NewId()
        self.txtCtrln2 = wx.TextCtrl(parentPanel, self.txtCtrln2Id, size=(50,25))
        self.txtCtrln2.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrln2.SetValue(str(self.n[1]))
        hbox.Add(self.txtCtrln2, border=5)

        self.spinn2Id = wx.NewId()
        self.spinn2 = wx.SpinButton(parentPanel, self.spinn2Id, style=wx.SP_VERTICAL)
        self.spinn2.Bind(wx.EVT_SPIN, self.OnSpin)
        self.spinn2.SetRange(0, 512)
        self.spinn2.SetValue(0)
        hbox.Add(self.spinn2, border=5)

        self.txtCtrln3Id = wx.NewId()
        self.txtCtrln3 = wx.TextCtrl(parentPanel, self.txtCtrln3Id, size=(50,25))
        self.txtCtrln3.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrln3.SetValue(str(self.n[2]))
        hbox.Add(self.txtCtrln3, border=5)

        self.spinn3Id = wx.NewId()
        self.spinn3 = wx.SpinButton(parentPanel, self.spinn3Id, style=wx.SP_VERTICAL)
        self.spinn3.Bind(wx.EVT_SPIN, self.OnSpin)
        self.spinn3.SetRange(0, 512)
        self.spinn3.SetValue(0)
        hbox.Add(self.spinn3, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "p")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlp1Id = wx.NewId()
        self.txtCtrlp1 = wx.TextCtrl(parentPanel, self.txtCtrlp1Id, size=(50,25))
        self.txtCtrlp1.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlp1.SetValue(str(self.p[0]))
        hbox.Add(self.txtCtrlp1, border=5)

        self.spinp1Id = wx.NewId()
        self.spinp1 = wx.SpinButton(parentPanel, self.spinp1Id, style=wx.SP_VERTICAL)
        self.spinp1.Bind(wx.EVT_SPIN, self.OnSpin)
        self.spinp1.SetRange(0, 25)
        self.spinp1.SetValue(0)
        hbox.Add(self.spinp1, border=5)

        self.txtCtrlp2Id = wx.NewId()
        self.txtCtrlp2 = wx.TextCtrl(parentPanel, self.txtCtrlp2Id, size=(50,25))
        self.txtCtrlp2.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlp2.SetValue(str(self.p[1]))
        hbox.Add(self.txtCtrlp2, border=5)

        self.spinp2Id = wx.NewId()
        self.spinp2 = wx.SpinButton(parentPanel, self.spinp2Id, style=wx.SP_VERTICAL)
        self.spinp2.Bind(wx.EVT_SPIN, self.OnSpin)
        self.spinp2.SetRange(0, 25)
        self.spinp2.SetValue(0)
        hbox.Add(self.spinp2, border=5)

        self.txtCtrlp3Id = wx.NewId()
        self.txtCtrlp3 = wx.TextCtrl(parentPanel, self.txtCtrlp3Id, size=(50,25))
        self.txtCtrlp3.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlp3.SetValue(str(self.p[2]))
        hbox.Add(self.txtCtrlp3, border=5)

        self.spinp3Id = wx.NewId()
        self.spinp3 = wx.SpinButton(parentPanel, self.spinp3Id, style=wx.SP_VERTICAL)
        self.spinp3.Bind(wx.EVT_SPIN, self.OnSpin)
        self.spinp3.SetRange(0, 25)
        self.spinp3.SetValue(0)
        hbox.Add(self.spinp3, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "m")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlm1Id = wx.NewId()
        self.txtCtrlm1 = wx.TextCtrl(parentPanel, self.txtCtrlm1Id, size=(50,25))
        self.txtCtrlm1.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlm1.SetValue(str(self.m[0]))
        hbox.Add(self.txtCtrlm1, border=5)

        self.spinm1Id = wx.NewId()
        self.spinm1 = wx.SpinButton(parentPanel, self.spinm1Id, style=wx.SP_VERTICAL)
        self.spinm1.Bind(wx.EVT_SPIN, self.OnSpin)
        self.spinm1.SetRange(0, 25)
        self.spinm1.SetValue(self.m[0])
        hbox.Add(self.spinm1, border=5)

        self.txtCtrlm2Id = wx.NewId()
        self.txtCtrlm2 = wx.TextCtrl(parentPanel, self.txtCtrlm2Id, size=(50,25))
        self.txtCtrlm2.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlm2.SetValue(str(self.m[1]))
        hbox.Add(self.txtCtrlm2, border=5)

        self.spinm2Id = wx.NewId()
        self.spinm2 = wx.SpinButton(parentPanel, self.spinm2Id, style=wx.SP_VERTICAL)
        self.spinm2.Bind(wx.EVT_SPIN, self.OnSpin)
        self.spinm2.SetRange(0, 25)
        self.spinm2.SetValue(self.m[1])
        hbox.Add(self.spinm2, border=5)

        self.txtCtrlm3Id = wx.NewId()
        self.txtCtrlm3 = wx.TextCtrl(parentPanel, self.txtCtrlm3Id, size=(50,25))
        self.txtCtrlm3.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlm3.SetValue(str(self.m[2]))
        hbox.Add(self.txtCtrlm3, border=5)

        self.spinm3Id = wx.NewId()
        self.spinm3 = wx.SpinButton(parentPanel, self.spinm3Id, style=wx.SP_VERTICAL)
        self.spinm3.Bind(wx.EVT_SPIN, self.OnSpin)
        self.spinm3.SetRange(0, 25)
        self.spinm3.SetValue(self.m[2])
        hbox.Add(self.spinm3, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

    def Show(self):
        ClassActions.Show(self)
        wk = self.parent.WorkGroup
        geo = wk.inspector.currentGeometry
        if geo.dim == 1:
            self.txtCtrln1.Show()
            self.spinn1.Show()

            self.txtCtrln2.Hide()
            self.spinn2.Hide()

            self.txtCtrln3.Hide()
            self.spinn3.Hide()

            self.txtCtrlp1.Show()
            self.spinp1.Show()

            self.txtCtrlp2.Hide()
            self.spinp2.Hide()

            self.txtCtrlp3.Hide()
            self.spinp3.Hide()

            self.txtCtrlm1.Show()
            self.spinm1.Show()

            self.txtCtrlm2.Hide()
            self.spinm2.Hide()

            self.txtCtrlm3.Hide()
            self.spinm3.Hide()

        if geo.dim == 2:
            self.txtCtrln1.Show()
            self.spinn1.Show()

            self.txtCtrln2.Show()
            self.spinn2.Show()

            self.txtCtrln3.Hide()
            self.spinn3.Hide()

            self.txtCtrlp1.Show()
            self.spinp1.Show()

            self.txtCtrlp2.Show()
            self.spinp2.Show()

            self.txtCtrlp3.Hide()
            self.spinp3.Hide()

            self.txtCtrlm1.Show()
            self.spinm1.Show()

            self.txtCtrlm2.Show()
            self.spinm2.Show()

            self.txtCtrlm3.Hide()
            self.spinm3.Hide()

    def Hide(self):
        self.txtCtrln1.Hide()
        self.spinn1.Hide()

        self.txtCtrln2.Hide()
        self.spinn2.Hide()

        self.txtCtrln3.Hide()
        self.spinn3.Hide()

        self.txtCtrlp1.Hide()
        self.spinp1.Hide()

        self.txtCtrlp2.Hide()
        self.spinp2.Hide()

        self.txtCtrlp3.Hide()
        self.spinp3.Hide()

        self.txtCtrlm1.Hide()
        self.spinm1.Hide()

        self.txtCtrlm2.Hide()
        self.spinm2.Hide()

        self.txtCtrlm3.Hide()
        self.spinm3.Hide()

        ClassActions.Hide(self)

    def asPatch(self):
        self.patch = True
        self.HideAttributs()

    def asGeometry(self):
        self.patch = False
        self.HideAttributs()

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            geo = wk.inspector.currentGeometry
            geoItem = wk.inspector.currentGeometryItem
            _geo = cad_geometry()
            for nrb in geo:
                geo_t = cad_geometry()
                geo_t.append(nrb)

                # ... refinement
                list_t = None
                if self.n.sum() > 0:
                    list_t = []
                    for axis in range(0,nrb.dim):
                        ub = nrb.knots[axis][0]
                        ue = nrb.knots[axis][-1]
                        t = []
                        if self.n[axis] > 0:
                            t = np.linspace(ub,ue,self.n[axis]+2)[1:-1]
                        list_t.append(t)

                list_p = None
                if self.p.sum() > 0:
                    list_p = []
                    for axis in range(0,nrb.dim):
                        list_p.append(np.max(self.p[axis] - nrb.degree[axis], 0))

                list_m = None
                if self.m.sum() > 0:
                    list_m = []
                    for axis in range(0,nrb.dim):
                        list_m.append(self.m[axis])

                geo_t.refine(list_t=list_t, list_p=list_p, list_m=list_m)
                _geo.append(geo_t[0])

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... refine geometry")
                    macro_script.append("_geo = cad_geometry()")

                    geo_id = wk.list_geo.index(geo)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("for nrb in geo:")
                    macro_script.append("\tgeo_t = cad_geometry()")
                    macro_script.append("\tgeo_t.append(nrb)")

                    str_list_t = [list(ts) for ts in list_t]
                    macro_script.append("\tlist_t = "+ str(str_list_t))
                    macro_script.append("\tlist_p = "+ str(list_p))
                    macro_script.append("\tlist_m = "+ str(list_m))
                    macro_script.append("\tgeo_t.refine(list_t=list_t, list_p=list_p, list_m=list_m)")
                    macro_script.append("\t_geo.append(geo_t[0])")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("# ...")
            # ...

            _geo.set_internal_faces(geo.internal_faces)
            _geo.set_external_faces(geo.external_faces)
            _geo.set_connectivity(geo.connectivity)

            geo_new = geometry(_geo)
            geo_newItem = wk.add_geometry(geo_new)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrln1Id:
                self.n[0] = int(event.GetString())
            if event.GetId() == self.txtCtrln2Id:
                self.n[1] = int(event.GetString())
            if event.GetId() == self.txtCtrln3Id:
                self.n[2] = int(event.GetString())

            if event.GetId() == self.txtCtrlp1Id:
                self.p[0] = int(event.GetString())
            if event.GetId() == self.txtCtrlp2Id:
                self.p[1] = int(event.GetString())
            if event.GetId() == self.txtCtrlp3Id:
                self.p[2] = int(event.GetString())

            if event.GetId() == self.txtCtrlm1Id:
                self.m[0] = int(event.GetString())
            if event.GetId() == self.txtCtrlm2Id:
                self.m[1] = int(event.GetString())
            if event.GetId() == self.txtCtrlm3Id:
                self.m[2] = int(event.GetString())
        except:
            pass

    def OnSpin(self, event):
        if event.GetId() == self.spinn1Id:
            self.txtCtrln1.SetValue(str(event.GetPosition()))
        if event.GetId() == self.spinn2Id:
            self.txtCtrln2.SetValue(str(event.GetPosition()))
        if event.GetId() == self.spinn3Id:
            self.txtCtrln3.SetValue(str(event.GetPosition()))

        if event.GetId() == self.spinp1Id:
            self.txtCtrlp1.SetValue(str(event.GetPosition()))
        if event.GetId() == self.spinp2Id:
            self.txtCtrlp2.SetValue(str(event.GetPosition()))
        if event.GetId() == self.spinp3Id:
            self.txtCtrlp3.SetValue(str(event.GetPosition()))

        if event.GetId() == self.spinm1Id:
            self.txtCtrlm1.SetValue(str(event.GetPosition()))
        if event.GetId() == self.spinm2Id:
            self.txtCtrlm2.SetValue(str(event.GetPosition()))
        if event.GetId() == self.spinm3Id:
            self.txtCtrlm3.SetValue(str(event.GetPosition()))
