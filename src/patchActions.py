# -*- coding: UTF-8 -*-
import wx
from geometry import geometry
from igakit.cad_geometry import cad_geometry, cad_nurbs
from viewer import Viewer
from numpy import pi, linspace, array, zeros
import numpy as np
from classActions import *
from objectActions import *

class PatchActions(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        # ...
        self.DEL_ID = wx.NewId() ; DEL_TAG = "Delete"
        self.PLJ_ID = wx.NewId() ; PLJ_TAG = "Plot Jacobian"
        self.PLM_ID = wx.NewId() ; PLM_TAG = "Plot Mesh"
        self.REF_ID = wx.NewId() ; REF_TAG = "Refine"
        self.ELV_ID = wx.NewId() ; ELV_TAG = "Elevate"
        self.TRS_ID = wx.NewId() ; TRS_TAG = "Translate"
        self.ROT_ID = wx.NewId() ; ROT_TAG = "Rotate"
        self.SCL_ID = wx.NewId() ; SCL_TAG = "Scale"
        self.SWP_ID = wx.NewId() ; SWP_TAG = "Swap"
        self.REV_ID = wx.NewId() ; REV_TAG = "Reverse"
        self.EXC_ID = wx.NewId() ; EXC_TAG = "Extract"
        self.EXR_ID = wx.NewId() ; EXR_TAG = "Extrude"
        self.PEX_ID = wx.NewId() ; PEX_TAG = "Polar Extrude"
        self.SPL_ID = wx.NewId() ; SPL_TAG = "Split"
        self.BEZ_ID = wx.NewId() ; BEZ_TAG = "Bezier"
        self.COO_ID = wx.NewId() ; COO_TAG = "Coons"
        self.TCO_ID = wx.NewId() ; TCO_TAG = "T-Coons"
        self.INT_ID = wx.NewId() ; INT_TAG = "Intersect"
        self.CPT_ID = wx.NewId() ; CPT_TAG = "Clone Points"
        self.CMP_ID = wx.NewId() ; CMP_TAG = "Compat"
        self.JOI_ID = wx.NewId() ; JOI_TAG = "Join"
        self.APX_ID = wx.NewId() ; APX_TAG = "Approximate"
        self.SC1_ID = wx.NewId() ; SC1_TAG = "Stick-C1"
        self.INS_ID = wx.NewId() ; INS_TAG = "Insert"
        self.TRP_ID = wx.NewId() ; TRP_TAG = "Transpose"
        self.RMP_ID = wx.NewId() ; RMP_TAG = "Remap"
        self.REM_ID = wx.NewId() ; REM_TAG = "Remove"
        self.SLC_ID = wx.NewId() ; SLC_TAG = "Slice"
        self.CLP_ID = wx.NewId() ; CLP_TAG = "Clamp"
        self.UCP_ID = wx.NewId() ; UCP_TAG = "Unclamp"
        self.RUL_ID = wx.NewId() ; RUL_TAG = "Ruled"
        self.RVL_ID = wx.NewId() ; RVL_TAG = "Revolve"
        self.SWE_ID = wx.NewId() ; SWE_TAG = "Sweep"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.APX_ID,APX_TAG])
        list_buttonsInfo.append([self.BEZ_ID,BEZ_TAG])
        list_buttonsInfo.append([self.CLP_ID,CLP_TAG])
        list_buttonsInfo.append([self.CMP_ID,CMP_TAG])
        list_buttonsInfo.append([self.CPT_ID,CPT_TAG])
        list_buttonsInfo.append([self.COO_ID,COO_TAG])
        list_buttonsInfo.append([self.DEL_ID,DEL_TAG])
        list_buttonsInfo.append([self.ELV_ID,ELV_TAG])
        list_buttonsInfo.append([self.EXC_ID,EXC_TAG])
        list_buttonsInfo.append([self.EXR_ID,EXR_TAG])
        list_buttonsInfo.append([self.INS_ID,INS_TAG])
        list_buttonsInfo.append([self.INT_ID,INT_TAG])
        list_buttonsInfo.append([self.JOI_ID,JOI_TAG])
        list_buttonsInfo.append([self.PEX_ID,PEX_TAG])
        list_buttonsInfo.append([self.PLJ_ID,PLJ_TAG])
        list_buttonsInfo.append([self.PLM_ID,PLM_TAG])
        list_buttonsInfo.append([self.REF_ID,REF_TAG])
        list_buttonsInfo.append([self.REM_ID,REM_TAG])
        list_buttonsInfo.append([self.REV_ID,REV_TAG])
        list_buttonsInfo.append([self.RMP_ID,RMP_TAG])
        list_buttonsInfo.append([self.ROT_ID,ROT_TAG])
        list_buttonsInfo.append([self.RUL_ID,RUL_TAG])
        list_buttonsInfo.append([self.RVL_ID,RVL_TAG])
        list_buttonsInfo.append([self.SC1_ID,SC1_TAG])
        list_buttonsInfo.append([self.SCL_ID,SCL_TAG])
        list_buttonsInfo.append([self.SLC_ID,SLC_TAG])
        list_buttonsInfo.append([self.SPL_ID,SPL_TAG])
        list_buttonsInfo.append([self.SWE_ID,SWE_TAG])
        list_buttonsInfo.append([self.SWP_ID,SWP_TAG])
        list_buttonsInfo.append([self.TCO_ID,TCO_TAG])
        list_buttonsInfo.append([self.TRS_ID,TRS_TAG])
        list_buttonsInfo.append([self.TRP_ID,TRP_TAG])
        list_buttonsInfo.append([self.UCP_ID,UCP_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo)

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.DEL_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            patch = wk.inspector.currentPatch
            patchItem = wk.inspector.currentPatchItem
            wk.remove_patch(patchItem, patch)
            wk.Refresh()
        if ID == self.PLJ_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            patch = wk.inspector.currentPatch
            import matplotlib.pyplot as plt
            geo = cad_geometry()
            geo.append(patch)
            print "TODO: Enter the Mesh-Resolution"
            geo.plotJacobians(MeshResolution=50)
            plt.colorbar()
            plt.show()
        if ID == self.PLM_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            patch = wk.inspector.currentPatch
            import matplotlib.pyplot as plt
            geo = cad_geometry()
            geo.append(patch)
            print "TODO: Enter the Mesh-Resolution"
            geo.plotMesh(MeshResolution=50)
            plt.show()
        if ID == self.REF_ID:
            self.parent.ShowAction(self.parent.patchActionsRefine)
        if ID == self.ELV_ID:
            self.parent.ShowAction(self.parent.patchActionsElevate)
        if ID == self.TRS_ID:
            self.parent.objectActionsTranslate.asPatch()
            self.parent.ShowAction(self.parent.objectActionsTranslate)
        if ID == self.ROT_ID:
            self.parent.objectActionsRotate.asPatch()
            self.parent.ShowAction(self.parent.objectActionsRotate)
        if ID == self.SCL_ID:
            self.parent.objectActionsScale.asPatch()
            self.parent.ShowAction(self.parent.objectActionsScale)
        if ID == self.SWP_ID:
            self.parent.ShowAction(self.parent.patchActionsSwap)
        if ID == self.REV_ID:
            self.parent.ShowAction(self.parent.patchActionsReverse)
        if ID == self.EXC_ID:
            self.parent.ShowAction(self.parent.patchActionsExtract)
        if ID == self.EXR_ID:
            self.parent.ShowAction(self.parent.patchActionsExtrude)
        if ID == self.TCO_ID:
            self.parent.ShowAction(self.parent.patchActionsTCoons)
        if ID == self.PEX_ID:
            self.parent.objectActionsPolarExtrude.asPatch()
            self.parent.ShowAction(self.parent.objectActionsPolarExtrude)
        if ID == self.SPL_ID:
            self.parent.ShowAction(self.parent.patchActionsSplit)
        if ID == self.RMP_ID:
            self.parent.ShowAction(self.parent.patchActionsRemap)
        if ID == self.REM_ID:
            self.parent.ShowAction(self.parent.patchActionsRemove)
        if ID == self.SLC_ID:
            self.parent.ShowAction(self.parent.patchActionsSlice)
        if ID == self.CLP_ID:
            self.parent.ShowAction(self.parent.patchActionsClamp)
        if ID == self.UCP_ID:
            self.parent.ShowAction(self.parent.patchActionsUnclamp)
        if ID == self.RVL_ID:
            self.parent.ShowAction(self.parent.patchActionsRevolve)
        if ID == self.BEZ_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            patch       = wk.inspector.currentPatch
            patchItem   = wk.inspector.currentPatchItem
            geoItem     = wk.inspector.tree.GetItemParent(patchItem)
            geo         = wk.inspector.tree.GetPyData(geoItem)
            patch_id    = geo.index(patch)

            _geo = cad_geometry()
            _geo.append(geo[patch_id])
            newgeo = _geo.toBezier(0)
            wk.add_geometry(geometry(newgeo))
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... convert to bezier surfaces")
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo     = wk.inspector.tree.GetPyData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("_geo = cad_geometry()")
                macro_script.append("_geo.append(patch)")
                macro_script.append("_geo = _geo.toBezier(0)")
                macro_script.append("wk.add_geometry(geometry(_geo))")
                macro_script.append("wk.Refresh()")
                macro_script.append("# ...")
            wk.Refresh()

        if ID == self.COO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            list_patchs = []
            for item in wk.inspector.tree.selectionsItems:
                patch = wk.inspector.tree.GetPyData(item)
                if patch.dim > 1:
                    print "Coons algorithm only works with curves"
                    return
                list_patchs.append(patch)
            if len(list_patchs) > 4:
                print "Coons algorithm needs 4 curves, but ", len(list_patchs), " curves was given"
                return

            from igakit.cad import coons, coonsInitialize
            c0 = list_patchs[0]
            c1 = list_patchs[1]
            c2 = list_patchs[2]
            c3 = list_patchs[3]
            curves = [[c1,c3],[c0,c2]]
            # make curves compatible (orientation)
            tol = wk.preferences.coons["tol"]
            curves = coonsInitialize(curves, tol=tol)
            # TODO must be set by the user
            nrb = coons(curves, tol=tol)
            cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)

            geo = cad_geometry()
            geo.append(cad_nrb)

            wk.add_geometry(geometry(geo))
            wk.Refresh()
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... coons algorithm")
                list_gp = []
                for item in wk.inspector.tree.selectionsItems:
                    patch   = wk.inspector.tree.GetPyData(item)
                    geoItem = wk.inspector.tree.GetItemParent(item)
                    geo     = wk.inspector.tree.GetPyData(geoItem)
                    list_gp.append([geo, patch])


                for i,gp in enumerate(list_gp):
                    geo = gp[0] ; patch = gp[1]
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("c"+str(i)+" = patch")

                macro_script.append("curves = [[c1,c3],[c0,c2]]")
                macro_script.append("tol = " + str(tol))
                macro_script.append("nrb = coons(curves, tol=tol)")
                macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                macro_script.append("_geo = cad_geometry()")
                macro_script.append("_geo.append(cad_nrb)")
                macro_script.append("wk.add_geometry(geometry(_geo))")
                macro_script.append("wk.Refresh()")
                macro_script.append("# ...")

        if ID == self.INT_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            list_patchs = []
            for item in wk.inspector.tree.selectionsItems:
                patch = wk.inspector.tree.GetPyData(item)
                if patch.dim > 1:
                    print "Intersection algorithm only works with curves"
                    return
                list_patchs.append(patch)
            if len(list_patchs) > 2:
                print "Intersection algorithm needs 2 curves, but "\
                        , len(list_patchs), " curves were given"
                return

            from igakit.cad import intersect_crv
            c0 = list_patchs[0]
            geo0 = cad_geometry()
            geo0.append(c0)

            c1 = list_patchs[1]
            geo1 = cad_geometry()
            geo1.append(c1)

            npts = wk.preferences.intersection["npts"]
            list_P, list_t, list_s, ierr = intersect_crv(c0,c1, npts=npts)

            list_t = np.asarray(list_t)
            list_t.sort()
            axis = 0
            for i,t in enumerate(list_t):
                geo0.split(i,t,axis)

            list_s = np.asarray(list_s)
            list_s.sort()
            axis = 0
            for i,t in enumerate(list_s):
                geo1.split(i,t,axis)

            wk.add_geometry(geometry(geo0))
            wk.add_geometry(geometry(geo1))
            wk.Refresh()

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... intersection algorithm")
                list_gp = []
                for item in wk.inspector.tree.selectionsItems:
                    patch   = wk.inspector.tree.GetPyData(item)
                    geoItem = wk.inspector.tree.GetItemParent(item)
                    geo     = wk.inspector.tree.GetPyData(geoItem)
                    list_gp.append([geo, patch])


                for i,gp in enumerate(list_gp):
                    geo = gp[0] ; patch = gp[1]
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("c"+str(i)+" = patch")

                macro_script.append("npts = " + str(wk.preferences.intersection["npts"]))

                macro_script.append("list_P, list_t, list_s, ierr = intersect_crv(c0,c1, npts=npts)")
                macro_script.append("geo0 = cad_geometry()")
                macro_script.append("geo0.append(c0)")
                macro_script.append("geo1 = cad_geometry()")
                macro_script.append("geo1.append(c1)")

                macro_script.append("list_t = np.asarray(list_t)")
                macro_script.append("list_t.sort()")
                macro_script.append("axis = 0")
                macro_script.append("for i,t in enumerate(list_t):")
                macro_script.append("\tgeo0.split(i,t,axis)")

                macro_script.append("list_s = np.asarray(list_s)")
                macro_script.append("list_s.sort()")
                macro_script.append("axis = 0")
                macro_script.append("for i,t in enumerate(list_s):")
                macro_script.append("\tgeo1.split(i,t,axis)")
                macro_script.append("")

                macro_script.append("wk.add_geometry(geometry(geo0))")
                macro_script.append("wk.add_geometry(geometry(geo1))")
                macro_script.append("wk.Refresh()")
                macro_script.append("# ...")

        if ID == self.RUL_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            list_patchs = []
            for item in wk.inspector.tree.selectionsItems:
                patch = wk.inspector.tree.GetPyData(item)
                if patch.dim > 2:
                    print "Ruled algorithm only works with 2 curves or 2 surfaces"
                    return
                list_patchs.append(patch)
            if len(list_patchs) > 2:
                print "Intersection algorithm needs 2 curves/surfaces, but "\
                        , len(list_patchs), " curves/surfaces were given"
                return

            from igakit.cad import ruled
            nrb0 = list_patchs[0]
            nrb1 = list_patchs[1]

            nrb = ruled(nrb0,nrb1)
            cnrb = cad_nurbs(nrb.knots, nrb.points, weights= nrb.weights)
            geo = cad_geometry()
            geo.append(cnrb)
            wk.add_geometry(geometry(geo))
            wk.Refresh()

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... ruled algorithm")
                list_gp = []
                for item in wk.inspector.tree.selectionsItems:
                    patch   = wk.inspector.tree.GetPyData(item)
                    geoItem = wk.inspector.tree.GetItemParent(item)
                    geo     = wk.inspector.tree.GetPyData(geoItem)
                    list_gp.append([geo, patch])


                for i,gp in enumerate(list_gp):
                    geo = gp[0] ; patch = gp[1]
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("c"+str(i)+" = patch")

                macro_script.append("nrb = ruled(c0,c1)")
                macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                macro_script.append("_geo = cad_geometry()")
                macro_script.append("_geo.append(cad_nrb)")
                macro_script.append("wk.add_geometry(geometry(_geo))")
                macro_script.append("wk.Refresh()")
                macro_script.append("# ...")

        if ID == self.SWE_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            list_patchs = []
            for item in wk.inspector.tree.selectionsItems:
                patch = wk.inspector.tree.GetPyData(item)
                if patch.dim > 2:
                    print "Sweep algorithm only works with curves and surfaces"
                    return
                list_patchs.append(patch)
            if len(list_patchs) > 2:
                print "Sweep algorithm needs 2 curves/surfaces, but "\
                        , len(list_patchs), " curves/surfaces were given"
                return

            from igakit.cad import sweep
            nrb0 = list_patchs[0]
            nrb1 = list_patchs[1]

            nrb = sweep(nrb0,nrb1)
            cnrb = cad_nurbs(nrb.knots, nrb.points, weights= nrb.weights)
            geo = cad_geometry()
            geo.append(cnrb)
            wk.add_geometry(geometry(geo))
            wk.Refresh()

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... sweep algorithm")
                list_gp = []
                for item in wk.inspector.tree.selectionsItems:
                    patch   = wk.inspector.tree.GetPyData(item)
                    geoItem = wk.inspector.tree.GetItemParent(item)
                    geo     = wk.inspector.tree.GetPyData(geoItem)
                    list_gp.append([geo, patch])


                for i,gp in enumerate(list_gp):
                    geo = gp[0] ; patch = gp[1]
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("c"+str(i)+" = patch")

                macro_script.append("nrb = sweep(c0,c1)")
                macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                macro_script.append("_geo = cad_geometry()")
                macro_script.append("_geo.append(cad_nrb)")
                macro_script.append("wk.add_geometry(geometry(_geo))")
                macro_script.append("wk.Refresh()")
                macro_script.append("# ...")

        if ID == self.CPT_ID:
            self.parent.ShowAction(self.parent.patchActionsClonePoints)
        if ID == self.CMP_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            list_patchs = []
            for item in wk.inspector.tree.selectionsItems:
                patch = wk.inspector.tree.GetPyData(item)
                list_patchs.append(patch)

            from igakit.cad import compat
            list_nrb = compat(*list_patchs)
            geo = cad_geometry()
            for nrb in list_nrb:
                geo.append(nrb)
            wk.add_geometry(geometry(geo))
            wk.Refresh()

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... compat algorithm")
                list_gp = []
                for item in wk.inspector.tree.selectionsItems:
                    patch   = wk.inspector.tree.GetPyData(item)
                    geoItem = wk.inspector.tree.GetItemParent(item)
                    geo     = wk.inspector.tree.GetPyData(geoItem)
                    list_gp.append([geo, patch])

                macro_script.append("list_patchs = []")
                for i,gp in enumerate(list_gp):
                    geo = gp[0] ; patch = gp[1]
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("list_patchs.append(patch)")

                macro_script.append("list_nrb = compat(*list_patchs)")
                macro_script.append("_geo = cad_geometry()")
                macro_script.append("for nrb in list_nrb:")
                macro_script.append("\t_geo.append(nrb)")
                macro_script.append("wk.add_geometry(geometry(_geo))")
                macro_script.append("wk.Refresh()")
                macro_script.append("# ...")

        if ID == self.JOI_ID:
            self.parent.objectActionsJoin.asPatch()
            self.parent.ShowAction(self.parent.objectActionsJoin)
        if ID == self.APX_ID:
            self.parent.ShowAction(self.parent.patchActionsApproximate)
        if ID == self.SC1_ID:
            self.parent.ShowAction(self.parent.patchActionsStickC1)
        if ID == self.INS_ID:
            self.parent.ShowAction(self.parent.patchActionsInsert)
        if ID == self.TRP_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            patch     = wk.inspector.currentPatch
            patchItem = wk.inspector.currentPatchItem
            patch.transpose()
