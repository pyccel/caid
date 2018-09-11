# -*- coding: UTF-8 -*-
# styled text using wxPython's
# wx.StyledTextCtrl(parent, id, pos, size, style, name)
# set up for folding and Python code highlighting
# source: Dietrich  16NOV2008
# http://www.python-forum.org/pythonforum/viewtopic.php?f=2&t=10065#

import  wx
import  wx.stc  as  stc
import  keyword
import os
import tempfile

def mktemp():
    fd, name = tempfile.mkstemp()
    os.close(fd)
    return name


if wx.Platform == '__WXMSW__':
    # for windows OS
    faces = {
        'times': 'Times New Roman',
        'mono' : 'Courier New',
        # try temporary switch to mono
        'helv' : 'Courier New',
        #'helv' : 'Arial',
        'other': 'Comic Sans MS',
        'size' : 10,
        'size2': 8,
        }
else:
    faces = {
        'times': 'Times',
        'mono' : 'Courier',
        'helv' : 'Helvetica',
        'other': 'new century schoolbook',
        'size' : 12,
        'size2': 10,
        }


class PythonSTC(stc.StyledTextCtrl):
    """
   set up for folding and Python code highlighting
   """
    def __init__(self, parent):
        stc.StyledTextCtrl.__init__(self, parent, wx.ID_ANY)

        # use Python code highlighting
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        # set other options ...
        self.SetProperty("fold", "1")
        self.SetMargins(0, 0)
        self.SetViewWhiteSpace(False)
        self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        self.SetEdgeColumn(78)
        self.SetCaretForeground("blue")

        # setup a margin to hold the fold markers
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        # fold markers use square headers
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,
            stc.STC_MARK_BOXMINUS, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER,
            stc.STC_MARK_BOXPLUS, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,
            stc.STC_MARK_VLINE, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,
            stc.STC_MARK_LCORNER, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,
            stc.STC_MARK_BOXPLUSCONNECTED, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID,
            stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL,
            stc.STC_MARK_TCORNER, "white", "#808080")

        # bind some events ...
        self.Bind(stc.EVT_STC_UPDATEUI, self.onUpdateUI)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.onMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPressed)

        # make some general styles ...
        # global default styles for all languages
        # set default font
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,
            "face:%(helv)s,size:%(size)d" % faces)
        # set default background color
        beige = '#F5F5DC'
        self.StyleSetBackground(style=stc.STC_STYLE_DEFAULT,
            back=beige)
        # reset all to be like the default
        self.StyleClearAll()

        # more global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,
            "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR,
            "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,
            "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,
            "fore:#000000,back:#FF0000,bold")

        # make the Python styles ...
        # default
        self.StyleSetSpec(stc.STC_P_DEFAULT,
            "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE,
            "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
        # number
        self.StyleSetSpec(stc.STC_P_NUMBER,
            "fore:#007F7F,size:%(size)d" % faces)
        # string
        self.StyleSetSpec(stc.STC_P_STRING,
            "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER,
            "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # keyword
        self.StyleSetSpec(stc.STC_P_WORD,
            "fore:#00007F,bold,size:%(size)d" % faces)
        # triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE,
            "fore:#7F0000,size:%(size)d" % faces)
        # triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE,
            "fore:#7F0000,size:%(size)d" % faces)
        # class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME,
            "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME,
            "fore:#007F7F,bold,size:%(size)d" % faces)
        # operators
        self.StyleSetSpec(stc.STC_P_OPERATOR,
            "bold,size:%(size)d" % faces)
        # identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER,
            "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK,
            "fore:#7F7F7F,size:%(size)d" % faces)
        # end of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL,
            "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d"\
                % faces)

        # register some images for use in the AutoComplete box
        self.RegisterImage(1,
            wx.ArtProvider.GetBitmap(wx.ART_TIP, size=(16,16)))
        self.RegisterImage(2,
            wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16,16)))
        self.RegisterImage(3,
            wx.ArtProvider.GetBitmap(wx.ART_COPY, size=(16,16)))

    def onKeyPressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()
        if key == 32 and event.ControlDown():
            pos = self.GetCurrentPos()
            # tips
            if event.ShiftDown():
                self.CallTipSetBackground("yellow")
                self.CallTipShow(pos, 'show tip stuff')
            # code completion (needs more work)
            else:
                kw = keyword.kwlist[:]
                # optionally add more ...
                kw.append("__init__?3")
                # Python sorts are case sensitive
                kw.sort()
                # so this needs to match
                self.AutoCompSetIgnoreCase(False)
                # registered images are specified with appended "?type"
                for i in range(len(kw)):
                    if kw[i] in keyword.kwlist:
                        kw[i] = kw[i] + "?1"
                self.AutoCompShow(0, " ".join(kw))
        else:
            event.Skip()

    def onUpdateUI(self, evt):
        """update the user interface"""
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)
        # check before
        if charBefore and chr(charBefore) in "[]{}()"\
                and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1
        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "[]{}()"\
                    and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos
        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)
        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

    def onMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.foldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())
                if self.GetFoldLevel(lineClicked) &\
                        stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldexpanded(lineClicked, True)
                        self.expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldexpanded(lineClicked):
                            self.SetFoldexpanded(lineClicked, False)
                            self.expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldexpanded(lineClicked, True)
                            self.expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)

    def foldAll(self):
        """folding folds, marker - to +"""
        lineCount = self.GetLineCount()
        expanding = True
        # find out if folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) &\
                    stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldexpanded(lineNum)
                break;
        lineNum = 0
        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) ==\
                    stc.STC_FOLDLEVELBASE:
                if expanding:
                    self.SetFoldexpanded(lineNum, True)
                    lineNum = self.expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldexpanded(lineNum, False)
                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)
            lineNum = lineNum + 1

    def expand(self, line, doexpand, force=False, visLevels=0, level=-1):
        """expanding folds, marker + to -"""
        lastChild = self.GetLastChild(line, level)
        line = line + 1
        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doexpand:
                    self.ShowLines(line, line)
            if level == -1:
                level = self.GetFoldLevel(line)
            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldexpanded(line, True)
                    else:
                        self.SetFoldexpanded(line, False)
                    line = self.expand(line, doexpand, force, visLevels-1)
                else:
                    if doexpand and self.GetFoldexpanded(line):
                        line = self.expand(line, True, force, visLevels-1)
                    else:
                        line = self.expand(line, False, force, visLevels-1)
            else:
                line = line + 1;
        return line


