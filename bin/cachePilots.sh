#! /bin/bash
#
# Build pilot tarball from SVN. Download RC pilot code from BNL
#

# ---------------------------------------------------------------------- 
#  FUNCTIONS
# ---------------------------------------------------------------------- 

createtarball()
{
    # function to create each pilot tar ball
    # first argument is the name of the tarball
    # the rest of arguments is the list of files to include in the tarball

    TARBALL=$1
    shift
    FILES=$@

    cd pilot3
    tar -czf ../$TARBALL $FILES
    cd ..
}

createtarballs()
{
    # function to create all pilot tar balls

    # tarball for ATLAS
    FILES=`ls pilot3/ | egrep -v "trivialPilot.py"`
    createtarball pilotcode.tar.gz $FILES

    # tarball for OSG
    FILES='trivialPilot.py pUtil.py myproxyUtils.py'
    createtarball pilotcodeOSG.tar.gz $FILES
}

# ---------------------------------------------------------------------- 


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

cd $CACHEPATH
svn co http://svnweb.cern.ch/guest/panda/pilot3/

# ---------------------------------------------------------------------- 
#  tarballs creation
# ---------------------------------------------------------------------- 

if [ $? == "0" ]; then
    createtarballs
else
    echo Subversion checkout gave an error
fi

# ---------------------------------------------------------------------- 

# Download test builds of the pilot code...
cd $CACHEPATH
for pilot in pilotcode-rc.tar.gz; do
    curl --connect-timeout 20 --max-time 120 -s -S -O http://project-atlas-gmsb.web.cern.ch/project-atlas-gmsb/${pilot}
done
