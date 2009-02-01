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


#
#  Screen-scapes the National Grid website to get data about the national
#   electricity demand
# 
#  Dale Lane (http://dalelane.co.uk/blog)
# 
class NationalGridDataSource():

    #
    # get the HTML for the realtime demand data webpage
    # 
    def DownloadRealtimeHTML(self):
        post_req = urllib2.Request('http://www.nationalgrid.com/ngrealtime/realtime/systemdata.aspx')
        post_resp = urllib2.urlopen(post_req)
        post_resp_body = post_resp.read()
        return post_resp_body

    #
    # get the demand (int) and frequency (float) values from the provided HTML
    # 
    def ParseRealtimeHTML(self, htmltext):
        demand = None
        frequency = None

        idx = htmltext.find("<div><p class='small'>Demand:")
        if idx > 0:
            idx += 29
            endidx = htmltext.find('MW', idx)
            if endidx > 0:
                substr = htmltext[idx : endidx]
                try:
                    demand = int(substr)
                except:
                    demand = -1

                idx = htmltext.find('Frequency:', idx)
                if idx > 0:
                    idx += 10
                    endidx = htmltext.find('Hz', idx)
                    if endidx > 0:
                        substr = htmltext[idx : endidx]
                        try:
                            frequency = float(substr)
                        except:
                            frequency = -1

        return demand, frequency
