# -*- coding: UTF-8 -*-

from igakit.cad_geometry import cad_geometry
from evaluator import CurveEvaluator, PatchEvaluator
from numpy import array, asarray
from OpenGL.GL import *
from theme import theme as Theme
from global_vars import strtoArray

theme = Theme()

ALPHA                   = theme.alpha
BETA                    = theme.beta
COLOR_DEFAULT_GEOMETRY  = theme.color_viewer('default_geometry')
COLOR_DEFAULT_PATCH     = theme.color_viewer('default_patch')
COLOR_DEFAULT_MESH      = theme.color_viewer('default_mesh')
COLOR_DEFAULT_POINTS    = theme.color_viewer('default_points')
SIZE_GEOMETRY_POINTS    = theme.size_points('geometry')
SIZE_PATCH_POINTS       = theme.size_points('patch')



def pointsToList(points):
        x = points[...,0]
        y = points[...,1]
        z = points[...,2]
        n = asarray(points.shape[:-1]).prod()
        x = x.reshape(n)
        y = y.reshape(n)
        z = z.reshape(n)

        return x,y,z

def controlToList(control):
        x = control[...,0]
        y = control[...,1]
        z = control[...,2]
        w = control[...,3]
        n = asarray(control.shape[:-1]).prod()
        x = x.reshape(n)
        y = y.reshape(n)
        z = z.reshape(n)
        w = w.reshape(n)

        return x,y,z,w

class PatchInfo(object):
    def __init__(self, patch):
        self.patch = patch
        self.show = True
        self.showPoints = False
        self.showMesh = False

        self._MeshColor      = None
        self._NurbsColor     = None
        self._PointsColor    = None

        self.steps          = None

        self.PointsSize     = SIZE_PATCH_POINTS

        self.name = None

        self.load_attributs()

    @property
    def MeshColor(self):
        return self._MeshColor

    @property
    def NurbsColor(self):
        return self._NurbsColor

    @property
    def PointsColor(self):
        return self._PointsColor

    def Show(self):
        self.show = True

    def Hide(self):
        self.show = False

    def ShowPoints(self):
        self.showPoints = True

    def HidePoints(self):
        self.showPoints = False

    def ShowMesh(self):
        self.showMesh = True

    def HideMesh(self):
        self.showMesh = False

    def set_meshColor(self,color):
        self.MeshColor = color

    def set_nurbsColor(self,color):
        self._NurbsColor = color
        self.patch.set_attribut("color-nurbs", str(self.NurbsColor))

    def set_pointsColor(self,color):
        self.PointsColor = color

    def set_pointsSize(self,size):
        self.PointsSize = size

    def set_steps(self, steps):
        self.steps = steps

    def set_name(self, name):
        self.name = name
        self.patch.set_attribut("name", str(name))

    def load_attributs(self):
        patch = self.patch
        # color nurbs
        try:
            self._NurbsColor = strtoArray(patch.get_attribut('color-nurbs'))
        except:
            self._NurbsColor     = None


