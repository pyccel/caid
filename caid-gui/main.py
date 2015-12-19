#!/usr/bin/python
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------

import wxversion
#wxversion.select("2.8")

from mainFrame import *

try:
    import sys
    filenames = sys.argv[1:]
except:
    filenames = None
    pass

from mainFrame import Frame

app = wx.App(redirect=False)   # Error messages go to popup window
top = Frame("CAID", filenames=filenames)
top.Show()
app.MainLoop()
