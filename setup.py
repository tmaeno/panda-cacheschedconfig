#!/usr/bin/env python
#
# Setup prog for cacheschedconfig
#
#
release_version='1.3.10'

import os
import stat
import glob
from setuptools import setup

        
# setup for distutils
setup(
    name="panda-cacheschedconfig",
    version=release_version,
    description='panda-cacheschedconfig package',
    long_description='''This package contains cacheschedconfig''',
    license='GPL',
    author='Panda Team',
    author_email='atlas-adc-panda-support@cern.ch',
    maintainer='Panda Team',
    maintainer_email='atlas-adc-panda-support@cern.ch',
    url='https://twiki.cern.ch/twiki/bin/view/Atlas/PanDA',
    packages=['cacheschedconfig'],
    data_files=[
                # crontab file
                ('/etc/cron.d', ['cron/cacheschedconfig',
                                 'cron/cachepilot',
                                       ]
                 ),
                # Utility wrapper script and main script
                ('/opt/cacheschedconfig/bin', ['bin/cacheSC.sh',
                                               'bin/cacheSchedConfig.py',
                                               'bin/cachePilots.sh',
                                               ]
                 ),
                ('/opt/cacheschedconfig/etc/sysconfig', ['etc/cacheschedconfig-sysconfig',
                                                         'etc/cachepilot-sysconfig',
                                                         ]
                 ),
                ]
)


for f in glob.glob(os.path.join('/opt/cacheschedconfig/bin','*.sh')):
    st = os.stat(f)
    try:
        os.chmod(f, st.st_mode|stat.S_IEXEC|stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)
    except Exception:
        pass
