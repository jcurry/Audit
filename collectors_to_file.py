#!/usr/bin/env python
# Author:		Jane Curry
# Date			Sept 11th 2012
# Description:		Output all Collectors with device instances to a file supplied by user
#                       Output gives Collector and device id
#                       Output is sorted on Collector and then device id
# Parameters:		File name for output
# Updates:
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
of.write(localtime + "\n")

# Need noopts=True or it barfs with the script options
dmd = ZenScriptBase(connect=True, noopts=True).dmd

colList=[]
for c in dmd.Monitors.getPerformanceMonitorNames():
  colList.append(c)
colList.sort()

for c in colList:
  of.write(' Collector %s \n\n' % (c))
  of.write('     Devices for Collector %s: ' % (c) )
  m = dmd.getDmdRoot('Monitors').getPerformanceMonitor(c)
  devlist=[]
  for d in m.devices():
    devlist.append(d.id)
  devlist.sort()
  for dev in devlist:
    d=dmd.Devices.findDevice(dev)
    of.write(' %s ,' % (d.id))
  of.write('\n\n')


of.close()

