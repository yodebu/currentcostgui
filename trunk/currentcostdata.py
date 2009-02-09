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
from string import atoi, atof

#
# Represents the data contained in a single update from a CurrentCost meter
#
# It's a Python object representation of the XML - as described here:
# http://cumbers.wordpress.com/2008/05/07/breakdown-of-currentcost-xml-output/
#
# The need for this class was reduced with the creation of the new parser 
# class (currentcostparser.py). It's only now used as a way of passing data back
# from the MQTT class (currentcostmqtt.py).
# 
#  Dale Lane (http://dalelane.co.uk/blog)
# 
class CurrentCostUpdate():
    kWattsHour02 = -1.1
    kWattsHour04 = -1.1
    kWattsHour06 = -1.1
    kWattsHour08 = -1.1
    kWattsHour10 = -1.1
    kWattsHour12 = -1.1
    kWattsHour14 = -1.1
    kWattsHour16 = -1.1
    kWattsHour18 = -1.1
    kWattsHour20 = -1.1
    kWattsHour22 = -1.1
    kWattsHour24 = -1.1
    kWattsHour26 = -1.1
    WattsDay01 = -1
    WattsDay02 = -1
    WattsDay03 = -1
    WattsDay04 = -1
    WattsDay05 = -1
    WattsDay06 = -1
    WattsDay07 = -1
    WattsDay08 = -1
    WattsDay09 = -1
    WattsDay10 = -1
    WattsDay11 = -1
    WattsDay12 = -1
    WattsDay13 = -1
    WattsDay14 = -1
    WattsDay15 = -1
    WattsDay16 = -1
    WattsDay17 = -1
    WattsDay18 = -1
    WattsDay19 = -1
    WattsDay20 = -1
    WattsDay21 = -1
    WattsDay22 = -1
    WattsDay23 = -1
    WattsDay24 = -1
    WattsDay25 = -1
    WattsDay26 = -1
    WattsDay27 = -1
    WattsDay28 = -1
    WattsDay29 = -1
    WattsDay30 = -1
    WattsDay31 = -1
    WattsMonth01 = -1
    WattsMonth02 = -1
    WattsMonth03 = -1
    WattsMonth04 = -1
    WattsMonth05 = -1
    WattsMonth06 = -1
    WattsMonth07 = -1
    WattsMonth08 = -1
    WattsMonth09 = -1
    WattsMonth10 = -1
    WattsMonth11 = -1
    WattsMonth12 = -1


    def UpdateProperty (self, key, value):
      if (key == "h02"):
        self.kWattsHour02 = atof(value)
      elif (key == "h04"):
        self.kWattsHour04 = atof(value)
      elif (key == "h06"):
        self.kWattsHour06 = atof(value)
      elif (key == "h08"):
        self.kWattsHour08 = atof(value)
      elif (key == "h10"):
        self.kWattsHour10 = atof(value)
      elif (key == "h12"):
        self.kWattsHour12 = atof(value)
      elif (key == "h14"):
        self.kWattsHour14 = atof(value)
      elif (key == "h16"):
        self.kWattsHour16 = atof(value)
      elif (key == "h18"):
        self.kWattsHour18 = atof(value)
      elif (key == "h20"):
        self.kWattsHour20 = atof(value)
      elif (key == "h22"):
        self.kWattsHour22 = atof(value)
      elif (key == "h24"):
        self.kWattsHour24 = atof(value)
      elif (key == "h26"):
        self.kWattsHour26 = atof(value)
      elif (key == "d01"):
        self.WattsDay01 = atoi(value)
      elif (key == "d02"):
        self.WattsDay02 = atoi(value)
      elif (key == "d03"):
        self.WattsDay03 = atoi(value)
      elif (key == "d04"):
        self.WattsDay04 = atoi(value)
      elif (key == "d05"):
        self.WattsDay05 = atoi(value)
      elif (key == "d06"):
        self.WattsDay06 = atoi(value)
      elif (key == "d07"):
        self.WattsDay07 = atoi(value)
      elif (key == "d08"):
        self.WattsDay08 = atoi(value)
      elif (key == "d09"):
        self.WattsDay09 = atoi(value)
      elif (key == "d10"):
        self.WattsDay10 = atoi(value)
      elif (key == "d11"):
        self.WattsDay11 = atoi(value)
      elif (key == "d12"):
        self.WattsDay12 = atoi(value)
      elif (key == "d13"):
        self.WattsDay13 = atoi(value)
      elif (key == "d14"):
        self.WattsDay14 = atoi(value)
      elif (key == "d15"):
        self.WattsDay15 = atoi(value)
      elif (key == "d16"):
        self.WattsDay16 = atoi(value)
      elif (key == "d17"):
        self.WattsDay17 = atoi(value)
      elif (key == "d18"):
        self.WattsDay18 = atoi(value)
      elif (key == "d19"):
        self.WattsDay19 = atoi(value)
      elif (key == "d20"):
        self.WattsDay20 = atoi(value)
      elif (key == "d21"):
        self.WattsDay21 = atoi(value)
      elif (key == "d22"):
        self.WattsDay22 = atoi(value)
      elif (key == "d23"):
        self.WattsDay23 = atoi(value)
      elif (key == "d24"):
        self.WattsDay24 = atoi(value)
      elif (key == "d25"):
        self.WattsDay25 = atoi(value)
      elif (key == "d26"):
        self.WattsDay26 = atoi(value)
      elif (key == "d27"):
        self.WattsDay27 = atoi(value)
      elif (key == "d28"):
        self.WattsDay28 = atoi(value)
      elif (key == "d29"):
        self.WattsDay29 = atoi(value)
      elif (key == "d30"):
        self.WattsDay30 = atoi(value)
      elif (key == "d31"):
        self.WattsDay31 = atoi(value)
      elif (key == "m01"):
        self.WattsMonth01 = atoi(value)
      elif (key == "m02"):
        self.WattsMonth02 = atoi(value)
      elif (key == "m03"):
        self.WattsMonth03 = atoi(value)
      elif (key == "m04"):
        self.WattsMonth04 = atoi(value)
      elif (key == "m05"):
        self.WattsMonth05 = atoi(value)
      elif (key == "m06"):
        self.WattsMonth06 = atoi(value)
      elif (key == "m07"):
        self.WattsMonth07 = atoi(value)
      elif (key == "m08"):
        self.WattsMonth08 = atoi(value)
      elif (key == "m09"):
        self.WattsMonth09 = atoi(value)
      elif (key == "m10"):
        self.WattsMonth10 = atoi(value)
      elif (key == "m11"):
        self.WattsMonth11 = atoi(value)
      elif (key == "m12"):
        self.WattsMonth12 = atoi(value)

