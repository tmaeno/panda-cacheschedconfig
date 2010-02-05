#! /bin/bash
#
# Build pilot tarball from SVN. Download RC pilot code from BNL
#
if [ -f /opt/cacheschedconfig/etc/sysconfig/cachepilot-sysconfig ]; then
    source /opt/cacheschedconfig/etc/sysconfig/cachepilot-sysconfig
fi

# Don't all fire at the same time
if [ "$1" != "--nowait" ]; then
    sleep $(($RANDOM%60))
fi

if [ ! -d $CACHEPATH ]; then
    mkdir -p $CACHEPATH
    if [ $? != "0" ]; then
	echo Failed to create $CACHEPATH
    fi
fi

# Need to set HOME=/tmp or svn tries to look at AFS and barfs
cd $CACHEPATH
svn co http://www.usatlas.bnl.gov/svn/panda/pilot3/
if [ $? == "0" ]; then
    cd pilot3
    tar -czf ../pilotcode.tar.gz *
else
    echo Subversion checkout gave an error
fi

# Download test builds of the pilot code...
cd $CACHEPATH
for pilot in pilotcode-dev-unvalid.tar.gz pilotcode-rc.tar.gz pilotcode-rc1.tar.gz; do
    BNLHOST=gridui07
    curl --connect-timeout 20 --max-time 120 -s -S -O http://${BNLHOST}.usatlas.bnl.gov:25880/cache/${pilot}
done
