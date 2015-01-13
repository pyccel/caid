#from ToolsDialog import ToolsDialog
#from CAIDPythonInterpretor import *
import wx
import os
import tempfile

def mktemp():
    fd, name = tempfile.mkstemp()
    os.close(fd)
    return name

class MenuCAIDTools(wx.Menu):

    def __init__(self, parent):

        wx.Menu.__init__(self)
        self.parent = parent
        self._enable_macro_recording = False
        self.initGUI()

    def initGUI(self):

        # add New File in the menu
        self.CommandLineID = wx.NewId()
        self.m_CommandLine = self.Append(self.CommandLineID, "Start Command L&ine\tF9", "Start Command Line.")
        self.PythonEditorID = wx.NewId()
        self.m_PythonEditor = self.Append(self.PythonEditorID, "Python Ed&itor\tF3", "Python Editor.")
        self.EditParametersID = wx.NewId()
        self.m_EditParameters = self.Append(self.EditParametersID, "Edit Parameters", "Edit Parameters.")
        self.AppendSeparator()

        self.MacroRecordingID = wx.NewId()
        self.m_MacroRecording = self.Append(self.MacroRecordingID, "M&acro recording...\tF4", "Macro recording.")
        self.ClearMacroRecordingID = wx.NewId()
        self.m_ClearMacroRecording = self.Append(self.ClearMacroRecordingID, "Cl&ear Macro recording", "Clear Macro recording.")
        self.AppendSeparator()

        # ...
        self.sm_Macros = wx.Menu()

        self.MacroID = wx.NewId()
        self.MacroTokaMeshID = wx.NewId()
        self.MacroMetricID = wx.NewId()
        self.MacroPreProcessTokamakID = wx.NewId()
        self.MacroOptimizationID = wx.NewId()
        self.MacroImportID = wx.NewId()
        self.MacroConnectivityID = wx.NewId()

        self.m_MacroTokaMesh = self.sm_Macros.Append(self.MacroTokaMeshID,  'Tokamesh', kind=wx.ITEM_RADIO)
        self.m_MacroMetric = self.sm_Macros.Append(self.MacroMetricID, 'Metric', kind=wx.ITEM_RADIO)
        self.m_MacroConnectivity = self.sm_Macros.Append(self.MacroConnectivityID, 'Connectivity', kind=wx.ITEM_RADIO)
        self.AppendMenu(self.MacroID, 'Macro', self.sm_Macros)
        # ...

        self.ExecuteEditorID = wx.NewId()
        self.m_ExecuteEditor = self.Append(self.ExecuteEditorID, "Execute Editor", "Execute Editor.")
        self.AppendSeparator()

        self.CustomizeID = wx.NewId()
        self.m_Customize = self.Append(self.CustomizeID, "Cus&tomize", "Customize.")
        self.AppendSeparator()

        # ... deactivate items
        self.m_EditParameters.Enable(False)

        self.m_ClearMacroRecording.Enable(False)

        self.m_MacroMetric.Enable(False)
        self.m_MacroConnectivity.Enable(False)

        self.m_ExecuteEditor.Enable(False)
        self.m_Customize.Enable(False)
        # ...

    def OnCommandLine(self, event):
        import PyShell as py
        self.shell = py.PyShell(self.parent)

    def OnEditParameters(self, event):
        print("OnEditParameters TODO")


    def OnCustomize(self, event):
        print("Customize TODO")

    def OnMacroRecording(self, event):
        wk = self.parent.tree.currentWorkGroup
        if wk is None:
            return

        self._enable_macro_recording = not self._enable_macro_recording

        if self._enable_macro_recording:
            wk.set_macroRecording(True)
            self.m_ClearMacroRecording.Enable(True)
            self.m_MacroRecording.SetText("St&op Macro recording\tF4")
        else:
            wk.set_macroRecording(False)
            self.m_MacroRecording.SetText("M&acro recording...\tF4")
            wk.macro_script.write()

    def OnClearMacroRecording(self, event):
        wk = self.parent.tree.currentWorkGroup
        if wk is None:
            return

        self.m_ClearMacroRecording.Enable(False)

        wk.macro_script.reset()

    def OnPythonEditor(self, event):
        wk = self.parent.tree.currentWorkGroup
        if wk is None:
            return

        # ... using PythonEditor
        _filename = mktemp()
        title = _filename
        try:
            wk.pythonEditor.Show(True)
            wk.pythonEditor.SetTitle(title)
            wk.pythonEditor.DoOpenFile(filename=_filename, last_name_saved=False)
        except:
            # if Editor has been closed
            from PythonEditor import Editor as PythonEditor
            wk.set_pythonEditor(PythonEditor(self.parent, -1, ''))
            wk.pythonEditor.SetTitle(title)
            wk.pythonEditor.DoOpenFile(filename=_filename, last_name_saved=False)
            wk.pythonEditor.Show(True)
        # ...

    def OnMacroMetric(self, event):
        print("OnMacroMetric TODO")

    def OnMacroConnectivity(self, event):
        print("OnMacroConnectivity TODO")

    def OnExecuteEditor(self, event):
        print("OnExecuteEditor TODO")

    def OnMacroTokaMesh(self, event):
        print("OnMacroTokaMesh TODO")
        from tokamesh_interface import PreferencesDialog

        wk = self.parent.tree.currentWorkGroup

        dlg = PreferencesDialog(self.parent, wk.viewer, title="TokaMesh Interface")
        dlg.ShowModal()
        dlg.Destroy()
