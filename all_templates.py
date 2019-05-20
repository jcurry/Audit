#!/usr/bin/env python
# Author:		Jane Curry
# Date			June 3rd 2016
# Description:		Output all local templates for a device to  a file
#                       Includes interface and filesystem components
#                       Output is sorted on device id
# Parameters:		File name for output
# Updated:              April 24th, 2019
#                       Outputs all templates for every device, noting which are local
#                       Includes all components with option for component class exclusion list
#
import sys
import time
from optparse import OptionParser
import Globals
from Products.ZenUtils.Utils import unused
unused(Globals)
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

# Component classes to exclude
#excludeComponentsList = []
#excludeComponentsList = ['IpService', 'OSProcess', 'IpRouteEntry', 'RabbitMQExchange']
excludeComponentsList = ['IpRouteEntry', 'RabbitMQExchange']
if excludeComponentsList:
    of.write(" Note that the following component classes are excluded from template processing %s \n\n" % (excludeComponentsList))

for dev in deviceList:
  d = dmd.Devices.findDevice(dev)
  of.write("\n Device Id %s \t Device Title %s \n" % (d.id, d.title))
  # get all device templates
  for t in d.getRRDTemplates():
      localDeviceFlag=False
      if d == t.__primary_parent__:
          localDeviceFlag=True  

      of.write("\t Device template is Local? %s \t Template Name %s \t Device template path %s \n" % ( localDeviceFlag, t.id, t.getRRDPath()))

  of.write("\t End of device templates.  Component templates are: \n")
  for comps in d.getDeviceComponents():
      if not comps.__class__.__name__ in excludeComponentsList:
          #of.write("\t \t Component %s of component class %s \n" % (comps.id, comps.__class__))
          of.write("\t \t Component %s of component class %s \n" % (comps.id, comps.__class__.__name__))
          #  Get all the component templates
          for compTemplate in comps.getRRDTemplates():
              comptpath = compTemplate.getRRDPath()
              localCompFlag = False
              if comptpath.find(d.id) >= 0:
                  localCompFlag = True
              of.write("\t \t  \t Template is Local ? %s \t Component template name is %s Component template path %s \n" % (localCompFlag, compTemplate.id, comptpath))

of.close()

