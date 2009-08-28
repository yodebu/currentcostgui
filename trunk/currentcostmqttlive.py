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
import os
import sys
import time
import string
from string import atoi, atof

from mqttClient import *
from tracer          import CurrentCostTracer


# this class provides logging and diagnostics
trc = CurrentCostTracer()


#
# Many CurrentCost users have their meters connected to a RSMB (Really Small
#  Message Broker) which means they may not want to disconnect it from this to 
#  be able to use this app. 
#  
# So we provide the ability to receive CurrentCost data via MQTT. This also 
#  lets us use the program remotely.
# 
# This class is used to provide the MQTT connection to download live data.
# 
# 
#  Dale Lane (http://dalelane.co.uk/blog)


class CurrentCostMQTTLiveConnection():

    subscriber = None
    
    #
    # Establish a connection to the MQTT broker
    # 
    def EstablishConnection(self, ipaddr, topicString, guihandle):
        global trc
        trc.FunctionEntry("currentcostmqttlive :: EstablishConnection")

        #
        # try and make the connection to the Broker
        # 
        
        connection = None
        try:
            connection = MqttConnection("currentcostguilive", ipaddr)
            connection.connect()
        except ConnectFailedException, exception:
            guihandle.exitOnError("Unable to connect (" + str(exception) + ")")
            trc.Error("Unable to connect (" + str(exception) + ")")
            trc.FunctionExit("currentcostmqttlive :: EstablishConnection")
            return

        #
        # define a subscription with the Broker
        # 

        subscriber = None
        try:
            self.subscriber = CurrentCostMQTTSubscriber(connection, str(topicString))
            self.subscriber.registerGuiCallbacks(guihandle, connection)
            self.subscriber.subscribe()
        except SubscribeFailedException, exception:
            guihandle.exitOnError("Unable to subscribe to topic (" + str(exception) + ")")
            trc.Error("Unable to connect (" + str(exception) + ")")
            trc.FunctionExit("currentcostmqttlive :: EstablishConnection")
            return

        trc.FunctionExit("currentcostmqttlive :: EstablishConnection")

    #
    # Disconnect from the MQTT broker
    # 
    def Disconnect(self):
        if self.subscriber != None:
            self.subscriber.endconnection()
            
    

#
# Implements the actual MQTT subscriber
# 
class CurrentCostMQTTSubscriber(MqttSubscriber):

    # where to send the data received
    guicallback = None
    # a handle to the MQTT client to use when disconnecting
    mqttconnection = None

    # store handles to use for callbacks
    def registerGuiCallbacks(self, ccgui, connection):
        global trc
        trc.FunctionEntry("CurrentCostMQTTSubscriber :: registerGuiCallbacks")
        self.guicallback = ccgui
        self.mqttconnection = connection
        trc.FunctionExit("CurrentCostMQTTSubscriber :: registerGuiCallbacks")

    # when a message is received, try and cast it to a float value for kwh
    #  and pass it back to the GUI for displaying
    def messageReceived(self, message):
        global trc
        trc.FunctionEntry("CurrentCostMQTTSubscriber :: messageReceived")
        MqttSubscriber.messageReceived(self, message)
        ccreading = None
        try:
            ccreading = float(message.data)
        except:
            trc.Error("Unable to parse reading from meter : " + str(message.data))
            self.guicallback.exitOnError('Unable to parse reading from meter: ' + str(message.data))
            trc.FunctionExit("CurrentCostMQTTSubscriber :: messageReceived")
            return
        self.guicallback.updateGraph(ccreading)
        trc.FunctionExit("CurrentCostMQTTSubscriber :: messageReceived")

    # disconnect when complete
    def endconnection(self):
        try:
            self.unsubscribe()
        except UnsubscribeFailedException, exception:
            # print str(exception)
            noop = 1
        try:
            self.mqttconnection.disconnect()
        except DisconnectFailedException, exception:
            # print str(exception)
            noop = 1