#            newpatch = patch.copy()
#            geoItem = wk.inspector.tree.GetItemParent(patchItem)
#            geo = wk.inspector.tree.GetPyData(geoItem)
#            wk.add_patch(geoItem, geo, newpatch)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... transpose patch")
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo     = wk.inspector.tree.GetPyData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("patch.transpose()")
                macro_script.append("wk.Refresh()")
                macro_script.append("# ...")
            wk.Refresh()

class PatchActionsTCoons(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.profile = 0

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "Profile")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlProfileId = wx.NewId()
        self.txtCtrlProfile = wx.TextCtrl(parentPanel, self.txtCtrlProfileId, size=(50,25))
        self.txtCtrlProfile.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlProfile.SetValue(str(self.profile))
        hbox.Add(self.txtCtrlProfile, border=5)

        self.Box.Add(hbox, border=5)
        # ...

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            list_patchs = []
            for item in wk.inspector.tree.selectionsItems:
                patch = wk.inspector.tree.GetPyData(item)
                if patch.dim > 1:
                    print "TCoons algorithm only works with curves"
                    return
                list_patchs.append(patch)
            if len(list_patchs) > 3:
                print "TCoons algorithm needs 3 curves, but ", len(list_patchs), " curves was given"
                return

            from igakit.cad_geometry import tcoons
            c0 = list_patchs[0]
            c1 = list_patchs[1]
            c2 = list_patchs[2]
            curves = [c0,c1,c2]
            nrb = tcoons(curves, profile=self.profile)
            cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)

            geo = cad_geometry()
            geo.append(cad_nrb)

            wk.add_geometry(geometry(geo))
            wk.Refresh()

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... tcoons algorithm")
                macro_script.append("# TODO")
                macro_script.append("# ...")

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlProfileId:
                self.profile = int(event.GetString())
        except:
            pass

