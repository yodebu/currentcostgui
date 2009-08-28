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
import urllib
import urllib2
import time
import re

from tracer             import CurrentCostTracer

# this class provides logging and diagnostics
trc = CurrentCostTracer()

#
#  
# 
#  Dale Lane (http://dalelane.co.uk/blog)
# 
class ElectricityGenerationDataSource():

    #
    # get the XML 
    # 
    def DownloadRealtimeXML(self):
        try:
            post_req = urllib2.Request('http://www.bmreports.com/bsp/additional/soapfunctions.php?element=generationbyfueltypetable')
            post_resp = urllib2.urlopen(post_req)
            post_resp_body = post_resp.read()
            return post_resp_body
        except Exception, exc:
            return 'Unable to download XML'

    def generateRE(self, energytype):
        return "<INST.*?<FUEL TYPE=\"" + energytype + "\".*?PCT=\"(.*?)\"></FUEL>.*?</INST>"
    #
    # 
    # 
    def ParseRealtimeXML(self, xml):
        global trc
        trc.FunctionEntry("ParseRealtimeXML")
        #trc.Trace(str(xml))
        energygendata = {}
        energygendata['UNKNOWN'] = 0.0000000000000000000000000001
        ccreadingskeys = [ 'CCGT', 'OCGT', 'OIL', 'COAL', 'NUCLEAR', 'WIND', 'PS', 'NPSHYD', 'OTHER', 'INTFR', 'INTIRL' ]
        for key in ccreadingskeys:
            regexp = self.generateRE(key)
            #trc.Trace(regexp)
            m = re.search(regexp, xml)
            energygendata[key] = float(m.group(1))
            trc.Trace(key + "   >>> " + str(m.group(1)) + "  ===> " + str(energygendata[key]))
            if energygendata[key] == 0.0:
                energygendata[key] = 0.00000000000000000000000001
        #trc.Trace(str(energygendata))
        trc.FunctionExit("ParseRealtimeXML")
        return energygendata
