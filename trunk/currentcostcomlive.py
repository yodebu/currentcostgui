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

#
#  Makes a direct serial connection to a CurrentCost meter, downloads a 
#   reading and extracts the channel 1 watts reading. This is converted into 
#   a floating point kW value which is returned to the GUI for displaying on 
#   a live data graph.
# 
#  This continues until Disconnect is called, at which point the serial port
#   is closed.
# 
# 
#  Dale Lane (http://dalelane.co.uk/blog)


class CurrentCostSerialConnection():

    #
    # Establish a connection to the CurrentCost meter
    # 
    def EstablishConnection(self, comportobj, guihandle):

        self.ser = comportobj
        self.toCancel = False
        
        #
        # look for the current reading in the data
        # 
        line = ""
        while self.toCancel == False:
            try:
                line = self.ser.readUpdate()
                
                idx = line.find('<ch1><watts>')
                if idx > 0:
                    idx += 12
                    endidx = line.find('</watts></ch1>', idx)
                    if endidx > 0:
                        substr = line[idx : endidx]
                        try:
                            ccreading = float(float(substr) / 1000)
                            guihandle.updateGraph(ccreading)
                        except:            
                            guihandle.exitOnError('Unable to parse reading from meter: ' + str(substr))
                            return
            except Exception, exception:
                if self.toCancel == False:
                    guihandle.exitOnError('Error reading from COM port: ' + str(exception))
                    return

        try:
            self.ser.disconnect()
        except:
            self.guicallback.exitOnError('Error when closing COM port')


    #
    # Disconnect from the MQTT broker
    # 
    def Disconnect(self):
        self.toCancel = True
        self.ser.disconnect()

