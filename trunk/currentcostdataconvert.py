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
        # months
        ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 1),  atoi(hist['mths']['m01']))
        ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 2),  atoi(hist['mths']['m02']))
        ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 3),  atoi(hist['mths']['m03']))
        ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 4),  atoi(hist['mths']['m04']))
        ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 5),  atoi(hist['mths']['m05']))
        ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 6),  atoi(hist['mths']['m06']))
        ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 7),  atoi(hist['mths']['m07']))
        ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 8),  atoi(hist['mths']['m08']))
        ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 9),  atoi(hist['mths']['m09']))
        ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 10), atoi(hist['mths']['m10']))
        ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 11), atoi(hist['mths']['m11']))
        ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 12), atoi(hist['mths']['m12']))
        # days
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 1),  atoi(hist['days']['d01']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 2),  atoi(hist['days']['d02']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 3),  atoi(hist['days']['d03']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 4),  atoi(hist['days']['d04']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 5),  atoi(hist['days']['d05']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 6),  atoi(hist['days']['d06']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 7),  atoi(hist['days']['d07']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 8),  atoi(hist['days']['d08']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 9),  atoi(hist['days']['d09']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 10), atoi(hist['days']['d10']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 11), atoi(hist['days']['d11']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 12), atoi(hist['days']['d12']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 13), atoi(hist['days']['d13']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 14), atoi(hist['days']['d14']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 15), atoi(hist['days']['d15']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 16), atoi(hist['days']['d16']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 17), atoi(hist['days']['d17']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 18), atoi(hist['days']['d18']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 19), atoi(hist['days']['d19']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 20), atoi(hist['days']['d20']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 21), atoi(hist['days']['d21']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 22), atoi(hist['days']['d22']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 23), atoi(hist['days']['d23']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 24), atoi(hist['days']['d24']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 25), atoi(hist['days']['d25']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 26), atoi(hist['days']['d26']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 27), atoi(hist['days']['d27']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 28), atoi(hist['days']['d28']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 29), atoi(hist['days']['d29']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 30), atoi(hist['days']['d30']))
        ccdb.StoreDayData(self.GetOldDay(reftimestamp, 31), atoi(hist['days']['d31']))
        # hours
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 0),  atof(hist['hrs']['h02']))
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 2),  atof(hist['hrs']['h04']))
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 4),  atof(hist['hrs']['h06']))
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 6),  atof(hist['hrs']['h08']))
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 8),  atof(hist['hrs']['h10']))
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 10), atof(hist['hrs']['h12']))
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 12), atof(hist['hrs']['h14']))
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 14), atof(hist['hrs']['h16']))
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 16), atof(hist['hrs']['h18']))
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 18), atof(hist['hrs']['h20']))
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 20), atof(hist['hrs']['h22']))
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 22), atof(hist['hrs']['h24']))
        ccdb.StoreHourData(self.GetOldHour(reftimestamp, 24), atof(hist['hrs']['h26']))


    # internal function used to convert data from the latest generation 
    #  CurrentCost meters (known as cc128)
    # 
    def storeTimedCurrentCostDatavcc128(self, reftimestamp, ccdb, hist):
        # months
        if 'm001' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 1),  atof(hist['m001']))
        if 'm002' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 2),  atof(hist['m002']))
        if 'm003' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 3),  atof(hist['m003']))
        if 'm004' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 4),  atof(hist['m004']))
        if 'm005' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 5),  atof(hist['m005']))
        if 'm006' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 6),  atof(hist['m006']))
        if 'm007' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 7),  atof(hist['m007']))
        if 'm008' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 8),  atof(hist['m008']))
        if 'm009' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 9),  atof(hist['m009']))
        if 'm010' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 10), atof(hist['m010']))
        if 'm011' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 11), atof(hist['m011']))
        if 'm012' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 12), atof(hist['m012']))
        if 'm013' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 13), atof(hist['m013']))
        if 'm014' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 14), atof(hist['m014']))
        if 'm015' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 15), atof(hist['m015']))
        if 'm016' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 16), atof(hist['m016']))
        if 'm017' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 17), atof(hist['m017']))
        if 'm018' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 18), atof(hist['m018']))
        if 'm019' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 19), atof(hist['m019']))
        if 'm020' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 20), atof(hist['m020']))
        if 'm021' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 21), atof(hist['m021']))
        if 'm022' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 22), atof(hist['m022']))
        if 'm023' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 23), atof(hist['m023']))
        if 'm024' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 24), atof(hist['m024']))
        if 'm025' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 25), atof(hist['m025']))
        if 'm026' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 26), atof(hist['m026']))
        if 'm027' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 27), atof(hist['m027']))
        if 'm028' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 28), atof(hist['m028']))
        if 'm029' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 29), atof(hist['m029']))
        if 'm030' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 30), atof(hist['m030']))
        if 'm031' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 31), atof(hist['m031']))
        if 'm032' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 32), atof(hist['m032']))
        if 'm033' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 33), atof(hist['m033']))
        if 'm034' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 34), atof(hist['m034']))
        if 'm035' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 35), atof(hist['m035']))
        if 'm036' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 36), atof(hist['m036']))
        if 'm037' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 37), atof(hist['m037']))
        if 'm038' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 38), atof(hist['m038']))
        if 'm039' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 39), atof(hist['m039']))
        if 'm040' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 40), atof(hist['m040']))
        if 'm041' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 41), atof(hist['m041']))
        if 'm042' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 42), atof(hist['m042']))
        if 'm043' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 43), atof(hist['m043']))
        if 'm044' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 44), atof(hist['m044']))
        if 'm045' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 45), atof(hist['m045']))
        if 'm046' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 46), atof(hist['m046']))
        if 'm047' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 47), atof(hist['m047']))
        if 'm048' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 48), atof(hist['m048']))
        if 'm049' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 49), atof(hist['m049']))
        if 'm050' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 50), atof(hist['m050']))
        if 'm051' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 51), atof(hist['m051']))
        if 'm052' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 52), atof(hist['m052']))
        if 'm053' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 53), atof(hist['m053']))
        if 'm054' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 54), atof(hist['m054']))
        if 'm055' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 55), atof(hist['m055']))
        if 'm056' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 56), atof(hist['m056']))
        if 'm057' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 57), atof(hist['m057']))
        if 'm058' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 58), atof(hist['m058']))
        if 'm059' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 59), atof(hist['m059']))
        if 'm060' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 60), atof(hist['m060']))
        if 'm061' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 61), atof(hist['m061']))
        if 'm062' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 62), atof(hist['m062']))
        if 'm063' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 63), atof(hist['m063']))
        if 'm064' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 64), atof(hist['m064']))
        if 'm065' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 65), atof(hist['m065']))
        if 'm066' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 66), atof(hist['m066']))
        if 'm067' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 67), atof(hist['m067']))
        if 'm068' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 68), atof(hist['m068']))
        if 'm069' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 69), atof(hist['m069']))
        if 'm070' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 70), atof(hist['m070']))
        if 'm071' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 71), atof(hist['m071']))
        if 'm072' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 72), atof(hist['m072']))
        if 'm073' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 73), atof(hist['m073']))
        if 'm074' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 74), atof(hist['m074']))
        if 'm075' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 75), atof(hist['m075']))
        if 'm076' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 76), atof(hist['m076']))
        if 'm077' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 77), atof(hist['m077']))
        if 'm078' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 78), atof(hist['m078']))
        if 'm079' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 79), atof(hist['m079']))
        if 'm080' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 80), atof(hist['m080']))
        if 'm081' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 81), atof(hist['m081']))
        if 'm082' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 82), atof(hist['m082']))
        if 'm083' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 83), atof(hist['m083']))
        if 'm084' in hist:
            ccdb.StoreMonthData(self.GetOldMonth(reftimestamp, 84), atof(hist['m084']))

        # days
        if 'd001' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 1),  atof(hist['d001']))
        if 'd002' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 2),  atof(hist['d002']))
        if 'd003' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 3),  atof(hist['d003']))
        if 'd004' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 4),  atof(hist['d004']))
        if 'd005' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 5),  atof(hist['d005']))
        if 'd006' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 6),  atof(hist['d006']))
        if 'd007' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 7),  atof(hist['d007']))
        if 'd008' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 8),  atof(hist['d008']))
        if 'd009' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 9),  atof(hist['d009']))
        if 'd010' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 10), atof(hist['d010']))
        if 'd011' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 11), atof(hist['d011']))
        if 'd012' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 12), atof(hist['d012']))
        if 'd013' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 13), atof(hist['d013']))
        if 'd014' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 14), atof(hist['d014']))
        if 'd015' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 15), atof(hist['d015']))
        if 'd016' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 16), atof(hist['d016']))
        if 'd017' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 17), atof(hist['d017']))
        if 'd018' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 18), atof(hist['d018']))
        if 'd019' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 19), atof(hist['d019']))
        if 'd020' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 20), atof(hist['d020']))
        if 'd021' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 21), atof(hist['d021']))
        if 'd022' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 22), atof(hist['d022']))
        if 'd023' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 23), atof(hist['d023']))
        if 'd024' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 24), atof(hist['d024']))
        if 'd025' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 25), atof(hist['d025']))
        if 'd026' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 26), atof(hist['d026']))
        if 'd027' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 27), atof(hist['d027']))
        if 'd028' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 28), atof(hist['d028']))
        if 'd029' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 29), atof(hist['d029']))
        if 'd030' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 30), atof(hist['d030']))
        if 'd031' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 31), atof(hist['d031']))
        if 'd032' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 32), atof(hist['d032']))
        if 'd033' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 33), atof(hist['d033']))
        if 'd034' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 34), atof(hist['d034']))
        if 'd035' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 35), atof(hist['d035']))
        if 'd036' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 36), atof(hist['d036']))
        if 'd037' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 37), atof(hist['d037']))
        if 'd038' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 38), atof(hist['d038']))
        if 'd039' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 39), atof(hist['d039']))
        if 'd040' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 40), atof(hist['d040']))
        if 'd041' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 41), atof(hist['d041']))
        if 'd042' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 42), atof(hist['d042']))
        if 'd043' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 43), atof(hist['d043']))
        if 'd044' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 44), atof(hist['d044']))
        if 'd045' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 45), atof(hist['d045']))
        if 'd046' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 46), atof(hist['d046']))
        if 'd047' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 47), atof(hist['d047']))
        if 'd048' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 48), atof(hist['d048']))
        if 'd049' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 49), atof(hist['d049']))
        if 'd050' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 50), atof(hist['d050']))
        if 'd051' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 51), atof(hist['d051']))
        if 'd052' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 52), atof(hist['d052']))
        if 'd053' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 53), atof(hist['d053']))
        if 'd054' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 54), atof(hist['d054']))
        if 'd055' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 55), atof(hist['d055']))
        if 'd056' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 56), atof(hist['d056']))
        if 'd057' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 57), atof(hist['d057']))
        if 'd058' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 58), atof(hist['d058']))
        if 'd059' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 59), atof(hist['d059']))
        if 'd060' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 60), atof(hist['d060']))
        if 'd061' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 61), atof(hist['d061']))
        if 'd062' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 62), atof(hist['d062']))
        if 'd063' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 63), atof(hist['d063']))
        if 'd064' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 64), atof(hist['d064']))
        if 'd065' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 65), atof(hist['d065']))
        if 'd066' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 66), atof(hist['d066']))
        if 'd067' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 67), atof(hist['d067']))
        if 'd068' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 68), atof(hist['d068']))
        if 'd069' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 69), atof(hist['d069']))
        if 'd070' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 70), atof(hist['d070']))
        if 'd071' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 71), atof(hist['d071']))
        if 'd072' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 72), atof(hist['d072']))
        if 'd073' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 73), atof(hist['d073']))
        if 'd074' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 74), atof(hist['d074']))
        if 'd075' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 75), atof(hist['d075']))
        if 'd076' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 76), atof(hist['d076']))
        if 'd077' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 77), atof(hist['d077']))
        if 'd078' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 78), atof(hist['d078']))
        if 'd079' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 79), atof(hist['d079']))
        if 'd080' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 80), atof(hist['d080']))
        if 'd081' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 81), atof(hist['d081']))
        if 'd082' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 82), atof(hist['d082']))
        if 'd083' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 83), atof(hist['d083']))
        if 'd084' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 84), atof(hist['d084']))
        if 'd085' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 85), atof(hist['d085']))
        if 'd086' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 86), atof(hist['d086']))
        if 'd087' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 87), atof(hist['d087']))
        if 'd088' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 88), atof(hist['d088']))
        if 'd089' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 89), atof(hist['d089']))
        if 'd090' in hist:
            ccdb.StoreDayData(self.GetOldDay(reftimestamp, 90), atof(hist['d090']))

        # hours
        if 'h746' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 744),  atof(hist['h746']))
        if 'h744' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 742),  atof(hist['h744']))
        if 'h742' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 740),  atof(hist['h742']))
        if 'h740' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 738),  atof(hist['h740']))
        if 'h738' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 736),  atof(hist['h738']))
        if 'h736' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 734),  atof(hist['h736']))
        if 'h734' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 732),  atof(hist['h734']))
        if 'h732' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 730),  atof(hist['h732']))
        if 'h730' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 728),  atof(hist['h730']))
        if 'h728' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 726),  atof(hist['h728']))
        if 'h726' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 724),  atof(hist['h726']))
        if 'h724' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 722),  atof(hist['h724']))
        if 'h722' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 720),  atof(hist['h722']))
        if 'h720' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 718),  atof(hist['h720']))
        if 'h718' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 716),  atof(hist['h718']))
        if 'h716' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 714),  atof(hist['h716']))
        if 'h714' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 712),  atof(hist['h714']))
        if 'h712' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 710),  atof(hist['h712']))
        if 'h710' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 708),  atof(hist['h710']))
        if 'h708' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 706),  atof(hist['h708']))
        if 'h706' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 704),  atof(hist['h706']))
        if 'h704' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 702),  atof(hist['h704']))
        if 'h702' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 700),  atof(hist['h702']))
        if 'h700' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 698),  atof(hist['h700']))
        if 'h698' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 696),  atof(hist['h698']))
        if 'h696' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 694),  atof(hist['h696']))
        if 'h694' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 692),  atof(hist['h694']))
        if 'h692' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 690),  atof(hist['h692']))
        if 'h690' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 688),  atof(hist['h690']))
        if 'h688' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 686),  atof(hist['h688']))
        if 'h686' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 684),  atof(hist['h686']))
        if 'h684' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 682),  atof(hist['h684']))
        if 'h682' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 680),  atof(hist['h682']))
        if 'h680' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 678),  atof(hist['h680']))
        if 'h678' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 676),  atof(hist['h678']))
        if 'h676' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 674),  atof(hist['h676']))
        if 'h674' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 672),  atof(hist['h674']))
        if 'h672' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 670),  atof(hist['h672']))
        if 'h670' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 668),  atof(hist['h670']))
        if 'h668' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 666),  atof(hist['h668']))
        if 'h666' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 664),  atof(hist['h666']))
        if 'h664' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 662),  atof(hist['h664']))
        if 'h662' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 660),  atof(hist['h662']))
        if 'h660' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 658),  atof(hist['h660']))
        if 'h658' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 656),  atof(hist['h658']))
        if 'h656' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 654),  atof(hist['h656']))
        if 'h654' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 652),  atof(hist['h654']))
        if 'h652' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 650),  atof(hist['h652']))
        if 'h650' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 648),  atof(hist['h650']))
        if 'h648' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 646),  atof(hist['h648']))
        if 'h646' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 644),  atof(hist['h646']))
        if 'h644' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 642),  atof(hist['h644']))
        if 'h642' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 640),  atof(hist['h642']))
        if 'h640' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 638),  atof(hist['h640']))
        if 'h638' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 636),  atof(hist['h638']))
        if 'h636' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 634),  atof(hist['h636']))
        if 'h634' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 632),  atof(hist['h634']))
        if 'h632' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 630),  atof(hist['h632']))
        if 'h630' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 628),  atof(hist['h630']))
        if 'h628' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 626),  atof(hist['h628']))
        if 'h626' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 624),  atof(hist['h626']))
        if 'h624' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 622),  atof(hist['h624']))
        if 'h622' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 620),  atof(hist['h622']))
        if 'h620' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 618),  atof(hist['h620']))
        if 'h618' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 616),  atof(hist['h618']))
        if 'h616' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 614),  atof(hist['h616']))
        if 'h614' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 612),  atof(hist['h614']))
        if 'h612' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 610),  atof(hist['h612']))
        if 'h610' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 608),  atof(hist['h610']))
        if 'h608' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 606),  atof(hist['h608']))
        if 'h606' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 604),  atof(hist['h606']))
        if 'h604' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 602),  atof(hist['h604']))
        if 'h602' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 600),  atof(hist['h602']))
        if 'h600' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 598),  atof(hist['h600']))
        if 'h598' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 596),  atof(hist['h598']))
        if 'h596' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 594),  atof(hist['h596']))
        if 'h594' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 592),  atof(hist['h594']))
        if 'h592' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 590),  atof(hist['h592']))
        if 'h590' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 588),  atof(hist['h590']))
        if 'h588' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 586),  atof(hist['h588']))
        if 'h586' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 584),  atof(hist['h586']))
        if 'h584' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 582),  atof(hist['h584']))
        if 'h582' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 580),  atof(hist['h582']))
        if 'h580' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 578),  atof(hist['h580']))
        if 'h578' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 576),  atof(hist['h578']))
        if 'h576' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 574),  atof(hist['h576']))
        if 'h574' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 572),  atof(hist['h574']))
        if 'h572' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 570),  atof(hist['h572']))
        if 'h570' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 568),  atof(hist['h570']))
        if 'h568' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 566),  atof(hist['h568']))
        if 'h566' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 564),  atof(hist['h566']))
        if 'h564' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 562),  atof(hist['h564']))
        if 'h562' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 560),  atof(hist['h562']))
        if 'h560' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 558),  atof(hist['h560']))
        if 'h558' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 556),  atof(hist['h558']))
        if 'h556' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 554),  atof(hist['h556']))
        if 'h554' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 552),  atof(hist['h554']))
        if 'h552' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 550),  atof(hist['h552']))
        if 'h550' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 548),  atof(hist['h550']))
        if 'h548' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 546),  atof(hist['h548']))
        if 'h546' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 544),  atof(hist['h546']))
        if 'h544' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 542),  atof(hist['h544']))
        if 'h542' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 540),  atof(hist['h542']))
        if 'h540' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 538),  atof(hist['h540']))
        if 'h538' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 536),  atof(hist['h538']))
        if 'h536' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 534),  atof(hist['h536']))
        if 'h534' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 532),  atof(hist['h534']))
        if 'h532' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 530),  atof(hist['h532']))
        if 'h530' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 528),  atof(hist['h530']))
        if 'h528' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 526),  atof(hist['h528']))
        if 'h526' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 524),  atof(hist['h526']))
        if 'h524' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 522),  atof(hist['h524']))
        if 'h522' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 520),  atof(hist['h522']))
        if 'h520' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 518),  atof(hist['h520']))
        if 'h518' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 516),  atof(hist['h518']))
        if 'h516' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 514),  atof(hist['h516']))
        if 'h514' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 512),  atof(hist['h514']))
        if 'h512' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 510),  atof(hist['h512']))
        if 'h510' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 508),  atof(hist['h510']))
        if 'h508' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 506),  atof(hist['h508']))
        if 'h506' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 504),  atof(hist['h506']))
        if 'h504' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 502),  atof(hist['h504']))
        if 'h502' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 500),  atof(hist['h502']))
        if 'h500' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 498),  atof(hist['h500']))
        if 'h498' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 496),  atof(hist['h498']))
        if 'h496' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 494),  atof(hist['h496']))
        if 'h494' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 492),  atof(hist['h494']))
        if 'h492' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 490),  atof(hist['h492']))
        if 'h490' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 488),  atof(hist['h490']))
        if 'h488' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 486),  atof(hist['h488']))
        if 'h486' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 484),  atof(hist['h486']))
        if 'h484' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 482),  atof(hist['h484']))
        if 'h482' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 480),  atof(hist['h482']))
        if 'h480' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 478),  atof(hist['h480']))
        if 'h478' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 476),  atof(hist['h478']))
        if 'h476' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 474),  atof(hist['h476']))
        if 'h474' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 472),  atof(hist['h474']))
        if 'h472' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 470),  atof(hist['h472']))
        if 'h470' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 468),  atof(hist['h470']))
        if 'h468' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 466),  atof(hist['h468']))
        if 'h466' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 464),  atof(hist['h466']))
        if 'h464' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 462),  atof(hist['h464']))
        if 'h462' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 460),  atof(hist['h462']))
        if 'h460' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 458),  atof(hist['h460']))
        if 'h458' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 456),  atof(hist['h458']))
        if 'h456' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 454),  atof(hist['h456']))
        if 'h454' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 452),  atof(hist['h454']))
        if 'h452' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 450),  atof(hist['h452']))
        if 'h450' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 448),  atof(hist['h450']))
        if 'h448' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 446),  atof(hist['h448']))
        if 'h446' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 444),  atof(hist['h446']))
        if 'h444' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 442),  atof(hist['h444']))
        if 'h442' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 440),  atof(hist['h442']))
        if 'h440' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 438),  atof(hist['h440']))
        if 'h438' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 436),  atof(hist['h438']))
        if 'h436' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 434),  atof(hist['h436']))
        if 'h434' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 432),  atof(hist['h434']))
        if 'h432' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 430),  atof(hist['h432']))
        if 'h430' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 428),  atof(hist['h430']))
        if 'h428' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 426),  atof(hist['h428']))
        if 'h426' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 424),  atof(hist['h426']))
        if 'h424' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 422),  atof(hist['h424']))
        if 'h422' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 420),  atof(hist['h422']))
        if 'h420' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 418),  atof(hist['h420']))
        if 'h418' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 416),  atof(hist['h418']))
        if 'h416' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 414),  atof(hist['h416']))
        if 'h414' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 412),  atof(hist['h414']))
        if 'h412' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 410),  atof(hist['h412']))
        if 'h410' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 408),  atof(hist['h410']))
        if 'h408' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 406),  atof(hist['h408']))
        if 'h406' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 404),  atof(hist['h406']))
        if 'h404' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 402),  atof(hist['h404']))
        if 'h402' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 400),  atof(hist['h402']))
        if 'h400' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 398),  atof(hist['h400']))
        if 'h398' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 396),  atof(hist['h398']))
        if 'h396' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 394),  atof(hist['h396']))
        if 'h394' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 392),  atof(hist['h394']))
        if 'h392' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 390),  atof(hist['h392']))
        if 'h390' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 388),  atof(hist['h390']))
        if 'h388' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 386),  atof(hist['h388']))
        if 'h386' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 384),  atof(hist['h386']))
        if 'h384' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 382),  atof(hist['h384']))
        if 'h382' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 380),  atof(hist['h382']))
        if 'h380' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 378),  atof(hist['h380']))
        if 'h378' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 376),  atof(hist['h378']))
        if 'h376' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 374),  atof(hist['h376']))
        if 'h374' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 372),  atof(hist['h374']))
        if 'h372' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 370),  atof(hist['h372']))
        if 'h370' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 368),  atof(hist['h370']))
        if 'h368' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 366),  atof(hist['h368']))
        if 'h366' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 364),  atof(hist['h366']))
        if 'h364' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 362),  atof(hist['h364']))
        if 'h362' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 360),  atof(hist['h362']))
        if 'h360' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 358),  atof(hist['h360']))
        if 'h358' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 356),  atof(hist['h358']))
        if 'h356' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 354),  atof(hist['h356']))
        if 'h354' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 352),  atof(hist['h354']))
        if 'h352' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 350),  atof(hist['h352']))
        if 'h350' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 348),  atof(hist['h350']))
        if 'h348' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 346),  atof(hist['h348']))
        if 'h346' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 344),  atof(hist['h346']))
        if 'h344' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 342),  atof(hist['h344']))
        if 'h342' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 340),  atof(hist['h342']))
        if 'h340' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 338),  atof(hist['h340']))
        if 'h338' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 336),  atof(hist['h338']))
        if 'h336' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 334),  atof(hist['h336']))
        if 'h334' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 332),  atof(hist['h334']))
        if 'h332' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 330),  atof(hist['h332']))
        if 'h330' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 328),  atof(hist['h330']))
        if 'h328' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 326),  atof(hist['h328']))
        if 'h326' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 324),  atof(hist['h326']))
        if 'h324' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 322),  atof(hist['h324']))
        if 'h322' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 320),  atof(hist['h322']))
        if 'h320' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 318),  atof(hist['h320']))
        if 'h318' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 316),  atof(hist['h318']))
        if 'h316' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 314),  atof(hist['h316']))
        if 'h314' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 312),  atof(hist['h314']))
        if 'h312' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 310),  atof(hist['h312']))
        if 'h310' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 308),  atof(hist['h310']))
        if 'h308' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 306),  atof(hist['h308']))
        if 'h306' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 304),  atof(hist['h306']))
        if 'h304' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 302),  atof(hist['h304']))
        if 'h302' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 300),  atof(hist['h302']))
        if 'h300' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 298),  atof(hist['h300']))
        if 'h298' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 296),  atof(hist['h298']))
        if 'h296' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 294),  atof(hist['h296']))
        if 'h294' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 292),  atof(hist['h294']))
        if 'h292' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 290),  atof(hist['h292']))
        if 'h290' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 288),  atof(hist['h290']))
        if 'h288' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 286),  atof(hist['h288']))
        if 'h286' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 284),  atof(hist['h286']))
        if 'h284' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 282),  atof(hist['h284']))
        if 'h282' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 280),  atof(hist['h282']))
        if 'h280' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 278),  atof(hist['h280']))
        if 'h278' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 276),  atof(hist['h278']))
        if 'h276' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 274),  atof(hist['h276']))
        if 'h274' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 272),  atof(hist['h274']))
        if 'h272' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 270),  atof(hist['h272']))
        if 'h270' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 268),  atof(hist['h270']))
        if 'h268' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 266),  atof(hist['h268']))
        if 'h266' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 264),  atof(hist['h266']))
        if 'h264' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 262),  atof(hist['h264']))
        if 'h262' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 260),  atof(hist['h262']))
        if 'h260' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 258),  atof(hist['h260']))
        if 'h258' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 256),  atof(hist['h258']))
        if 'h256' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 254),  atof(hist['h256']))
        if 'h254' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 252),  atof(hist['h254']))
        if 'h252' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 250),  atof(hist['h252']))
        if 'h250' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 248),  atof(hist['h250']))
        if 'h248' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 246),  atof(hist['h248']))
        if 'h246' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 244),  atof(hist['h246']))
        if 'h244' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 242),  atof(hist['h244']))
        if 'h242' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 240),  atof(hist['h242']))
        if 'h240' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 238),  atof(hist['h240']))
        if 'h238' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 236),  atof(hist['h238']))
        if 'h236' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 234),  atof(hist['h236']))
        if 'h234' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 232),  atof(hist['h234']))
        if 'h232' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 230),  atof(hist['h232']))
        if 'h230' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 228),  atof(hist['h230']))
        if 'h228' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 226),  atof(hist['h228']))
        if 'h226' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 224),  atof(hist['h226']))
        if 'h224' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 222),  atof(hist['h224']))
        if 'h222' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 220),  atof(hist['h222']))
        if 'h220' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 218),  atof(hist['h220']))
        if 'h218' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 216),  atof(hist['h218']))
        if 'h216' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 214),  atof(hist['h216']))
        if 'h214' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 212),  atof(hist['h214']))
        if 'h212' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 210),  atof(hist['h212']))
        if 'h210' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 208),  atof(hist['h210']))
        if 'h208' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 206),  atof(hist['h208']))
        if 'h206' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 204),  atof(hist['h206']))
        if 'h204' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 202),  atof(hist['h204']))
        if 'h202' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 200),  atof(hist['h202']))
        if 'h200' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 198),  atof(hist['h200']))
        if 'h198' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 196),  atof(hist['h198']))
        if 'h196' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 194),  atof(hist['h196']))
        if 'h194' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 192),  atof(hist['h194']))
        if 'h192' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 190),  atof(hist['h192']))
        if 'h190' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 188),  atof(hist['h190']))
        if 'h188' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 186),  atof(hist['h188']))
        if 'h186' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 184),  atof(hist['h186']))
        if 'h184' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 182),  atof(hist['h184']))
        if 'h182' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 180),  atof(hist['h182']))
        if 'h180' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 178),  atof(hist['h180']))
        if 'h178' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 176),  atof(hist['h178']))
        if 'h176' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 174),  atof(hist['h176']))
        if 'h174' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 172),  atof(hist['h174']))
        if 'h172' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 170),  atof(hist['h172']))
        if 'h170' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 168),  atof(hist['h170']))
        if 'h168' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 166),  atof(hist['h168']))
        if 'h166' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 164),  atof(hist['h166']))
        if 'h164' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 162),  atof(hist['h164']))
        if 'h162' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 160),  atof(hist['h162']))
        if 'h160' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 158),  atof(hist['h160']))
        if 'h158' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 156),  atof(hist['h158']))
        if 'h156' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 154),  atof(hist['h156']))
        if 'h154' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 152),  atof(hist['h154']))
        if 'h152' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 150),  atof(hist['h152']))
        if 'h150' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 148),  atof(hist['h150']))
        if 'h148' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 146),  atof(hist['h148']))
        if 'h146' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 144),  atof(hist['h146']))
        if 'h144' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 142),  atof(hist['h144']))
        if 'h142' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 140),  atof(hist['h142']))
        if 'h140' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 138),  atof(hist['h140']))
        if 'h138' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 136),  atof(hist['h138']))
        if 'h136' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 134),  atof(hist['h136']))
        if 'h134' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 132),  atof(hist['h134']))
        if 'h132' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 130),  atof(hist['h132']))
        if 'h130' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 128),  atof(hist['h130']))
        if 'h128' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 126),  atof(hist['h128']))
        if 'h126' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 124),  atof(hist['h126']))
        if 'h124' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 122),  atof(hist['h124']))
        if 'h122' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 120),  atof(hist['h122']))
        if 'h120' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 118),  atof(hist['h120']))
        if 'h118' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 116),  atof(hist['h118']))
        if 'h116' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 114),  atof(hist['h116']))
        if 'h114' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 112),  atof(hist['h114']))
        if 'h112' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 110),  atof(hist['h112']))
        if 'h110' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 108),  atof(hist['h110']))
        if 'h108' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 106),  atof(hist['h108']))
        if 'h106' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 104),  atof(hist['h106']))
        if 'h104' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 102),  atof(hist['h104']))
        if 'h102' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 100),  atof(hist['h102']))
        if 'h100' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 98),  atof(hist['h100']))
        if 'h098' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 96),  atof(hist['h098']))
        if 'h096' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 94),  atof(hist['h096']))
        if 'h094' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 92),  atof(hist['h094']))
        if 'h092' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 90),  atof(hist['h092']))
        if 'h090' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 88),  atof(hist['h090']))
        if 'h088' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 86),  atof(hist['h088']))
        if 'h086' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 84),  atof(hist['h086']))
        if 'h084' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 82),  atof(hist['h084']))
        if 'h082' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 80),  atof(hist['h082']))
        if 'h080' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 78),  atof(hist['h080']))
        if 'h078' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 76),  atof(hist['h078']))
        if 'h076' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 74),  atof(hist['h076']))
        if 'h074' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 72),  atof(hist['h074']))
        if 'h072' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 70),  atof(hist['h072']))
        if 'h070' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 68),  atof(hist['h070']))
        if 'h068' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 66),  atof(hist['h068']))
        if 'h066' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 64),  atof(hist['h066']))
        if 'h064' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 62),  atof(hist['h064']))
        if 'h062' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 60),  atof(hist['h062']))
        if 'h060' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 58),  atof(hist['h060']))
        if 'h058' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 56),  atof(hist['h058']))
        if 'h056' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 54),  atof(hist['h056']))
        if 'h054' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 52),  atof(hist['h054']))
        if 'h052' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 50),  atof(hist['h052']))
        if 'h050' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 48),  atof(hist['h050']))
        if 'h048' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 46),  atof(hist['h048']))
        if 'h046' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 44),  atof(hist['h046']))
        if 'h044' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 42),  atof(hist['h044']))
        if 'h042' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 40),  atof(hist['h042']))
        if 'h040' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 38),  atof(hist['h040']))
        if 'h038' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 36),  atof(hist['h038']))
        if 'h036' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 34),  atof(hist['h036']))
        if 'h034' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 32),  atof(hist['h034']))
        if 'h032' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 30),  atof(hist['h032']))
        if 'h030' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 28),  atof(hist['h030']))
        if 'h028' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 26),  atof(hist['h028']))
        if 'h026' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 24),  atof(hist['h026']))
        if 'h024' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 22),  atof(hist['h024']))
        if 'h022' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 20),  atof(hist['h022']))
        if 'h020' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 18),  atof(hist['h020']))
        if 'h018' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 16),  atof(hist['h018']))
        if 'h016' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 14),  atof(hist['h016']))
        if 'h014' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 12),  atof(hist['h014']))
        if 'h012' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 10),  atof(hist['h012']))
        if 'h010' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 8),  atof(hist['h010']))
        if 'h008' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 6),  atof(hist['h008']))
        if 'h006' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 4),  atof(hist['h006']))
        if 'h004' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 2),  atof(hist['h004']))
        if 'h002' in hist:
            ccdb.StoreHourData(self.GetOldHour(reftimestamp, 0),  atof(hist['h002']))

