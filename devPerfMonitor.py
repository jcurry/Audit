#!/usr/bin/env python
# Author:		Jane Curry
# Date			Dec 20th 2013
# Description:		Output the performance monitor for all devices
#                       Output gives device id and performance monitor
#                       Output is sorted on device id
# Parameters:		File name for output
#
import sys
import time
from optparse import OptionParser
import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase


parser = OptionParser()
parser.add_option("-f", "--file", dest="outputFile",
                  help="Please specify full path to output file", metavar="FILE")

(options, args) = parser.parse_args()

if not options.outputFile:
    parser.print_help()
    sys.exit()

of = open(options.outputFile, "w")
localtime = time.asctime( time.localtime(time.time()) )
of.write(localtime + "\n\n")

# Need noopts=True or it barfs with the script options
dmd = ZenScriptBase(connect=True, noopts=True).dmd

deviceList=[]
for dev in dmd.Devices.getSubDevices():
  deviceList.append(dev.id)
#Sort the device on id
deviceList.sort()

for dev in deviceList:
  d = dmd.Devices.findDevice(dev)
  of.write("Device Id %s \t \t \t \t Performance monitor %s \n" % (d.id, d.getPerformanceServerName()))

of.close()

