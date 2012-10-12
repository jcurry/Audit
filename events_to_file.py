#!/usr/bin/env python
# Author:		Jane Curry
# Date			Sept 12th 2012
# Description:		Output all event classes with event mappings to a file supplied by user
#                       Output gives event class and event class mappings
#                       Output is sorted on event class and then event class mapping
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
    of.write('Event class %s \n' % (dc.getOrganizerName()))
    of.write('    Event Instances (mappings): ')
    maplist=[]
    for mi in dc.instances():
      if not mi.regex:
        mi.regex = 'None'
      tup = ( mi.id, mi.regex )
      maplist.append(tup)
    # Need to get a sorted list of mappings
    maplist.sort()
    for map in maplist:
      of.write(' Mapping instance %s , has regex %s' % (map[0], map[1]))
    of.write('\n\n')

traverse.level = 1
root = dmd.getDmdRoot('Events')
traverse(root, of)
printTree(dclist, of)

of.close()

