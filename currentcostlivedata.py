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
import datetime

from matplotlib.dates import DayLocator, HourLocator, MinuteLocator, DateFormatter
from threading import Thread

from currentcostcomlive import CurrentCostSerialConnection
from nationalgriddata   import NationalGridDataSource

#
# Displays a graph showing live CurrentCost data. 
#
#  Dale Lane (http://dalelane.co.uk/blog)
#
class CurrentCostLiveData():
    #
    # where are we getting live data from?
    CONNECTION_NONE   = 0
    CONNECTION_MQTT   = 1
    CONNECTION_SERIAL = 2

    connectionType = CONNECTION_NONE

    #
    # which other live feeds should be shown?
    showNationalGridDemand = False
    showNationalGridFrequency = False

    # graphs where the live data is shown
    livegraph = None
    livegraphNGDemand    = None
    livegraphNGFrequency = None

    #
    # handle to the GUI where the graph is shown
    guicallback = None

    #
    # live data store - dates and the readings
    #  assuming equivalent indices - e.g. the third date goes with
    #       the third reading
    ccdates = []
    ccreadings = []

    ngdemanddates = []
    ngdemandreadings = []

    ngfreqdates = []
    ngfreqreadings = []

    # background threads actually getting the live data
    mqttClient = None
    comClient  = None
    ngdClient  = None


    starttime = None



    #
    # redraw all active graphs
    # 
    def redrawGraph(self):

        #
        # Step 1:
        #   update the graph plots
        # 
        if len(self.ccdates) > 0:
            try:
                self.livegraph.plot_date(self.ccdates, 
                                         self.ccreadings,
                                         'r-')
            except Exception, e:
                print 'DEBUG: error - failed to plot data on livegraph'
                print e
                print str(e)
                print str(e.message)
                return False
        
        if self.livegraphNGDemand != None and len(self.ngdemanddates) > 0:
            try:
                # update the graph
                self.livegraphNGDemand.plot_date(self.ngdemanddates, 
                                                 self.ngdemandreadings,
                                                 'b-')
            except Exception, e:
                print 'DEBUG: error - failed to plot data on national grid graph'
                print str(e)
                print str(e.message)
                return False
        
        #
        # Step 2: 
        #   disable auto-scaling
        #    there is a bug when use twinx to plot data series for multiple y
        #    axes on a single graph. the scaling sometimes gets out of sync, so
        #    you get two x-axes overlaid on each other, with slightly different
        #    zoom factors
        # 
        #    so we scale all x-axes manually
        # 
        if len(self.ccdates) > 0:
            self.livegraph.set_autoscale_on = False
        if self.livegraphNGDemand != None:
            self.livegraphNGDemand.set_autoscale_on = False
        
        #
        # Step 3:
        #   rotate labels on x-axis
        #    makes the timestamps fit better when rendered vertically
        # 
        try:
            for label in self.livegraph.get_xticklabels():
                label.set_rotation(90)
        except Exception, e:
            print 'DEBUG: error - failed to rotate axis labels on live graph'
            print str(e)
            print str(e.message)
            return False
        if self.livegraphNGDemand != None:
            try:
                for label in self.livegraphNGDemand.get_xticklabels():
                    label.set_rotation(90)
            except Exception, e:
                print 'DEBUG: error - failed to rotate axis labels on NG graph'
                print str(e)
                print str(e.message)
                return False
        
        #
        # Step 4:
        #   manually zoom all graphs to same scale - keeping x-axes in sync
        # 
        endtime = datetime.datetime.now()
        self.livegraph.set_xlim(xmin=self.starttime, xmax=endtime)
        if self.showNationalGridDemand == True:
            self.livegraphNGDemand.set_xlim(xmin=self.starttime, xmax=endtime)
        
        #
        # Step 5:
        #   format x-axis labels
        #    don't know how to switch one of these off, so we create multiple
        #    identical axes, and try to ignore the fact that you can see it's
        #    slightly thicker as drawn twice in the same place!
        try:
            # format the dates on the x-axis
            if len(self.ccdates) > 0:
                self.livegraph.xaxis.set_major_formatter(DateFormatter('%H:%M.%S'))
                self.livegraph.xaxis.set_minor_formatter(DateFormatter('%H:%M.%S'))
            if self.livegraphNGDemand != None:
                self.livegraphNGDemand.xaxis.set_major_formatter(DateFormatter('%H:%M.%S'))
                self.livegraphNGDemand.xaxis.set_minor_formatter(DateFormatter('%H:%M.%S'))
        except Exception, e:
            print 'DEBUG: error - failed to assign xaxis formatters'
            print str(e)
            print str(e.message)
            return False
        
        #
        # Step 6:
        #   final step - redraw all active graphs
        # 
        try:
            self.livegraph.figure.canvas.draw()
        except Exception, e:
            print 'DEBUG: error - failed to redraw live canvas'
            print str(e)
            print str(e.message)
            return False
        if self.livegraphNGDemand != None:
            try:
                self.livegraphNGDemand.figure.canvas.draw()
            except Exception, e:
                print 'DEBUG: error - failed to redraw NG canvas'
                print str(e)
                print str(e.message)
                return False
        
        #
        # graph redraw complete
        return True


    #
    # called when another CurrentCost reading is available
    # 
    #  the new reading is appended to the set, and the graph is refreshed
    # 
    def updateGraph(self, ccreading):
        # store the new reading
        self.ccdates.append(datetime.datetime.now())
        self.ccreadings.append(ccreading)

        # redraw the graph with the new reading
        self.redrawGraph()


    #
    # called to create a connection to the CurrentCost meter
    # 
    def connect(self, guihandle, connType, graphaxes, ipaddr, topic, com):
        # store globals
        self.connectionType = connType
        self.livegraph = graphaxes
        self.guicallback = guihandle

        # prepare graph for drawing
        self.livegraph.cla()
        self.livegraph.set_ylabel('kWh')
        self.livegraph.grid(True)
        self.livegraph.set_autoscale_on = False

        if self.starttime == None:
            self.starttime = datetime.datetime.now()

        if self.connectionType == self.CONNECTION_MQTT:
            self.ipaddress = ipaddr
            self.topicstring = topic
    
            mqttClientModule = __import__("currentcostmqttlive")
            self.mqttClient = mqttClientModule.CurrentCostMQTTConnection()
    
            backgroundThread = MQTTUpdateThread(self.mqttClient, ipaddr, topic, self)
            backgroundThread.start()
        elif self.connectionType == self.CONNECTION_SERIAL:
            self.comport = com

            self.comClient = CurrentCostSerialConnection()

            backgroundThread = SerialUpdateThread(self.comClient, com, self)
            backgroundThread.start()
        else:
            print 'Unsupported connection type'


    # 
    # called to disconnect from the CurrentCost meter
    # 
    #  existing graph should be left untouched
    # 
    def disconnect(self):
        if self.connectionType == self.CONNECTION_MQTT:
            if self.mqttClient != None:
                self.mqttClient.Disconnect()
        elif self.connectionType == self.CONNECTION_SERIAL:
            if self.comClient != None:
                self.comClient.Disconnect()

        if self.ngdClient != None:
            self.ngdClient.stopUpdates()

        # re-initialise variables
        self.connectionType = self.CONNECTION_NONE
        self.livegraph = None

    #
    # called to return an error to the GUI for displaying to the user
    # 
    #  we disconnect before displaying the error
    # 
    def exitOnError(self, errmsg):
        self.disconnect()
        self.guicallback.displayLiveConnectFailure(errmsg)


    #
    # called when another National Grid data is available
    # 
    #  the new reading is appended to the set, and the graph is refreshed
    # 
    def updateNationalGridGraph(self, ngdemand, ngfrequency):

        if self.showNationalGridDemand == True:
            # store the new National Grid data reading
            self.ngdemanddates.append(datetime.datetime.now())
            self.ngdemandreadings.append(ngdemand)

            # if we are also plotting live CurrentCost readings, we allow the 
            #  CurrentCost update function to redraw the graph (otherwise, 
            #  having two threads redrawing the graph at the same time tends to
            #  screw matplotlib up). 
            # if we are only plotting National Grid data, then we need to redraw
            #  the graph now
            if self.connectionType == self.CONNECTION_NONE:
                self.redrawGraph()

        if self.showNationalGridFrequency == True:
            # store the new reading
            self.ngfreqdates.append(datetime.datetime.now())
            self.ngfreqreadings.append(ngfrequency)
    
            # if we are also plotting live CurrentCost readings, we allow the 
            #  CurrentCost update function to redraw the graph (otherwise, 
            #  having two threads redrawing the graph at the same time tends to
            #  screw matplotlib up). 
            # if we are only plotting National Grid data, then we need to redraw
            #  the graph now
            if self.connectionType == self.CONNECTION_NONE:
                self.redrawGraph()




    #
    # stop and start the download and display of national electricity demand
    #  data from the National Grid
    # 
    def toggleNationalGridDemandData(self, livegraphaxes):

        if self.showNationalGridDemand == False:
            # we are not currently showing national demand data, but we 
            #  are about to start
            self.showNationalGridDemand = True

            # if this is a new graph, we need to make a note of the 
            #  far-left x-axis value for zooming purposes
            if self.starttime == None:
                self.starttime = datetime.datetime.now()

            # store a handle to the parent graph if required (only if we 
            #  are viewing National Grid data without personal CurrentCost data)
            if self.livegraph == None:
                self.livegraph = livegraphaxes

            # if we are re-starting an existing graph, we don't need to create
            #  the axes to draw on.
            # otherwise, we create them now
            if self.livegraphNGDemand == None:
                self.livegraphNGDemand = self.livegraph.twinx()
                self.livegraphNGDemand.set_ylabel('UK electricity demand (MW)')

            # create a background thread that will poll the National Grid
            #  website and return national electricity demand values
            self.ngdClient = NationalGridUpdateThread(self)
            self.ngdClient.start()
        else:
            # we are currently showing national demand data, but we are 
            #   about to stop
            self.showNationalGridDemand = False

            # stop the background thread
            self.ngdClient.stopUpdates()





