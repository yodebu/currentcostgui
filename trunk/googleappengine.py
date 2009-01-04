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
import cookielib
import wx
import wx.aui

import simplejson as json

from string import atoi






# represents a CurrentCost group as stored in the Google App Engine database
class GroupData:
    groupname = "name"
    groupdesc = "desc"
    groupdata = {}


#
#  class used to connect to the Google App Engine web service
#
#    the web service requires a logon, so the functions here allow for login
#     credentials to be collected and submitted to the web server
#
# 
# 
#  Dale Lane (http://dalelane.co.uk/blog)
# 
class GoogleAppEngine():

    googleemail  = None
    googlepasswd = None

    #
    # collect a username and password from the user - using wxpython dialogs
    # 
    def RequestGoogleCredentials(self, gui):
        if self.googlepasswd == None:
            creddlg = wx.TextEntryDialog(gui, 
                                         'Please enter your email address:',
                                         'CurrentCost')
            if self.googleemail:
                creddlg.SetValue(self.googleemail)
            if creddlg.ShowModal() == wx.ID_OK:
                self.googleemail = creddlg.GetValue()
                creddlg.Destroy()
            else:
                creddlg.Destroy()
                return False
    
            creddlg = wx.PasswordEntryDialog(gui, 
                                             'Please enter your password:',
                                             'CurrentCost')
            if creddlg.ShowModal() == wx.ID_OK:
                self.googlepasswd = creddlg.GetValue()
                creddlg.Destroy()
            else:
                creddlg.Destroy()
                return False

        return True






    #
    # verifies that we are allowed to download updates from a specified user
    # 
    def VerifyPermissionsForUser(self, gui, ccdatabase, username):

        # retrieve last-used-username from client local db - use to prefill 
        #  the GUI that will request Google credentials
        if not self.googleemail:
            self.googleemail = ccdatabase.RetrieveSetting("googleemail")

        # get username and password from user
        if self.RequestGoogleCredentials(gui) == False:
            return 

        # persist the username - to save it needing to be entered next time
        ccdatabase.StoreSetting("googleemail", self.googleemail)

        # log on to Google App Engine - creating a cookie to use when we start
        #  downloading data

        try:
            self.AuthenticateWebService(self.googleemail, self.googlepasswd)
        except urllib2.URLError, err:
                errdlg = wx.MessageDialog(gui,
                                          "Failed to connect to CurrentCost server",
                                          'CurrentCost', 
                                          style=(wx.OK | wx.ICON_ERROR))
                errdlg.ShowModal()        
                errdlg.Destroy()
                return 
        except urllib2.HTTPError, err:
            if err.code == 403:
                errdlg = wx.MessageDialog(gui,
                                          "Username / password not recognised",
                                          'CurrentCost', 
                                          style=(wx.OK | wx.ICON_ERROR))
                errdlg.ShowModal()        
                errdlg.Destroy()
                return 
            else:
                print err.code

        # check username with Google App Engine 
        postreq_data = urllib.urlencode( { "username"  : username } )
        post_req = urllib2.Request('http://currentcost.appspot.com/friends/verify', data=postreq_data)
        post_resp = urllib2.urlopen(post_req)
        post_resp_body = post_resp.read()

        if post_resp_body == "OK":
            return True
        elif post_resp_body == "Unknown friend user":
            return None

        return False


    def DownloadCurrentCostUserDataFromGoogle(self, username):
        # check username with Google App Engine 
        postreq_data = urllib.urlencode( { "username"  : username } )
        post_req = urllib2.Request('http://currentcost.appspot.com/friends/getweekavg', data=postreq_data)
        post_resp = urllib2.urlopen(post_req)
        post_resp_body = post_resp.read()
        return json.loads(post_resp_body)



    #
    # downloads group averages from Google App Engine
    # 
    def DownloadCurrentCostDataFromGoogle(self, gui, ccdatabase):

        # retrieve last-used-username from client local db - use to prefill 
        #  the GUI that will request Google credentials
        if not self.googleemail:
            self.googleemail = ccdatabase.RetrieveSetting("googleemail")

        # get username and password from user
        if self.RequestGoogleCredentials(gui) == False:
            return 

        # persist the username - to save it needing to be entered next time
        ccdatabase.StoreSetting("googleemail", self.googleemail)

        numitems = 3
        curidx   = 0

        # prepare progress dialog

        progdlg = wx.ProgressDialog ('CurrentCost', 
                                     'Connecting to CurrentCost web service', 
                                     maximum = numitems, 
                                     style=wx.PD_CAN_ABORT)

        # log on to Google App Engine - creating a cookie to use when we start
        #  downloading data

        try:
            self.AuthenticateWebService(self.googleemail, self.googlepasswd)
        except urllib2.URLError, err:
                errdlg = wx.MessageDialog(gui,
                                          "Failed to connect to CurrentCost server",
                                          'CurrentCost', 
                                          style=(wx.OK | wx.ICON_ERROR))
                errdlg.ShowModal()        
                errdlg.Destroy()
                progdlg.Update(numitems, "Failed to upload")
                progdlg.Destroy()
                return 
        except urllib2.HTTPError, err:
            if err.code == 403:
                errdlg = wx.MessageDialog(gui,
                                          "Username / password not recognised",
                                          'CurrentCost', 
                                          style=(wx.OK | wx.ICON_ERROR))
                errdlg.ShowModal()        
                errdlg.Destroy()
                progdlg.Update(numitems, "Failed to upload")
                progdlg.Destroy()
                return 
            else:
                print err.code

        progdlg.Update(curidx, 'Connection made. Getting your groups list')
        curidx += 1

        # download averages from Google App Engine

        post_req = urllib2.Request('http://currentcost.appspot.com/groups/list/svc')
        post_resp = urllib2.urlopen(post_req)
        post_resp_body = post_resp.read()

        # translate data received from Google App Engine into a store that 
        #  can be drawn by the client GUI

        currentcostgroups = {}

        progdlg.Update(curidx, 'Downloading group data')

        grpslist = json.loads(post_resp_body)
        for group in grpslist:
            grpid = grpslist[group]['id']
            currentcostgroups[grpid] = GroupData()
            currentcostgroups[grpid].groupname = grpslist[group]['name']
            currentcostgroups[grpid].groupdesc = grpslist[group]['description']
            currentcostgroups[grpid].groupdata = self.DownloadGroupDataFromGoogle(grpid)

        # download day averages that is used to draw a scatter diagram
        curidx += 1
        progdlg.Update(curidx, 'Downloading daily data')

        post_req = urllib2.Request('http://currentcost.appspot.com/ccdata/days')
        post_resp = urllib2.urlopen(post_req)
        post_resp_body = post_resp.read()

        dailydata = json.loads(post_resp_body)

        # complete - finished with progress dialog
        progdlg.Destroy()

        currentcostdata = {}
        currentcostdata['groupdata'] = currentcostgroups
        currentcostdata['daydata'] = dailydata

        return currentcostdata


    #
    # downloads list of groups that user is a member of
    # 
    def DownloadGroupDataFromGoogle(self, groupid):
        post_req = urllib2.Request('http://currentcost.appspot.com/ccdata/avg?groupid=' + str(groupid))
        post_resp = urllib2.urlopen(post_req)
        post_resp_body = post_resp.read()
        groupdata = json.loads(post_resp_body)
        return groupdata


    #
    # upload history data to Google App Engine
    # 
    def UploadCurrentCostDataToGoogle(self, gui, ccdatabase):

        # retrieve last-used-username from client local db - use to prefill 
        #  the GUI that will request Google credentials
        if not self.googleemail:
            self.googleemail = ccdatabase.RetrieveSetting("googleemail")

        # get username and password from user
        if self.RequestGoogleCredentials(gui) == False:
            return False

        # persist the username - to save it needing to be entered next time
        ccdatabase.StoreSetting("googleemail", self.googleemail)


        # create a progress dialog 
        numitems = ccdatabase.CountHourData() + ccdatabase.CountDayData() + ccdatabase.CountMonthData() + 4
        curidx   = 0

        progdlg = wx.ProgressDialog ('CurrentCost', 'Connecting to CurrentCost web service', maximum = numitems, style=wx.PD_CAN_ABORT)


        # log on to Google App Engine - creating a cookie to use when we start
        #  uploading data

        try:
            self.AuthenticateWebService(self.googleemail, self.googlepasswd)
        except urllib2.HTTPError, err:
            if err.code == 403:
                errdlg = wx.MessageDialog(self,
                                          "Username / password not recognised",
                                          'CurrentCost', 
                                          style=(wx.OK | wx.ICON_ERROR))
                errdlg.ShowModal()        
                errdlg.Destroy()
                progdlg.Update(numitems, "Failed to upload")
                progdlg.Destroy()
                return False
            else:
                print err.code

        progdlg.Update(curidx, 'Connection made')

        curidx += 1

        ################################################################
        # 
        # UPLOAD    HOURS
        # 
        ################################################################

        progdlg.Update(curidx, 'Uploading hourly data')
        curidx += 1

        # each data item is uploaded individually
        #  so we want to loop through all of the locally stored data items
        #   uploading each one in turn
        # 
        # so that we don't upload a data item multiple times, we keep a track 
        #  of what we've uploaded before
        # 
        # instead of iterating through all locally stored hour data, we 
        #  request from the local database the next hour data item that we 
        #  know we have not yet uploaded
        # 
        # once successfully uploaded, we inform the local client database, so 
        #  that it will not attempt this again

        updat = ccdatabase.GetHourDataToUpload()
        while updat:
            (tocontinue, toskip) = progdlg.Update(curidx, 'Uploading hourly data')
            if tocontinue == False:
                progdlg.Update(numitems, "Cancelled")
                progdlg.Destroy()
                return False

            curidx += 1

            # don't upload empty items (CurrentCost meters fill in empty 
            #   values with 0)

            if updat['ccvalue'] > 0:
                postreq_data = urllib.urlencode( { "ccdatatype"  : "hour",
                                                   "ccdatavalue" : updat['ccvalue'],
                                                   "ccyear"      : updat['timestamp'].year,
                                                   "ccmonth"     : updat['timestamp'].month,
                                                   "ccdate"      : updat['timestamp'].day,
                                                   "cchour"      : updat['timestamp'].hour } )
                post_req = urllib2.Request('http://currentcost.appspot.com/ccdata/add', data=postreq_data)
                post_resp = urllib2.urlopen(post_req)
                post_resp_body = post_resp.read()
    
                if post_resp_body != "OK":
                    print post_resp_body

            # mark this as uploaded, and get the next one to upload
            ccdatabase.ConfirmHourDataUploaded(updat)
            updat = ccdatabase.GetHourDataToUpload()


        ################################################################
        # 
        # UPLOAD    DAYS
        # 
        ################################################################

        progdlg.Update(curidx, 'Uploading daily data')
        curidx += 1

        # each data item is uploaded individually
        #  so we want to loop through all of the locally stored data items
        #   uploading each one in turn
        # 
        # so that we don't upload a data item multiple times, we keep a track 
        #  of what we've uploaded before
        # 
        # instead of iterating through all locally stored days data, we 
        #  request from the local database the next day data item that we 
        #  know we have not yet uploaded
        # 
        # once successfully uploaded, we inform the local client database, so 
        #  that it will not attempt this again

        updat = ccdatabase.GetDayDataToUpload()
        while updat:
            (tocontinue, toskip) = progdlg.Update(curidx, 'Uploading daily data')
            if tocontinue == False:
                progdlg.Update(numitems, "Cancelled")
                progdlg.Destroy()
                return False

            curidx += 1

            # don't upload empty items (CurrentCost meters fill in empty 
            #   values with 0)

            if updat['ccvalue'] > 0:
                postreq_data = urllib.urlencode( { "ccdatatype"  : "day",
                                                   "ccdatavalue" : updat['ccvalue'],
                                                   "ccyear"      : updat['timestamp'].year,
                                                   "ccmonth"     : updat['timestamp'].month,
                                                   "ccdate"      : updat['timestamp'].day,
                                                   "cchour"      : 0 } )
                post_req = urllib2.Request('http://currentcost.appspot.com/ccdata/add', data=postreq_data)
                post_resp = urllib2.urlopen(post_req)
                post_resp_body = post_resp.read()
    
                if post_resp_body != "OK":
                    print post_resp_body

            # mark this as uploaded, and get the next one to upload
            ccdatabase.ConfirmDayDataUploaded(updat)
            updat = ccdatabase.GetDayDataToUpload()


        ################################################################
        # 
        # UPLOAD    MONTHS
        # 
        ################################################################

        progdlg.Update(curidx, 'Uploading monthly data')
        curidx += 1

        # each data item is uploaded individually
        #  so we want to loop through all of the locally stored data items
        #   uploading each one in turn
        # 
        # so that we don't upload a data item multiple times, we keep a track 
        #  of what we've uploaded before
        # 
        # instead of iterating through all locally stored months data, we 
        #  request from the local database the next month data item that we 
        #  know we have not yet uploaded
        # 
        # once successfully uploaded, we inform the local client database, so 
        #  that it will not attempt this again

        updat = ccdatabase.GetMonthDataToUpload()
        while updat:
            (tocontinue, toskip) = progdlg.Update(curidx, 'Uploading monthly data')
            if tocontinue == False:
                progdlg.Update(numitems, "Cancelled")
                progdlg.Destroy()
                return False

            curidx += 1

            # don't upload empty items (CurrentCost meters fill in empty 
            #   values with 0)

            if updat['ccvalue'] > 0:  
                postreq_data = urllib.urlencode( { "ccdatatype"  : "month",
                                                   "ccdatavalue" : updat['ccvalue'],
                                                   "ccyear"      : updat['timestamp'].year,
                                                   "ccmonth"     : updat['timestamp'].month,
                                                   "ccdate"      : updat['timestamp'].day,
                                                   "cchour"      : 0 } )
                post_req = urllib2.Request('http://currentcost.appspot.com/ccdata/add', data=postreq_data)
                post_resp = urllib2.urlopen(post_req)
                post_resp_body = post_resp.read()
    
                if post_resp_body != "OK":
                    print post_resp_body
    
            # mark this as uploaded, and get the next one to upload
            ccdatabase.ConfirmMonthDataUploaded(updat)
            updat = ccdatabase.GetMonthDataToUpload()

        #
        # complete. tidy-up
        progdlg.Update(curidx, 'Upload complete')
        progdlg.Destroy()
        return True
        

    #
    # log on to Google App Engine
    # 
    def AuthenticateWebService(self, users_email_address, users_password):
        # we use a cookie to authenticate with Google App Engine
        #  by registering a cookie handler here, this will automatically store the 
        #  cookie returned when we use urllib2 to open http://currentcost.appspot.com/_ah/login
        cookiejar = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        urllib2.install_opener(opener)
        
        #
        # get an AuthToken from Google accounts
        #
        auth_uri = 'https://www.google.com/accounts/ClientLogin'
        authreq_data = urllib.urlencode({ "Email":   users_email_address,
                                          "Passwd":  users_password,
                                          "service": "ah",
                                          "source":  "currentcostclient",
                                          "accountType": "HOSTED_OR_GOOGLE" })
        auth_req = urllib2.Request(auth_uri, data=authreq_data)
        auth_resp = urllib2.urlopen(auth_req)
        auth_resp_body = auth_resp.read()
        # auth response includes several fields - we're interested in 
        #  the bit after Auth= 
        auth_resp_dict = dict(x.split("=")
                              for x in auth_resp_body.split("\n") if x)
        authtoken = auth_resp_dict["Auth"]
        
        #
        # get a cookie
        # 
        #  the call to request a cookie will also automatically redirect us to the page
        #   that we want to go to
        #  the cookie jar will automatically provide the cookie when we reach the 
        #   redirected location
        
        serv_uri = 'http://currentcost.appspot.com/ccdata/auth'
        
        serv_args = {}
        serv_args['continue'] = serv_uri
        serv_args['auth']     = authtoken
        
        full_serv_uri = "http://currentcost.appspot.com/_ah/login?%s" % (urllib.urlencode(serv_args))
        
        serv_req = urllib2.Request(full_serv_uri)
        serv_resp = urllib2.urlopen(serv_req)
        serv_resp_body = serv_resp.read()


    # 
    # query the web service for the latest version of the client application
    # 
    def GetDesktopVersion(self):
        try:  
            post_req = urllib2.Request('http://currentcost.appspot.com/svc/version')
            post_resp = urllib2.urlopen(post_req)
            post_resp_body = post_resp.read()
            return post_resp_body
        except:
            return "unknown"

