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

from string import atoi, atof
import datetime

# this class provides logging and diagnostics
from tracer                 import CurrentCostTracer


trc = CurrentCostTracer()

#
# CurrentCost data parser 
# 
# A CurrentCost update (as described in currentcostdata.py) is a relative
#  description of your electricity usage.
#
# E.g. you used this much electricity 2 hours ago
#
# This class converts this into an absolute description of your electricity
#   usage.
#
# E.g. you used this much electricity at 1pm
# 
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
class CurrentCostDataConverter:


    ###############################################################################
    #
    # timestamp helper functions 
    # 
    ###############################################################################

    #
    # creates absolute datetime object based on num of months ago relative to now
    def GetOldMonth(self, referenceDate, monthsago):
        numyears  = monthsago / 12
        nummonths = monthsago % 12

        newmonth = referenceDate.month - nummonths
        newyear  = referenceDate.year  - numyears

        if newmonth <= 0:
            newmonth += 12
            newyear -= 1

        return datetime.date(newyear, newmonth, 1)
    
    #
    # creates absolute datetime object based on num of days ago relative to now    
    def GetOldDay(self, referenceDate, daysago):
        d = datetime.timedelta(days=daysago)
        basetime = referenceDate - d
        return datetime.date(basetime.year, basetime.month, basetime.day)
    
    #
    # creates absolute datetime object based on num of hours ago relative to now
    def GetOldHour(self, referenceDate, hoursago):
        if referenceDate.hour % 2 == 0:
            hoursago = hoursago + 1

        d = datetime.timedelta(hours=hoursago)
        basetime = referenceDate - d
        return datetime.datetime(basetime.year, basetime.month, basetime.day, basetime.hour, 0, 0)



    # internal function used to convert data from the second generation 
    #  CurrentCost meters (the first to include history data)
    # 
    def storeTimedCurrentCostDatav2(self, reftimestamp, ccdb, hist):
        global trc
        trc.FunctionEntry("storeTimedCurrentCostDatav2")

        # months
        for i in range(1, 10):
            key = "m00" + str(i)
            if key in hist:
                ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, i), atoi(hist['mths'][key]))
        for i in range(10, 13):
            key = "m0" + str(i)
            if key in hist:
                ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, i), atoi(hist['mths'][key]))

        # days
        for i in range(1, 10):
            key = "d00" + str(i)
            if key in hist:
                ccdb.StoreDayData(self.GetOldDay(reftimestamp, i),  atoi(hist['days'][key]))
        for i in range(10, 32):
            key = "d0" + str(i)
            if key in hist:
                ccdb.StoreDayData(self.GetOldDay(reftimestamp, i),  atoi(hist['days'][key]))

        # hours
        for i in range(2, 9, 2):
            key = "h00" + str(i)
            if key in hist:
                ccdb.StoreHourData(self.GetOldHour(reftimestamp, i - 2),  atof(hist['hrs'][key]))
        for i in range(10, 27, 2):
            key = "h0" + str(i)
            if key in hist:
                ccdb.StoreHourData(self.GetOldHour(reftimestamp, i - 2),  atof(hist['hrs'][key]))

        trc.FunctionExit("storeTimedCurrentCostDatav2")


    # internal function used to convert data from the latest generation 
    #  CurrentCost meters (known as cc128)
    # 
    def storeTimedCurrentCostDatavcc128(self, reftimestamp, ccdb, hist):
        global trc
        trc.FunctionEntry("storeTimedCurrentCostDatavcc128")

        # months
        for i in range(1, 10):
            key = "m00" + str(i)
            if key in hist:
                ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, i), atof(hist[key]))
        for i in range(10, 85):
            key = "m0" + str(i)
            if key in hist:
                ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, i), atof(hist[key]))

        # days
        for i in range(1, 10):
            key = "d00" + str(i)
            if key in hist:
                ccdb.StoreDayData(self.GetOldDay(reftimestamp, i),  atof(hist[key]))
        for i in range(10, 91):
            key = "d0" + str(i)
            if key in hist:
                ccdb.StoreDayData(self.GetOldDay(reftimestamp, i),  atof(hist[key]))

        # hours
        for i in range(2, 9, 2):
            key = "h00" + str(i)
            if key in hist:
                ccdb.StoreHourData(self.GetOldHour(reftimestamp, i - 2),  atof(hist[key]))
        for i in range(10, 99, 2):
            key = "h0" + str(i)
            if key in hist:
                ccdb.StoreHourData(self.GetOldHour(reftimestamp, i - 2),  atof(hist[key]))
        for i in range(100, 747, 2):
            key = "h" + str(i)
            if key in hist:
                ccdb.StoreHourData(self.GetOldHour(reftimestamp, i - 2),  atof(hist[key]))

        trc.FunctionExit("storeTimedCurrentCostDatavcc128")
