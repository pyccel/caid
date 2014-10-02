# -*- coding: UTF-8 -*-

import OpenGL
from OpenGL import GLU
from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLU import *
from MenuCAIDViewer import MenuCAIDViewer
import numpy as np
from numpy import sin, pi, cos

from theme import theme as Theme

theme = Theme()

ALPHA                   = theme.alpha
BETA                    = theme.beta


class GLEvaluator():
    def __init__(self, nrb):
        self.nrb = nrb
        self.glID = gluNewNurbsRenderer()

    def __del__(self):
        gluDeleteNurbsRenderer(self.glID)

    def draw(self):
        pass

class CurveEvaluator(GLEvaluator):
    def __init__(self, nrb, steps=None \
                 , MeshColor=None \
                 , NurbsColor=None \
                 , alpha=ALPHA):
        GLEvaluator.__init__(self, nrb)
        if steps is None:
            steps = [50]

        self.patch = nrb

        self.uKnot = self.nrb.knots[0]
        self.u_min = self.nrb.knots[0][0]
        self.u_max = self.nrb.knots[0][-1]
        self.u_steps = steps[0]

        self.generateNormals = False
        self.target = GL_MAP1_VERTEX_4

#        self.evalPolygonMode = GL_LINE
        self.evalPolygonMode = GL_FILL

        self.controlPoints = nrb.control

        self.MeshColor = list(MeshColor) + [ALPHA]
        self.NurbsColor = list(NurbsColor) + [ALPHA]

    def drawSurface(self, z):
        self.controlPoints[:,2] = z

    def drawMesh(self, blend=False):
        pass
#        glColor4f(*self.MeshColor)
#        glMap1f(self.target,
#                   self.u_min, self.u_max,
#                   self.controlPoints)
#        glEnable(self.target)
#        glMapGrid1f(self.u_steps, self.u_min, self.u_max)
#        glEvalMesh1(self.evalPolygonMode, 0, self.u_steps)


    def drawNurbs(self, blend=False):
        if blend:
            glEnable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glColor4f(*self.NurbsColor)
        glPointSize(10.0)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)
        gluBeginCurve(self.glID)
        gluNurbsCurve(self.glID,
                        self.uKnot,
                        self.controlPoints,
                        self.target)
        gluEndCurve(self.glID)
        if blend:
            glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

    def draw(self, mesh=False, nurbs=True, blend=False):
        if nurbs:
            self.drawNurbs(blend=blend)
        if mesh:
            self.drawMesh(blend=blend)

class PatchEvaluator(GLEvaluator):
    def __init__(self, nrb, steps=None \
                 , MeshColor=None \
                 , NurbsColor=None \
                 , alpha=ALPHA):
        GLEvaluator.__init__(self, nrb)
        if steps is None:
            steps = [2,2]

        self.patch = nrb

        self.uKnot = self.nrb.knots[0]
        self.vKnot = self.nrb.knots[1]
        self.u_min = self.nrb.knots[0][0]
        self.u_max = self.nrb.knots[0][-1]
        self.u_steps = steps[0]
        self.v_min = self.nrb.knots[1][0]
        self.v_max = self.nrb.knots[1][-1]
        self.v_steps = steps[1]

        # can be replaced by nrb.breaks()
        _u = np.unique(self.uKnot)
        list_u = []
        for u0,u1 in zip(_u[0:-1], _u[1:]):
            list_u.append(np.linspace(u0,u1,self.u_steps))
        self.u = np.concatenate(list_u)

        # can be replaced by nrb.breaks()
        _v = np.unique(self.vKnot)
        list_v = []
        for v0,v1 in zip(_v[0:-1], _v[1:]):
            list_v.append(np.linspace(v0,v1,self.v_steps))
        self.v = np.concatenate(list_v)

        self.generateNormals = False
        self.target = GL_MAP2_VERTEX_4

        self.evalPolygonMode = GL_LINE
#        self.evalPolygonMode = GL_FILL

        self.controlPoints = nrb.control

        self.MeshColor = list(MeshColor) + [alpha]
        self.NurbsColor = list(NurbsColor) + [alpha]


    def drawSurface(self, z):
        self.controlPoints[:,:,2] = z