class Editor(wx.Frame):
    def __init__(self, parent, id, title, size=(800, 500)):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=size)

        self.parent = parent

        # variables
        self.modify = False
        self.last_name_saved = ''
        self.replace = False

        # setting up menubar
        menubar = wx.MenuBar()

        file = wx.Menu()
        new = wx.MenuItem(file, 101, '&New\tCtrl+N', 'Creates a new document')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_OTHER, (16,16))
        new.SetBitmap(bmp)
        file.Append(new)

        fopen = wx.MenuItem(file, 102, '&Open\tCtrl+O', 'Open an existing file')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16,16))
        fopen.SetBitmap(bmp)
        file.Append(fopen)
        file.AppendSeparator()

        save = wx.MenuItem(file, 103, '&Save\tCtrl+S', 'Save the file')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, (16,16))
        save.SetBitmap(bmp)
        file.Append(save)

        saveas = wx.MenuItem(file, 104, 'Save &As...\tShift+Ctrl+S', 'Save the file with a different name')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_OTHER, (16,16))
        saveas.SetBitmap(bmp)
        file.Append(saveas)
        file.AppendSeparator()

        quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, (16,16))
        quit.SetBitmap(bmp)
        file.Append(quit)

        edit = wx.Menu()
        cut = wx.MenuItem(edit, 106, '&Cut\tCtrl+X', 'Cut the Selection')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_OTHER, (16,16))
        cut.SetBitmap(bmp)
        edit.Append(cut)

        copy = wx.MenuItem(edit, 107, '&Copy\tCtrl+C', 'Copy the Selection')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_OTHER, (16,16))
        copy.SetBitmap(bmp)
        edit.Append(copy)

        paste = wx.MenuItem(edit, 108, '&Paste\tCtrl+V', 'Paste text from clipboard')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_OTHER, (16,16))
        paste.SetBitmap(bmp)
        edit.Append(paste)

        delete = wx.MenuItem(edit, 109, '&Delete', 'Delete the selected text')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_OTHER, (16,16))
        delete.SetBitmap(bmp)

        edit.Append(delete)
        edit.AppendSeparator()
        edit.Append(110, 'Select &All\tCtrl+A', 'Select the entire text')

        view = wx.Menu()
        view.Append(111, '&Statusbar', 'Show StatusBar')

        help = wx.Menu()
        about = wx.MenuItem(help, 112, '&About\tF1', 'About Editor')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16,16))
        about.SetBitmap(bmp)
        help.Append(about)

        menubar.Append(file, '&File')
        menubar.Append(edit, '&Edit')
        menubar.Append(view, '&View')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.NewApplication, id=101)
        self.Bind(wx.EVT_MENU, self.OnOpenFile, id=102)
        self.Bind(wx.EVT_MENU, self.OnSaveFile, id=103)
        self.Bind(wx.EVT_MENU, self.OnSaveAsFile, id=104)
        self.Bind(wx.EVT_MENU, self.QuitApplication, id=105)
        self.Bind(wx.EVT_MENU, self.OnCut, id=106)
        self.Bind(wx.EVT_MENU, self.OnCopy, id=107)
        self.Bind(wx.EVT_MENU, self.OnPaste, id=108)
        self.Bind(wx.EVT_MENU, self.OnDelete, id=109)
        self.Bind(wx.EVT_MENU, self.OnSelectAll, id=110)
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, id=111)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=112)

        # setting up toolbar
        self.toolbar = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT )
        bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_OTHER, (16,16))
        self.toolbar.AddTool(801, 'New', bmp, '')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16,16))
        self.toolbar.AddTool(802, 'Open', bmp, '')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, (16,16))
        self.toolbar.AddTool(803, 'Save', bmp, '')
        self.toolbar.AddSeparator()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_OTHER, (16,16))
        self.toolbar.AddTool(804, 'Cut', bmp, '')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_OTHER, (16,16))
        self.toolbar.AddTool(805, 'Copy', bmp, '')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_OTHER, (16,16))
        self.toolbar.AddTool(806, 'Paste', bmp, '')
        self.toolbar.AddSeparator()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_OTHER, (16,16))
        self.toolbar.AddTool(807, 'Run', bmp, '')
        self.toolbar.AddSeparator()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, (16,16))
        self.toolbar.AddTool(808, 'Exit', bmp, '')
        self.toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.NewApplication, id=801)
        self.Bind(wx.EVT_TOOL, self.OnOpenFile, id=802)
        self.Bind(wx.EVT_TOOL, self.OnSaveFile, id=803)
        self.Bind(wx.EVT_TOOL, self.OnCut, id=804)
        self.Bind(wx.EVT_TOOL, self.OnCopy, id=805)
        self.Bind(wx.EVT_TOOL, self.OnPaste, id=806)
        self.Bind(wx.EVT_TOOL, self.OnExecute, id=807)
        self.Bind(wx.EVT_TOOL, self.QuitApplication, id=808)

        self._stc_edit = PythonSTC(self)

        # line numbers in the margin
        self._stc_edit.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self._stc_edit.SetMarginWidth(1, 25)

        self.Bind(wx.EVT_CLOSE, self.QuitApplication)

        self.StatusBar()

        self.Centre()
