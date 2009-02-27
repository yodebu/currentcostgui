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
import time


from threading import Thread
from Queue     import Queue

from currentcostdb            import CurrentCostDB
from currentcostdatafunctions import CurrentCostDataFunctions

#
# 
#
#  Dale Lane (http://dalelane.co.uk/blog)
#
class CurrentCostHistoryData():
    #
    # where are we getting live data from?
    CONNECTION_NONE   = 0
    CONNECTION_MQTT   = 1
    CONNECTION_SERIAL = 2

    connectionType = CONNECTION_NONE
    closing = False

    #
    # handle to the GUI where the graph is shown
    guicallback = None

    # background threads actually getting the history data
    mqttClient = None
    comClient  = None
    dbThread   = None


    #
    # called when another CurrentCost reading is available
    # 
    #  the new reading is appended to the set
    # 
    def updateData(self, ccupdate):
        if self.dbThread != None:
            self.dbThread.addNewData(ccupdate)

    #
    # called to create a connection to the CurrentCost meter
    # 
    def connect(self, guihandle, dbFilePath, connType, ipaddr, topic):
        # store globals
        self.connectionType = connType

        if self.connectionType == self.CONNECTION_MQTT:
            self.ipaddress = ipaddr
            self.topicstring = topic
    
            mqttClientModule = __import__("currentcostmqtthistory")
            self.mqttClient = mqttClientModule.CurrentCostMQTTConnection()
    
            backgroundThread = MQTTUpdateThread(self.mqttClient, ipaddr, topic, self)
            backgroundThread.start()

            self.dbThread = DatabaseUpdateThread(dbFilePath)
            self.dbThread.start()
            
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
        self.closing = True

        if self.connectionType == self.CONNECTION_MQTT:
            if self.mqttClient != None:
                self.mqttClient.Disconnect()
        elif self.connectionType == self.CONNECTION_SERIAL:
            if self.comClient != None:
                self.comClient.Disconnect()

        if self.dbThread != None:
            self.dbThread.shutdown()
            

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
    def __init__(self, comclienthandle, comportclass, liveagent):
        Thread.__init__(self)
        self.comClient = comclienthandle
        self.comport = comportclass
        self.graphhandle = liveagent
    def run(self):
        res = self.comClient.EstablishConnection(self.comport, 
                                                 self.graphhandle)


# a background thread used to insert data into the database
class DatabaseUpdateThread(Thread):
    dbloc = None
    pendingUpdates = None
    running = True

    def __init__(self, dblocation):
        Thread.__init__(self)
        self.dbloc = dblocation
        self.pendingUpdates = Queue(0)
    def addNewData(self, newupdate):
        self.pendingUpdates.put(newupdate)
    def shutdown(self):
        self.running = False
        self.pendingUpdates.put(None)
    def run(self):
        ccfuncs = CurrentCostDataFunctions()
        dbconn = CurrentCostDB()

        dbconn.InitialiseDB(self.dbloc)

        while self.running == True:
            # the get operation on a Queue is a blocking get - so we can leave
            # this thread waiting here until new data is received
            # (more efficient than sleeping, and easier than notifying)
            nextupdate = self.pendingUpdates.get()
            if nextupdate != None:
                # adding 'None' to the queue is how we signal a shutdown for 
                #  the thread - this will cause us to drop out of the bottom
                #  of the while loop
                ccfuncs.ParseCurrentCostXML(dbconn, nextupdate)

