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
import serial
import time
import string

from currentcostparser import CurrentCostDataParser
from currentcostdb     import CurrentCostDB
from tracer            import CurrentCostTracer 

# class for logging diagnostics
trc = CurrentCostTracer()

#
#  
# 
# 
#  Dale Lane (http://dalelane.co.uk/blog)


class CurrentCostSerialHistoryConnection():

    guicallback = None

    #
    # Establish a connection to the CurrentCost meter
    # 
    def EstablishConnection(self, comportobj, guihandle, dbfilelocation):
        global trc
        trc.FunctionEntry("EstablishConnection")
        self.ser = comportobj
        self.toCancel = False
        self.guicallback = guihandle

        myparser = CurrentCostDataParser()

        #
        # we create our own connection to the database here
        # 
        # we need our own connection to the database because we are running
        #  in a background thread, and pysqlite (used to implement the database) 
        #  cannot reuse a connection across multiple threads
        # the connection is relatively low cost, so having two connections open 
        #  - one for the GUI thread and one for this background worker thread - 
        #  doesn't seem like a burdensome extravagance :-)
        # 
        dbconnection = CurrentCostDB()
        dbconnection.InitialiseDB(dbfilelocation)


        #
        # look for the current reading in the data
        # 
        line = ""
        receivedHistory = False
        while self.toCancel == False:
            try:
                line = self.ser.readUpdate()

                # try to parse the XML
                currentcoststruct = myparser.parseCurrentCostXML(line)
        
                if currentcoststruct != None:
                    if 'hist' in currentcoststruct['msg']:
                        # we have received history data - parse and store the CurrentCost 
                        #  data in the datastore
                        # the parser will return the number of updates still expected 
                        #  (0 if this was the last or only expected update)
                        myparser.storeTimedCurrentCostData(dbconnection)
                        receivedHistory = True
                    elif receivedHistory == True:
                        # we received live data only
                        # if we have received un-graphed history data, we refresh the
                        # graphs now
                        trc.Trace("finished receiving history data - need to redraw graphs")
                        self.guicallback.updateGraphs()
                        receivedHistory = False
                
            except Exception, exception:
                if self.toCancel == False:
                    self.guicallback.exitOnError('Error reading from COM port: ' + str(exception))
                    trc.Error("Error when closing COM port")
                    trc.Error(str(exception))
                    trc.FunctionExit("EstablishConnection")
                    return


        # cleanup
        dbconnection.CloseDB()

        try:
            self.ser.disconnect()
        except Exception, exc:
            self.guicallback.exitOnError('Error when closing COM port')
            trc.Error("Error when closing COM port")
            trc.Error(str(exc))

        trc.FunctionExit("EstablishConnection")

    #
    # Disconnect from the serial port
    # 
    def Disconnect(self):
        self.toCancel = True
        self.ser.disconnect()