class geometry(cad_geometry):
    def __init__(self, geo=None):
        cad_geometry.__init__(self)
        self.list_patchInfo = []
        if geo is not None:
            for i in range(0, geo.npatchs):
                P = geo[i]
                # this is really a clone and not a copy
                patch = P.clone()
                self.append(patch)
                # add attributs from xml description when it exists
                self.list_patchInfo.append(PatchInfo(patch))
            self.set_internal_faces(geo.internal_faces)
            self.set_external_faces(geo.external_faces)
            self.set_connectivity(geo.connectivity)
            self.set_attributs(geo.attributs)

        self.MeshColor      = COLOR_DEFAULT_MESH
        self.NurbsColor     = Theme().color_viewer('default_patch') #COLOR_DEFAULT_GEOMETRY
        self.PointsColor    = COLOR_DEFAULT_POINTS

        self.PointsSize     = SIZE_GEOMETRY_POINTS

        self.showPoints = False
        self.showMesh = False
        self._show = True

        # needed for the tree inspector
        self._treeItem = None

        # needed when extracting faces for the instpector tree
        self.face = None

    @property
    def treeItem(self):
        return self._treeItem

    def set_treeItem(self, item):
        self._treeItem = item

    def append(self, nrb):
        cad_geometry.append(self,nrb)
        self.list_patchInfo.append(PatchInfo(nrb))

    def load_attributs(self):
        # color nurbs
        self.NurbsColor = strtoArray(self.get_attribut('color-nurbs'))

        # Hide/Show geometry
        try:
            self._show = self.get_attribut('show')
            if self._show is None:
                self._show = True
        except:
            self._show = False

    def save_attributs(self):
        # color nurbs
        self.set_attribut('color-nurbs', str(self.NurbsColor))
        # Hide/Show geometry
        self.set_attribut('show', str(self.show))

    @property
    def show(self):
        return self._show

    def Show(self):
        self._show = True

    def Hide(self):
        self._show = False

    def ShowPoints(self):
        self.showPoints = True

    def HidePoints(self):
        self.showPoints = False

    def ShowMesh(self):
        self.showMesh = True

    def HideMesh(self):
        self.showMesh = False

    def set_meshColor(self,color):
        self.MeshColor = color

    def set_nurbsColor(self,color):
        self.NurbsColor = color
        self.set_attribut("color-nurbs", str(self.NurbsColor))

    def set_pointsColor(self,color):
        self.PointsColor = color

    def set_pointsSize(self,size):
        self.PointsSize = size

    def remove_patch(self, patch):
        index = self.index(patch)
        patchInfo = self.list_patchInfo[index]
        self.list_patchInfo.remove(patchInfo)
        self.remove(patch)

    def OnDelete(self, event):
        sel = self.listbox.GetSelection()
        if sel != -1:
            self.listbox.Delete(sel)

    def OnClear(self, event):
        self.listbox.Clear()

    def display(self):
        for i in range(0, self.npatchs):
            self.display_patch(i)

    def display_patch(self, i):
        pass

    def DrawControlPoints(self,nrb,PointsColor=None,alpha=ALPHA, blend=False):
        if PointsColor is None:
            PointsColor = self.PointsColor
        PointsColor = list(PointsColor) + [ALPHA]

        x,y,z = pointsToList(nrb.points)
        if blend:
            glEnable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glColor4f(*PointsColor)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)
        glPointSize(self.PointsSize)
        glBegin(GL_POINTS)
        for _x,_y,_z in zip(x,y,z):
            glVertex(_x,_y,_z)
        glEnd()
        if blend:
            glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

    def GetEvaluator(self, nrb \
                     , MeshColor=None \
                     , NurbsColor=None \
                     , alpha=ALPHA \
                     , steps=None):
        if MeshColor is None:
            MeshColor = self.MeshColor
        if NurbsColor is None:
            NurbsColor = self.NurbsColor

        if nrb.dim == 1:
            evaluator = CurveEvaluator(nrb\
                                       , MeshColor=MeshColor\
                                       , NurbsColor=NurbsColor\
                                       , alpha=alpha\
                                       , steps=steps)
        if nrb.dim == 2:
            evaluator = PatchEvaluator(nrb\
                                       , MeshColor=MeshColor\
                                       , NurbsColor=NurbsColor\
                                       , alpha=alpha\
                                       , steps=steps)
        return evaluator

    def Draw(self, nrb=None \
             , MeshColor=None \
             , NurbsColor=None \
             , PointsColor=None \
             , alpha=ALPHA \
             , blend=False):

        if NurbsColor is None:
            if self.NurbsColor is None:
                NurbsColor = list(asarray(Theme().color_viewer('default_patch')).copy())
            else:
                NurbsColor = list(asarray(self.NurbsColor).copy())
        if self.show:
            if nrb is not None:
                list_nrb = [nrb]
            else:
                list_nrb = self._list

            for i in range(0,len(list_nrb)):
                nrb = list_nrb[i]
                nrbInfo = self.list_patchInfo[i]
                if nrbInfo.show:
                    _NurbsColor = asarray(NurbsColor).copy()
                    if nrbInfo.NurbsColor is not None:
                        _NurbsColor = asarray(nrbInfo.NurbsColor).copy()
                    NurbsSteps = nrbInfo.steps
                    evaluator = self.GetEvaluator(nrb \
                                                  , MeshColor=MeshColor \
                                                  , NurbsColor=_NurbsColor \
                                                  , alpha=alpha\
                                                  , steps=NurbsSteps)
                    showMesh = self.showMesh or nrbInfo.showMesh
                    evaluator.draw(mesh=showMesh, nurbs=True, blend=blend)
                if self.showPoints or nrbInfo.showPoints:
                    # Draw control points
                    self.DrawControlPoints(nrb \
                                           , PointsColor=PointsColor \
                                           ,alpha=alpha, blend=blend)

#######################################################################
if __name__ == '__main__':
    from igakit.cad_geometry import square
    import matplotlib.pyplot as plt
    s1 = square(n=[3,3])
    geo1 = geometry()
    for nrb in s1:
        geo1.append(nrb)
    geo1.plotMesh() ; plt.show()
    geo2 = geometry(s1)
    geo2.plotMesh() ; plt.show()
