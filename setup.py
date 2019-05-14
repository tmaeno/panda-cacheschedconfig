#!/usr/bin/env python
#
# Setup prog for cacheschedconfig
#
#
release_version='1.3.7'

import re
import sys
import commands
from distutils.core import setup
from distutils.command.install import install as install_org
from distutils.command.install_data import install_data as install_data_org

        
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
