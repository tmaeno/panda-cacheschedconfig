#! /bin/bash
#
# Build pilot tarball from cvmfs. Download RC pilot code from Paul's gmsb www area
#

# ----------------------------------------------------------------------
#  FUNCTIONS
# ----------------------------------------------------------------------

createtarball_cvmfs()
{
    # function to create each pilot tar ball
    # first argument is the name of the tarball
    # the rest of arguments is the list of files to include in the tarball

    TARBALL=$1
    TARBALL_TMP=$1_tmp
    shift
    FILES=$@

    cd $CACHEPATH/latest_cache
    tar -czf ../$TARBALL_TMP $FILES
    mv ../$TARBALL_TMP ../$TARBALL
    cd $CACHEPATH
}

createtarballs_cvmfs()
{
    # function to create all pilot tar balls

    # tarball for ATLAS
    FILES=`ls $CACHEPATH/latest_cache`
    createtarball_cvmfs pilotcode-PICARD.tar.gz $FILES
}

getfiles_cvmfs()
{
    # function to get the files from git

    # delete cache directory
    if [ -d $CACHEPATH/latest_cache ]; then
        rm -rf $CACHEPATH/latest_cache
    fi

    # get latest zip from github and unzip it
    cp -r /cvmfs/atlas.cern.ch/repo/sw/PandaPilot/pilot/latest $CACHEPATH/latest_cache
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


if [ $? == "0" ]; then
    getfiles_cvmfs
else
    echo Could not copy the pilot code from cvmfsd
fi

if [ $? == "0" ]; then
    createtarballs_cvmfs
else
    echo Could not create the tarballs
fi

# ----------------------------------------------------------------------

# Download test builds of the pilot code...
cd $CACHEPATH
for pilot in pilotcode-rc.tar.gz; do
    curl --connect-timeout 20 --max-time 120 -s -S -O http://project-atlas-gmsb.web.cern.ch/project-atlas-gmsb/${pilot}
done