# a background thread used to create an MQTT connection
class MQTTUpdateThread(Thread):
    def __init__(self, mqttclienthandle, ipaddr, topic, liveagent):
        Thread.__init__(self)
        self.mqttClient = mqttclienthandle
        self.ipaddress = ipaddr
        self.topicstring = topic
        self.graphhandle = liveagent
    def run(self):
        res = self.mqttClient.EstablishConnection(self.ipaddress, 
                                                  self.topicstring, 
                                                  self.graphhandle)

# a background thread used to create a serial connection
class SerialUpdateThread(Thread):
    def __init__(self, comclienthandle, comportclass, liveagent):
        Thread.__init__(self)
        self.comClient = comclienthandle
        self.comport = comportclass
        self.graphhandle = liveagent
    def run(self):
        res = self.comClient.EstablishConnection(self.comport, 
                                                 self.graphhandle)

# a background thread used to download National Grid data
class NationalGridUpdateThread(Thread):
    disconnect = False
    ngdata = None
    def __init__(self, liveagent):
        Thread.__init__(self)
        self.graphhandle = liveagent
        self.disconnect = False
        self.ngdata = NationalGridDataSource()
    def stopUpdates(self):
        self.disconnect = True
    def run(self):
        while self.disconnect == False:
            nghtml = self.ngdata.DownloadRealtimeHTML()
            demand, freq = self.ngdata.ParseRealtimeHTML(nghtml)
            self.graphhandle.updateNationalGridGraph(demand, freq)
        

