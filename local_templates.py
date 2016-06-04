#!/usr/bin/env python
# Author:		Jane Curry
# Date			June 3rd 2016
# Description:		Output all local templates for a device to  a fil
#                       Includes interface and filesystem components
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
  for t in d.getRRDTemplates():
      if d == t.__primary_parent__:

        of.write("Device Id %s \t Device Title %s \t Local Device templates %s Local Device template path %s \n" % (d.id, d.title, t.id, t.getRRDPath()))
  for fs in d.os.filesystems():
      for t in fs.getRRDTemplates():
          tpath = t.getRRDPath()
          if tpath.find(d.id) >= 0:
              of.write("\t Device id %s \t FileSystem Id %s \t  Local Device Filesystem template %s \t Local Device Filesystem template path %s \n" % (d.id, fs.title,  t.id, tpath))

  for i in d.os.interfaces():
      for t in i.getRRDTemplates():
          tpath = t.getRRDPath()
          if tpath.find(d.id) >= 0:
              of.write("\t \t Device id %s \t Interface Id %s \t  Local Device Interface template %s \t Local Device Interface template path %s \n" % (d.id, i.id,  t.id, tpath))


of.close()

