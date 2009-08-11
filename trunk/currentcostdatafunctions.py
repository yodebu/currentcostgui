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
import datetime
import csv
import os



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
# It also converts historical CurrentCost data into averages, and functions
#  to export CurrentCost data to CSV files.
# 
# 
#  Dale Lane (http://dalelane.co.uk/blog)
# 
class CurrentCostDataFunctions():

    def ParseCurrentCostXML(self, ccdb, newupd):
        today = datetime.date.today()
        #
        ccdb.StoreMonthData(self.GetOldMonth(today, 1),  newupd.WattsMonth01)
        ccdb.StoreMonthData(self.GetOldMonth(today, 2),  newupd.WattsMonth02)
        ccdb.StoreMonthData(self.GetOldMonth(today, 3),  newupd.WattsMonth03)
        ccdb.StoreMonthData(self.GetOldMonth(today, 4),  newupd.WattsMonth04)
        ccdb.StoreMonthData(self.GetOldMonth(today, 5),  newupd.WattsMonth05)
        ccdb.StoreMonthData(self.GetOldMonth(today, 6),  newupd.WattsMonth06)
        ccdb.StoreMonthData(self.GetOldMonth(today, 7),  newupd.WattsMonth07)
        ccdb.StoreMonthData(self.GetOldMonth(today, 8),  newupd.WattsMonth08)
        ccdb.StoreMonthData(self.GetOldMonth(today, 9),  newupd.WattsMonth09)
        ccdb.StoreMonthData(self.GetOldMonth(today, 10), newupd.WattsMonth10)
        ccdb.StoreMonthData(self.GetOldMonth(today, 11), newupd.WattsMonth11)
        ccdb.StoreMonthData(self.GetOldMonth(today, 12), newupd.WattsMonth12)
        #
        ccdb.StoreDayData(self.GetOldDay(today, 1),  newupd.WattsDay01)
        ccdb.StoreDayData(self.GetOldDay(today, 2),  newupd.WattsDay02)
        ccdb.StoreDayData(self.GetOldDay(today, 3),  newupd.WattsDay03)
        ccdb.StoreDayData(self.GetOldDay(today, 4),  newupd.WattsDay04)
        ccdb.StoreDayData(self.GetOldDay(today, 5),  newupd.WattsDay05)
        ccdb.StoreDayData(self.GetOldDay(today, 6),  newupd.WattsDay06)
        ccdb.StoreDayData(self.GetOldDay(today, 7),  newupd.WattsDay07)
        ccdb.StoreDayData(self.GetOldDay(today, 8),  newupd.WattsDay08)
        ccdb.StoreDayData(self.GetOldDay(today, 9),  newupd.WattsDay09)
        ccdb.StoreDayData(self.GetOldDay(today, 10), newupd.WattsDay10)
        ccdb.StoreDayData(self.GetOldDay(today, 11), newupd.WattsDay11)
        ccdb.StoreDayData(self.GetOldDay(today, 12), newupd.WattsDay12)
        ccdb.StoreDayData(self.GetOldDay(today, 13), newupd.WattsDay13)
        ccdb.StoreDayData(self.GetOldDay(today, 14), newupd.WattsDay14)
        ccdb.StoreDayData(self.GetOldDay(today, 15), newupd.WattsDay15)
        ccdb.StoreDayData(self.GetOldDay(today, 16), newupd.WattsDay16)
        ccdb.StoreDayData(self.GetOldDay(today, 17), newupd.WattsDay17)
        ccdb.StoreDayData(self.GetOldDay(today, 18), newupd.WattsDay18)
        ccdb.StoreDayData(self.GetOldDay(today, 19), newupd.WattsDay19)
        ccdb.StoreDayData(self.GetOldDay(today, 20), newupd.WattsDay20)
        ccdb.StoreDayData(self.GetOldDay(today, 21), newupd.WattsDay21)
        ccdb.StoreDayData(self.GetOldDay(today, 22), newupd.WattsDay22)
        ccdb.StoreDayData(self.GetOldDay(today, 23), newupd.WattsDay23)
        ccdb.StoreDayData(self.GetOldDay(today, 24), newupd.WattsDay24)
        ccdb.StoreDayData(self.GetOldDay(today, 25), newupd.WattsDay25)
        ccdb.StoreDayData(self.GetOldDay(today, 26), newupd.WattsDay26)
        ccdb.StoreDayData(self.GetOldDay(today, 27), newupd.WattsDay27)
        ccdb.StoreDayData(self.GetOldDay(today, 28), newupd.WattsDay28)
        ccdb.StoreDayData(self.GetOldDay(today, 29), newupd.WattsDay29)
        ccdb.StoreDayData(self.GetOldDay(today, 30), newupd.WattsDay30)
        ccdb.StoreDayData(self.GetOldDay(today, 31), newupd.WattsDay31)
        #
        currtime = datetime.datetime.now()
        #
        ccdb.StoreHourData(self.GetOldHour(currtime, 0),  newupd.kWattsHour02)
        ccdb.StoreHourData(self.GetOldHour(currtime, 2),  newupd.kWattsHour04)
        ccdb.StoreHourData(self.GetOldHour(currtime, 4),  newupd.kWattsHour06)
        ccdb.StoreHourData(self.GetOldHour(currtime, 6),  newupd.kWattsHour08)
        ccdb.StoreHourData(self.GetOldHour(currtime, 8),  newupd.kWattsHour10)
        ccdb.StoreHourData(self.GetOldHour(currtime, 10), newupd.kWattsHour12)
        ccdb.StoreHourData(self.GetOldHour(currtime, 12), newupd.kWattsHour14)
        ccdb.StoreHourData(self.GetOldHour(currtime, 14), newupd.kWattsHour16)
        ccdb.StoreHourData(self.GetOldHour(currtime, 16), newupd.kWattsHour18)
        ccdb.StoreHourData(self.GetOldHour(currtime, 18), newupd.kWattsHour20)
        ccdb.StoreHourData(self.GetOldHour(currtime, 20), newupd.kWattsHour22)
        ccdb.StoreHourData(self.GetOldHour(currtime, 22), newupd.kWattsHour24)
        ccdb.StoreHourData(self.GetOldHour(currtime, 24), newupd.kWattsHour26)           

    #
    ######################### 
    # 
    # functions to translate dates from relative to absolute
    # 
    #########################
    # 

    def GetOldMonth(self, referenceDate, monthsago):
        newmonth = referenceDate.month - monthsago
        newyear  = referenceDate.year
    
        if newmonth <= 0:
            newmonth += 12
            newyear -= 1
    
        return datetime.date(newyear, newmonth, 1)
        
    def GetOldDay(self, referenceDate, daysago):
        newday = referenceDate.day - daysago
        newmonth = referenceDate.month
        newyear = referenceDate.year
    
        if newday <= 0:
            d = datetime.timedelta(days=daysago)
            sub = referenceDate - d
            newday = sub.day
            newmonth = sub.month
            newyear = sub.year
    
        return datetime.date(newyear, newmonth, newday)
    
    def GetOldHour(self, referenceDate, hoursago):
        if referenceDate.hour % 2 == 0:
            hoursago = hoursago + 1
    
        newhour = referenceDate.hour - hoursago
        newday = referenceDate.day
        newmonth = referenceDate.month
        newyear = referenceDate.year
    
        if newhour < -24:
            newhour += 48
            d = datetime.timedelta(hours=hoursago)
            sub = referenceDate - d
            newday = sub.day
            newmonth = sub.month
            newyear = sub.year        
        elif newhour < 0:
            newhour += 24
            d = datetime.timedelta(hours=hoursago)
            sub = referenceDate - d
            newday = sub.day
            newmonth = sub.month
            newyear = sub.year
    
        return datetime.datetime(newyear, newmonth, newday, newhour, 0, 0)


    #
    ######################### 
    # 
    # functions to export CurrentCost data to CSV files
    # 
    #########################
    # 

    # export hour data to CSV
    def ExportHourData(self, filepath, datacollection):
        f = open(filepath, 'wt')
        fieldnames = ('Date', 'Time', 'kWH')
        writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel')
        headers = {}
        for n in fieldnames:
            headers[n] = n
        writer.writerow(headers)

        datadates = datacollection.keys()
        datadates.sort()

        for nextdate in datadates:
            writer.writerow( { 'Date': nextdate.date(),
                               'Time': nextdate.time(), 
                               'kWH' : datacollection[nextdate] } )
        f.close()

    # export days data to CSV
    def ExportDateData(self, filepath, datacollection):
        f = open(filepath, 'wt')
        fieldnames = ('Date', 'kWH')
        writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel')
        headers = {}
        for n in fieldnames:
            headers[n] = n
        writer.writerow(headers)

        datadates = datacollection.keys()
        datadates.sort()

        for nextdate in datadates:
            writer.writerow( { 'Date': nextdate,
                               'kWH' : datacollection[nextdate] } )

        f.close()        




    #
    ######################### 
    # 
    # functions to calculate average days and weeks
    # 
    #########################
    # 

    def CalculateAverageDay(self, hourData):
        hoursCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        hoursSum   = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        hoursAvg   = {}

        if len(hourData) == 0:
            for i in range(0, 24):
                avtime = datetime.datetime(2000, 1, 1, i, 0, 0)   # don't care about the date - wont be seen
                hoursAvg[avtime] = 0
            return hoursAvg

        for k, v in hourData.iteritems():
            if v > 0:
                if k.weekday() >= 5:
                    hoursCount[k.hour] += 1
                    hoursSum[k.hour] += v

        for i in range(0, 24):
            avtime = datetime.datetime(2000, 1, 1, i, 0, 0)   # don't care about the date - wont be seen
            if hoursCount[i] != 0:
                hoursAvg[avtime] = hoursSum[i] / hoursCount[i]

        return hoursAvg

    def CalculateAverageWeek(self, dayData):
        daysCount = [0, 0, 0, 0, 0, 0, 0]
        daysSum   = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        weekAvg = {}

        if len(dayData) == 0:
            for i in range(0, 7):
                avday = datetime.datetime(2008, 9, i+1)    # chosen a week where i = 0 will create a Monday
                weekAvg[avday] = 0
            return weekAvg

        for k, v in dayData.iteritems():
            if v > 0:
                daysCount[k.weekday()] += 1
                daysSum[k.weekday()] += v

        for i in range(0, 7):
            avday = datetime.datetime(2008, 9, i+1)    # chosen a week where i = 0 will create a Monday
            if daysCount[i] != 0:
                weekAvg[avday] = daysSum[i] / daysCount[i]

        return weekAvg
