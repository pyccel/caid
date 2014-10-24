# -*- coding: UTF-8 -*-
import sys
import numpy as np
from numpy import array, linspace, zeros, zeros_like
from caid.cad_geometry import cad_geometry
#from igakit.graphics import glFreeType

try:
    from OpenGL.arrays import vbo
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
except:
    print '''ERROR: PyOpenGL not installed properly.'''



def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source )
    glCompileShader(shader)

    status = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not status:
        print_log(shader)
        glDeleteShader(shader)
        raise ValueError, 'Shader compilation failed'
    return shader

def compile_program(vertex_source, fragment_source):
    vertex_shader = None
    fragment_shader = None
    program = glCreateProgram()

    if vertex_source:
        vertex_shader = compile_shader(vertex_source, GL_VERTEX_SHADER)
        glAttachShader(program, vertex_shader)
    if fragment_source:
        fragment_shader = compile_shader(fragment_source, GL_FRAGMENT_SHADER)
        glAttachShader(program, fragment_shader)

    glLinkProgram(program)

    if vertex_shader:
        glDeleteShader(vertex_shader)
    if fragment_shader:
        glDeleteShader(fragment_shader)

    return program

def print_log(shader):
    length = glGetShaderiv(shader, GL_INFO_LOG_LENGTH )

    if length > 0:
        log = glGetShaderInfoLog(shader, length)
        print log

def display_text( value, x,y,  windowHeight, windowWidth, step = 18, color=[1.,0.,0.] ):
    """
    Draw the given text at given 2D position in window
    """
    glMatrixMode(GL_PROJECTION)
    glColor3f(*color)
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    # glPushMatrix()
    matrix = glGetDouble( GL_PROJECTION_MATRIX )

    glLoadIdentity();
    glOrtho(0.0, windowHeight or 32, 0.0, windowWidth or 32, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();
    glRasterPos2i(x, y);
    lines = 0
    for character in value:
        if character == '\n':
            glRasterPos2i(x, y-(lines*18))
        else:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character));
    glPopMatrix();
    glMatrixMode(GL_PROJECTION);
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    # glPopMatrix();
    glLoadMatrixd( matrix ) # should have un-decorated alias for this...

    glMatrixMode(GL_MODELVIEW);

class viewer(object):
    def __init__(self, title="", size=(100,100) \
                 , str_VS=None, str_FS=None, vertex_shader=GL_QUADS \
                , backGroundColor=(1.0, 1.0, 1.0, 0.0) \
                , vbo  = None \
                , menu = None):
        self._program         = None
        self._str_VS          = None  # vector shader
        self._str_FS          = None  # fragment shader
        self._vertex_shader   = None
        self._vbo             = vbo
        self.v_array          = None
        self._menu            = menu
        self.vmin = self.vmax = None
        self.xmin = self.xmax = None
        self.ymin = self.ymax = None
        self.zmin = self.zmax = None

#        self.g_fViewDistance = 9.
        self.g_fViewDistance = -5.
        self.g_Width = 500
        self.g_Height = 500

        self.g_nearPlane = 1.
        self.g_farPlane = 1000.

        self.action = ""
        self.xStart = yStart = 0.
        self.zoom = 50.

        self.xRotate = 0.
        self.yRotate = 0.
        self.zRotate = 0.

        self.xTrans = 0.
        self.yTrans = 0.

        self._backGroundColor = backGroundColor

        glutInit(sys.argv)
        glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize (self.g_Width, self.g_Height)
        glutInitWindowPosition (*list(size))
        self._windowID = glutCreateWindow (title)

        self.init (str_VS=str_VS, str_FS=str_FS, vertex_shader=vertex_shader)

        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.keyboard)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)

    @property
    def windowID(self):
        return self._windowID

    @property
    def menu(self):
        return self._menu

    @property
    def vbo(self):
        return self._vbo

    def set_vbo(self, v):
        self._vbo = v

    def Refresh(self):
        w = self.g_Width
        h = self.g_Height
        glViewport (0, 0, w, h)
        glutPostRedisplay()

    def Clean(self):
        self.cleanVertexBuffer()

    def resetView(self):
        self.zoom = 50.
        self.xRotate = 0.
        self.yRotate = 0.
        self.zRotate = 0.
        self.xTrans = 0.
        self.yTrans = 0.

        glutPostRedisplay()

    def init(self, str_VS=None, str_FS=None, vertex_shader=GL_QUADS):
        glClearColor (*self._backGroundColor)
        glShadeModel (GL_FLAT)
        if (str_VS is not None) and (str_FS is not None):
            self._str_VS = str_VS
            self._str_FS = str_FS
            self._vertex_shader = vertex_shader
            self._program = compile_program(str_VS, str_FS)
            glUseProgram ( self._program )

    def display(self):
        glClear (GL_COLOR_BUFFER_BIT)
        glLoadIdentity ()             # clear the matrix
        # viewing transformation
