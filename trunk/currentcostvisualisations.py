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

from dateutil.relativedelta import relativedelta
from matplotlib.dates import DayLocator, HourLocator, MonthLocator, YearLocator, WeekdayLocator, DateFormatter, date2num, drange


#
# Draws matplotlib bar graphs of CurrentCost data
# 
# 
#   Dale Lane (http://dalelane.co.uk/blog)
# 

class CurrentCostVisualisations():


    #
    # add a note to the graph
    # 
    def AddNote(self, notetext, clickedaxes, clickeddatetime, dtfraction, clickedkwh, graphunits, lastkwh, clickedaxestype):
        # do we want to plot data in kWh or financial cost?
        kwhfactor = None
        if graphunits == "kWh":
            kwhfactor = 1
        else:
            kwhfactor = float(lastkwh)

        wdth = None
        ctr = None
        arrowlength = 0
        spacing = 0

        if clickedaxestype == "hours":
            wdth = 0.083333333333333333333333333333333
            ctr = clickeddatetime + datetime.timedelta(hours=1) + datetime.timedelta(days=dtfraction)
            spacing = 0.1 * kwhfactor
            arrowlength = 1 * kwhfactor
        elif clickedaxestype == "days":
            wdth = 1
            ctr = clickeddatetime + datetime.timedelta(hours=12)
            spacing = 0.5 * kwhfactor
            arrowlength = 3 * kwhfactor
        elif clickedaxestype == "months":
            wdth = nummdays(clickeddatetime)
            ctr = clickeddatetime + datetime.timedelta(days=(wdth / 2))
            spacing = 10 * kwhfactor
            arrowlength = 60 * kwhfactor

        clickedaxes.annotate(notetext, 
                             arrowprops=dict(facecolor='black', shrink=0.05),
                             xy=(ctr,     (clickedkwh * kwhfactor) + spacing),
                             xytext=(ctr, (clickedkwh * kwhfactor) + arrowlength),
                             horizontalalignment='center',
                             picker=True)
        clickedaxes.figure.canvas.draw()


    #
    # draw hourly power usage
    # 
    def PlotHourlyData(self, axes, hourData, graphunits, lastkwh):

        # do we want to plot data in kWh or financial cost?
        kwhfactor = None
        if graphunits == "kWh":
            kwhfactor = 1
        else:
            kwhfactor = float(lastkwh)

        # initialise graph canvas
        axes.cla()
        axes.grid(True)
        axes.set_ylabel(graphunits)
        axes.set_title('Power usage by hour')

        # each data item represents two hours
        #  two hours is (2 / 24) of a day - which is why we want each bar
        #  to be (2/24) wide
        barwidth = 0.083333333333333333333333333333333

        # plot each hour data item
        for k, v in hourData.iteritems():
            # we don't plot 0 items - matplotlib doesn't handle it very well, 
            # often throwing an exception if we try!
            if v > 0:
                axes.bar(k, (v * kwhfactor), width=barwidth, color='b', picker=True)

        # rotate the axes labels
        for label in axes.get_xticklabels():
            label.set_picker(True)
            label.set_rotation(90)

        # we zoom and pan the graph so that by default it shows us the last
        #  seven days worth of hourly updates
        today = datetime.date.today()
        aweekago = datetime.timedelta(days=6)
        endoftoday = datetime.timedelta(days=1)
        mindate = today - aweekago
        maxdate = today + endoftoday
        axes.set_xlim(xmin=mindate, xmax=maxdate)

    
    #
    # draw daily power usage
    # 
    def PlotDailyData(self, axes, dayData, graphunits, lastkwh):

        # do we want to plot data in kWh or financial cost?
        kwhfactor = None
        if graphunits == "kWh":
            kwhfactor = 1
        else:
            kwhfactor = float(lastkwh)

        # initialise graph canvas
        axes.cla()
        axes.grid(True)
        axes.set_ylabel(graphunits)
        axes.set_title('Power usage by day')
    
        # plot each day data item
        for k, v in dayData.iteritems():
            # we don't plot 0 items - matplotlib doesn't handle it very well, 
            # often throwing an exception if we try!
            if v > 0:
                # we colour weekdays and weekends differently
                if k.weekday() >= 5:
                    axes.bar(k, (v * kwhfactor), width=1, color='g', picker=True)
                else:
                    axes.bar(k, (v * kwhfactor), width=1, color='b', picker=True)
    
        # rotate the axes labels
        for label in axes.get_xticklabels():
            label.set_picker(True)
            label.set_rotation(90)

        # we zoom and pan the graph so that by default it shows us the last
        #  month's worth of daily updates
        today = datetime.date.today()
        aweek = datetime.timedelta(days=31)
        mindate = today - aweek
        axes.set_xlim(xmin=mindate, xmax=today)


    #
    # draw monthly power usage
    # 
    def PlotMonthlyData(self, axes, monthData, graphunits, lastkwh):

        # do we want to plot data in kWh or financial cost?
        kwhfactor = None
        if graphunits == "kWh":
            kwhfactor = 1
        else:
            kwhfactor = float(lastkwh)

        # initialise graph canvas
        axes.cla()
        axes.grid(True)
        axes.set_ylabel(graphunits)
        axes.set_title('Power usage by month')
    
        # plot each hour data item
        for k, v in monthData.iteritems():
            # we don't plot 0 items - matplotlib doesn't handle it very well, 
            # often throwing an exception if we try!
            if v > 0:
                wdth = nummdays(k)
                #ctr = k + datetime.timedelta(days=(wdth / 2))
                axes.bar(k, (v * kwhfactor), width=wdth, color='r', picker=True)
                #axes.annotate('problems', 
                #              arrowprops=dict(facecolor='black', shrink=0.05),
                #              xy=(ctr,     (v * kwhfactor) + 10),
                #              xytext=(k,   (v * kwhfactor) + 50))

        # rotate the axes labels
        for label in axes.get_xticklabels():
            label.set_picker(True)
            label.set_rotation(90)



    #
    # plot a graph of an average day
    # 
    def PlotAverageDay(self, averageDay, axes, trendstxt, graphunits, lastkwh):

        # do we want to plot data in kWh or financial cost?
        kwhfactor = None
        if graphunits == "kWh":
            kwhfactor = 1
        else:
            kwhfactor = float(lastkwh)

        # initialise graph canvas
        axes.cla()
        axes.grid(True)
        axes.set_ylabel(graphunits)
        axes.set_title('Power usage in an average weekday')
    
        # each data item represents two hours
        #  two hours is (2 / 24) of a day - which is why we want each bar
        #  to be (2/24) wide
        barwidth = 0.083333333333333333333333333333333

        # as well as drawing an average day, we want to write a message on the
        #  'trends' page, which states what the highest average hour is
        # 
        # so while drawing the graph, we store the highest value
        highesthour = -1
        highesthourval = -1
    
        # plot each hour data item
        for avtime in averageDay:
            avval = averageDay[avtime]
            if avval > highesthourval:
                highesthourval = avval
                highesthour = avtime.hour
            # we don't plot 0 items - matplotlib doesn't handle it very well, 
            # often throwing an exception if we try!
            if avval > 0:
                axes.bar(avtime, (avval * kwhfactor), width=barwidth, color='g', picker=True)

        # if we have successfully identified which average hour typically has 
        #  the highest usage, we write a message about this to the 'trends' page
        if highesthour != -1:
            endtimehr = highesthour + 2
            if highesthour == 23:
                endtimehr = 1   
            trendstxt.UpdateTrendText(5, 
                                      "You typically use the most electricity between " + ("%d" % highesthour) + ":00 and " + ("%d" % endtimehr) + ":00")
    

    #
    # plot a graph of an average week
    # 
    def PlotAverageWeek(self, averageWeek, axes, trendstxt, graphunits, lastkwh):

        # do we want to plot data in kWh or financial cost?
        kwhfactor = None
        if graphunits == "kWh":
            kwhfactor = 1
        else:
            kwhfactor = float(lastkwh)

        # initialise graph canvas
        axes.cla()
        axes.grid(True)
        axes.set_ylabel(graphunits)
        axes.set_title('Power usage in an average week')
    
        # as well as drawing an average day, we want to write a message on the
        #  'trends' page, which states what the highest average hour is
        # 
        # so while drawing the graph, we store the highest value
        highestday = -1
        highestdayval = -1
    
        # plot each day data item
        for avday in averageWeek:
            avval = averageWeek[avday]
            if avval > highestdayval:
                highestdayval = avval
                highestday = avday.weekday()
            # we don't plot 0 items - matplotlib doesn't handle it very well, 
            # often throwing an exception if we try!
            if avval != 0:
                axes.bar(avday, (avval * kwhfactor), width=1, color='g', picker=True)

        # if we have successfully identified which average day typically has 
        #  the highest usage, we write a message about this to the 'trends' page
        try:
            daytodisplay = datetime.date(2008, 9, highestday + 1)
            trendstxt.UpdateTrendText(6, "You typically use the most electricity on " + daytodisplay.strftime("%A") + "s")
        except:
            print highestday



    #
    # plot the user's usage compared with the average usage of the group that 
    #  they are a member of
    # 
    # plot: 1) most recent week's data
    #       2) user's average week data
    #       3) group's average week data
    # 
    def PlotGroupWeekData(self, recentWeekData, averageWeekData, groupdata, groupdataaxes):

        # initialise graph canvas
        groupdataaxes.cla()
        groupdataaxes.grid(True)
        groupdataaxes.set_ylabel('kWh')
        groupdataaxes.set_title('Daily power usage (' + groupdata.groupdesc + ')')

        # each bar will take up a quarter of a full bar's width
        #  we want three bars, with spacing
        barwidth = 0.25

        # bars we are about to draw (need the handles to be able to add 
        #  the legend afterwards)
        recentbar = None
        avweekbar = None
        groupbar  = None

        # we need to find the most recent weeks set of daily data
        #  initialise a place to store that here
        recentdates = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        recentdatekeys = recentWeekData.keys()
        recentdatekeys.sort(reverse=True)

        # loop counter
        idx = 0

        # search for the most recent weeks set of daily data
        for nextdate in recentdatekeys:
            if idx >= 7:
                break
            idx += 1
            recentdates[nextdate.weekday()] = recentWeekData[nextdate]

        # draw the user's average week
        for avday in averageWeekData:
            avval = averageWeekData[avday]
            # we don't plot 0 items - matplotlib doesn't handle it very well, 
            # often throwing an exception if we try!
            if avval != 0:
                avweekbar = groupdataaxes.bar(datetime.datetime(avday.year,
                                                                avday.month,
                                                                avday.day,
                                                                6,
                                                                0,
                                                                0),
                                              avval, 
                                              width=barwidth, 
                                              color='#006600', 
                                              picker=True)

        # draw the other bars
        for i in range(0, 7):
            # chosen a week where i = 0 will create a Monday
            rcday = datetime.datetime(2008, 9, i+1)
            rcval = recentdates[i]
            avday = datetime.datetime(2008, 9, i+1, 12, 0, 0)
            avval = groupdata.groupdata['days'][str(i)]

            #
            # draw the user's most recent week

            # we don't plot 0 items - matplotlib doesn't handle it very well, 
            # often throwing an exception if we try!
            if rcval != 0:
                recentbar = groupdataaxes.bar(rcday, 
                                              rcval, 
                                              width=barwidth, 
                                              color='#33CC00',
                                              picker=True)
            #
            # draw the user's most recent week

            # we don't plot 0 items - matplotlib doesn't handle it very well, 
            # often throwing an exception if we try!
            if avval != 0:
                groupbar = groupdataaxes.bar(avday, 
                                             avval, 
                                             width=barwidth, 
                                             color='#003399',
                                             picker=True)

        # add a legend to explain the three bars
        groupdataaxes.legend( (recentbar, 
                               avweekbar, 
                               groupbar), 
                              ('your latest week', 
                               'your average week', 
                               groupdata.groupname) )

        # format the canvas
        groupdataaxes.xaxis.set_major_locator(DayLocator(range(0,8,1)))
        groupdataaxes.xaxis.set_major_formatter(DateFormatter('            %a'))
        groupdataaxes.figure.canvas.draw()


    # 
    # plot average daily usage for specific users
    # 
    def PlotFriendsWeekData(self, frienddataaxes, friendData):

        # initialise graph canvas
        frienddataaxes.cla()
        frienddataaxes.grid(True)
        frienddataaxes.set_ylabel('kWh')
        frienddataaxes.set_title('Average daily power usage')

        # how many users we want to display determines the width of the bars
        numusers = len(friendData)
        barwidth = 1.0 / (numusers + 1)
        hrwidth = 24 / (numusers + 1)

        # bars we are about to draw (need the handles to be able to add 
        #  the legend afterwards)
        userbars  = {}

        # different colour bar for each user
        useridx = 0
        colors = [ '#006600', '#EECC00', '#003399', '#663300' ]

        # draw the user's average week
        for username in friendData:

            # for each user...

            for i in range(0, 7):

                # for each day of the week...

                # check we have a value for this day before trying to access
                if str(i) in friendData[username]:                   
                    avval = friendData[username][str(i)]
                
                    # we don't plot 0 items - matplotlib doesn't handle it very well, 
                    # often throwing an exception if we try!
                    if avval != 0:
                        userbars[username] = frienddataaxes.bar(datetime.datetime(2008, 
                                                                                  9, 
                                                                                  i+1, 
                                                                                  useridx * hrwidth, 
                                                                                  0, 
                                                                                  0), 
                                                                avval, 
                                                                width=barwidth, 
                                                                color=colors[useridx],
                                                                picker=True)

            # increment counter - so we pick a different colour for the next user
            useridx = useridx + 1

        # graph drawing complete - time to tidy up

        # add legend
        numusers = len(userbars)
        if numusers == 1:
            frienddataaxes.legend((userbars[userbars.keys()[0]]), (userbars.keys()))
        elif numusers == 2:
            frienddataaxes.legend((userbars[userbars.keys()[0]], userbars[userbars.keys()[1]]),
                                  (userbars.keys()[0], userbars.keys()[1]) )
        elif numusers == 3:
            frienddataaxes.legend((userbars[userbars.keys()[0]], userbars[userbars.keys()[1]], userbars[userbars.keys()[2]]),
                                  (userbars.keys()[0], userbars.keys()[1], userbars.keys()[2]) )
        elif numusers == 4:
            frienddataaxes.legend((userbars[userbars.keys()[0]], userbars[userbars.keys()[1]], userbars[userbars.keys()[2]], userbars[userbars.keys()[3]]),
                                  (userbars.keys()[0], userbars.keys()[1], userbars.keys()[2], userbars.keys()[3]) )

        # format the canvas
        frienddataaxes.xaxis.set_major_locator(DayLocator(range(0,8,1)))
        frienddataaxes.xaxis.set_major_formatter(DateFormatter('            %a'))
        frienddataaxes.figure.canvas.draw()

    # 
    # plot average daily usage for specific users
    # 
    def PlotDailyScatterGraph(self, daydataaxes, averageWeekData, dailyData):

        # prepare store of x,y values for scatter graph
        personaldates = []
        personaldata = []
        everyonedates = []
        everyonedata = []

        # turn the collection of dailyData into a set of x,y values
        monday = datetime.datetime(2008, 9, 1, 0, 0, 0)
        mondaydate = date2num(monday)
        for dataitem in dailyData['mon']:
            everyonedates.append(mondaydate)
            everyonedata.append(float(dailyData['mon'][dataitem]))
        if averageWeekData[monday]:
            personaldates.append(mondaydate)
            personaldata.append(float(averageWeekData[monday]))

        tuesday = datetime.datetime(2008, 9, 2, 0, 0, 0)
        tuesdaydate = date2num(tuesday)
        for dataitem in dailyData['tue']:
            everyonedates.append(tuesdaydate)
            everyonedata.append(float(dailyData['tue'][dataitem]))
        if averageWeekData[tuesday]:
            personaldates.append(tuesdaydate)
            personaldata.append(float(averageWeekData[tuesday]))

        wednesday = datetime.datetime(2008, 9, 3, 0, 0, 0)
        wednesdaydate = date2num(wednesday)
        for dataitem in dailyData['wed']:
            everyonedates.append(wednesdaydate)
            everyonedata.append(float(dailyData['tue'][dataitem]))
        if averageWeekData[wednesday]:
            personaldates.append(wednesdaydate)
            personaldata.append(float(averageWeekData[wednesday]))

        thursday = datetime.datetime(2008, 9, 4, 0, 0, 0)
        thursdaydate = date2num(thursday)
        for dataitem in dailyData['thu']:
            everyonedates.append(thursdaydate)
            everyonedata.append(float(dailyData['thu'][dataitem]))
        if averageWeekData[thursday]:
            personaldates.append(thursdaydate)
            personaldata.append(float(averageWeekData[thursday]))


        friday = datetime.datetime(2008, 9, 5, 0, 0, 0)
        fridaydate = date2num(friday)
        for dataitem in dailyData['fri']:
            everyonedates.append(fridaydate)
            everyonedata.append(float(dailyData['fri'][dataitem]))
        if averageWeekData[friday]:
            personaldates.append(fridaydate)
            personaldata.append(float(averageWeekData[friday]))

        saturday = datetime.datetime(2008, 9, 6, 0, 0, 0)
        saturdaydate = date2num(saturday)
        for dataitem in dailyData['sat']:
            everyonedates.append(saturdaydate)
            everyonedata.append(float(dailyData['sat'][dataitem]))
        if averageWeekData[saturday]:
            personaldates.append(saturdaydate)
            personaldata.append(float(averageWeekData[saturday]))

        sunday = datetime.datetime(2008, 9, 7, 0, 0, 0)
        sundaydate = date2num(sunday)
        for dataitem in dailyData['sun']:
            everyonedates.append(sundaydate)
            everyonedata.append(float(dailyData['sun'][dataitem]))        
        if averageWeekData[sunday]:
            personaldates.append(sundaydate)
            personaldata.append(float(averageWeekData[sunday]))


        # initialise graph canvas
        daydataaxes.cla()
        daydataaxes.grid(False)
        daydataaxes.set_ylabel('kWh')
        daydataaxes.set_title('Everyone\'s average daily power usage')

        # plot the set of x,y values
        daydataaxes.scatter(everyonedates, everyonedata, s=80,  color="green", marker='x')
        daydataaxes.scatter(personaldates, personaldata, s=120, color="red",   marker='^')

        # format the canvas        
        daydataaxes.xaxis.set_major_formatter(DateFormatter('%a'))
        daydataaxes.set_ylim(ymin=0)
        daydataaxes.set_xlim(xmin=date2num(datetime.datetime(2008, 8, 31, 18, 0, 0)), 
                             xmax=date2num(datetime.datetime(2008, 9, 7, 6, 0, 0)))

        # finished! draw the graph
        daydataaxes.figure.canvas.draw()


    #
    # 'Target Line' - a horizontal line we can draw across bar graphs to give
    #   a target usage to aim for
    # 
    #  we have a method to add this line, and a method to delete it once drawn
    # 

    def DrawTargetLine(self, targetvalue, axes, graphunits, lastkwh):
        # do we want to plot data in kWh or financial cost?
        kwhfactor = 1
        if graphunits != "kWh":
            kwhfactor = float(lastkwh)

        line = axes.axhline(y=(targetvalue * kwhfactor), color='y', linewidth=2)  
        axes.figure.canvas.draw()
        return line

    def DeleteTargetLine(self, targetvalue, axes):
        targetvalue.remove()
        axes.figure.canvas.draw()

    #
    # identify some textual descriptions of trends in the CurrentCost data
    # 
    # 
    def IdentifyTrends(self, trends, hourData, dayData, monthData):
        lowesthour   = 99999999
        highesthour  = 0
        lowestday    = 99999999
        highestday   = 0
        lowestmonth  = 99999999
        highestmonth = 0
        dayyesterday = 0
        dayweekago   = 0
        yesterday    = datetime.date.today() - datetime.timedelta(days=1)
        oneweekago   = datetime.date.today() - datetime.timedelta(days=8)
        thismonth    = datetime.date(datetime.date.today().year,
                                     datetime.date.today().month,
                                     1)
        onemonthago   = thismonth - relativedelta(months=1)
        twomonthsago  = thismonth - relativedelta(months=2)
        threemonthsago= thismonth - relativedelta(months=3)
        fourmonthsago = thismonth - relativedelta(months=4)
        fivemonthsago = thismonth - relativedelta(months=5)
        sixmonthsago  = thismonth - relativedelta(months=6)
        sevenmonthsago= thismonth - relativedelta(months=7)
        eightmonthsago= thismonth - relativedelta(months=8)
        ninemonthsago = thismonth - relativedelta(months=9)
        tenmonthsago  = thismonth - relativedelta(months=10)
        month0        = 0
        month1        = 0
        month2        = 0
        month3        = 0
        month4        = 0
        month5        = 0
        month6        = 0
        month7        = 0
        month8        = 0
        month9        = 0
        month10       = 0
    
        for k, v in hourData.iteritems():
            if v > 0:
                if v < lowesthour:
                    lowesthour = v
                elif v > highesthour:
                    highesthour = v                 
        for k, v in dayData.iteritems():
            if v > 0:
                if v < lowestday:
                    lowestday = v
                elif v > highestday:
                    highestday = v
                if k == yesterday:
                    dayyesterday = v
                elif k == oneweekago:
                    dayweekago = v
        for k, v in monthData.iteritems():
            if v > 0:
                if k == thismonth:
                    month0 = v
                elif k == onemonthago:
                    month1 = v
                elif k == twomonthsago:
                    month2 = v
                elif k == threemonthsago:
                    month3 = v
                elif k == fourmonthsago:
                    month4 = v
                elif k == fivemonthsago:
                    month5 = v
                elif k == sixmonthsago:
                    month6 = v
                elif k == sevenmonthsago:
                    month7 = v
                elif k == eightmonthsago:
                    month8 = v
                elif k == ninemonthsago:
                    month9 = v
                elif k == tenmonthsago:
                    month10 = v

        if lowesthour != 99999999:
            trends.UpdateTrendText(1, "Lowest recorded electricity usage over a two-hour period is " + ("%.3f" % lowesthour) + " kWh.   Highest is " + ("%.3f" % highesthour) + " kWh")
        if lowestday != 99999999:
            trends.UpdateTrendText(2, "Lowest recorded daily electricity usage is " + ("%.2f" % lowestday) + " kWh.   Highest is " + ("%.2f" % highestday) + " kWh")
        if dayyesterday > 0:
            if dayyesterday < dayweekago:
                trends.UpdateTrendText(3, "Yesterday, your daily recorded electricity usage (" + ("%.2f" % dayyesterday) + "kWh) was lower than last " + oneweekago.strftime("%A") + " (" + ("%.2f" % dayweekago) + " kWh)")
            elif dayyesterday > dayweekago:
                trends.UpdateTrendText(3, "Yesterday, your daily recorded electricity usage (" + ("%.2f" % dayyesterday) + "kWh) was higher than last " + oneweekago.strftime("%A") + " (" + ("%.2f" % dayweekago) + " kWh)")
            else:
                trends.UpdateTrendText(3, "Your daily recorded electricity usage yesterday (" + ("%.2f" % dayyesterday) + "kWh) was the same as last " + oneweekago.strftime("%A") + " (" + ("%.2f" % dayweekago) + "kWh)")
        if month1 < month2:
            mth = 1
            if month2 < month3:
                mth += 1
                if month3 < month4:
                    mth += 1
                    if month4 < month5:
                        mth += 1
                        if month5 < month6:
                            mth += 1
                            if month6 < month7:
                                mth += 1
                                if month7 < month8:
                                    mth += 1
                                    if month8 < month9:
                                        mth += 1
                                        if month9 < month10:
                                            mth += 1
            trends.UpdateTrendText(4, "Your monthly electricity usage has decreased every month for the last " + ("%d" % mth) + " months")
        elif month1 > month2:
            mth = 1
            if month2 > month3:
                mth += 1
                if month3 > month4:
                    mth += 1
                    if month4 > month5:
                        mth += 1
                        if month5 > month6:
                            mth += 1
                            if month6 > month7:
                                mth += 1
                                if month7 > month8:
                                    mth += 1
                                    if month8 > month9:
                                        mth += 1
                                        if month9 > month10:
                                            mth += 1
            trends.UpdateTrendText(4, "Your monthly electricity usage has increased every month for the last " + ("%d" % mth) + " months")
        else:
            mth = 1
            if month2 == month3:
                mth += 1
                if month3 == month4:
                    mth += 1
                    if month4 == month5:
                        mth += 1
                        if month5 == month6:
                            mth += 1
                            if month6 == month7:
                                mth += 1
                                if month7 == month8:
                                    mth += 1
                                    if month8 == month9:
                                        mth += 1
                                        if month9 == month10:
                                            mth += 1
            trends.UpdateTrendText(4, "Your monthly electricity usage has remained consistent for the last " + ("%d" % mth) + " months")


#
# utility function to get the number of days in a month
# 
def nummdays (adate):
  if adate.month == 12:
    return 31
  elif adate.month == 11:
    return 30
  elif adate.month == 10:
    return 31
  elif adate.month == 9:
    return 30
  elif adate.month == 8:
    return 31
  elif adate.month == 7:
    return 31
  elif adate.month == 6:
    return 30
  elif adate.month == 5:
    return 31
  elif adate.month == 4:
    return 30
  elif adate.month == 3:
    return 31
  elif adate.month == 1:
    return 31
  elif adate.month == 2:
    if (adate.year % 4) == 0:
      return 29
    else:
      return 28