#        self.Show(True)

    @property
    def text(self):
        return self._stc_edit

    def NewApplication(self, event):
        editor = Editor(None, -1, 'Editor')
        editor.Centre()
        editor.Show()

    def OnOpenFile(self, event):
        file_name = os.path.basename(self.last_name_saved)
        if self.modify:
            dlg = wx.MessageDialog(self, 'Save changes?', '', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL |
                        wx.ICON_QUESTION)
            val = dlg.ShowModal()
            if val == wx.ID_YES:
                self.OnSaveFile(event)
                self.DoOpenFile()
            elif val == wx.ID_CANCEL:
                dlg.Destroy()
            else:
                self.DoOpenFile()
        else:
            self.DoOpenFile()

    def DoOpenFile(self, filename=None, last_name_saved=True):
        if filename is None:
            wcd = 'All files (*)|*|Editor files (*.ef)|*.ef|'
            dir = os.getcwd()
            open_dlg = wx.FileDialog(self, message='Choose a file', defaultDir=dir, defaultFile='',
                            wildcard=wcd, style=wx.OPEN|wx.CHANGE_DIR)
            if open_dlg.ShowModal() == wx.ID_OK:
                path = open_dlg.GetPath()
        else:
            path = filename

        try:
            file = open(path, 'r')
            text = file.read()
            file.close()
            # equivalent of GetLastPosition in TextCtrl
            if self.text.DocumentEnd():
                self.text.Clear()
            # equivalent of WriteText in TextCtrl
            self.text.SetText(text)
            if last_name_saved:
                self.last_name_saved = path
            self.statusbar.SetStatusText('', 1)
            self.modify = False

            self.SetTitle(path)

        except IOError as error:
            dlg = wx.MessageDialog(self, 'Error opening file\n' + str(error))
            dlg.ShowModal()

        except UnicodeDecodeError as error:
            dlg = wx.MessageDialog(self, 'Error opening file\n' + str(error))
            dlg.ShowModal()

        if filename is None:
            open_dlg.Destroy()

        return path

    def OnSaveFile(self, event):
        if self.last_name_saved:

            try:
                file = open(self.last_name_saved, 'w')
                # equivalent of GetValue in TextCtrl
                text = self.text.GetText()
                file.write(text)
                file.close()
                self.statusbar.SetStatusText(os.path.basename(self.last_name_saved) + ' saved', 0)
                self.modify = False
                self.statusbar.SetStatusText('', 1)

            except IOError as error:
                dlg = wx.MessageDialog(self, 'Error saving file\n' + str(error))
                dlg.ShowModal()
        else:
            self.OnSaveAsFile(event)

    def OnSaveAsFile(self, event):
        wcd='All files(*)|*|Editor files (*.ef)|*.ef|'
        dir = os.getcwd()
        save_dlg = wx.FileDialog(self, message='Save file as...', defaultDir=dir, defaultFile='',
                        wildcard=wcd, style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if save_dlg.ShowModal() == wx.ID_OK:
            path = save_dlg.GetPath()

            try:
                file = open(path, 'w')
                # equivalent of GetValue in TextCtrl
                text = self.text.GetText()
                file.write(text)
                file.close()
                self.last_name_saved = os.path.basename(path)
                self.statusbar.SetStatusText(self.last_name_saved + ' saved', 0)
                self.modify = False
                self.statusbar.SetStatusText('', 1)

                self.SetTitle(path)

            except IOError as error:
                dlg = wx.MessageDialog(self, 'Error saving file\n' + str(error))
                dlg.ShowModal()
        save_dlg.Destroy()

    def OnCut(self, event):
        self.text.Cut()

    def OnCopy(self, event):
        self.text.Copy()

    def OnPaste(self, event):
        self.text.Paste()

    def QuitApplication(self, event):
        if self.modify:
            dlg = wx.MessageDialog(self, 'Save before Exit?', '', wx.YES_NO | wx.YES_DEFAULT |
                        wx.CANCEL | wx.ICON_QUESTION)
            val = dlg.ShowModal()
            if val == wx.ID_YES:
                self.OnSaveFile(event)
                if not self.modify:
                    wx.Exit()
            elif val == wx.ID_CANCEL:
                dlg.Destroy()
            else:
                self.Destroy()
        else:
            self.Destroy()

    def OnDelete(self, event):
        # delete selection equivalent of self.text.Remove(self.text.GetSelection()) in
        # TextCtrl
        self.text.Clear()

    def OnSelectAll(self, event):
        self.text.SelectAll()

    def OnTextChanged(self, event):
        self.modify = True
        self.statusbar.SetStatusText(' modified', 1)
        event.Skip()

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_INSERT:
            if not self.replace:
                self.statusbar.SetStatusText('INS', 2)
                self.replace = True
            else:
                self.statusbar.SetStatusText('', 2)
                self.replace = False
        event.Skip()

    def ToggleStatusBar(self, event):
        if self.statusbar.IsShown():
            self.statusbar.Hide()
        else:
            self.statusbar.Show()

    def StatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-5, -2, -1])

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, '\tEditor\t\n Another Tutorial\njan bodnar 2005-2006',
                                'About Editor', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExecute(self, event):
        import PyShell as py
        self.shell = py.Interpreter(self.parent, self.last_name_saved)

# --------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    Editor(None, -1, 'Editor').Show()
    app.MainLoop()
