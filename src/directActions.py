# -*- coding: UTF-8 -*-
import wx
from geometry import geometry
from igakit.cad import join
from caid.cad_geometry import cad_geometry, cad_nurbs
from caid.cad_geometry import linear
from viewer import Viewer
from numpy import pi, linspace, array, asarray
import numpy as np
from numpy import cos, pi
from customDialogs import edtTxtDialog

class directActions(object):
    def __init__(self, workGroup):
        self.workGroup  = workGroup
        self.inspector  = workGroup.inspector
        self.viewer     = workGroup.viewer

    def createLines(self):
        wk = self.workGroup
        list_P = wk.viewer.MarkerPoints
        list_crv = []
        for P,Q in zip(list_P[:-1], list_P[1:]):
            points = np.zeros((2,2))
            points[0,0] = P[0] ; points[0,1] = P[1]
            points[1,0] = Q[0] ; points[1,1] = Q[1]
            crv = linear(points = points)[0]
            list_crv.append(crv)
        nrb = list_crv[0]
        axis = 0
        for crv in list_crv[1:]:
            nrb = join(nrb, crv, axis)

        wk.viewer.CleanMarkerPoints()
        geo = cad_geometry()
        geo.append(nrb)
        wk.add_geometry(geometry(geo))
        wk.Refresh()

    def createArc(self):
        wk = self.workGroup
        list_P = wk.viewer.MarkerPoints
        if len(list_P) != 3 :
            print "You have to specify 3 markers."
            return

        dlg = edtTxtDialog(None, title="Edit Angle")
        dlg.ShowModal()
        ls_text = dlg.getValue()
        try:
            lr_degree = float(ls_text)
        except:
            lr_degree = 0.0

        theta = lr_degree * pi / 180

        dlg.Destroy()

        A0 = list_P[0]
        A1 = list_P[1]
        A2 = list_P[2]

        knots       = [0.,0.,0.,1.,1.,1.]
        C           = np.zeros((3,3))
        C[0,:]      = A0[:3]
        C[1,:]      = A1[:3]
        C[2,:]      = A2[:3]
        weights     = [1.,cos(theta),1.]

        nrb = cad_nurbs([knots], C, weights=weights)

        wk.viewer.CleanMarkerPoints()
        geo = cad_geometry()
        geo.append(nrb)
        wk.add_geometry(geometry(geo))
        wk.Refresh()

    def createBilinear(self):
        wk = self.workGroup
        list_P = wk.viewer.MarkerPoints
        if len(list_P) != 4 :
            print "You have to specify 4 markers."
            return

        A = list_P[0]
        B = list_P[1]
        C = list_P[2]
        D = list_P[3]

        points = np.zeros((2,2,3))

        points[0,0,:] = A[:3]
        points[1,0,:] = B[:3]
        points[0,1,:] = C[:3]
        points[1,1,:] = D[:3]

