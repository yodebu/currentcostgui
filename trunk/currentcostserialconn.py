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

import serial
import threading       # this class needs to be thread-safe

#
# Opens a serial connection to CurrentCost meters
# 
#  Dale Lane (http://dalelane.co.uk/blog)
# 
class CurrentCostConnection():

    connection = None
    connerr = None

    lock = threading.Lock()

    #
    # connect to the specified COM port (or serial device for Linux etc.)
    # 
    #  it attempts to make connections using settings appropriate to all known
    #   models of CurrentCost meter 
    # 
    #  Input: 'portdet' - the serial device details
    #    (e.g. for Windows, this will be something like 'COM9' and on Linux, it
    #      will be something like '/dev/ttyUSB')
    def connect(self, portdet):

        # check if already connected - reuse existing connection if possible
        if self.connection != None:
            return True

        # the 'classic' meters are still the most common, so we try that first
        try:
            # connect to the CurrentCost meter
            self.connection = serial.Serial(port=portdet, timeout=5)

            # if we are here, we connected successfully

            # we sanity check the data we are receiving - the CC128 will let us
            #  connect okay, but the data is garbage with these settings
            # 
            # we assume that a decent connection should output at least one 
            #  '<' in any 20 bytes of data received
            testdata = self.connection.read(20)
            xmlsearch = testdata.find('<')
            if xmlsearch != -1:
                return True
            else:
                self.connection.close()
        except serial.SerialException, msg:
            # we won't report a failure yet - as we haven't attempted a CC128
            # connection yet
            self.connerr = msg
        except:
            # we won't report a failure yet - as we haven't attempted a CC128
            # connection yet
            self.connerr = msg

        # if we are here, we failed to connect using the 'classic' meter settings
        # so we attempt a connection using CC128 settings now
        try:
            # connect to the CurrentCost meter
            self.connection = serial.Serial(port=portdet,
                                            baudrate=57600,
                                            bytesize=serial.EIGHTBITS,
                                            parity=serial.PARITY_NONE,
                                            stopbits=serial.STOPBITS_ONE,
                                            timeout=3)
            # if we are here, we connected successfully
            return True
        except serial.SerialException, msg:
            # we won't report a failure yet 
            self.connerr = msg
        except:
            # we won't report a failure yet 
            self.connerr = msg

        # if we are here, we failed to connect on both attempts
        raise self.connerr

    #
    # closes any active serial connection
    def disconnect(self):
        if self.connection != None:
            self.connection.close()
            self.connection = None

    #
    # reads a line of XML from any active serial connection
    #   
    #  this class can potentially be used by multiple threads, so it is 
    #   important for synchronisation to be maintained
    # 
    def readUpdate(self):

        if self.connection != None:
            try:
                self.lock.acquire()
                line = self.connection.readline()
                line = line.rstrip('\r\n')
                return line
            except serial.SerialException, err:
                self.disconnect()
                raise err
            except Exception, msg:
                self.disconnect()
                raise msg
            finally:
                self.lock.release()

    #
    # test for connection
    # 
    def isConnected(self):
        return (self.connection != None)
