# -*- coding: utf-8 -*-

#
# CurrentCost parsing
#
#    Copyright (C) 2009  Dale Lane
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

import datetime
import xml.parsers.expat


# this class converts relative timestamps into absolute timestamps
from currentcostdataconvert import CurrentCostDataConverter

# this class provides logging and diagnostics
from tracer                 import CurrentCostTracer


trc = CurrentCostTracer()

#
# CurrentCost XML parser written to handle CC128 data
# 
# Note that this is provided to help get you started, but it lacks careful
#  error-handling or proper documentation.
#
# If you have any questions about it, or even just find it useful, please do
#  let me know - dale.lane@gmail.com
#
#
#  Dale Lane (http://dalelane.co.uk/blog)
#
class CurrentCostDataParser:

    ###############################################################################
    #
    # parser variables
    # 
    ###############################################################################

    # multi-dimensional array used to store a representation of CurrentCost XML
    currentcoststruct = {}
    # stack which is used to keep track of current pointer into the CurrentCost XML
    currentpointer = []
    # how many elements have we seen called <data>?
    data_element_count = 0

    # used to translate relative timestamps in CurrentCost data into timestamps
    converter = CurrentCostDataConverter()


    ###############################################################################
    #
    # data structure functions
    # 
    ###############################################################################

    # Internal function used to support the parser.
    #
    # Inserts new data into the multi-dimensional array
    # 
    # Inputs:
    #   structure - the multi-dimensional array 
    #   ptr - a stack which identifies the array element to add the data to
    #           for example:
    #          e.g. <xml><animal><canine><dog>Pluto</dog></canine></animal></xml>
    #           will result in a stack that looks like 
    #             ['xml','animal','canine','dog']
    #          which is interpreted as a request to add newdata to
    #             structure['xml']['animal']['canine']['dog']
    #   newdata - data to insert
    # 
    # Outputs:
    #   returns a handle to the element inserted into the array
    # 
    def insertIntoStructure(self, structure, ptr, newdata):
        laststructitem = len(structure) - 1
        parent = ptr
        for i, element in enumerate(structure):
            if i == laststructitem:
                parent[element] = newdata
            else:
                if element not in parent:
                    parent[element] = {}
            parent = parent[element]
        return parent


    ###############################################################################
    #
    # XML parsing functions 
    # 
    ###############################################################################
    
    # Internal function used to support the parser.
    #
    # start of an XML element. keep track of where we are in the XML tree
    def start_element(self, name, attrs):    
        element_name = str(name)
        if element_name == 'data':
            # we have treat <data> as a special case, because the CurrentCost XML
            # format has multiple different elements at the same level in the XML
            # tree all called 'data'. 
            # we need to be able to distinguish between them, so we append a unique
            # number to the name
            # this currently has the effect of resulting in matching with the sensor
            # value 
            #   e.g. <data4><sensor>4</sensor></data4>
            # but for now we will treat this as a happy coincidence and avoid 
            # relying on it too heavily, in case this is not always the case
            element_name = 'data' + str(self.data_element_count)
            self.data_element_count += 1
            self.currentpointer.append(element_name)
        else:
            self.currentpointer.append(element_name)
    # Internal function used to support the parser.
    #
    # end of an XML element. keep track of where we are in the XML tree
    def end_element(self, name):
        self.currentpointer.pop()
    # Internal function used to support the parser.
    #
    # XML element contains data - insert into the structure we are creating to 
    #   represent the XML data
    def char_data(self, data):
        ptr = self.insertIntoStructure(self.currentpointer, 
                                       self.currentcoststruct, 
                                       data)

    # External function used to invoke the parser.
    #
    # Parses the provided line of CurrentCost XML data, and returns a 
    # multi-dimensional array representation of the data
    # 
    # Inputs:
    #   xmldata - line of XML data
    # 
    # Outputs:
    #   handle to the internal CurrentCost data structure
    # 
    def parseCurrentCostXML(self, xmldata):
        global trc
        trc.FunctionEntry("parseCurrentCostXML")

        # reset the internal store
        trc.Trace("resetting parser stores")
        self.currentcoststruct = {}
        self.currentpointer = []

        xmldata = xmldata.strip()
        
        while xmldata and not xmldata.startswith("<"):
            trc.Trace("Removing garbage at start of xml data")
            xmldata = xmldata[1:]

        if not xmldata:
            trc.Trace("sanity test - XML packet empty")
            trc.FunctionExit("parseCurrentCostXML")
            return None

        # sanity check before running parser
        if xmldata.startswith('<msg>') == False:
            trc.Trace("sanity test - XML missing opening <msg> tag - aborting")
            trc.Trace(xmldata)
            trc.FunctionExit("parseCurrentCostXML")
            return None
        if xmldata.endswith('</msg>') == False:
            trc.Trace("sanity test - XML missing closing </msg> tag - aborting")
            trc.Trace(xmldata)
            trc.FunctionExit("parseCurrentCostXML")
            return None

        try:
            trc.Trace("creating parser")
            p = xml.parsers.expat.ParserCreate()
            p.StartElementHandler  = self.start_element
            p.EndElementHandler    = self.end_element
            p.CharacterDataHandler = self.char_data
            p.Parse(xmldata, 1)
            trc.Trace("parsed CurrentCost XML")
            trc.FunctionExit("parseCurrentCostXML")
            return self.currentcoststruct
        except xml.parsers.expat.ExpatError, err:
            #print("Received incomplete or invalid data from CurrentCost meter.")            
            # reset the internal stores
            trc.Trace("XML parsing error")
            trc.Trace("ExpatError : " + str(err))
            trc.Trace("resetting parser stores (again)")
            self.currentcoststruct = {}
            self.currentpointer = []
        except Exception, msg:
            #print 'Unknown error: ' + str(msg)
            # reset the internal stores
            trc.Trace("unknown error during XML parsing")
            trc.Trace("Exception : " + str(msg))
            trc.Trace("resetting parser stores (again)")
            self.currentcoststruct = {}
            self.currentpointer = []

        trc.FunctionExit("parseCurrentCostXML")
        return None


    ###############################################################################
    #
    # time conversion functions
    # 
    ###############################################################################

    # External function used to invoke the translation of CurrentCost data into
    #  an data with absolute timestamps, and store in the provided data store
    # 
    # Selects internal functions based on the CurrentCost software version id
    #  stored in the CurrentCost data. 
    # 
    # These internal functions have been moved to a separate class, because 
    #  they're huge! And fairly dull.
    # 
    # Inputs:
    #   ccdb - class where data should be stored
    # 
    # Outputs:
    #   None
    # 
    def storeTimedCurrentCostData(self, ccdb):
        global trc
        trc.FunctionEntry("storeTimedCurrentCostData")

        # prepare a reference timestamp
        today = datetime.datetime.now()

        # the newer CC128 meter splits the history data over multiple updates
        # we use this number to indicate how many updates are remaining
        trc.Trace("initialising 'updatesremaining' to '?'")
        updatesremaining = '?'

        # different versions of the CurrentCost meter stored the version number
        #  in different places - so this if...else sequence is a little over-complex
        trc.Trace("self.currentcoststruct['msg'] == " + str(self.currentcoststruct['msg']))
        if 'src' in self.currentcoststruct['msg']:
            trc.Trace("found 'src' in self.currentcoststruct['msg']")
            trc.Trace("self.currentcoststruct['msg']['src'] == " + str(self.currentcoststruct['msg']['src']))
            if 'sver' in self.currentcoststruct['msg']['src']:
                # version 2  ('classic') CurrentCost meters
                trc.Trace("found 'sver' in self.currentcoststruct['msg']['src']")
                if 'hist' in self.currentcoststruct['msg']:
                    trc.Trace("found 'hist' in self.currentcoststruct['msg']")
                    self.converter.storeTimedCurrentCostDatav2(today, ccdb, self.currentcoststruct['msg']['hist'])
                    updatesremaining = 0
            elif self.currentcoststruct['msg']['src'].startswith('CC128-v'):                
                # version CC128 ('envi') CurrentCost meters
                trc.Trace("CC128 version : " + str(self.currentcoststruct['msg']['src']))
                if 'hist' in self.currentcoststruct['msg']:
                    # for now, only looking at data on sensor 0 - the 'whole house' sensor
                    #  to get different sensor data, change the 'if' statement below
                    trc.Trace("found 'hist' in self.currentcoststruct['msg']")
                    for dataobj in self.currentcoststruct['msg']['hist']:
                        trc.Trace("next data object in self.currentcoststruct['msg']['hist']:")
                        trc.Trace(str(dataobj))
                        if dataobj.startswith('data'):
                            trc.Trace("found data in history")
                            if self.currentcoststruct['msg']['hist'][dataobj]['sensor'] == '0':
                                trc.Trace("storing data for sensor 0")
                                self.converter.storeTimedCurrentCostDatavcc128(today, ccdb, self.currentcoststruct['msg']['hist'][dataobj])                            
                                keys = (self.currentcoststruct['msg']['hist'][dataobj]).keys()
                                keys.sort()
                                for key in keys:
                                    keynumchk = key[0]
                                    # we assume that we wont receive a mixture of key types in one 
                                    #  update (e.g. hours mixed with months)
                                    if keynumchk == 'h':
                                        trc.Trace("received history data containing hourly history data")
                                        keynumstr = key[1:len(key)]
                                        updatesremaining = int(keynumstr) / 2
                                        break
                                    elif keynumchk == 'd':
                                        trc.Trace("received history data containing daily history data")
                                        # the meter can return between 0 and 2 updates with daily data
                                        # and between 0 and 2 updates with monthly data
                                        # so at this point (where we have received an update with days
                                        # in it) we assume that there can be at most 3 updates remaining
                                        updatesremaining = 3
                                        break
                                    elif keynumchk == 'm':
                                        trc.Trace("received history data containing monthly history data")
                                        # the meter can return between 0 and 2 updates with monthly data
                                        # so at this point (where we have received an update with months
                                        # in it) we assume that there can be at most 1 update remaining
                                        updatesremaining = 1
                                        break
                                    else:
                                        trc.Trace("Uknown data in history", keynumchk, self.currentcoststruct['msg']['hist'][dataobj])
                            else:
                                trc.Trace("Got data for sensor %s, sensors others than 0 are not supported yet" % self.currentcoststruct['msg']['hist'][dataobj]['sensor'] + str( self.currentcoststruct['msg']['hist'][dataobj]))

                else:
                    trc.Trace("This is not a history packet, ignoring: " + str( self.currentcoststruct))
            else:
                trc.Trace("Unknow currentcost hardware version for xmldata: " + str( self.currentcoststruct))
        else:
            trc.Trace("<src> not found in <msg>, Unknow xml format: " + str( self.currentcoststruct))


        trc.FunctionExit("storeTimedCurrentCostData")
        return updatesremaining
