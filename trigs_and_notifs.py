#!/usr/bin/env python

# Author:               Jane Curry
# Date                  Dec 13th 2013
# Description:          This doesn't provide pretty output as a notification may have several triggers
#                       You get all TRIGGERNAMEs, followed by all TRIGGERUUIDs, followed by all TRIGGERRULEs
#                       However, it provides the linkage between notifications and the triggers that drive them
#                       and shows the use of the trigger uuid from the notification being used to access the
#                       trigger rule
# Parameters:           File name for output
# Updates:              Feb 5th 2016
#                       Finally sorted out subscription linkages from triggers and notifications
#                       Note that some triggers appear to have subscribers that don't link back to a name
#                         through the subscriber_uuid and these pairings do NOT appear in the GUI
#

import Globals
import sys
import time
import pprint
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
 
of.write('NOTIFICATION LIST\n\n') 
of.write('=================\n')


# get sorted list of notifications
notiflist = []
for note in facade.getNotifications():
    notiflist.append(note)
newnotiflist = sorted(notiflist, key=lambda p: str(p.name))

for note in newnotiflist:
    # Notification is an object
    # Recipients is a list of user dictionaries where user is
    #   { label , manage, type, value (UUID), write }
    # Deliver a list of user / group names
    recip_string = ''
    substrigrule = ''
    try:
      if len(note.recipients) == 0:
        recip_string = 'No Users'
      else:
        for rp in note.recipients:
          recip_string = recip_string + rp['label'] + "    "
    except:
      pass

    try:
      # Subscriptions is a list of trigger dictionary links where
      #    subscriptions is { name, UUID }
      for s in note.subscriptions:
        # Use the note.subscriptions[s]['uuid'] field to access other data about the trigger
        # Deliver a string with all the trigger rules
        trig = facade.getTrigger(s['uuid'])
        substrigrule = substrigrule + '    ' + trig['name'] + '  ' + str(trig['rule']['source']) + '\n'
    except:
      pass
    # The _guid field is what needs to marry up with the subscriber_uuid in the trigger['subscriptions']
    of.write('NOTIFICATION Name %s  Enabled %s Description %s Action %s Delay Secs %s Repeat %s  _guid %s  \n ' % (str(note.name), str(note.enabled), str(note.description), str(note.action), str(note.delay_seconds), str(note.repeat_seconds), str(note._object._guid) ))
    of.write('Recipients (users)  %s \n' % (recip_string))
    pprint.pprint(note.recipients, of)
    of.write('\n')
    of.write('Subscriptions (ie. Triggers) \n')
    pprint.pprint(note.subscriptions, of)
    of.write('\n')
    of.write('Subscriber trigger rules \n ')
    of.write('%s \n\n ' % (substrigrule))

# get sorted list of triggers
triglist = []
for trig in facade.getTriggers():
    triglist.append(trig)
newtriglist = sorted(triglist, key=lambda p: str(p['name']))

of.write('\n\nTRIGGER LIST\n\n') 
of.write('============\n')
for trig in newtriglist:
    # trig is a dictionary with
    #    { name, uuid, enabled, rule, subscriptions, users}
    #        where rule is a dictionary { api_version, source, type}
    #        and subscriptions is a list of dictionaries of notifications with
    #             { delay_seconds, repeat_seconds, send_initial_occurrence, subscriber_uuid, trigger_uuid, uuid }
    #                where trigger_uuid matches this trigger's uuid field and subscriber_uuid matches notification _guid
    #        and users is a list of dictionaries of users with
    #             { label , manage, type, value (UUID), write }

    if 'subscriptions' in trig:
      for n in trig['subscriptions']:
          # Get the name of the notification in the subscription, if it exists
          # Note that there seem to be old? redundant? subscriptions that still exist
          # They are the ones whose subscriber_uuid does not match any notification object _guid
          try:  
              #of.write(' subscriber_uuid is %s and uuid is %s \n' % (n['subscriber_uuid'], n['uuid']))
              for n1 in facade.getNotifications():  
                  if n1._object._guid == n['subscriber_uuid']:
                      #of.write(' subscriber notification name is %s \n' % (n1._object.id))
                      n['notif_name'] = n1._object.id
          except:
            pass  

    of.write('TRIGGER name is %s  Enabled is %s UUID is %s  \n' % (trig['name'], trig['enabled'], trig['uuid']))
    if 'rule' in trig:
      of.write('Trigger rule is \n')
      pprint.pprint(trig['rule'], of)
    else:
      of.write(' No Trigger rules')
    of.write('\n')
    if 'subscriptions' in trig:
      of.write('Subscriptions (ie. Notifications) \n')
      for n in trig['subscriptions']:
        if 'notif_name' in n:
          pprint.pprint(n, of)
        else:
          of.write('No notification name for notification subscriber with subscriber_uuid %s \n' % (n['subscriber_uuid']))
    else:
      of.write('No Subscriptions (ie. Notifications) ')
    of.write('\n')
    if 'users' in trig:
      of.write('Users  \n')
      pprint.pprint(trig['users'], of)
    else:
      of.write(' No users')
    of.write('\n\n')
