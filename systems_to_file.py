#!/usr/bin/env python
# Author:		Jane Curry
# Date			Sept 11th 2012
# Description:		Output all Systems with device instances to a file supplied by user
#                       Output gives System and device id
#                       Output is sorted on System and then device id
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

dclist=[]
def traverse(dc, of):
  dclist.append(dc)
  for subdc in dc.children():
    traverse.level +=1
    traverse(subdc, of)
    traverse.level -=1
  return dclist.sort()

def printTree(dclist, of):
  # First sort the device classes by path name
  listNames=[]
  for dc in dclist:
    listNames.append(dc.getOrganizerName())
  listNames.sort()

  for dcname in listNames:
    dc=root.getOrganizer(dcname)
    of.write('System %s \n' % (dc.getOrganizerName()))
    of.write('    Devices: for system %s ' % (dc.getOrganizerName()))
    devlist=[]
    for d in dc.getSubDevices():
      devlist.append(d.id)
    # Need to get a sorted list of devices
    devlist.sort()
    for dev in devlist:
      d=dmd.Devices.findDevice(dev)
      of.write(' %s ,' % (d.id))
    of.write('\n\n')

traverse.level = 1
root = dmd.getDmdRoot('Systems')
traverse(root, of)
printTree(dclist, of)

of.close()

