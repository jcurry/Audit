#!/usr/bin/env python
# Author:		Jane Curry
# Date			Sept 18th 2012
# Description:		Output all groups with alerting rules with schedules to a file supplied by user
#                       Output gives group, alerting rule, schedule
#                       Output is sorted on group, then alerting rule, then schedule
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
for u in dmd.ZenUsers.getAllGroupSettingsNames():
  uList.append(u)
uList.sort()

for u in uList:
  of.write(' Group %s : \n' % (u))
  usetting = dmd.ZenUsers.getGroupSettings(u)
    # do standard stuff first
  of.write(' Group %s settings: netMapStartObject is %s , Default Admin Role is %s , email is %s \n' % (u, usetting.netMapStartObject, usetting.defaultAdminRole, usetting.email))
  # Then do roles and groups
  # NB. no roles for Groups
  #if usetting.adminRoles():
  #  of.write('Admin Roles for %s are %s \n' % (u, str(usetting.adminRoles())))
  # NB. no roles for Groups
  of.write(' Group %s has Users %s in this Group  \n' % (u, str(usetting.getMemberUserIds())))
  # Then alerting rules
  if usetting.getActionRules():
    arList=[]
    for r in usetting.getActionRules():
      arList.append(r)
    arList.sort()
    for r in arList:
      of.write('    Rule id %s , where clause %s , sendClear is %s , Delay is %s , Action type is %s , Enabled? %s  \n' % ( r.id, r.where, r.sendClear, r.delay, r.action, r.enabled))
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

