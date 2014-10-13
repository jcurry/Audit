#!/usr/bin/env python
# Author:		Jane Curry
# Date			Sept 12th 2012
# Description:		Output all Mibs in mibs (/)and mib suborganizers
#                       Output gives organizer name and MIB name
#                       Output is sorted on organizer and then MIB name
# Parameters:		File name for output
# Updates:              October 13th, 2014  Sort mib organizers based on organizer name

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
  for mo in newdclist:
    of.write('Mib Organizer %s \n' % (mo.getOrganizerName()))
    of.write('    Mibs: ')
    miblist=[]
    for m in mo.mibs():
      miblist.append(m.id)
    # Need to get a sorted list of mibs
    miblist.sort()
    for m in miblist:
      of.write(' %s ,' % (m))
    of.write('\n\n')

traverse.level = 1
root = dmd.getDmdRoot('Mibs')
traverse(root, of)
printTree(dclist, of)

of.close()

