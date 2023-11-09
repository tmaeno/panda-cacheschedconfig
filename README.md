This package has been merged into PanDA server > daemons and is no longer used as a standalone package
------------------------------------------------------------------------------------------------------


cachescedconfig
---------------

cacheschedconfig dumps schedconfig into a single directory organised
by queue, in order to make queue data downloads both fast and robust.

The RPM also includes code to build the pilot tarball caches from SVN.


How it works
------------

The RPM installs the cron files cachepilot and cacheschedconfig into /etc/cron.d.

The crons run the wrapper scripts cachePilots.sh and cacheSC.sh.

cachePilots.sh is a self contained shell script.

cacheSC.sh adds the correct option for the cache location to the real script,
which is cacheSchedConfig.py.

cacheSchedConfig.py uses the CacheSchedConfig module to do the actual work of
interacting with the DB tables and building the cached output files.

In each case the code should be reasonably straightforward to understand.


Adding fields for the pilot
---------------------------

The cacheSchedConfig.queueDataFields controls which fields find their way into
the pilot and factory versions of the schedconfig cache files. To add a new field
for the pilot just add it to the cacheSchedConfig.queueDataFields['pilot'] list.

Note the list of fields is independent of the format used in the cache (which can
be 'pilot', 'txt' or 'json').

Please see the INSTALLATION file for advice on deployment at CERN.


Installation
--------

To build this package from source do

git clone panda-cacheschedconfig
cd panda-cacheschedconfig
rm -rf dist; python setup.py sdist; pip install dist/p*.tar.gz --upgrade --force-reinstall --no-deps; pip install dist/p*.tar.gz --upgrade