#        gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
#        glScalef (1.0, 1.0, 1.0)      # modeling transformation

#        gluLookAt(0, 0, -self.g_fViewDistance, 0, 0, 0, -.1, 0, 0)   #-.1,0,0
        gluLookAt(0.0, 0.0, -self.g_fViewDistance, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)   #-.1,0,0
        # Set perspective (also zoom)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.zoom, float(self.g_Width)/float(self.g_Height),self.g_nearPlane, self.g_farPlane)
        glMatrixMode(GL_MODELVIEW)
        # Render the scene
        self.polarView()

        # ------------------------------
        if self.vbo is not None:
            try:
                self.vbo.bind()
                try:
                    glEnableClientState(GL_VERTEX_ARRAY);
                    glEnableClientState(GL_COLOR_ARRAY);

                    glVertexPointer(3, GL_FLOAT, 24, self.vbo )
                    glColorPointer(3, GL_FLOAT, 24, self.vbo+12 )

                    n = self.vbo.shape[0]
                    glDrawArrays(self._vertex_shader, 0, n)
                finally:
                    self.vbo.unbind()
                    glDisableClientState(GL_VERTEX_ARRAY);
                    glDisableClientState(GL_COLOR_ARRAY);
            finally:
                pass
        # ------------------------------

        glFlush ()

    def reshape (self, w, h):
        self.g_Width = w
        self.g_Height = h

        glViewport (0, 0, w, h)
#        glMatrixMode (GL_PROJECTION)
#        glLoadIdentity ()
#    #    glFrustum (-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
#        glFrustum (1.0, -1.0, -1.0, 1.0, 1.5, 20.0)
#        glMatrixMode (GL_MODELVIEW)

    def polarView(self):
        glTranslatef( self.yTrans/100., 0.0, 0.0 )
        glTranslatef(  0.0, -self.xTrans/100., 0.0)
        glRotatef( -self.zRotate, 0.0, 0.0, 1.0)
        glRotatef( -self.xRotate, 1.0, 0.0, 0.0)
        glRotatef( -self.yRotate, .0, 1.0, 0.0)

    def keyboard(self, key, x, y):
        if key in ['m','M']:
            if self.menu is not None:
                app = wx.App(False)
                frame = ViewerPreferences(self, self.menu)
                app.MainLoop()

#        if key in ['h','H']:
#            glutSetWindow(self.windowID)
#            glutHideWindow()
#        if key in ['s','S']:
#            glutSetWindow(self.windowID)
#            glutShowWindow()
        if key == chr(27):
            import sys
            sys.exit(0)

    def mouse(self, button, state, x, y):
        if (button==GLUT_LEFT_BUTTON):
            if (glutGetModifiers() == GLUT_ACTIVE_SHIFT):
                self.action = "MOVE_EYE_2"
            else:
                self.action = "MOVE_EYE"
        elif (button==GLUT_MIDDLE_BUTTON):
            self.action = "TRANS"
        elif (button==GLUT_RIGHT_BUTTON):
            self.action = "ZOOM"
        self.xStart = x
        self.yStart = y

    def motion(self, x, y):
        if (self.action=="MOVE_EYE"):
            self.xRotate += x - self.xStart
            self.yRotate -= y - self.yStart
        elif (self.action=="MOVE_EYE_2"):
            self.zRotate += y - self.yStart
        elif (self.action=="TRANS"):
            self.xTrans += x - self.xStart
            self.yTrans += y - self.yStart
        elif (self.action=="ZOOM"):
            self.zoom -= y - self.yStart
            if self.zoom > 150.:
                self.zoom = 150.
            elif self.zoom < 1.1:
                self.zoom = 1.1
        else:
            print("unknown action\n", self.action)
        self.xStart = x
        self.yStart = y
        glutPostRedisplay()

    def main(self, *args, **kwargs):
        self.update(*args, **kwargs)

        glutMainLoop()

    def update(self, *args, **kwargs):
        return

    def updateVertexBuffer(self, V):
        V = V.astype(np.float32)
        v_array = zeros((V.shape[0],6))
        v_array[:,:4] = V[:,:4]
        self.appendVertexBuffer(v_array)

        self.xmin = np.min(v_array[:,0])
        self.ymin = np.min(v_array[:,1])
        self.zmin = np.min(v_array[:,2])
        self.vmin = np.min(v_array[:,4])

        self.vmax = np.max(v_array[:,0])
        self.xmax = np.max(v_array[:,1])
        self.ymax = np.max(v_array[:,2])
        self.zmax = np.max(v_array[:,4])

    def finalizeVertexBuffer(self):
        return

    def cleanVertexBuffer(self):
        self.v_array = None

    def appendVertexBuffer(self, v):
        nold = 0
        if self.v_array is not None:
            nold = self.v_array.shape[0]
        nnew = v.shape[0]
