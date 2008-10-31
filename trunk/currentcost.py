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
import os
import sys
import urllib
import urllib2
import cookielib
import pickle 
import wx
import wx.aui
import matplotlib as mpl
import numpy as np
import datetime
import pylab
import xml.parsers.expat
import math
import serial
import datetime
import webbrowser

from googleappengine           import GoogleAppEngine
from googleappengine           import GroupData as CurrentCostGroupData
from currentcostgraphs         import Plot, PlotNotebook, TextPage
from currentcostdatafunctions  import CurrentCostDataFunctions
from currentcostdata           import CurrentCostUpdate
from currentcostvisualisations import CurrentCostVisualisations
from currentcostdb             import CurrentCostDB

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as Toolbar
from matplotlib.dates import DayLocator, HourLocator, MonthLocator, YearLocator, WeekdayLocator, DateFormatter, drange
from matplotlib.patches import Rectangle, Patch
from matplotlib.text import Text



###############################################################################
# 
# CurrentCost
# 
#  A Python application to graphically represent data received from a 
#   CurrentCost meter.
# 
#  Useful links:
#  -------------   
#     Overview of the app
#                            http://currentcost.appspot.com/static/welcome.html
#  
#     Blog posts:
#         1st version of the app              http://dalelane.co.uk/blog/?p=280
#                                             http://dalelane.co.uk/blog/?p=281
#         Re-working the app plans            http://dalelane.co.uk/blog/?p=288
#         Current version of the app          http://dalelane.co.uk/blog/?p=297
#         Seeking feedback                    http://dalelane.co.uk/blog/?p=298
#         Adding web services functions       http://dalelane.co.uk/blog/?p=305
#         Seeking testers for web services    http://dalelane.co.uk/blog/?p=307
# 
#     Providing support
#         http://getsatisfaction.com/dalelane/products/dalelane_currentcost_gui
#
# 
# 
#  Dale Lane (http://dalelane.co.uk/blog)
#
###############################################################################


############################################################################
# 
# OVERVIEW OF THE CODE
# ====================
# 
#   currentcost.py               - main entry function, and implements the 
#                                     GUI's menus and their actions
#   currentcostdata.py           - represents data contained in a single 
#                                     update from a CurrentCost meter
#   currentcostdatafunctions.py  - converts the relative description of usage
#                                     in a CurrentCost update into absolute
#   currentcostdb.py             - sqlite DB to persist CurrentCost usage 
#                                     data, and settings and preferences
#   currentcostgraphs.py         - matplotlib/wxPython code to implement the 
#                                     tabs that make up the GUI
#   currentcostvisualisations.py - draws bar graphs of CurrentCost data
#   googleappengine.py           - gets data from a Google App Engine web 
#                                     service to show other user's data
# 
############################################################################




###############################################################################
# GLOBALS
# 
#   This was initially a hacked-together few hundred lines of script, so 
#    most things were stored in globals. It grew organically, and I've yet
#    to come back and tidy these bits up. 
# 
#   These really don't need to be globals, and the intention is to complete 
#    refactoring of the code so that they are no longer stored here.
# 

#
# these are the different graphs that we draw on
trendspg = None    # trends
axes1 = None       # hours
axes2 = None       # days   
axes3 = None       # months
axes4 = None       # average day
axes5 = None       # average week

# the GUI that we add tabs to
plotter = None

# connection to the database used to store CurrentCost data
ccdb   = CurrentCostDB()

# used to represent a CurrentCost update downloaded from the device
newupd = CurrentCostUpdate ()

# stores the unit to be used in graphs
graphunits = "kWh"


