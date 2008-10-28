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
from pysqlite2 import dbapi2 as sqlite
import datetime, time

#
# We use a SQLite database to persist data - both historical CurrentCost data,
#   and user preferences and settings.
# 
# This class is used to provide the database.
# 
# 
#  Dale Lane (http://dalelane.co.uk/blog)

class CurrentCostDB():

    # connection to the database
    connection = None

    # connect to the database
    #
    # create tables if not already found
    # 
    def InitialiseDB(self, dbfilepath):
        self.connection = sqlite.connect(dbfilepath, detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
        cursor = self.connection.cursor()

        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND NAME="settings" ORDER BY name')
        if not cursor.fetchone():
            cursor.execute('CREATE TABLE settings(settingkey TEXT unique, settingvalue TEXT)')

        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND NAME="hourdata" ORDER BY name')
        if not cursor.fetchone():
            cursor.execute('CREATE TABLE hourdata(ts timestamp unique, ccvalue REAL, hourofday INT, uploaded INT)')
        
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND NAME="daydata" ORDER BY name')
        if not cursor.fetchone():
            cursor.execute('CREATE TABLE daydata(d date unique, ccvalue REAL, dayofweek INT, uploaded INT)')
        
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND NAME="monthdata" ORDER BY name')
        if not cursor.fetchone():
            cursor.execute('CREATE TABLE monthdata(d date unique, ccvalue REAL, uploaded INT)')

        self.connection.commit()

    # store a key-value pair in the database
    def StoreSetting(self, key, value):
        self.connection.execute('INSERT OR REPLACE INTO settings(settingkey, settingvalue) values(?, ?)',
                                (key, value))
        self.connection.commit()        

    # retrieve the value from a key-value pair in the database
    def RetrieveSetting(self, key):
        cursor = self.connection.cursor()
        cursor.execute('SELECT settingkey, settingvalue FROM settings WHERE settingkey="' + key + '"')
        row = cursor.fetchone()
        if row:
            return row[1]
        else:
            return None

    #
    ############################################################
    # helper functions for storing data in the database
    # 
    ############################################################ 
    #
    def StoreHourData(self, timestamp, ccvalue):
        self.connection.execute('INSERT OR REPLACE INTO hourdata(ts, ccvalue, hourofday, uploaded) values(?, ?, ?, ?)',
                                (timestamp, ccvalue, timestamp.hour, 0))
        self.connection.commit()
    def StoreDayData(self, timestamp, ccvalue):
        self.connection.execute('INSERT OR REPLACE INTO daydata(d, ccvalue, dayofweek, uploaded) values(?, ?, ?, ?)',
                                (timestamp, ccvalue, timestamp.weekday(), 0))
        self.connection.commit()
    def StoreMonthData(self, timestamp, ccvalue):
        self.connection.execute('INSERT OR REPLACE INTO monthdata(d, ccvalue, uploaded) values(?, ?, ?)',
                                (timestamp, ccvalue, 0))
        self.connection.commit()

    #
    ############################################################
    # helper functions for retrieving data from the database
    # 
    ############################################################ 
    #

    # COUNT THE NUMBER OF OBJECTS IN THE DATABASE

    def CountMonthData(self):
        cnt = 0
        for row in self.connection.execute("SELECT * FROM monthdata"):
            cnt += 1
        return cnt
    def CountDayData(self):
        cnt = 0
        for row in self.connection.execute("SELECT * FROM daydata"):
            cnt += 1
        return cnt
    def CountHourData(self):
        cnt = 0
        for row in self.connection.execute("SELECT * FROM hourdata"):
            cnt += 1
        return cnt


    ##################
    # MONTHS

    # get the next recorded month's electricity usage that we've not already
    #  uploaded to the Google App Engine web service
    def GetMonthDataToUpload(self):
        monthdataitem = {}
        cursor = self.connection.cursor()
        cursor.execute('SELECT d, ccvalue FROM monthdata WHERE uploaded=0')
        row = cursor.fetchone()
        if row:
            monthdataitem['timestamp'] = row[0]
            monthdataitem['ccvalue']   = row[1]
            return monthdataitem
        else:
            return None

    # confirm that the provided data item has been uploaded successfully, so 
    #  that it will not be uploaded again
    def ConfirmMonthDataUploaded(self, monthdataitem):
        self.connection.execute('INSERT OR REPLACE INTO monthdata(d, ccvalue, uploaded) values(?, ?, ?)',
                                (monthdataitem['timestamp'], monthdataitem['ccvalue'], 1))
        self.connection.commit()

    # convert the database's store of monthly electricity usage into a 
    #  dictionary. 
    # 
    # this is a hang-over from an earlier version of the application which used
    #  pickle to store dictionaries as a way of persisting historical data
    # 
    # the conversion to using pysqlite is not complete, so this is a helper 
    #  function used by methods which depend on having a dictionary
    # 
    # ideally, this function will no longer be required once the migration to 
    #  pysqlite is complete.
    # 
    def GetMonthDataCollection(self):
        monthdatacollection = {}
        for row in self.connection.execute("SELECT d, ccvalue FROM monthdata"):
            monthdatacollection[row[0]] = row[1]
        return monthdatacollection


    ##################
    # DAYS

    # get the next recorded day's electricity usage that we've not already
    #  uploaded to the Google App Engine web service
    def GetDayDataToUpload(self):
        daydataitem = {}
        cursor = self.connection.cursor()
        cursor.execute('SELECT d, ccvalue FROM daydata WHERE uploaded=0')
        row = cursor.fetchone()
        if row:
            daydataitem['timestamp'] = row[0]
            daydataitem['ccvalue']   = row[1]
            return daydataitem
        else:
            return None

    # confirm that the provided data item has been uploaded successfully, so 
    #  that it will not be uploaded again
    def ConfirmDayDataUploaded(self, daydataitem):
        self.connection.execute('INSERT OR REPLACE INTO daydata(d, ccvalue, uploaded) values(?, ?, ?)',
                                (daydataitem['timestamp'], daydataitem['ccvalue'], 1))
        self.connection.commit()

    # convert the database's store of day electricity usage into a 
    #  dictionary. 
    # 
    # this is a hang-over from an earlier version of the application which used
    #  pickle to store dictionaries as a way of persisting historical data
    # 
    # the conversion to using pysqlite is not complete, so this is a helper 
    #  function used by methods which depend on having a dictionary
    # 
    # ideally, this function will no longer be required once the migration to 
    #  pysqlite is complete.
    # 
    def GetDayDataCollection(self):
        daydatacollection = {}
        for row in self.connection.execute("SELECT d, ccvalue FROM daydata"):
            daydatacollection[row[0]] = row[1]
        return daydatacollection


    ##################
    # HOURS

    # get the next recorded hours' electricity usage that we've not already
    #  uploaded to the Google App Engine web service
    def GetHourDataToUpload(self):
        hourdataitem = {}
        cursor = self.connection.cursor()
        cursor.execute('SELECT ts, ccvalue FROM hourdata WHERE uploaded=0')
        row = cursor.fetchone()
        if row:
            hourdataitem['timestamp'] = row[0]
            hourdataitem['ccvalue']   = row[1]
            return hourdataitem
        else:
            return None

    # confirm that the provided data item has been uploaded successfully, so 
    #  that it will not be uploaded again
    def ConfirmHourDataUploaded(self, hourdataitem):
        self.connection.execute('INSERT OR REPLACE INTO hourdata(ts, ccvalue, uploaded) values(?, ?, ?)',
                                (hourdataitem['timestamp'], hourdataitem['ccvalue'], 1))
        self.connection.commit()

    # convert the database's store of hourly electricity usage into a 
    #  dictionary. 
    # 
    # this is a hang-over from an earlier version of the application which used
    #  pickle to store dictionaries as a way of persisting historical data
    # 
    # the conversion to using pysqlite is not complete, so this is a helper 
    #  function used by methods which depend on having a dictionary
    # 
    # ideally, this function will no longer be required once the migration to 
    #  pysqlite is complete.
    # 
    def GetHourDataCollection(self):
        hourdatacollection = {}
        for row in self.connection.execute("SELECT ts, ccvalue FROM hourdata"):
            hourdatacollection[row[0]] = row[1]
        return hourdatacollection

