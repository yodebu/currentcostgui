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

    # graph where the live data is shown
    livegraph = None

    #
    # handle to the GUI where the graph is shown
    guicallback = None

    #
    # live data store - dates and the readings
    #  assuming equivalent indices - e.g. the third date goes with
    #       the third reading
    ccdates = []
    ccreadings = []

    # background threads actually getting the live data
    mqttClient = None
    comClient  = None


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
        # disconnect from MQTT 
        if self.connectionType == self.CONNECTION_MQTT:
            if self.mqttClient != None:
                self.mqttClient.Disconnect()
        elif self.connectionType == self.CONNECTION_SERIAL:
            if self.comClient != None:
                self.comClient.Disconnect()

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