class PatchActionsClonePoints(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.cbMarkersID = wx.NewId()
        self.cbMarkers = wx.CheckBox(parentPanel,
                              self.cbMarkersID,'Using Markers', (10, 10))
        self.cbMarkers.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cbMarkers.SetValue(False)

        hbox.Add(self.cbMarkers, border=5)

        self.Box.Add(hbox, border=5)
        # ...

#        # ...
#        hbox = wx.BoxSizer(wx.HORIZONTAL)
#
#        self.cbSelectionsID = wx.NewId()
#        self.cbSelections = wx.CheckBox(parentPanel,
#                                self.cbSelectionsID,'Using Selections', (10, 10))
#        self.cbSelections.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
#        self.cbSelections.SetValue(False)
#
#        hbox.Add(self.cbSelections, border=5)
#
#        self.Box.Add(hbox, border=5)
#        # ...

    def Show(self):
        ClassActions.Show(self)

        wk = self.parent.WorkGroup
        if len(wk.viewer.MarkerPoints) > 0:
            self.cbMarkers.SetValue(True)
        else:
            self.cbMarkers.SetValue(False)
#        if len(wk.viewer.list_SelectedPoints) > 0:
#            self.cbSelections.SetValue(True)
#            list_Q = []
#            for selectedPoints in wk.viewer.list_SelectedPoints:
#                list_Q += selectedPoints.points
#            wk.viewer.CleanSelectedPoints()
#        else:
#            self.cbSelections.SetValue(False)

    def EvtCheckBox(self, event):
        return
#        if event.GetId() == self.cbMarkersID:
#            self.cbSelections.SetValue(False)
#        if event.GetId() == self.cbSelectionsID:
#            self.cbMarkers.SetValue(False)

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup

            self._patch     = wk.inspector.currentPatch
            self._patchItem = wk.inspector.currentPatchItem
            self._geoItem   = wk.inspector.tree.GetItemParent(self._patchItem)
            self._geo       = wk.inspector.tree.GetPyData(self._geoItem)

            patch = wk.inspector.currentPatch
            patch_old = patch.copy()

            P = patch.points
            # we suppose that the current selection is the last one done
            selectedPoints  = wk.viewer.list_SelectedPoints[-1]
            list_ijk        = selectedPoints.indices
            if self.cbMarkers.GetValue():
                list_Q = wk.viewer.MarkerPoints
                if patch.dim == 1:
                    for ij,Q in zip(list_ijk, list_Q):
                        P[ij[0],:2] = Q[:2]
                if patch.dim == 2:
                    for ij,Q in zip(list_ijk, list_Q):
                        P[ij[0],ij[1],:2] = Q[:2]
                wk.viewer.CleanMarkerPoints()
                wk.viewer.CleanSelectedPoints()
#            if self.cbSelections.GetValue():
#                list_Q = selectedPoints.points
#                if patch.dim == 1:
#                    for ij,Q in zip(list_ijk, list_Q):
#                        P[ij[0],:2] = Q[:2]
#                if patch.dim == 2:
#                    for ij,Q in zip(list_ijk, list_Q):
#                        P[ij[0],ij[1],:2] = Q[:2]
#                wk.viewer.CleanSelectedPoints()

            patch.set_points(P)
            wk.Refresh(inspector=True)

            # undo action
#            patch     = self._patch
            patchItem = self._patchItem
            geo       = self._geo
            geoItem   = self._geoItem
            old       = patch_old

            undo = UndoModifyPatch(wk, patchItem, patch, old, geo, geoItem)
            wk.appendAction(undo)

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... clone control points")
                macro_script.append("# TODO")
                macro_script.append("# ...")

class PatchActionsSplit(ClassActions):
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

        self.axis  =  0
        self.knot  =  0.

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxisId = wx.NewId()
        self.txtCtrlAxis = wx.TextCtrl(parentPanel, self.txtCtrlAxisId, size=(50,25))
        self.txtCtrlAxis.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAxis.SetValue(str(self.axis))
        hbox.Add(self.txtCtrlAxis, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "knot")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlKnotId = wx.NewId()
        self.txtCtrlKnot = wx.TextCtrl(parentPanel, self.txtCtrlKnotId)
        self.txtCtrlKnot.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlKnot.SetValue(str(self.knot))
        hbox.Add(self.txtCtrlKnot, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

    def asPatch(self):
        self.patch = True

    def asGeometry(self):
        self.patch = False

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.geometryActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            patch = wk.inspector.currentObject
            patchItem = wk.inspector.currentPatchItem
#            geoItem = wk.inspector.tree.GetItemParent(patchItem)
#            geo = wk.inspector.tree.GetPyData(geoItem)
            geo = cad_geometry()
            geo.append(patch)
            i = geo.index(patch)
            t = self.knot
            axis = self.axis
            geo.split(i,t,axis)
            wk.add_geometry(geometry(geo))
            wk.Refresh()

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... split patch")
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentObjectItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo     = wk.inspector.tree.GetPyData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch_id = " + str(i))
                macro_script.append("axis = " + str(axis))
                macro_script.append("t = " + str(t))
                macro_script.append("_geo = cad_geometry()")
                macro_script.append("_geo.append(geo[patch_id])")
                macro_script.append("_geo.split(0,t,axis)")
                macro_script.append("wk.add_geometry(geometry(_geo))")
                macro_script.append("wk.Refresh()")
                macro_script.append("# ...")

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAxisId:
                self.axis = int(event.GetString())
            if event.GetId() == self.txtCtrlKnotId:
                self.knot = float(event.GetString())
        except:
            pass

class PatchActionsSwap(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.axis1  = 0
        self.axis2  = 1

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis-1")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxis1Id = wx.NewId()
        self.txtCtrlAxis1 = wx.TextCtrl(parentPanel, self.txtCtrlAxis1Id)
        self.txtCtrlAxis1.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAxis1.SetValue(str(self.axis1))
        hbox.Add(self.txtCtrlAxis1, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis-2")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxis2Id = wx.NewId()
        self.txtCtrlAxis2 = wx.TextCtrl(parentPanel, self.txtCtrlAxis2Id)
        self.txtCtrlAxis2.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAxis2.SetValue(str(self.axis2))
        hbox.Add(self.txtCtrlAxis2, border=5)

        self.Box.Add(hbox, border=5)
        # ...


    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.patchActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            patch = wk.inspector.currentObject
            patch.swap(self.axis1, self.axis2)

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... swap patch")
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentObjectItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo     = wk.inspector.tree.GetPyData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("axis1 = "+str(self.axis1))
                macro_script.append("axis2 = "+str(self.axis2))
                macro_script.append("patch.swap(axis1, axis2)")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")

            wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAxis1Id:
                self.axis1 = int(event.GetString())
            if event.GetId() == self.txtCtrlAxis2Id:
                self.axis2 = int(event.GetString())
        except:
            pass

class PatchActionsReverse(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.axis1  = 0

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxis1Id = wx.NewId()
        self.txtCtrlAxis1 = wx.TextCtrl(parentPanel, self.txtCtrlAxis1Id)
        self.txtCtrlAxis1.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAxis1.SetValue(str(self.axis1))
        hbox.Add(self.txtCtrlAxis1, border=5)

        self.Box.Add(hbox, border=5)
        # ...


    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.patchActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            patch = wk.inspector.currentObject
            patchItem = wk.inspector.currentObjectItem
            patch.reverse(self.axis1)
            wk.Refresh()

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... reverse patch")
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentObjectItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo     = wk.inspector.tree.GetPyData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("axis1 = " + str(self.axis1))
                macro_script.append("patch.reverse(axis1)")
                macro_script.append("wk.Refresh()")
                macro_script.append("# ...")

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAxis1Id:
                self.axis1 = int(event.GetString())
        except:
            pass

class PatchActionsRefine(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.axis  = 0
        self.n     = 0

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxisId = wx.NewId()
        self.txtCtrlAxis = wx.TextCtrl(parentPanel, self.txtCtrlAxisId, size=(50,25))
        self.txtCtrlAxis.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAxis.SetValue(str(self.axis))
        hbox.Add(self.txtCtrlAxis, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "n")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlnId = wx.NewId()
        self.txtCtrln = wx.TextCtrl(parentPanel, self.txtCtrlnId)
        self.txtCtrln.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrln.SetValue(str(self.n))
        hbox.Add(self.txtCtrln, border=5)

        self.Box.Add(hbox, border=5)
        # ...

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.patchActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            patch = wk.inspector.currentObject
            patchItem = wk.inspector.currentPatchItem
            geoItem = wk.inspector.tree.GetItemParent(patchItem)
            geo = wk.inspector.tree.GetPyData(geoItem)
            nrb = patch.copy()
            ub = nrb.knots[self.axis][0]
            ue = nrb.knots[self.axis][-1]
            t = linspace(ub,ue,self.n+2)[1:-1]
            nrb.refine(self.axis, t)
            cnrb = cad_nurbs(nrb.knots, nrb.points, weights= nrb.weights)
            wk.add_patch(geoItem, geo, cnrb)

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... refine patch")
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentPatchItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo = wk.inspector.tree.GetPyData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("nrb = patch.copy()")
                macro_script.append("axis = "+str(self.axis))
                macro_script.append("t = "+str(list(t)))
                macro_script.append("nrb.refine(axis, t)")
                macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                macro_script.append("geoItem = geo.treeItem")
                macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")

            wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAxisId:
                self.axis = int(event.GetString())
            if event.GetId() == self.txtCtrlnId:
                self.n = int(event.GetString())
        except:
            pass

class PatchActionsElevate(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.axis  = 0
        self.n     = 0

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxisId = wx.NewId()
        self.txtCtrlAxis = wx.TextCtrl(parentPanel, self.txtCtrlAxisId, size=(50,25))
        self.txtCtrlAxis.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAxis.SetValue(str(self.axis))
        hbox.Add(self.txtCtrlAxis, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "n")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlnId = wx.NewId()
        self.txtCtrln = wx.TextCtrl(parentPanel, self.txtCtrlnId)
        self.txtCtrln.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrln.SetValue(str(self.n))
        hbox.Add(self.txtCtrln, border=5)

        self.Box.Add(hbox, border=5)
        # ...

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.patchActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            patch = wk.inspector.currentObject
            patch.elevate(self.axis, times=self.n)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... elevate patch")
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentObjectItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo     = wk.inspector.tree.GetPyData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("axis = " + str(self.axis))
                macro_script.append("times = " + str(self.n))
                macro_script.append("patch.elevate(axis, times=times)")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")
            wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAxisId:
                self.axis = int(event.GetString())
            if event.GetId() == self.txtCtrlnId:
                self.n = int(event.GetString())
        except:
            pass

class PatchActionsExtract(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.face  = 0

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "face")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlFaceId = wx.NewId()
        self.txtCtrlFace = wx.TextCtrl(parentPanel, self.txtCtrlFaceId)
        self.txtCtrlFace.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlFace.SetValue(str(self.face))
        hbox.Add(self.txtCtrlFace, border=10)

        self.Box.Add(hbox, border=5)
        # ...

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.patchActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            patch     = wk.inspector.currentPatch
            patchItem = wk.inspector.currentPatchItem
            geoItem = wk.inspector.tree.GetItemParent(patchItem)
            geo = wk.inspector.tree.GetPyData(geoItem)
            nrb = patch.extract_face(self.face)
            wk.add_patch(geoItem, geo, nrb)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... extract-face patch")
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentPatchItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo = wk.inspector.tree.GetPyData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("face = "+str(self.face))
                macro_script.append("nrb = patch.extract_face(face)")
                macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                macro_script.append("geoItem = geo.treeItem")
                macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")

            wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlFaceId:
                self.face = int(event.GetString())
        except:
            pass

class PatchActionsExtrude(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.displ = zeros(3)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "displ")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrln1Id = wx.NewId()
        self.txtCtrln1 = wx.TextCtrl(parentPanel, self.txtCtrln1Id, size=(50,25))
        self.txtCtrln1.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrln1.SetValue(str(self.displ[0]))
        hbox.Add(self.txtCtrln1, border=5)

        self.txtCtrln2Id = wx.NewId()
        self.txtCtrln2 = wx.TextCtrl(parentPanel, self.txtCtrln2Id, size=(50,25))
        self.txtCtrln2.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrln2.SetValue(str(self.displ[1]))
        hbox.Add(self.txtCtrln2, border=5)

        self.txtCtrln3Id = wx.NewId()
        self.txtCtrln3 = wx.TextCtrl(parentPanel, self.txtCtrln3Id, size=(50,25))
        self.txtCtrln3.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrln3.SetValue(str(self.displ[2]))
        hbox.Add(self.txtCtrln3, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...


    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.patchActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            patch     = wk.inspector.currentPatch
            patchItem = wk.inspector.currentPatchItem
            geoItem = wk.inspector.tree.GetItemParent(patchItem)
            geo = wk.inspector.tree.GetPyData(geoItem)
            from igakit.cad import extrude
            from igakit.cad_geometry import cad_nurbs
            nrb = extrude(patch, displ=self.displ)
            cnrb = cad_nurbs(nrb.knots, nrb.points, weights= nrb.weights)
            wk.add_patch(geoItem, geo, cnrb)
            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... extrude patch")
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentPatchItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo = wk.inspector.tree.GetPyData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("displ = "+str(list(self.displ)))
                macro_script.append("nrb = extrude(patch, displ=displ)")
                macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                macro_script.append("geoItem = geo.treeItem")
                macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")
            wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrln1Id:
                self.displ[0] = float(event.GetString())
            if event.GetId() == self.txtCtrln2Id:
                self.displ[1] = float(event.GetString())
            if event.GetId() == self.txtCtrln3Id:
                self.displ[2] = float(event.GetString())
        except:
            pass

class PatchActionsApproximate(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.s  = 0.1
        self.nsteps  = 100
        self.n  =  np.zeros(3,dtype=np.int)
        self.p  =  np.zeros(3,dtype=np.int)

        self.ub = None
        self.ue = None

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

        text = wx.StaticText(parentPanel, -1, "Smooth")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlSmoothId = wx.NewId()
        self.txtCtrlSmooth = wx.TextCtrl(parentPanel, self.txtCtrlSmoothId, size=(50,25))
        self.txtCtrlSmooth.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlSmooth.SetValue(str(self.s))
        hbox.Add(self.txtCtrlSmooth, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "Steps")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlStepsId = wx.NewId()
        self.txtCtrlSteps = wx.TextCtrl(parentPanel, self.txtCtrlStepsId, size=(50,25))
        self.txtCtrlSteps.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlSteps.SetValue(str(self.nsteps))
        hbox.Add(self.txtCtrlSteps, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.methods = ['chord', 'centripetal', 'uniform']

        self.comboBox = wx.ComboBox(parentPanel, -1 \
                                    , pos=(50, 170), size=(150,-1) \
                                    , choices=self.methods \
                                    , style=wx.CB_READONLY )
        hbox.Add(self.comboBox, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "ub")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlUbId = wx.NewId()
        self.txtCtrlUb = wx.TextCtrl(parentPanel, self.txtCtrlUbId, size=(50,25))
        self.txtCtrlUb.Bind(wx.EVT_TEXT, self.EvtText)
#        self.txtCtrlUb.SetValue(str(self.ub))
        hbox.Add(self.txtCtrlUb, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "ue")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlUeId = wx.NewId()
        self.txtCtrlUe = wx.TextCtrl(parentPanel, self.txtCtrlUeId, size=(50,25))
        self.txtCtrlUe.Bind(wx.EVT_TEXT, self.EvtText)
#        self.txtCtrlUe.SetValue(str(self.ue))
        hbox.Add(self.txtCtrlUe, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        self.comboBox.SetStringSelection("chord")
        self.method = "chord"

        self.parentPanel.Bind(wx.EVT_COMBOBOX, self.OnSelectComboBox)

    def Show(self):
        ClassActions.Show(self)
        wk = self.parent.WorkGroup
        patch = wk.inspector.currentPatch
        if patch.dim == 1:
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
        if patch.dim == 2:
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

        ClassActions.Hide(self)

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.patchActions)
        if ID == self.GO_ID:
            # inspector = self.parent
            wk = self.parent.WorkGroup
            patch     = wk.inspector.currentPatch
            patchItem = wk.inspector.currentPatchItem
            if patch.dim in [2,3]:
                raise("Approximation not yet implemented for 2D and 3D.")
            if patch.dim == 1:
                from plugin.curfit import run
                geo = run(  patch \
                          , self.method \
                          , self.n[0] \
                          , self.p[0] \
                          , self.s \
                          , self.nsteps\
                          , ub=self.ub \
                          , ue=self.ue)

                wk.add_geometry(geometry(geo))

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... approximate patch")
                    macro_script.append("from plugin.curfit import run")
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("method = \""+str(self.method)+"\"")
                    macro_script.append("n      = "+str(self.n[0]))
                    macro_script.append("p      = "+str(self.p[0]))
                    macro_script.append("s      = "+str(self.s))
                    macro_script.append("nsteps = "+str(self.nsteps))
                    macro_script.append("ub     = "+str(self.ub))
                    macro_script.append("ue     = "+str(self.ue))
                    macro_script.append("_geo = run(patch, method, n, p, s, nsteps, ub=ub, ue=ue)")
                    macro_script.append("wk.add_geometry(geometry(_geo))")
                    macro_script.append("wk.Refresh()")
                    macro_script.append("# ...")

            wk.Refresh()

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

            if event.GetId() == self.txtCtrlSmoothId:
                self.s      = float(event.GetString())
            if event.GetId() == self.txtCtrlStepsId:
                self.nsteps = int(event.GetString())

            if event.GetId() == self.txtCtrlUbId:
                self.ub      = float(event.GetString())
            if event.GetId() == self.txtCtrlUeId:
                self.ue      = float(event.GetString())

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

    def OnSelectComboBox(self, event):
        item = event.GetSelection()
        self.method = str(self.methods[item])

class PatchActionsStickC1(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.ib  = 0
        self.ie  = 0

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "ib")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlibId = wx.NewId()
        self.txtCtrlib = wx.TextCtrl(parentPanel, self.txtCtrlibId)
        self.txtCtrlib.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlib.SetValue(str(self.ib))
        hbox.Add(self.txtCtrlib, border=10)

        text = wx.StaticText(parentPanel, -1, "ie")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlieId = wx.NewId()
        self.txtCtrlie = wx.TextCtrl(parentPanel, self.txtCtrlieId)
        self.txtCtrlie.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlie.SetValue(str(self.ie))
        hbox.Add(self.txtCtrlie, border=10)

        self.Box.Add(hbox, border=5)
        # ...

    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.patchActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            list_patchs = [] ; list_faces = []
            for faceItem in wk.inspector.tree.selectionsItems:
                face        = wk.inspector.tree.GetPyData(faceItem)
                patchItem   = wk.inspector.tree.GetItemParent(wk.inspector.tree.GetItemParent(faceItem))
                patch       = wk.inspector.tree.GetPyData(patchItem)

                face_id = face.face

                list_patchs.append(patch)
                list_faces.append(face_id)
            if len(list_patchs) > 2:
                print "Stick-C1 algorithm needs 2 nurbs, but ", len(list_patchs), " were given"
                return

            from igakit.cad import stickC1
            nrb_m   = list_patchs[0]
            nrb_s   = list_patchs[1]
            face_m  = list_faces[0]
            face_s  = list_faces[1]

            ib = self.ib ; ie = self.ie
            nrb_s = stickC1(nrb_m,nrb_s,face_m,face_s,ib=ib,ie=ie)

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... stickC1 algorithm")
                list_gp = []
                for faceItem in wk.inspector.tree.selectionsItems:
                    face      = wk.inspector.tree.GetPyData(faceItem)
                    patchItem = wk.inspector.tree.GetItemParent(wk.inspector.tree.GetItemParent(faceItem))
                    patch   = wk.inspector.tree.GetPyData(patchItem)
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo     = wk.inspector.tree.GetPyData(geoItem)
                    list_gp.append([geo, patch])


                for i,gp in enumerate(list_gp):
                    geo = gp[0] ; patch = gp[1]
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("nrb_"+str(i)+" = patch")

                macro_script.append("nrb_m = nrb_0")
                macro_script.append("nrb_s = nrb_1")
                macro_script.append("face_m = "+str(face_m))
                macro_script.append("face_s = "+str(face_s))
                macro_script.append("ib = "+str(ib))
                macro_script.append("ie = "+str(ie))
                macro_script.append("nrb_s = stickC1(nrb_m,nrb_s,face_m,face_s,ib=ib,ie=ie)")
                macro_script.append("wk.Refresh()")
                macro_script.append("# ...")

            wk.Refresh()

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlibId:
                self.ib = int(event.GetString())
            if event.GetId() == self.txtCtrlieId:
                self.ie = int(event.GetString())
        except:
            pass

class PatchActionsInsert(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.knot  = None
        self.axis  = None

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "knot")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlKnotId = wx.NewId()
        self.txtCtrlKnot = wx.TextCtrl(parentPanel, self.txtCtrlKnotId)
        self.txtCtrlKnot.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlKnot, border=10)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxisId = wx.NewId()
        self.txtCtrlAxis = wx.TextCtrl(parentPanel, self.txtCtrlAxisId, size=(50,25))
        self.txtCtrlAxis.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlAxis, border=5)

        self.Box.Add(hbox, border=5)
        # ...


    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.patchActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            patch     = wk.inspector.currentPatch
            patchItem = wk.inspector.currentPatchItem
            geoItem = wk.inspector.tree.GetItemParent(patchItem)
            geo = wk.inspector.tree.GetPyData(geoItem)
            from igakit.cad_geometry import cad_nurbs
            if (self.knot is not None) and (self.axis is not None):
                knot = self.knot
                axis = self.axis
                nrb = patch.copy().insert(axis,knot)
                cnrb = cad_nurbs(nrb.knots, nrb.points, weights= nrb.weights)
                wk.add_patch(geoItem, geo, cnrb)
                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... insert-knot patch")
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("nrb = patch.copy()")
                    macro_script.append("axis = "+str(self.axis))
                    macro_script.append("knot = "+str(self.knot))
                    macro_script.append("nrb = nrb.insert(axis,knot)")
                    macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")

                wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlKnotId:
                self.knot = float(event.GetString())
            if event.GetId() == self.txtCtrlAxisId:
                self.axis = int(event.GetString())
        except:
            pass

class PatchActionsRemap(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.start = None
        self.end   = None
        self.axis  = None

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "start")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlStartId = wx.NewId()
        self.txtCtrlStart = wx.TextCtrl(parentPanel, self.txtCtrlStartId)
        self.txtCtrlStart.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlStart, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "end")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlEndId = wx.NewId()
        self.txtCtrlEnd = wx.TextCtrl(parentPanel, self.txtCtrlEndId)
        self.txtCtrlEnd.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlEnd, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxisId = wx.NewId()
        self.txtCtrlAxis = wx.TextCtrl(parentPanel, self.txtCtrlAxisId, size=(50,25))
        self.txtCtrlAxis.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlAxis, border=5)

        self.Box.Add(hbox, border=5)
        # ...


    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.patchActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            patch     = wk.inspector.currentPatch
            patchItem = wk.inspector.currentPatchItem
            geoItem = wk.inspector.tree.GetItemParent(patchItem)
            geo = wk.inspector.tree.GetPyData(geoItem)
            from igakit.cad_geometry import cad_nurbs
            if (self.start is not None) \
               and (self.end is not None) \
               and (self.axis is not None):
                start = self.start
                end   = self.end
                axis = self.axis
                nrb = patch.copy().remap(axis,start,end)
                cnrb = cad_nurbs(nrb.knots, nrb.points, weights= nrb.weights)
                wk.add_patch(geoItem, geo, cnrb)

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... remap patch")
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("nrb = patch.copy()")
                    macro_script.append("axis  = "+str(self.axis))
                    macro_script.append("start = "+str(self.start))
                    macro_script.append("end   = "+str(self.end))
                    macro_script.append("nrb.remap(axis,start,end)")
                    macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")

                wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlStartId:
                self.start = float(event.GetString())
            if event.GetId() == self.txtCtrlEndId:
                self.end = float(event.GetString())
            if event.GetId() == self.txtCtrlAxisId:
                self.axis = int(event.GetString())
        except:
            pass


class PatchActionsRemove(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.axis  = None
        self.knot  = None
        self.times = 1
        self.deviation = 1.0e-9

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "knot")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlKnotId = wx.NewId()
        self.txtCtrlKnot = wx.TextCtrl(parentPanel, self.txtCtrlKnotId)
        self.txtCtrlKnot.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlKnot, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "times")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlTimesId = wx.NewId()
        self.txtCtrlTimes = wx.TextCtrl(parentPanel, self.txtCtrlTimesId)
        self.txtCtrlTimes.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlTimes, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "deviation")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlDeviationId = wx.NewId()
        self.txtCtrlDeviation = wx.TextCtrl(parentPanel, self.txtCtrlDeviationId)
        self.txtCtrlDeviation.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlDeviation, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxisId = wx.NewId()
        self.txtCtrlAxis = wx.TextCtrl(parentPanel, self.txtCtrlAxisId, size=(50,25))
        self.txtCtrlAxis.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlAxis, border=5)

        self.Box.Add(hbox, border=5)
        # ...


    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.patchActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            patch     = wk.inspector.currentPatch
            patchItem = wk.inspector.currentPatchItem
            geoItem = wk.inspector.tree.GetItemParent(patchItem)
            geo = wk.inspector.tree.GetPyData(geoItem)
            from igakit.cad_geometry import cad_nurbs
            if (self.knot is not None) \
               and (self.axis is not None):
                value = self.knot
                times = self.times
                deviation  = self.deviation
                axis  = self.axis
                nrb = patch.copy().remove(axis, value, times=times, deviation=deviation)
                cnrb = cad_nurbs(nrb.knots, nrb.points, weights= nrb.weights)
                wk.add_patch(geoItem, geo, cnrb)

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... remove-knot patch")
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("nrb = patch.copy()")
                    macro_script.append("axis = "+str(axis))
                    macro_script.append("value = "+str(value))
                    macro_script.append("times = "+str(times))
                    macro_script.append("deviation = "+str(deviation))
                    macro_script.append("nrb.remove(axis, value, times=times, deviation=deviation)")
                    macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")

                wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlKnotId:
                self.knot = float(event.GetString())
            if event.GetId() == self.txtCtrlDeviationId:
                self.deviation = float(event.GetString())
            if event.GetId() == self.txtCtrlTimesId:
                self.times = int(event.GetString())
            if event.GetId() == self.txtCtrlAxisId:
                self.axis = int(event.GetString())
        except:
            pass


class PatchActionsSlice(ClassActions):
    def __init__(self, parent, parentPanel, parentBox):
        self.GO_ID = wx.NewId() ; GO_TAG = "Go"

        list_buttonsInfo = []
        list_buttonsInfo.append([self.GO_ID, GO_TAG])
        # ...

        ClassActions.__init__(self, parent, parentPanel, parentBox,
                              list_buttonsInfo, backButton=True)

        self.start = None
        self.end   = None
        self.axis  = None

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "start")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlStartId = wx.NewId()
        self.txtCtrlStart = wx.TextCtrl(parentPanel, self.txtCtrlStartId)
        self.txtCtrlStart.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlStart, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "end")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlEndId = wx.NewId()
        self.txtCtrlEnd = wx.TextCtrl(parentPanel, self.txtCtrlEndId)
        self.txtCtrlEnd.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlEnd, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxisId = wx.NewId()
        self.txtCtrlAxis = wx.TextCtrl(parentPanel, self.txtCtrlAxisId, size=(50,25))
        self.txtCtrlAxis.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlAxis, border=5)

        self.Box.Add(hbox, border=5)
        # ...


    def OnClick(self, event):
        ID = event.GetId()
        if ID == self.BCK_ID:
            self.parent.ShowAction(self.parent.patchActions)
        if ID == self.GO_ID:
            wk = self.parent.WorkGroup
            patch     = wk.inspector.currentPatch
            patchItem = wk.inspector.currentPatchItem
            from igakit.cad_geometry import cad_nurbs
            if (self.start is not None) \
               and (self.end is not None) \
               and (self.axis is not None):
                start = self.start
                end   = self.end
                axis = self.axis
                nrb = patch.copy().slice(axis,start,end)
                cnrb = cad_nurbs(nrb.knots, nrb.points, weights= nrb.weights)
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo = wk.inspector.tree.GetPyData(geoItem)
                wk.add_patch(geoItem, geo, cnrb)

                # macro recording
                if wk.macroRecording:
                    macro_script = wk.macro_script
                    macro_script.new_line()
                    macro_script.append("# ... slice patch")
                    patch = wk.inspector.currentObject
                    patchItem = wk.inspector.currentPatchItem
                    geoItem = wk.inspector.tree.GetItemParent(patchItem)
                    geo = wk.inspector.tree.GetPyData(geoItem)
                    geo_id   = wk.list_geo.index(geo)
                    patch_id = geo.index(patch)
                    macro_script.append("geo_id = "+str(geo_id))
                    macro_script.append("patch_id = "+str(patch_id))
                    macro_script.append("geo = geometries[geo_id]")
                    macro_script.append("patch = geo[patch_id]")
                    macro_script.append("nrb = patch.copy()")
                    macro_script.append("axis  = "+str(axis))
                    macro_script.append("start = "+str(start))
                    macro_script.append("end   = "+str(end))
                    macro_script.append("nrb = nrb.slice(axis,start,end)")
                    macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                    macro_script.append("geoItem = geo.treeItem")
                    macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                    macro_script.append("wk.Refresh(inspector=True)")
                    macro_script.append("# ...")

                wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlStartId:
                self.start = float(event.GetString())
            if event.GetId() == self.txtCtrlEndId:
                self.end = float(event.GetString())
            if event.GetId() == self.txtCtrlAxisId:
                self.axis = int(event.GetString())
        except:
            pass

