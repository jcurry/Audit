#!/usr/bin/env python
# Author:		Jane Curry
# Date			Sept 18th 2012
# Description:		Output all Maintenance Windows to a file supplied by user
#                       Output gives Maintenance Windows
#                       Output is sorted on Maintenance Windows
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
of.write(localtime + "\n\n")

# Need noopts=True or it barfs with the script options
dmd = ZenScriptBase(connect=True, noopts=True).dmd

zendev = dmd.Devices.findDevice('*')
mwin=zendev.maintenanceWindowSearch()

colList=[]
for c in mwin:
  colList.append(c)
colList.sort()

tuplist=[]
#for c in colList:
for c in zendev.maintenanceWindowSearch():
  ob=c.getObject()
  devlist=[]
  for d in ob.fetchDevices():
    devlist.append(d.id)
  devlist.sort()
  if ob.started:
    startedTime=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(ob.started))
  else:
    startedTime='None'
  if ob.start:
    startTime=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(ob.start))
  else:
    startedTime='None'
  tup=( ob.displayName(), str(ob.target()), ob.enabled, startTime, ob.duration, ob.repeat, startedTime, devlist)
  tuplist.append(tup)
tuplist.sort()

for i in tuplist:
  of.write('Maintenance Window %s  Target is %s Enabled is %s Start Time is %s Duration is %s mins Repeat is %s Started Time is %s \n\n' % (i[0], i[1], i[2], i[3], i[4], i[5], i[6] ))
  of.write('    Devices for this maintenance window are %s \n' % (i[7]))
  of.write('\n')


of.close()

