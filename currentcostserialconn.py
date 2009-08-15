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

from tracer import CurrentCostTracer 

import serial
import threading       # this class needs to be thread-safe

#
# Opens a serial connection to CurrentCost meters
# 
#  Dale Lane (http://dalelane.co.uk/blog)
# 

# class for logging diagnostics
trc = CurrentCostTracer()


class CurrentCostConnection:

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
        global trc
        trc.FunctionEntry("currentcostserialconn :: connect")

        # check if already connected - reuse existing connection if possible
        if self.connection != None:
            trc.Trace("already connected - will reuse existing connection")
            trc.FunctionExit("currentcostserialconn :: connect")
            return True

        # the 'classic' meters are still the most common, so we try that first
        try:
            # connect to the CurrentCost meter
            trc.Trace("creating serial connection definition using port " + portdet + " and timeout of 5 seconds")
            self.connection = serial.Serial(port=portdet, timeout=5)

            # if we are here, we connected successfully

            # we sanity check the data we are receiving - the CC128 will let us
            #  connect okay, but the data is garbage with these settings
            # 
            # we assume that a decent connection should output at least one 
            #  '<' in any 20 bytes of data received
            trc.Trace("connection apparently successful - sanity testing by reading 20 bytes from the meter:")
            testdata = self.connection.read(20)
            trc.Trace(str(testdata))
            xmlsearch = testdata.find('<')
            if xmlsearch != -1:
                trc.Trace("think we connected successfully")
                trc.FunctionExit("currentcostserialconn :: connect")
                return True
            else:
                trc.Trace("think the connection isn't working - so we close this first attempt")
                self.connection.close()
        except serial.SerialException, msg:
            # we won't report a failure yet - as we haven't attempted a CC128
            # connection yet
            trc.Trace("SerialException - failed to connect")
            trc.Trace(str(msg))
            self.connerr = msg
        except:
            # we won't report a failure yet - as we haven't attempted a CC128
            # connection yet
            trc.Trace("Exception - failed to connect")
            trc.Trace(str(msg))
            self.connerr = msg

        # if we are here, we failed to connect using the 'classic' meter settings
        # so we attempt a connection using CC128 settings now
        try:
            # connect to the CurrentCost meter
            trc.Trace("retrying connection using CC128 baud rate using port " + portdet + " and timeout of 3 seconds")
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
            trc.Trace("SerialException - failed to connect")
            trc.Trace(str(msg))
            self.connerr = msg
        except:
            # we won't report a failure yet 
            trc.Trace("Exception - failed to connect")
            trc.Trace(str(msg))
            self.connerr = msg

        trc.FunctionExit("currentcostserialconn :: connect")

        # if we are here, we failed to connect on both attempts
        raise self.connerr

    #
    # closes any active serial connection
    def disconnect(self):
        global trc
        trc.FunctionEntry("currentcostserialconn :: disconnect")
        if self.connection != None:
            trc.Trace("closing connection")
            self.connection.close()
            self.connection = None
        trc.FunctionExit("currentcostserialconn :: disconnect")

    #
    # reads a line of XML from any active serial connection
    #   
    #  this class can potentially be used by multiple threads, so it is 
    #   important for synchronisation to be maintained
    # 
    def readUpdate(self):
        global trc
        trc.FunctionEntry("currentcostserialconn :: readUpdate")
        if self.connection != None:
            try:
                trc.Trace("aquiring sync lock")
                self.lock.acquire()
                line = self.connection.readline()
                line = line.rstrip('\r\n')
                trc.Trace("read a line from currentcost meter:")
                trc.Trace(line)
                trc.FunctionExit("currentcostserialconn :: readUpdate")
                return line
            except serial.SerialException, err:
                trc.Error("encountered error while trying to read from CurrentCost meter")
                trc.Error("SerialException " + str(err))
                self.disconnect()
                trc.FunctionExit("currentcostserialconn :: readUpdate")
                raise err
            except Exception, msg:
                trc.Error("encountered error while trying to read from CurrentCost meter")
                trc.Error("Exception " + str(err))
                self.disconnect()
                trc.FunctionExit("currentcostserialconn :: readUpdate")
                raise msg
            finally:
                trc.Trace("releasing sync lock")
                self.lock.release()
        trc.FunctionExit("currentcostserialconn :: readUpdate")

    #
    # test for connection
    # 
    def isConnected(self):
        global trc
        trc.Trace("currentcostserialconn :: isConnected - returning " + str((self.connection != None)))
        return (self.connection != None)