class PatchActionsClamp(ClassActions):
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

        self.axis = None
        self.side = None

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrln1Id = wx.NewId()
        self.txtCtrln1 = wx.TextCtrl(parentPanel, self.txtCtrln1Id, size=(50,25))
        self.txtCtrln1.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrln1, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "side")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlp1Id = wx.NewId()
        self.txtCtrlp1 = wx.TextCtrl(parentPanel, self.txtCtrlp1Id, size=(50,25))
        self.txtCtrlp1.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlp1, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

    def Show(self):
        ClassActions.Show(self)
        wk = self.parent.WorkGroup
        nrb = wk.inspector.currentPatch

    def Hide(self):
        self.txtCtrln1.Hide()
        self.txtCtrlp1.Hide()

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
            patch = wk.inspector.currentPatch
            patchItem = wk.inspector.currentPatchItem
            axis = self.axis
            side = self.side
            if (axis is not None) and (side is not None):
                nrb = patch.copy().clamp(axis=axis,side=side)
            else:
                nrb = patch.copy().clamp()
            cnrb = cad_nurbs(nrb.knots, nrb.points, weights= nrb.weights)
            geoItem = wk.inspector.tree.GetItemParent(patchItem)
            geo = wk.inspector.tree.GetPyData(geoItem)
            wk.add_patch(geoItem, geo, cnrb)

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... clamp patch")
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentPatchItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo = wk.inspector.tree.GetPyData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("nrb = patch.copy()")
                if (axis is not None) and (side is not None):
                    macro_script.append("axis = "+str(axis))
                    macro_script.append("side = "+str(side))
                    macro_script.append("nrb.clamp(axis=axis,side=side)")
                else:
                    macro_script.append("nrb.clamp()")
                macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                macro_script.append("geoItem = geo.treeItem")
                macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")

            wk.Refresh(inspector=True)

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrln1Id:
                self.axis = int(event.GetString())

            if event.GetId() == self.txtCtrlp1Id:
                self.side = int(event.GetString())
        except:
            pass

