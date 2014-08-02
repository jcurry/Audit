#!/usr/bin/env python
# Author:		Jane Curry
# Date			Sept 2828th 2012
# Description:		Output all alerting rules with schedules for a user, to a file supplied by user
#                       Output gives user, user/group association, alerting rule, schedule
#                       Output includes users individual rules and those for user groups that they are a member of
#                       Output is sorted on User, then alerting rule, then schedule
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

uList=[]
for u in dmd.ZenUsers.getAllUserSettingsNames():
  uList.append(u)
uList.sort()

for u in uList:
  of.write('User %s : \n' % (u))
  usetting = dmd.ZenUsers.getUserSettings(u)

  # Do alerting rules for specific user first
  if usetting.getActionRules():
    arList=[]
    for r in usetting.getActionRules():
      arList.append(r)
    arList.sort()
    for r in arList:
      of.write('    Rule id %s , where clause %s , sendClear is %s , Delay is %s , Action type is %s , Enabled? %s  \n' % ( r.id, r.where, r.sendClear, r.delay, r.action, r.enabled))

    # Get schedules for rule if they exist
    if r.windows():
      wList=[]
      for w in r.windows():
        wList.append(w)
      wList.sort()
      for w in wList:
        of.write('        Schedule for rule %s is called %s , start time is %s , duration is %s minutes, Repeat factor is %s \n' % (r.id, w.id, time.asctime( time.localtime(w.start) ),  w.duration, w.repeat))

  # Then check user groups that a user is in
  # Need to exclude admin user as it seems to have a tuple for its getUserGroupSettingsNames() rather than a list
  # Need to check whether group exists or not
#  if u != 'admin':
  if True:  
    userGroupsList = usetting.getUserGroupSettingsNames() 
    if userGroupsList:
      userGroupsList.sort() 
      of.write('    User %s is in User Groups %s  \n' % (u, str(usetting.getUserGroupSettingsNames())))
      for g in userGroupsList:
        of.write('Group %s : \n' % (g))
        gsetting = dmd.ZenUsers.getGroupSettings(g)
        # Check whether rule exists for this group
        if gsetting.getActionRules():
          arList=[]
          for r in gsetting.getActionRules():
            arList.append(r)
          arList.sort()
          for r in arList:
            of.write('    Rule id %s , where clause %s , sendClear is %s , Delay is %s , Action type is %s , Enabled? %s  \n' % ( r.id, r.where, r.sendClear, r.delay, r.action, r.enabled))

          # Check whether the rule has a schedule
          if r.windows():
            wList=[]
            for w in r.windows():
              wList.append(w)
            wList.sort()
            for w in wList:
              of.write('        Schedule for rule %s is called %s , start time is %s , duration is %s minutes, Repeat factor is %s \n' % (r.id, w.id, time.asctime( time.localtime(w.start) ),  w.duration, w.repeat))
    of.write('\n')
of.write('\n')

of.close()