#    def drawMesh(self):
#        glColor4f(*self.MeshColor)
#        glMap2f(self.target,
#                   self.u_min, self.u_max,
#                   self.v_min, self.v_max,
#                   self.controlPoints)
#        glEnable(self.target)
#        glMapGrid2f(self.u_steps, self.u_min, self.u_max \
#                    , self.v_steps, self.v_min, self.v_max)
#        glEvalMesh2(self.evalPolygonMode, 0, self.u_steps, 0, self.v_steps)

    def drawMesh(self, blend=False):
        glColor4f(*self.MeshColor)
#        u = np.linspace(self.u_min, self.u_max, self.u_steps)
#        v = np.linspace(self.v_min, self.v_max, self.v_steps)
        u = self.u
        v = self.v

        nrb = self.patch
        P = nrb.evaluate(u,v)
        n,m,d = P.shape
        glDisable(GL_DEPTH_TEST)
        glEnable(self.target)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
#        glPolygonMode(GL_FRONT, GL_LINE)
        for j in range(0,m):
            glBegin(GL_LINES)
            for i in range(0,n-1):
                glVertex(P[i  ,j,0], P[i  ,j,1], P[i  ,j,2])
                glVertex(P[i+1,j,0], P[i+1,j,1], P[i+1,j,2])
            glEnd()

        for i in range(0,n):
            glBegin(GL_LINES)
            for j in range(0,m-1):
                glVertex(P[i,j  ,0], P[i,j  ,1], P[i,j  ,2])
                glVertex(P[i,j+1,0], P[i,j+1,1], P[i,j+1,2])
            glEnd()
        glEnable(GL_DEPTH_TEST)

    def drawNurbs(self, blend=False):
#        glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.5)
#        light_diffuse = [1.0, 1.0, 1.0, 1.0]
#        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

#        glBegin(GL_QUADS)
#        glTexCoord2f(0,0)
#        glVertex2f(-1,-1)
#        glTexCoord2f(1,0)
#        glVertex2f( 1,-1)
#        glTexCoord2f(1,1)
#        glVertex2f( 1, 1)
#        glTexCoord2f(0,1)
#        glVertex2f(-1, 1)
#        glEnd()
#
#        glUseProgram(0) # shaders interfer with pure pixel drawing
#        glBindTexture( GL_TEXTURE_2D, 0 ) # textures do so as well
#
#        firew = 100
#        for i in range(0,firew):
#            glRasterPos2f(-1+2*i/(firew+0.0),-0.999)
#            a = np.ones((1,1,3))
#            glDrawPixelsf(GL_LUMINANCE,a)
##            glDrawPixelsf(GL_LUMINANCE,[[[np.random.random()]]])
##        glPopAttrib(GL_VIEWPORT_BIT)

        if blend:
            glEnable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glColor4f(*self.NurbsColor)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)
        gluBeginSurface(self.glID)
        gluNurbsSurface(self.glID,
                        self.uKnot,
                        self.vKnot,
                        self.controlPoints,
                        self.target)
        gluEndSurface(self.glID)
        if blend:
            glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

    def drawNurbsByCell(self, blend=False):
        u = self.u
        v = self.v

        nrb = self.patch
        P = nrb.evaluate(u,v)
        n,m,d = P.shape
#        glEnable(self.target)
#        glPolygonMode(GL_FRONT, GL_FILL)
#        glPolygonMode(GL_BACK, GL_FILL)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        if blend:
            glEnable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        for j in range(0,m-1):
            for i in range(0,n-1):
                glBegin(GL_QUADS)

                [x,y,z] = P[i+1,j,:]
                glColor4f(*self.NurbsColor)
                glVertex(x,y,z)

                [x,y,z] = P[i+1,j+1,:]
                glColor4f(*self.NurbsColor)
                glVertex(x,y,z)

                [x,y,z] = P[i,j+1,:]
                glColor4f(*self.NurbsColor)
                glVertex(x,y,z)

                [x,y,z] = P[i,j,:]
                glColor4f(*self.NurbsColor)
                glVertex(x,y,z)

                glEnd()
        if blend:
            glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

    def draw(self, mesh=False, nurbs=True, blend=False):
        if nurbs:
            if self.patch.__class__.__name__ in ["cad_grad_nurbs"]:
                self.drawNurbsByCell(blend=blend)
            else:
                self.drawNurbs(blend=blend)
        if mesh:
            self.drawMesh(blend=blend)


