###############################################################################
# 
# CurrentCost
# 
#  A Python application to graphically represent data received from a 
#   CurrentCost meter.
# 
#  Useful links:
#  -------------   
#     Overview of the app
#                            http://code.google.com/p/currentcostgui/
#  
#     Blog posts:
#         1st version of the app              http://dalelane.co.uk/blog/?p=280
#                                             http://dalelane.co.uk/blog/?p=281
#         Re-working the app plans            http://dalelane.co.uk/blog/?p=288
#         Current version of the app          http://dalelane.co.uk/blog/?p=297
#         Seeking feedback                    http://dalelane.co.uk/blog/?p=298
#         Adding web services functions       http://dalelane.co.uk/blog/?p=305
#         Seeking testers for web services    http://dalelane.co.uk/blog/?p=307
#         Setting personal targets            http://dalelane.co.uk/blog/?p=333
#         Adding webservice showing all users http://dalelane.co.uk/blog/?p=434
#         Updating the parser                 http://dalelane.co.uk/blog/?p=456
#         Graphing National Grid data         http://dalelane.co.uk/blog/?p=469
#         Measuring costs from live graph     http://dalelane.co.uk/blog/?p=1142
# 
#     Providing support
#         http://getsatisfaction.com/dalelane/products/dalelane_currentcost_gui
#
# 
# 
#  Dale Lane (http://dalelane.co.uk/blog)
#
###############################################################################


############################################################################
# 
# OVERVIEW OF THE CODE
# ====================
# 
#   currentcost.py               - main entry function, and implements the 
#                                     GUI's menus and their actions
#   currentcostserialconn.py     - makes a serial connection to a CurrentCost
#                                     meter
#   currentcostdata.py           - represents data contained in a single 
#                                     update from a CurrentCost meter
#   currentcostparser.py         - CurrentCost XML data parser used when 
#                                     receiving data over serial connection
#   currentcostdataconvert.py    - used by XML parser to convert relative 
#                                     time descriptions into absolute
#   currentcostdatafunctions.py  - converts the relative description of usage
#                                     in a CurrentCost update into absolute
#   currentcostdb.py             - sqlite DB to persist CurrentCost usage 
#                                     data, and settings and preferences
#   currentcostgraphs.py         - matplotlib/wxPython code to implement the 
#                                     tabs that make up the GUI
#   currentcostvisualisations.py - draws bar graphs of CurrentCost data
#   currentcostmqtt.py           - downloads history data from a remote 
#                                     CurrentCost meter via MQTT
#   googleappengine.py           - gets data from a Google App Engine web 
#                                     service to show other user's data
#   currentcostlivedata.py       - draws tab to display a graph of live data
#   currentcostmqttlive.py       - downloads live data for the live graph 
#                                     from a remote CurrentCost meter via MQTT
#   currentcostcomlive.py        - downloads live data for the live graph 
#                                     from a CurrentCost meter
#   currentcosthistorydata       - implements a download manager to handle 
#                                     background downloading of history data
#   currentcostmqtthistory.py    - downloads historical data if downloading 
#                                     all updates in background via MQTT
#   currentcostcomhistory.py     - downloads historical data if downloading 
#                                     all updates in background 
#   nationalgriddata.py          - downloads live national electricity usage 
#                                     data from the National Grid realtime feed
# 
############################################################################

#############################################################################
#
# RUNNING THE CODE
# ================
#
#  python currentcost.py
#
#    list of required pre-requisites maintained at
#     http://code.google.com/p/currentcostgui/wiki/Prerequisites
#
#############################################################################
