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

    #
    # called when another CurrentCost reading is available
    # 
    #  the new reading is appended to the set, and the graph is refreshed
    # 
    def updateGraph(self, ccreading):
        try:
            # store the new reading
            self.ccdates.append(datetime.datetime.now())
            self.ccreadings.append(ccreading)

            # update the graph
            self.livegraph.plot_date(self.ccdates, 
                                     self.ccreadings,
                                     'r-')

            # format the dates on the x-axis
            self.livegraph.xaxis.set_major_formatter(DateFormatter('%H:%M.%S'))

            # rotate the axes labels
            for label in self.livegraph.get_xticklabels():
                label.set_picker(True)
                label.set_rotation(90)

            # redraw the graph
            self.livegraph.figure.canvas.draw()
        except Exception, e:
            print str(e)
            print str(e.message)

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
            try:
                # store the new reading
                self.ngdemanddates.append(datetime.datetime.now())
                self.ngdemandreadings.append(ngdemand)
    
                # update the graph
                self.livegraphNGDemand.plot_date(self.ngdemanddates, 
                                                 self.ngdemandreadings,
                                                 'b-')
    
                # format the dates on the x-axis
                self.livegraphNGDemand.xaxis.set_major_formatter(DateFormatter('%H:%M.%S'))
    
                # rotate the axes labels
                for label in self.livegraphNGDemand.get_xticklabels():
                    label.set_picker(True)
                    label.set_rotation(90)

                # redraw the (original) graph - to sync axes
                self.livegraph.figure.canvas.draw()
            except Exception, e:
                print str(e)
                print str(e.message)

        if self.showNationalGridFrequency == True:
            try:
                # store the new reading
                self.ngfreqdates.append(datetime.datetime.now())
                self.ngfreqreadings.append(ngfrequency)
    
                # update the graph
                self.livegraphNGFrequency.plot_date(self.ngfreqdates, 
                                                    self.ngfreqreadings,
                                                    'g-')
    
                # format the dates on the x-axis
                self.livegraphNGFrequency.xaxis.set_major_formatter(DateFormatter('%H:%M.%S'))
    
                # rotate the axes labels
                for label in self.livegraphNGFrequency.get_xticklabels():
                    label.set_picker(True)
                    label.set_rotation(90)

                # redraw the (original) graph - to sync axes
                self.livegraph.figure.canvas.draw()
            except Exception, e:
                print str(e)
                print str(e.message)


    def toggleNationalGridDemandData(self):

        if self.showNationalGridDemand == False:
            self.showNationalGridDemand = True

            self.livegraphNGDemand = self.livegraph.twinx()
            self.livegraphNGDemand.set_ylabel('UK electricity demand (MW)')

            self.ngdClient = NationalGridUpdateThread(self)
            self.ngdClient.start()
        else:
            self.ngdClient.stopUpdates()
            self.showNationalGridDemand = False
          






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
    def __init__(self, comclienthandle, comportstr, liveagent):
        Thread.__init__(self)
        self.comClient = comclienthandle
        self.comport = comportstr
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
        
