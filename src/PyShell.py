import wx
from wx import py
import os
import __main__
from plugin.poisson import run as run_poisson

class PyShell(object):
    def __init__(self, parent):
        self.parent = parent

        # ...
        self.setVisibleVariables()
        # ...

        # ...
        confDir = wx.StandardPaths.Get().GetUserDataDir()
        if not os.path.exists(confDir):
            os.mkdir(confDir)
        fileName = os.path.join(confDir, 'config')

        self.config = wx.FileConfig(localFilename=fileName)
        self.config.SetRecordDefaults(True)

        self.frame = py.shell.ShellFrame(parent=parent,config=self.config, dataDir=confDir)
        self.frame.Show()
        # ...

    def setVisibleVariables(self):
        wk = self.parent.tree.currentWorkGroup

        # ... workgroup
        __main__.__dict__["workgroup"]  = wk
        # ... geometry elements
        __main__.__dict__["geometries"]  = wk.list_geo
        # ...
        __main__.__dict__["run_poisson"]  = run_poisson


class Interpreter(object):
    def __init__(self, parent, filename):
        self.parent = parent
        self._locals = {}

        self._shell = py.interpreter.Interpreter(locals=self._locals)

        # ...
        self.setVisibleVariables()
        # ...

        # ... execute filename
        file = open(filename, 'r')
        text = file.read()
        file.close()

#        self._shell.showtraceback()
        self._shell.runcode(text)
        # ...

    def setVisibleVariables(self):
        wk = self.parent.tree.currentWorkGroup

        # ... workgroup
        __main__.__dict__["workgroup"]  = wk
        # ... geometry elements
        __main__.__dict__["geometries"]  = wk.list_geo
        # ...
        __main__.__dict__["run_poisson"]  = run_poisson


        self._locals["__main__"] = __main__
        # make all __main__.__dict__ variables visible
        for key, value in list(__main__.__dict__.items()):
            pretext = str(key) + " = __main__.__dict__[\"" + str(key) + "\"]"
            self._shell.runsource(pretext)
