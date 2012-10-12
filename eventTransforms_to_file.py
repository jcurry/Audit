#!/usr/bin/env python
# Author:		Jane Curry
# Date			Sept 12th 2012
# Description:		Output all event classes with event transforms to a file supplied by user
#                       Output gives event class, event class transform and any event class mapping transform
#                       Output is sorted on event class and then event class transform
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
  # First sort the event classes by path name
  listNames=[]
  for dc in dclist:
    listNames.append(dc.getOrganizerName())
  listNames.sort()

  for dcname in listNames:
    dc=root.getOrganizer(dcname)
    if dc.transform:
      of.write('Event class %s Event Class Transform\n' % (dc.getOrganizerName()))
      of.write('%s \n' % (dc.transform))
      of.write('\n')
    maplist=[]
    for mi in dc.instances():
      maplist.append(mi)
    # Need to get a sorted list of mappings
    maplist.sort()
    for map in maplist:
      if map.transform:
        of.write('Event class %s : Event Class Mapping Transform for %s : \n' % (dc.getOrganizerName(), map.id))
        of.write('%s \n' % (map.transform))
        of.write('\n')

traverse.level = 1
root = dmd.getDmdRoot('Events')
traverse(root, of)
printTree(dclist, of)

of.close()

