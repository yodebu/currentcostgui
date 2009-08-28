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

import logging

from time import strftime

#
# A class to collect debug and trace information.
#
#
#  Dale Lane (http://dalelane.co.uk/blog)
# 

enableTrace = False

# used for indenting trace
stackDepth = 0
indentStr  = ""

class CurrentCostTracer():

    def EnableTrace(self, val):
        global enableTrace
        enableTrace = val
    def IsTraceEnabled(self):
        global enableTrace
        return enableTrace

    def InitialiseTraceFile(self):
        global enableTrace, stackDepth, indentStr

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            filename='currentcostdiagnostics.log',
                            filemode='w+')

        if enableTrace == True:
            stackDepth = 0
            indentStr  = ""
    
            logging.info("CurrentCost software - v 0.9.28")
            logging.info("-------------------------------")


    def Trace(self, debuginfo):
        global enableTrace, indentStr
        if enableTrace == True:
            logging.debug("DEBUG " + indentStr + " " + debuginfo)

    def Error(self, errorinfo):
        global enableTrace, indentStr        
        logging.error("ERROR " + indentStr + " " + errorinfo)



    def FunctionEntry(self, functionname):
        global enableTrace, indentStr, stackDepth
        if enableTrace == True:
            stackDepth += 1
    
            logging.info("ENTRY " + indentStr + " " + functionname)
    
            self.prepareIndentString()

    def FunctionExit(self, functionname):
        global enableTrace, indentStr, stackDepth
        if enableTrace == True:
            stackDepth -= 1
            self.prepareIndentString()
    
            logging.info("EXIT  " + indentStr + " " + functionname)


    def prepareIndentString(self):
        global indentStr, stackDepth
        indentStr = ""
        for i in range(0, stackDepth):
            indentStr += "  "