class PatchActionsUnclamp(ClassActions):
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

        self.axis = None
        self.side = None

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrln1Id = wx.NewId()
        self.txtCtrln1 = wx.TextCtrl(parentPanel, self.txtCtrln1Id, size=(50,25))
        self.txtCtrln1.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrln1, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "side")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlp1Id = wx.NewId()
        self.txtCtrlp1 = wx.TextCtrl(parentPanel, self.txtCtrlp1Id, size=(50,25))
        self.txtCtrlp1.Bind(wx.EVT_TEXT, self.EvtText)
        hbox.Add(self.txtCtrlp1, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

    def Show(self):
        ClassActions.Show(self)
        wk = self.parent.WorkGroup
        nrb = wk.inspector.currentPatch

    def Hide(self):
        self.txtCtrln1.Hide()
        self.txtCtrlp1.Hide()

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
            patch = wk.inspector.currentPatch
            patchItem = wk.inspector.currentPatchItem
            axis = self.axis
            side = self.side
            if (axis is not None) and (side is not None):
                nrb = patch.copy().unclamp(axis=axis,side=side)
            else:
                nrb = patch.copy().unclamp()
            cnrb = cad_nurbs(nrb.knots, nrb.points, weights= nrb.weights)
            geoItem = wk.inspector.tree.GetItemParent(patchItem)
            geo = wk.inspector.tree.GetPyData(geoItem)
            wk.add_patch(geoItem, geo, cnrb)

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... unclamp patch")
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentPatchItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo = wk.inspector.tree.GetPyData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("nrb = patch.copy()")
                if (axis is not None) and (side is not None):
                    macro_script.append("axis = "+str(axis))
                    macro_script.append("side = "+str(side))
                    macro_script.append("nrb.unclamp(axis=axis,side=side)")
                else:
                    macro_script.append("nrb.unclamp()")
                macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                macro_script.append("geoItem = geo.treeItem")
                macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")

            wk.Refresh()

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrln1Id:
                self.axis = int(event.GetString())

            if event.GetId() == self.txtCtrlp1Id:
                self.side = int(event.GetString())
        except:
            pass

class PatchActionsRevolve(ClassActions):
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

        self.axis = 2
        self.angle_min = 0.
        self.angle_max = 2*pi
        self.point = zeros(3)

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "axis")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAxisId = wx.NewId()
        self.txtCtrlAxis = wx.TextCtrl(parentPanel, self.txtCtrlAxisId, size=(50,25))
        self.txtCtrlAxis.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAxis.SetValue(str(self.axis))
        hbox.Add(self.txtCtrlAxis, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "angle-min")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAngleMinId = wx.NewId()
        self.txtCtrlAngleMin = wx.TextCtrl(parentPanel, self.txtCtrlAngleMinId, size=(50,25))
        self.txtCtrlAngleMin.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAngleMin.SetValue(str(self.angle_min))
        hbox.Add(self.txtCtrlAngleMin, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "angle-max")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrlAngleMaxId = wx.NewId()
        self.txtCtrlAngleMax = wx.TextCtrl(parentPanel, self.txtCtrlAngleMaxId, size=(50,25))
        self.txtCtrlAngleMax.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrlAngleMax.SetValue(str(self.angle_max))
        hbox.Add(self.txtCtrlAngleMax, border=5)

        self.Box.Add(hbox, border=5)
        # ...

        # ...
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(parentPanel, -1, "point")
        hbox.Add(text, 0, wx.ALL, 5)

        self.txtCtrln1Id = wx.NewId()
        self.txtCtrln1 = wx.TextCtrl(parentPanel, self.txtCtrln1Id, size=(50,25))
        self.txtCtrln1.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrln1.SetValue(str(self.point[0]))
        hbox.Add(self.txtCtrln1, border=5)

        self.txtCtrln2Id = wx.NewId()
        self.txtCtrln2 = wx.TextCtrl(parentPanel, self.txtCtrln2Id, size=(50,25))
        self.txtCtrln2.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrln2.SetValue(str(self.point[1]))
        hbox.Add(self.txtCtrln2, border=5)

        self.txtCtrln3Id = wx.NewId()
        self.txtCtrln3 = wx.TextCtrl(parentPanel, self.txtCtrln3Id, size=(50,25))
        self.txtCtrln3.Bind(wx.EVT_TEXT, self.EvtText)
        self.txtCtrln3.SetValue(str(self.point[2]))
        hbox.Add(self.txtCtrln3, border=5)

        self.Box.Add(hbox, 0, wx.EXPAND, 5)
        # ...

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
            patch = wk.inspector.currentPatch
            patchItem = wk.inspector.currentPatchItem
            geoItem = wk.inspector.tree.GetItemParent(patchItem)
            geo = wk.inspector.tree.GetPyData(geoItem)
            axis = self.axis
            point = self.point
            angle = [self.angle_min, self.angle_max]
            from igakit.cad import revolve
            nrb = revolve(patch, point, axis, angle=angle)
            cnrb = cad_nurbs(nrb.knots, nrb.points, weights= nrb.weights)
            wk.add_patch(geoItem, geo, cnrb)

            # macro recording
            if wk.macroRecording:
                macro_script = wk.macro_script
                macro_script.new_line()
                macro_script.append("# ... revolve patch")
                patch = wk.inspector.currentObject
                patchItem = wk.inspector.currentPatchItem
                geoItem = wk.inspector.tree.GetItemParent(patchItem)
                geo = wk.inspector.tree.GetPyData(geoItem)
                geo_id   = wk.list_geo.index(geo)
                patch_id = geo.index(patch)
                macro_script.append("geo_id = "+str(geo_id))
                macro_script.append("patch_id = "+str(patch_id))
                macro_script.append("geo = geometries[geo_id]")
                macro_script.append("patch = geo[patch_id]")
                macro_script.append("point = "+str(list(point)))
                macro_script.append("axis = "+str(axis))
                macro_script.append("angle = "+str(angle))
                macro_script.append("nrb = revolve(patch, point, axis, angle=angle)")
                macro_script.append("cad_nrb = cad_nurbs(nrb.knots, nrb.points, weights=nrb.weights)")
                macro_script.append("geoItem = geo.treeItem")
                macro_script.append("wk.add_patch(geoItem, geo, cad_nrb)")
                macro_script.append("wk.Refresh(inspector=True)")
                macro_script.append("# ...")

            wk.Refresh()

    def EvtText(self, event):
        try:
            if event.GetId() == self.txtCtrlAxisId:
                self.axis = int(event.GetString())

            if event.GetId() == self.txtCtrlAngleMinId:
                self.angle_min = float(event.GetString())
            if event.GetId() == self.txtCtrlAngleMaxId:
                self.angle_max = float(event.GetString())

            if event.GetId() == self.txtCtrln1Id:
                self.point[0] = float(event.GetString())
            if event.GetId() == self.txtCtrln2Id:
                self.point[1] = float(event.GetString())
            if event.GetId() == self.txtCtrln3Id:
                self.point[2] = float(event.GetString())

        except:
            pass
