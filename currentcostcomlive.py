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


class CurrentCostSerialLiveConnection():

    numberOfErrors = 0

    #
    # Establish a connection to the CurrentCost meter
    # 
    def EstablishConnection(self, comportobj, guihandle):

        self.ser = comportobj
        self.toCancel = False
        self.numberOfErrors = 0
        
        #
        # look for the current reading in the data
        # 
        line = ""
        while self.toCancel == False:
            try:
                line = self.ser.readUpdate()

                try:
                    ccreading = self.parseLiveXML(line)                
                    guihandle.updateGraph(ccreading)
                except:            
                    # Exiting on a single garbled string from the 
                    #  serial port is a bit extreme - it isn't unusual 
                    #  to get a partial string, particularly if we've 
                    #  been reading from the serial port for a few 
                    #  hours
                    # So we count the number of times we hit an error
                    #  and only exit after we see ten of them
                    if self.numberOfErrors < 10:
                        self.numberOfErrors += 1
                    else:
                        guihandle.exitOnError('Unable to parse reading from meter: ' + str(line))
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
    # Parse live XML
    # 
    # Read a line of XML, identify the three live channel watts values, and 
    #  return the sum of them
    # 
    def parseLiveXML(self, line):

        START_TAG_LENGTH = 12    # 12 is the length of the "<chX><watts>" string
        END_TAG_LENGTH = 14    # 14 is the length of the "</watts></chX>" string

        ccreading = 0

        idx = line.find('<ch1><watts>')
        if idx <= 0:
            raise Exception('Unable to find an opening ch1 tag')
        idx += START_TAG_LENGTH

        endidx = line.find('</watts></ch1>', idx)
        if endidx <= 0:
            raise Exception('Unable to find a closing ch1 tag')

        substr = line[idx : endidx]

        ccreading += float(float(substr) / 1000)

        idx = line.find('<ch2><watts>', endidx)
        if idx <= 0:
            raise Exception('Unable to find an opening ch2 tag')
        idx += START_TAG_LENGTH

        endidx = line.find('</watts></ch2>', idx)
        if endidx <= 0:
            raise Exception('Unable to find a closing ch2 tag')

        substr = line[idx : endidx]

        ccreading += float(float(substr) / 1000)

        idx = line.find('<ch3><watts>', endidx)
        if idx <= 0:
            raise Exception('Unable to find an opening ch3 tag')
        idx += START_TAG_LENGTH

        endidx = line.find('</watts></ch3>', idx)
        if endidx <= 0:
            raise Exception('Unable to find a closing ch3 tag')

        substr = line[idx : endidx]

        ccreading += float(float(substr) / 1000)

        return ccreading



    #
    # Disconnect from the MQTT broker
    # 
    def Disconnect(self):
        self.toCancel = True
        self.ser.disconnect()