#        weights[0,0] = A[3]
#        weights[1,0] = B[3]
#        weights[0,1] = C[3]
#        weights[1,1] = D[3]

        from caid.cad_geometry import bilinear
        nrb = bilinear(points=points)[0]

        wk.viewer.CleanMarkerPoints()
        geo = cad_geometry()
        geo.append(nrb)
        wk.add_geometry(geometry(geo))
        wk.Refresh()

    def SelectedToMarkersPoints(self):
        wk = self.workGroup
        list_Q = []
        for selectedPoints in wk.viewer.list_SelectedPoints:
            list_Q += selectedPoints.points
        for P in list_Q:
            wk.viewer.AddMarkerPoint(P)
        wk.Refresh()

    def CloneSelectedPoints(self):
        wk = self.workGroup
        patch = wk.inspector.currentPatch
        P = patch.control
        # we suppose that the current selection is the last one done
        selectedPoints  = wk.viewer.list_SelectedPoints[-1]
        list_ijk        = selectedPoints.indices

        list_Q = wk.viewer.MarkerPoints
        if patch.dim == 1:
            for ij,Q in zip(list_ijk, list_Q):
                P[ij[0],:] = Q[:]
        if patch.dim == 2:
            for ij,Q in zip(list_ijk, list_Q):
                P[ij[0],ij[1],:] = Q[:]

        patch._array = P
        patch.set_points(P[...,:3])
        wk.viewer.CleanMarkerPoints()
        wk.viewer.CleanSelectedPoints()
        wk.Refresh(inspector=True)

    def cutCurve(self):
        wk = self.workGroup
        try:
            list_patchs = []
            for item in wk.inspector.tree.selectionsItems:
                patch = wk.inspector.tree.GetPyData(item)
                if patch.dim > 1:
                    print "cut curves algorithm only works with curves"
                    return
                list_patchs.append(patch)
            if len(list_patchs) > 1:
                print "cut curves algorithm needs 1 curve, but "\
                        , len(list_patchs), " curves were given"
                return

            from caid.utils.intersect import intersect_crv
            c0 = list_patchs[0]
            geo0 = cad_geometry()
            geo0.append(c0)

            freq = wk.viewer.cutCurveFreq
            list_P = wk.viewer.CutCurvePoints[::freq]
            x,y,z = zip(*list_P)
            x = np.asarray(x)
            y = np.asarray(y)
            z = np.asarray(z)
            from scipy import interpolate
            smooth = 0.
            degree = 3
            tck,u = interpolate.splprep([x,y],s=smooth, k=degree)
            knots = tck[0]
            Px = tck[1][0]
            Py = tck[1][1]
            C  = np.zeros((len(Px),3))
            C[:,0] = array(Px)
            C[:,1] = array(Py)
            c1 = cad_nurbs([knots], C)
            geo1 = cad_geometry()
            geo1.append(c1)

            list_P, list_t, list_s, ierr = intersect_crv(c0,c1)

            list_t = np.asarray(list_t)
            list_t.sort()
            axis = 0
            for i,t in enumerate(list_t):
                geo0.split(i,t,axis)

            wk.add_geometry(geometry(geo0))
            wk.Refresh()
        except:
            self.statusbar.SetStatusText('Cannot use cut Curve. Check that a patch is selected on the inspector' )

    def removeObject(self):
        wk = self.workGroup
        # ... removing a geometry
        geo = wk.inspector.currentGeometry
        geoItem = wk.inspector.currentGeometryItem
        if geo is not None:
            wk.remove_geometry(geoItem, geo)
            wk.Refresh()
            return

        # ... removing a patch
        patch = wk.inspector.currentPatch
        patchItem = wk.inspector.currentPatchItem
        if patch is not None:
            wk.remove_patch(patchItem, patch)
            wk.Refresh()
            return

        # removing a field
        field = wk.fields.currentField
        fieldItem = wk.fields.currentFieldItem
        if field is not None:
            wk.remove_field(fieldItem, field)
            wk.Refresh()
            return

    def renameObject(self):
        wk = self.workGroup
        # ... renaming a geometry
        geo = wk.inspector.currentGeometry
        geoItem = wk.inspector.currentGeometryItem
        if geo is not None:
            from customDialogs import edtTxtDialog
            dlg = edtTxtDialog(None, title="Rename Geometry", size=(200,75))
            dlg.ShowModal()
            ls_text = dlg.getValue()
            try:
                name = str(ls_text)
            except:
                name = None
            dlg.Destroy()
            if name is not None:
                geo.set_attribut("name",name)
            wk.inspector.tree.update()
            wk.inspector.reset_currentAll()
        # ... renaming a patch
        patch = wk.inspector.currentPatch
        patchItem = wk.inspector.currentPatchItem
        if patch is not None:
            geoItem     = wk.inspector.tree.GetItemParent(patchItem)
            geo         = wk.inspector.tree.GetPyData(geoItem)
            patch_id    = geo.index(patch)
            patchInfo   = geo.list_patchInfo[patch_id]

            from customDialogs import edtTxtDialog
            dlg = edtTxtDialog(None, title="Rename Patch", size=(200,75) )
            dlg.ShowModal()
            ls_text = dlg.getValue()
            try:
                name = str(ls_text)
            except:
                name = None
            dlg.Destroy()
            if name is not None:
                patchInfo.set_name(name)
            wk.inspector.tree.update()
            wk.inspector.reset_currentAll()

