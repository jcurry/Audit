#!/usr/bin/env python

# Author:               Jane Curry
# Date                  Dec 13th 2013
# Description:          This doesn't provide pretty output as a notification may have several triggers
#                       You get all TRIGGERNAMEs, followed by all TRIGGERUUIDs, followed by all TRIGGERRULEs
#                       However, it provides the linkage between notifications and the triggers that drive them
#                       and shows the use of the trigger uuid from the notification being used to access the
#                       trigger rule
# Parameters:           File name for output
# Updates:              October 13th 2014.  Explicitly output triggers and notifications
#

import Globals
import sys
import time
from optparse import OptionParser
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

dmd = ZenScriptBase(connect=True, noopts=True).dmd

from Products.Zuul import getFacade
facade = getFacade('triggers')
 
of.write('TRIGGERS \n')
# get sorted list of triggers
triglist = []
for trig in facade.getTriggers():
    triglist.append(trig)
newtriglist = sorted(triglist, key=lambda p: str(p['name']))

for trig in newtriglist:
    of.write(' Trigger name %s    Trigger Rule %s \n ' % (str(trig['name']), str(trig['rule']['source'])))

of.write('\n NOTIFICATIONS \n')
notiflist = []
for note in facade.getNotifications():
    notiflist.append(note)
newnotiflist = sorted(notiflist, key=lambda p: str(p.name))

for note in newnotiflist:
    rp = ''
    subsname = ''
    subsuuid = ''
    substrigrule = ''
    try:
      if len(note.recipients) == 0:
        rp = 'NONE'
      else:
        for recip in range(0,len(note.recipients)):
          rp = rp + str(note.recipients[recip]['label']) + '::'
    except:
      pass

    try:
      if len(note.subscriptions) == 0:
        subsname = 'NONE'
      else:
        for s in range(0,len(note.subscriptions)):
          subsname = subsname + str(note.subscriptions[s]['name']) + '::'
          subsuuid = subsuuid + str(note.subscriptions[s]['uuid']) + '::'
          # Use the note.subscriptions[s]['uuid'] field to access other data about the trigger
          trig = facade.getTrigger(note.subscriptions[s]['uuid'])
          substrigrule = substrigrule + 'Trigger Name: ' + str(trig['name']) + ' :  Trigger rule: ' + str(trig['rule']['source']) + '::'
    except:
      pass
    of.write('       Name %s  Enabled %s Description %s Delay Secs %s Repeat %s Subscriber Name %s Subscriber UUID %s Subscriber trigger rule:  %s  \n ' % (str(note.name), str(note.enabled), str(note.description), str(note.delay_seconds), rp,  subsname,  subsuuid,  substrigrule))