#        try:
        v_array = zeros((nold+nnew,6))
        if self.v_array is not None:
            v_array[:nold,:] = self.v_array
        v_array[nold:nold+nnew,:] = v
        v_array = v_array.astype(np.float32)
        v_array = array( v_array, 'f')
        self._vbo = vbo.VBO( v_array )
        self.v_array = v_array
#        except:
#            print "Error occurs with nold ", nold, " nnew ", nnew

########################################################################
import wx
class TabPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self, parent, page, list_btns):
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
        if page == -1:
            self.NextBtn.Disable()

        for info in list_btns:
            idBtn     = info[0]
            labelBtn  = info[1]
            actionBtn = info[2]
            btn = wx.Button(self, id=idBtn, label=labelBtn)
            btn.Bind(wx.EVT_BUTTON, actionBtn)
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

########################################################################
class Action(object):
    def __init__(self, func, label=""):
        def _func(event, *args, **kwargs):
            return func(*args, **kwargs)
        self._func = _func
        self._label = label
        self._id = wx.NewId()

    @property
    def label(self):
        return self._label

    @property
    def action(self):
        return self._func

    @property
    def id(self):
        return self._id

class Menu(object):
    def __init__(self):
        self._currentElt = -1
        self._list = []

    def append(self, list_actions, label=""):
        self._list.append([label, list_actions])

    @property
    def npages(self):
        return len(self._list)

    def next(self):
        if self.npages == 0:
            raise StopIteration
        self._currentElt += 1
        if self._currentElt >= self.npages:
            self._currentElt = -1
            raise StopIteration
        return self._list[self._currentElt]

    def __iter__(self):
        return self

    def __getitem__(self, key):
        return self._list[key]
########################################################################
class ViewerPreferences(wx.Frame):
    """
    Frame that holds all other widgets
    """

    #----------------------------------------------------------------------
    def __init__(self, Viewer, menu):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "",
                          size=(200,500)
                          )
        panel = wx.Panel(self)
        self._viewer = Viewer
        self._menu = menu
        notebook = wx.Notebook(panel)

        nPages = menu.npages
        for ipage in range(0, nPages):
            M = menu[ipage]
            nBtns = len(M[1])
            page_label = M[0]
            list_btns = []
            for action in M[1]:
                btn_id      = action.id
                btn_label   = action.label
                btn_action  = action.action
                list_btns.append([btn_id, btn_label, btn_action])
            itab = TabPanel(notebook, ipage, list_btns)
            notebook.AddPage(itab, page_label)

        self._notebook = notebook

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()

        self.Show()

    @property
    def viewer(self):
        return self._viewer


# ------------------------------------------
if __name__ == "__main__":
    # ------------------------------------------
    # Vertex Shader
    str_VS = """
    varying vec4 vertex_color;
    void main()
    {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    vertex_color = gl_Color;
    }
    """

    # Fragment Shader
    str_FS = """
    varying vec4 vertex_color;
    void main()
    {
    gl_FragColor = vertex_color;
    }
    """
    vertex_shader=GL_TRIANGLES
    my_vbo = vbo.VBO(
            array( [
                [  0, 1, 0,  0,1,0 ],
                [ -1,-1, 0,  1,1,0 ],
                [  1,-1, 0,  0,1,1 ],
                [  2,-1, 0,  1,0,0 ],
                [  4,-1, 0,  0,1,0 ],
                [  4, 1, 0,  0,0,1 ],
                [  2,-1, 0,  1,0,0 ],
                [  4, 1, 0,  0,0,1 ],
                [  2, 1, 0,  0,1,1 ],
            ],'f')
        )
    # ------------------------------------------

    # ------------------------------------------
    def menu_action1(a, b=10):
        print "menu_action1"
    def menu_action2(c=23):
        print "menu_action2"
    def menu_action3():
        print "menu_action3"

    action1_1 = Action(menu_action1, "action1")
    action1_2 = Action(menu_action2, "action2")
    action2_1 = Action(menu_action3, "action3")

    my_menu = Menu()
    my_menu.append([action1_1, action1_2], label="page1")
    my_menu.append([action2_1], label="page2")
    # ------------------------------------------

    V = viewer(title='MyViewer' \
               , str_VS=str_VS, str_FS=str_FS \
               , vertex_shader=vertex_shader \
               , backGroundColor=(0.0, 0.0, 0.0, 0.0) \
              , vbo = my_vbo \
              , menu = my_menu)

    V.main()
