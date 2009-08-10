# -*- coding: utf-8 -*-

#
# CurrentCost GUI
# 
#    Copyright (C) 2008  Dale Lane
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  The author of this code can be contacted at Dale.Lane@gmail.com
#    Any contact about this application is warmly welcomed.
#
import wx
import wx.aui
import matplotlib as mpl

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx, _load_bitmap
from matplotlib.dates import DayLocator, HourLocator, MonthLocator, YearLocator, WeekdayLocator, DateFormatter, drange
from matplotlib.patches import Rectangle, Patch
from matplotlib.text import Text


#
# Implements the tabs we use in the GUI - either to draw a graph, or a TextPage 
#  for the 'trends' page.
# 
# Also includes a custom toolbar for use with Matplotlib graphs
#
#  Dale Lane (http://dalelane.co.uk/blog)


class Plot(wx.Panel):    
    def __init__(self, parent, id = -1, dpi = None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        self.figure = mpl.figure.Figure(dpi=dpi, figsize=(2,2))
        self.canvas = Canvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas,1,wx.EXPAND)
        sizer.Add(self.toolbar, 0 , wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)


class PlotNotebook(wx.Panel):
    def __init__(self, parent, id = -1):
        # parent is a frame --> MyFrame (wx.Frame)
        wx.Panel.__init__(self, parent, id=id)
        self.nb = wx.aui.AuiNotebook(self, style=wx.aui.AUI_NB_TAB_MOVE)
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def add(self,name="plot"):
        page = Plot(self.nb)
        self.nb.AddPage(page,name)
        return page.figure

    def deletepage(self,pagename):
        for i in range(0, self.nb.GetPageCount()):
           if self.nb.GetPageText(i) == pagename:
                self.nb.DeletePage(i)
                return

    def selectpage(self,pagename):
        for i in range(0, self.nb.GetPageCount()):
           if self.nb.GetPageText(i) == pagename:
                self.nb.SetSelection(i)
                return

    def addtextpage(self,name):
        page = TextPage(self.nb)
        self.nb.AddPage(page,name)
        return page

#
# we override the matplotlib toolbar class to remove the subplots function, 
#  which we do not use
# 
class Toolbar(NavigationToolbar2Wx): 

    ON_CUSTOM_LEFT  = wx.NewId()
    ON_CUSTOM_RIGHT = wx.NewId()

    # rather than copy and edit the whole (rather large) init function, we run
    # the super-classes init function as usual, then go back and delete the 
    # button we don't want
    def __init__(self, plotCanvas):
        CONFIGURE_SUBPLOTS_TOOLBAR_BTN_POSITION = 6
        NavigationToolbar2Wx.__init__(self, plotCanvas)        
        # delete the toolbar button we don't want
        self.DeleteToolByPos(CONFIGURE_SUBPLOTS_TOOLBAR_BTN_POSITION) 
        # add the new toolbar buttons that we do want
        self.AddSimpleTool(self.ON_CUSTOM_LEFT, _load_bitmap('stock_left.xpm'),
                           'Pan to the left', 'Pan graph to the left')
        wx.EVT_TOOL(self, self.ON_CUSTOM_LEFT, self._on_custom_pan_left)
        self.AddSimpleTool(self.ON_CUSTOM_RIGHT, _load_bitmap('stock_right.xpm'),
                           'Pan to the right', 'Pan graph to the right')
        wx.EVT_TOOL(self, self.ON_CUSTOM_RIGHT, self._on_custom_pan_right)

    # in theory this should never get called, because we delete the toolbar 
    #  button that calls it. but in case it does get called (e.g. if there
    # is a keyboard shortcut I don't know about) then we override the method 
    # that gets called - to protect against the exceptions that it throws
    def configure_subplot(self, evt):
        print 'ERROR: This application does not support subplots'

    # pan the graph to the left
    def _on_custom_pan_left(self, evt):
        ONE_SCREEN = 7   # we default to 1 week
        axes = self.canvas.figure.axes[0]
        x1,x2 = axes.get_xlim()
        ONE_SCREEN = x2 - x1
        axes.set_xlim(x1 - ONE_SCREEN, x2 - ONE_SCREEN)
        self.canvas.draw()

    # pan the graph to the right
    def _on_custom_pan_right(self, evt):
        ONE_SCREEN = 7   # we default to 1 week
        axes = self.canvas.figure.axes[0]
        x1,x2 = axes.get_xlim()
        ONE_SCREEN = x2 - x1
        axes.set_xlim(x1 + ONE_SCREEN, x2 + ONE_SCREEN)
        self.canvas.draw()


#
# a GUI tab that we can write text to
# 
#  used to implement the 'trends' page in the GUI
# 
#  includes a helper function to update the text displayed on this page
# 
class TextPage(wx.Panel):
    def __init__(self, parent, id = -1, dpi = None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        #
        self.text = wx.StaticText(self, -1, "Your CurrentCost data", wx.Point(30, 20))
        self.text.SetFont(wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        self.text.SetSize(self.text.GetBestSize())
        #
        self.trend1 = wx.StaticText(self, -1, "will be described here after data is received...", wx.Point(35, 80))
        self.trend1.SetFont(wx.Font(11, wx.DEFAULT, wx.ITALIC, wx.NORMAL))
        self.trend1.SetSize(self.trend1.GetBestSize())
        # 
        self.trend2 = wx.StaticText(self, -1, " ",wx.Point(35, 120))
        self.trend2.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.trend2.SetSize(self.trend2.GetBestSize())
        # 
        self.trend3 = wx.StaticText(self, -1, " ",wx.Point(35, 160))
        self.trend3.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.trend3.SetSize(self.trend3.GetBestSize())
        #
        self.trend4 = wx.StaticText(self, -1, " ",wx.Point(35, 200))
        self.trend4.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.trend4.SetSize(self.trend4.GetBestSize())
        # 
        self.trend5 = wx.StaticText(self, -1, " ",wx.Point(35, 240))
        self.trend5.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.trend5.SetSize(self.trend5.GetBestSize())
        # 
        self.trend6 = wx.StaticText(self, -1, " ",wx.Point(35, 280))
        self.trend6.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.trend6.SetSize(self.trend6.GetBestSize())
        # 
        self.figure = mpl.figure.Figure(dpi=dpi, figsize=(2,2))

    def UpdateTrendText(self, trendnum, trendtext):
        if trendnum == 1:
            self.trend1.SetLabel(trendtext)
            self.trend1.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
            self.trend1.SetSize(self.trend1.GetBestSize())
        elif trendnum == 2:
            self.trend2.SetLabel(trendtext)
        elif trendnum == 3:
            self.trend3.SetLabel(trendtext)
        elif trendnum == 4:
            self.trend4.SetLabel(trendtext)
        elif trendnum == 5:
            self.trend5.SetLabel(trendtext)
        elif trendnum == 6:
            self.trend6.SetLabel(trendtext)