class MyFrame(wx.Frame):
    f1 = None
    MENU_SHOWKWH = None
    MENU_SHOWGBP = None

    def Build_Menus(self):
        global f1, MENU_SHOWKWH, MENU_SHOWGBP

        MENU_HELP    = wx.NewId()
        MENU_CONFIG  = wx.NewId()
        MENU_LOADDB  = wx.NewId()
        MENU_SHOWKWH = wx.NewId()
        MENU_SHOWGBP = wx.NewId()
        MENU_EXPORT1 = wx.NewId()
        MENU_EXPORT2 = wx.NewId()
        MENU_EXPORT3 = wx.NewId()
        MENU_SYNC    = wx.NewId()
        MENU_UPLOAD  = wx.NewId()
        MENU_DNLOAD  = wx.NewId()
        MENU_ACCNT   = wx.NewId()
        MENU_PROFILE = wx.NewId()
        MENU_UPDATES = wx.NewId()
        MENU_BUGREPT = wx.NewId()
        MENU_MANUAL  = wx.NewId()

        menuBar = wx.MenuBar()

        f0 = wx.Menu()
        f0.Append(MENU_CONFIG, "Connect...", "Connect to a CurrentCost meter")

        f1 = wx.Menu()
        f1.Append(MENU_SHOWKWH, "Display kWH", "Show kWH on CurrentCost graphs", kind=wx.ITEM_CHECK)
        f1.Append(MENU_SHOWGBP, "Display GBP", "Show GBP on CurrentCost graphs", kind=wx.ITEM_CHECK)
        f1.Check(MENU_SHOWKWH, True)
        f1.Check(MENU_SHOWGBP, False)

        f2 = wx.Menu()
        f2.Append(MENU_EXPORT1, "Export hours to CSV...", "Export stored two-hourly CurrentCost data to a CSV spreadsheet file")
        f2.Append(MENU_EXPORT2, "Export days to CSV...", "Export stored daily CurrentCost data to a CSV spreadsheet file")
        f2.Append(MENU_EXPORT3, "Export months to CSV...", "Export stored monthly CurrentCost data to a CSV spreadsheet file")
        #f2.AppendSeparator()
        #f2.Append(MENU_MANUAL,  "Import XML", "Manually import XML CurrentCost data")

        f3 = wx.Menu()
        #f3.Append(MENU_UPLOAD,  "Upload data to web...", "Upload CurrentCost data to the web")
        #f3.Append(MENU_DNLOAD,  "Download data from web...", "Download CurrentCost data from your groups from the web")
        f3.Append(MENU_SYNC,  "Sync with web...", "Synchronise your CurrentCost data with the web to see how you compare with your groups")
        f3.AppendSeparator()
        f3.Append(MENU_ACCNT,   "Create account...", "Create an account online to store and access CurrentCost data")
        f3.Append(MENU_PROFILE, "Manage profile...", "Manage online profile")

        f4 = wx.Menu()
        f4.Append(MENU_HELP, "About",  "Show basic info about this app")
        f4.Append(MENU_UPDATES, "Check for updates", "Check that the desktop application is up-to-date")
        f4.Append(MENU_BUGREPT, "Report a bug", "Please use getsatisfaction to report bugs, ask questions, or request features")


        menuBar.Append(f0, "&Options")
        menuBar.Append(f1, "&Data")
        menuBar.Append(f2, "&Export")
        menuBar.Append(f3, "&Web")
        menuBar.Append(f4, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.onAbout,           id=MENU_HELP)
        self.Bind(wx.EVT_MENU, self.onConnect,         id=MENU_CONFIG)
        self.Bind(wx.EVT_MENU, self.onExportHours,     id=MENU_EXPORT1)
        self.Bind(wx.EVT_MENU, self.onExportDays,      id=MENU_EXPORT2)
        self.Bind(wx.EVT_MENU, self.onExportMonths,    id=MENU_EXPORT3)
        self.Bind(wx.EVT_MENU, self.onUploadData,      id=MENU_UPLOAD)
        self.Bind(wx.EVT_MENU, self.onDownloadData,    id=MENU_DNLOAD)
        self.Bind(wx.EVT_MENU, self.onSyncData,        id=MENU_SYNC)
        self.Bind(wx.EVT_MENU, self.onManageAcct,      id=MENU_ACCNT)
        self.Bind(wx.EVT_MENU, self.onManageAcct,      id=MENU_PROFILE)
        self.Bind(wx.EVT_MENU, self.onUpdatesCheck,    id=MENU_UPDATES)
        self.Bind(wx.EVT_MENU, self.onShowWebsite,     id=MENU_BUGREPT)
        self.Bind(wx.EVT_MENU, self.onShowKWH,         id=MENU_SHOWKWH)
        self.Bind(wx.EVT_MENU, self.onShowGBP,         id=MENU_SHOWGBP)
        self.Bind(wx.EVT_MENU, self.getDataFromXML,    id=MENU_MANUAL)


    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1024, 768))
        self.Build_Menus()
        self.statusBar = wx.StatusBar(self, -1)
        self.statusBar.SetFieldsCount(1)
        self.SetStatusBar(self.statusBar)
        iconfile = 'electricity.ico'
        icon1 = wx.Icon(iconfile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon1)


    # display info about the app
    def onAbout (self, event):
        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon('electricity.ico', wx.BITMAP_TYPE_ICO))
        info.SetName('CurrentCost')
        info.Developers = ['Dale Lane']
        info.Description = "Draws interactive graphs using the data from a CurrentCost electricity meter"
        info.Version = "0.9.9"
        info.WebSite = ("http://getsatisfaction.com/dalelane/company_products", "getsatisfaction.com/dalelane")
        wx.AboutBox(info)

    # helper function to update the status bar
    def UpdateStatusBar(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            self.statusBar.SetStatusText(("%.2f kWh" % y), 0)



    #################
    # 
    # web links - launch web pages
    # 
    def onManageAcct(self, event):
        webbrowser.open_new_tab('http://currentcost.appspot.com/profile')

    def onShowWebsite(self, event):
        webbrowser.open_new_tab('http://getsatisfaction.com/dalelane/products/dalelane_currentcost_gui')


    #####################
    # 
    # web services functions - connect to Google App Engine
    # 

    #
    # check with the web service for updates to the client

    def onUpdatesCheck(self, event):
        gae = GoogleAppEngine()
        latestversion = gae.GetDesktopVersion()

        if latestversion == "unknown":
            confdlg = wx.MessageDialog(self,
                                       "Unable to connect to CurrentCost web service",
                                       'CurrentCost', 
                                       style=(wx.OK | wx.ICON_EXCLAMATION))
            result = confdlg.ShowModal()        
            confdlg.Destroy()
        elif latestversion != "0.9.9":
            confdlg = wx.MessageDialog(self,
                                       "A newer version of this application (" + latestversion + ") is available.",
                                       'CurrentCost', 
                                       style=(wx.OK | wx.ICON_EXCLAMATION))
            result = confdlg.ShowModal()        
            confdlg.Destroy()
        else:
            confdlg = wx.MessageDialog(self,
                                       "Your version of the application is up to date.",
                                       'CurrentCost', 
                                       style=(wx.OK | wx.ICON_INFORMATION))
            result = confdlg.ShowModal()        
            confdlg.Destroy()


    # wrapper for upload then download
    def onSyncData(self, event):
        gae = GoogleAppEngine()
        if self.uploadData(gae) == True:
            self.downloadData(gae)

    #
    # download group averages from Google
    
    def onDownloadData(self, event):
        gae = GoogleAppEngine()
        self.downloadData(gae)

    def downloadData(self, gae):
        global plotter, ccdb

        hourDataCollection = ccdb.GetHourDataCollection()
        dayDataCollection = ccdb.GetDayDataCollection()

        ccvis = CurrentCostVisualisations()

        ccdata = CurrentCostDataFunctions()
        averageDayData = ccdata.CalculateAverageDay(hourDataCollection)
        averageWeekData = ccdata.CalculateAverageWeek(dayDataCollection)

        groupdata = gae.DownloadCurrentCostDataFromGoogle(self, ccdb)
        if groupdata:
            for group in groupdata:
                tabname = groupdata[group].groupname + " : week"
                plotter.deletepage(tabname)
                groupdataaxes = plotter.add(tabname).gca()
                ccvis.PlotGroupWeekData(dayDataCollection, averageWeekData, groupdata[group], groupdataaxes)

    #
    # upload user data to Google
    
    def onUploadData(self, event):
        gae = GoogleAppEngine()
        self.uploadData(gae)

    def uploadData(self, gae):
        global ccdb

        confdlg = wx.MessageDialog(self,
                                   "This will upload your historical electricity "
                                   "usage data to a publicly-accessible web server. \n\n"
                                   "Every effort will be made to ensure that this "
                                   "data will only be visible in anonymised forms - "
                                   "such as as a part of averages - and not as "
                                   "individual electricity records identified with "
                                   "specific users. \n\n"
                                   "However, if you have any concerns about this "
                                   "information being public, please click NO now.",
                                   'Are you sure?', 
                                   style=(wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION))
        result = confdlg.ShowModal()        
        confdlg.Destroy()

        if result != wx.ID_YES:
            return

        return gae.UploadCurrentCostDataToGoogle(self, ccdb)


    #####################
    # 
    # export functions - export to CSV

    def onExportHours(self, event):
        global ccdb
        hourDataCollection = ccdb.GetHourDataCollection()
        dialog = wx.FileDialog( None, style = wx.SAVE, wildcard="Comma-separated values files (*.csv)|*.csv")
        if dialog.ShowModal() == wx.ID_OK:
            ccdatafn = CurrentCostDataFunctions()
            ccdatafn.ExportHourData(dialog.GetPath(), hourDataCollection)
            self.SetStatusText("CurrentCost data exported to " + dialog.GetPath())
        dialog.Destroy()

    def onExportDays(self, event):
        global ccdb
        dayDataCollection = ccdb.GetDayDataCollection()
        dialog = wx.FileDialog( None, style = wx.SAVE, wildcard="Comma-separated values files (*.csv)|*.csv")
        if dialog.ShowModal() == wx.ID_OK:
            ccdatafn = CurrentCostDataFunctions()
            ccdatafn.ExportDateData(dialog.GetPath(), dayDataCollection)
            self.SetStatusText("CurrentCost data exported to " + dialog.GetPath())
        dialog.Destroy()

    def onExportMonths(self, event):
        global ccdb
        monthDataCollection = ccdb.GetMonthDataCollection()
        dialog = wx.FileDialog( None, style = wx.SAVE, wildcard="Comma-separated values files (*.csv)|*.csv")
        if dialog.ShowModal() == wx.ID_OK:
            ccdatafn = CurrentCostDataFunctions()
            ccdatafn.ExportDateData(dialog.GetPath(), monthDataCollection)
            self.SetStatusText("CurrentCost data exported to " + dialog.GetPath())
        dialog.Destroy()


    #
    # connect to a CurrentCost meter
    #  
    #  if data is successfully retrieved, then redraw the graphs using the new
    #   data
    # 
    def onConnect (self, event):
        global axes1, axes2, axes3, axes4, axes5, trendspg, ccdb
        dlg = wx.TextEntryDialog(self, 'Specify the COM port to connect to:','CurrentCost')
        lastcom = ccdb.RetrieveSetting("comport")
        if lastcom:
            dlg.SetValue(lastcom)
        if dlg.ShowModal() == wx.ID_OK:
            newcom = dlg.GetValue()
            if lastcom != newcom:
                ccdb.StoreSetting("comport", newcom)
            dialog = wx.ProgressDialog ('CurrentCost', 'Connecting to CurrentCost meter', maximum = 11, style=wx.PD_CAN_ABORT)
            if getDataFromCurrentCostMeter(dlg.GetValue(), dialog) == True:
                drawMyGraphs(axes1, axes2, axes3, axes4, axes5, trendspg, dialog, False)
            dialog.Destroy()
        dlg.Destroy()


    #
    # manually enter XML for parsing - for test use only
    
    def getDataFromXML(self, event):        
        global newupd, ccdb
        # 
        line = ""
        dlg = wx.TextEntryDialog(self, 'Enter the XML:', 'CurrentCost')
        if dlg.ShowModal() == wx.ID_OK:
            line = dlg.GetValue()
    
        try:
            p = xml.parsers.expat.ParserCreate()
            p.StartElementHandler = start_element
            p.EndElementHandler = end_element
            p.CharacterDataHandler = char_data
            p.Parse(line, 1)
        except xml.parsers.expat.ExpatError:
            dialog.Update(1, 'Received invalid data')
            return False
        #
        ccfuncs = CurrentCostDataFunctions()
        ccfuncs.ParseCurrentCostXML(ccdb, newupd)
        # 
        return True


    #
    # redraw the graphs to use kWh as a unit in the graph
    #
    def onShowKWH (self, event):
        global f1, MENU_SHOWKWH, MENU_SHOWGBP, graphunits, axes1, axes2, axes3, axes4, axes5, trendspg

        # update the GUI to show what the user has selected
        f1.Check(MENU_SHOWKWH, True)
        f1.Check(MENU_SHOWGBP, False)
        graphunits = "kWh"

        # redraw the graphs
        progdlg = wx.ProgressDialog ('CurrentCost', 'Initialising CurrentCost data store', maximum = 11, style=wx.PD_CAN_ABORT)
        drawMyGraphs(axes1, axes2, axes3, axes4, axes5, trendspg, progdlg, True)
        progdlg.Destroy()

    #
    # redraw the graphs to use financial cost as the units in the graph
    # 
    def onShowGBP (self, event):
        global f1, MENU_SHOWKWH, MENU_SHOWGBP, ccdb, graphunits, axes1, axes2, axes3, axes4, axes5, trendspg
        #
        dlg = wx.TextEntryDialog(self, 'Cost of electricity (in GBP per kWh):','CurrentCost')
        # retrieve the last-used setting
        lastkwh = ccdb.RetrieveSetting("kwhcost")
        if lastkwh:
            dlg.SetValue(lastkwh)
        if dlg.ShowModal() == wx.ID_OK:
            newkwh = dlg.GetValue()
            test = None
            try:
                # check that we have been given a value that can be turned
                #  into a number
                test = float(newkwh)
            except:
                errdlg = wx.MessageDialog(None,
                                          'Not a number',
                                          'CurrentCost', 
                                          style=(wx.OK | wx.ICON_EXCLAMATION))
                errdlg.ShowModal()        
                errdlg.Destroy()
                f1.Check(MENU_SHOWKWH, True)
                f1.Check(MENU_SHOWGBP, False)
                  
            if test != None:
                if lastkwh != newkwh:
                    ccdb.StoreSetting("kwhcost", newkwh)
                graphunits = "GBP"
                f1.Check(MENU_SHOWKWH, False)
                f1.Check(MENU_SHOWGBP, True)
                progdlg = wx.ProgressDialog ('CurrentCost', 'Initialising CurrentCost data store', maximum = 11, style=wx.PD_CAN_ABORT)    
                drawMyGraphs(axes1, axes2, axes3, axes4, axes5, trendspg, progdlg, True)
                progdlg.Destroy()
        dlg.Destroy()


#####################################
# XML parsing functions
#
def start_element(name, attrs):
    global currentelement
    currentelement = name
def end_element(name):
    global currentelement
    currentelement = "none"
def char_data(data):
    global currentelement, newupd
    newupd.UpdateProperty(currentelement, data)

currentelement = "none"


def getDataFromCurrentCostMeter(portdet, dialog):
    global newupd, ccdb
    # 
    dialog.Update(0, 'Connecting to CurrentCost meter')
    ser = ""
    try:
        # connect to the CurrentCost meter
        ser = serial.Serial(port=portdet, timeout=5)
    except serial.SerialException, msg:
        dialog.Update(11, 'Failed to connect to CurrentCost meter')
        errdlg = wx.MessageDialog(None,
                                  'Serial Exception: ' + str(msg),
                                  'Failed to connect to CurrentCost meter', 
                                  style=(wx.OK | wx.ICON_EXCLAMATION))
        errdlg.ShowModal()        
        errdlg.Destroy()
        return False
    except:
        dialog.Update(11, 'Failed to connect to CurrentCost meter')
        return False
    line = ""

    # we keep trying to get an update from the CurrentCost meter
    #  until we successfully populate the CurrentCost data object
    while newupd.WattsDay01 == -1:
        (tocontinue, toskip) = dialog.Update(1, 'Waiting for data from CurrentCost meter')
        if tocontinue == False:
            dialog.Update(10, 'Cancelled. Closing connection to CurrentCost meter')
            ser.close()
            dialog.Update(11, 'Cancelled.')
            return False
        try:
            line = ser.readline()
            #
            p = xml.parsers.expat.ParserCreate()
            p.StartElementHandler = start_element
            p.EndElementHandler = end_element
            p.CharacterDataHandler = char_data
            p.Parse(line, 1)
        except xml.parsers.expat.ExpatError:
            dialog.Update(1, 'Received incomplete data from CurrentCost meter. Waiting for a new reading')
        except serial.SerialException, err:
            dialog.Update(11, 'Failed to receive data from CurrentCost meter')
            errdlg = wx.MessageDialog(None,
                                      'Serial Exception: ' + str(err),
                                      'Failed to receive data from CurrentCost meter', 
                                      style=(wx.OK | wx.ICON_EXCLAMATION))
            errdlg.ShowModal()        
            errdlg.Destroy()
            ser.Close()
            return False
    #
    ser.close()
    dialog.Update(2, 'Parsing data received from CurrentCost meter')
    #
    ccfuncs = CurrentCostDataFunctions()
    ccfuncs.ParseCurrentCostXML(ccdb, newupd)
    # 
    return True


#
# redraw graphs on each of the tabs
# 
def drawMyGraphs(axes1, axes2, axes3, axes4, axes5, trendspg, dialog, changeaxesonly):
    global ccdb, graphunits

    lastkwh = ccdb.RetrieveSetting("kwhcost")

    hourDataCollection = ccdb.GetHourDataCollection()
    dayDataCollection = ccdb.GetDayDataCollection()
    monthDataCollection = ccdb.GetMonthDataCollection()

    if len(hourDataCollection) == 0:
        dialog.Update(11, 'Data store initialised')
        return

    ccvis = CurrentCostVisualisations()

    dialog.Update(3, 'Charting hourly electricity usage...')
    ccvis.PlotHourlyData(axes1, hourDataCollection, graphunits, lastkwh)

    dialog.Update(4, 'Charting daily electricity usage...')
    ccvis.PlotDailyData(axes2, dayDataCollection, graphunits, lastkwh)

    dialog.Update(5, 'Charting monthly electricity usage...')
    ccvis.PlotMonthlyData(axes3, monthDataCollection, graphunits, lastkwh)

    ccdata = CurrentCostDataFunctions()
    averageDayData = ccdata.CalculateAverageDay(hourDataCollection)
    averageWeekData = ccdata.CalculateAverageWeek(dayDataCollection)

    if changeaxesonly == False:
        dialog.Update(6, 'Identifying electricity usage trends...')
        ccvis.IdentifyTrends(trendspg, hourDataCollection, dayDataCollection, monthDataCollection)

    dialog.Update(7, 'Charting an average day...')
    if averageDayData:
        ccvis.PlotAverageDay(averageDayData, axes4, trendspg, graphunits, lastkwh)

    dialog.Update(8, 'Charting an average week...')
    if averageWeekData:
        ccvis.PlotAverageWeek(averageWeekData, axes5, trendspg, graphunits, lastkwh)

    dialog.Update(9, 'Formatting charts...')
    #    
    daysl = DayLocator() 
    hoursl = HourLocator(range(12,24,12)) 
    datesFmt = DateFormatter('%d %b')
    timesFmt = DateFormatter('%I%p') #('%H:%M')
    axes1.xaxis.set_minor_formatter(timesFmt)
    axes1.xaxis.set_major_formatter(datesFmt)
    axes1.xaxis.set_major_locator(daysl) 
    axes1.xaxis.set_minor_locator(hoursl)    
    # 
    # 
    daysFmt  = DateFormatter('%d')
    mthsFmt  = DateFormatter('%b %y')
    datesl = DayLocator(range(2,31,2)) 
    monthsl = MonthLocator()
    axes2.xaxis.set_major_formatter(mthsFmt)
    axes2.xaxis.set_major_locator(monthsl)
    axes2.xaxis.set_minor_formatter(daysFmt)
    axes2.xaxis.set_minor_locator(datesl)
    #
    monthsFmt = DateFormatter('%b')
    yearsFmt = DateFormatter('%Y')
    axes3.xaxis.set_minor_formatter(monthsFmt)
    monthsl = MonthLocator(range(2,13,1))
    yearsl = YearLocator()
    axes3.xaxis.set_major_locator(yearsl)
    axes3.xaxis.set_minor_locator(monthsl)
    axes3.xaxis.set_major_formatter(yearsFmt)
    #
    axes4.xaxis.set_major_locator(HourLocator(range(1, 24, 2)))
    axes4.xaxis.set_major_formatter(DateFormatter('%H00'))
    #
    axes5.xaxis.set_major_locator(DayLocator(range(0,8,1)))
    axes5.xaxis.set_major_formatter(DateFormatter('%a'))
    #
    dialog.Update(10, 'Complete. Redrawing...')
    #
    try:
        axes1.figure.canvas.draw()
    except:
        plotter.deletepage('hourly')
    try:
        axes2.figure.canvas.draw()
    except:
        plotter.deletepage('daily')
    try:
        axes3.figure.canvas.draw() # error?
    except:
        plotter.deletepage('monthly')
    try:
        axes4.figure.canvas.draw()
    except:
        plotter.deletepage('average day')
    try:
        axes5.figure.canvas.draw()
    except:
        plotter.deletepage('average week')
    dialog.Update(11, 'Complete')


#
# walks the user through connecting to the database used to persist 
#   historical CurrentCost usage data, and settings and preferences
# 
def connectToDatabase():
    global ccdb, axes1, axes2, axes3, axes4, axes5, trendspg

    dbLocation = ""
    askForLocation = False

    currentdir = sys.path[0]

    # special case : py2exe-compiled apps store the zip in a different place
    if os.path.basename(currentdir) == "library.zip":
        currentdir = os.path.join(currentdir, "..")

    settingsfile = os.path.join(currentdir, "currentcost.dat")

    if os.path.isfile(settingsfile) == False:
        welcome = wx.MessageDialog(None,
                                   "It looks like this is the first time that you've used this application.\n\n"
                                   "The first thing that we need to do is to create a local file which the application can use to store historical CurrentCost readings. \n\n"
                                   "Once you click OK, the application will ask you to specify where you want this to be stored.\n\n"
                                   "After doing this, you can use 'Options'->'Connect' to get your first set of data from a connected CurrentCost meter",
                                   'Welcome to CurrentCost!', 
                                   style=(wx.OK | wx.ICON_INFORMATION))
        welcome.ShowModal()        
        welcome.Destroy()
        askForLocation = True
    else:
        settingscontents = open(settingsfile, 'r')
        dbLocation = settingscontents.read()
        settingscontents.close()
        if os.path.isfile(dbLocation) == False:
            askForLocation = True
            errdlg = wx.MessageDialog(None,
                                      "The application failed to find the file used to store CurrentCost data.\n\n"
                                      "Please click 'OK', then help locate the file. \n\n"
                                      "If you no longer have this file, enter the location and name of a new file to create a new data store.",
                                      'Welcome to CurrentCost!', 
                                      style=(wx.OK | wx.ICON_EXCLAMATION))
            errdlg.ShowModal()        
            errdlg.Destroy()


    if askForLocation:
        dialog = wx.FileDialog(None, 
                               style = wx.OPEN, 
                               message="Identify file where CurrentCost data should be stored",
                               wildcard="CurrentCost data files (*.ccd)|*.ccd")
        if dialog.ShowModal() == wx.ID_OK:
            dbLocation = dialog.GetPath()
        else:
            dialog.Destroy()
            byebye = wx.MessageDialog(None,
                                      "The application needs somewhere to store data. \n\n"
                                      "Sorry, without this, we need to end the app now. Hope you try again later!",
                                      'Welcome to CurrentCost!', 
                                      style=(wx.OK | wx.ICON_EXCLAMATION))
            byebye.ShowModal()        
            byebye.Destroy()
            return False
        dialog.Destroy()


    progdlg = wx.ProgressDialog ('CurrentCost', 'Initialising CurrentCost data store', maximum = 11, style=wx.PD_CAN_ABORT)    
    ccdb.InitialiseDB(dbLocation)

    settingscontents = open(settingsfile, 'w')
    settingscontents.write(dbLocation)
    settingscontents.close()

    drawMyGraphs(axes1, axes2, axes3, axes4, axes5, trendspg, progdlg, False)
    progdlg.Destroy()
    return True


def demo():
    app = wx.App()
    frame = MyFrame(None,-1,'CurrentCost')
    #
    global plotter, axes1, axes2, axes3, axes4, axes5, trendspg
    #
    plotter = PlotNotebook(frame)
    # 
    trendspg = plotter.addtextpage('trends')
    axes1    = plotter.add('hourly').gca()
    axes2    = plotter.add('daily').gca()
    axes3    = plotter.add('monthly').gca()    
    axes4    = plotter.add('average day').gca()
    axes5    = plotter.add('average week').gca()
    #
    axes1.figure.canvas.mpl_connect('motion_notify_event', frame.UpdateStatusBar)    
    axes2.figure.canvas.mpl_connect('motion_notify_event', frame.UpdateStatusBar)
    axes3.figure.canvas.mpl_connect('motion_notify_event', frame.UpdateStatusBar)
    axes4.figure.canvas.mpl_connect('motion_notify_event', frame.UpdateStatusBar)
    axes5.figure.canvas.mpl_connect('motion_notify_event', frame.UpdateStatusBar)
    # 
    frame.Show()
    #
    if connectToDatabase() == False:
        return
    app.MainLoop()
    



if __name__ == "__main__": demo()

