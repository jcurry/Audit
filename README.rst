==========================================================
Audit scripts to document data in the Zenoss Zope database
==========================================================


Description
===========

These python scripts have been designed to document the contents of various elements
in the Zenoss Zope database.
    * Devices
    * Device Classes
    * Device Groups
    * Systems
    * Locations
    * Event classes with mappings
    * Event transforms
    * Users
    * User groups
    * Alerting rules for users (including any user groups they are in)
    * Maintenance windows
    * Mibs
    * Processes
    * Collectors

The scripts take a single parameter, "-f <output file>" eg.

    ./deviceClasses_to_file.py -f deviceClasses_to_file.out


The output is text and all entries are sorted, with a view to being able to run these
audit scripts on an "old" system and a "new" system and diff the outputs.

Requirements & Dependencies
===========================

    * Zenoss Versions Supported: 3.x and 4.2
    * External Dependencies: None
    * ZenPack Dependencies: None
    * Installation Notes: Untar the package. Run as the zenoss user.
    * Configuration: 

Limitations
===========

Download
========
Download the package from:

* Zenoss Audit Scripts `Zenoss Audit Scripts`_


Change History
==============
    * 1.0 initial release


Screenshots
===========
|deviceClasses_to_file|
|processes_to_file|
|users_to_file|


.. External References Below. Nothing Below This Line Should Be Rendered

.. _Zenoss Audit Scripts: https://github.com/downloads/jcurry/Audit/zenoss_audit_scripts.tar

.. |deviceClasses_to_file| image:: http://github.com/jcurry/Audit/raw/master/screenshots/deviceClasses_to_file_out.jpg

                                                                        

