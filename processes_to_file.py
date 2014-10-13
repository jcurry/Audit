#!/usr/bin/env python
# Author:		Jane Curry
# Date			Sept 19th 2012
# Description:		Output all Processes in osProcessClasses (/) process suborganizers
#                       Output gives process name / organizer name and process name
#                       Output is sorted on organizer and then process name
# Parameters:		File name for output
# Updates:              October 13th, 2014  Sort process organizers based on organizer name
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

  newdclist = sorted(dclist, key=lambda p: p.getOrganizerName() )
  for po in newdclist:
    of.write('Process Organizer %s \n' % (po.getOrganizerName()))
    proclist=[]
    for p in po.osProcessClasses():
      tup=(p.id, p.regex, p.ignoreParameters, p.zMonitor)
      proclist.append(tup)
    # Need to get a sorted list of processes
    proclist.sort()
    for p in proclist:
      of.write('    Process Id %s , Process regex %s , Ignore Parameters is %s , Zmonitor flag is %s \n' % (p[0], p[1], p[2], p[3]))
    of.write('\n')

traverse.level = 1
root = dmd.getDmdRoot('Processes')
traverse(root, of)
printTree(dclist, of)

of.close()

