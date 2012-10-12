#!/usr/bin/env python
# Author:		Jane Curry
# Date			Sept 11th 2012
# Description:		Output all devices to a file supplied by user
#                       Output gives id, title and manageIp
#                       Output is sorted on device id
# Parameters:		File name for output
# Updates:		Updated to print NO IP ADDRESS is no manageIp attribute
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
  if d.manageIp:
    of.write("Device Id %s \t Device Title %s \t Device manageIp %s \n" % (d.id, d.title, d.manageIp))
  else:
    of.write("Device Id %s \t Device Title %s \t Device manageIp NO IP ADDRESS \n" % (d.id, d.title))

of.close()

