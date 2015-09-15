#
# Dump schedconfig on a per-queue basis into cache files
#

# DB Connection
from cacheschedconfig.OraDBProxy2 import NewDBProxy as DBProxy
from copy import deepcopy
from datetime import datetime
from optparse import OptionParser
import calendar
import sys
import os

try:
    import json as json
except ImportError, err:
    print >>sys.stderr, 'No json module found: %s. Fallback to simplejson.' % err
    try:
        import simplejson as json
    except ImportError, err:
        print >>sys.stderr, 'No simplejson module found: %s' % err
        sys.exit(1)


class cacheSchedConfig:
    '''
    Class to dump schedconfig on a per-queue basis into cache files
    '''
    def __init__(self):
        self.proxyS = None
        self.queueData = None
        self.cloudStatus = None
        # Define this here, but could be more flexible...
        self.queueDataFields = {
                                # Note that json dumps always use sort_keys=True; for pilot format
                                # the order defined here is respected
                                'pilot' : ['appdir', 'allowdirectaccess', 'cloud', 'datadir', 'dq2url', 'copytool', 'copytoolin', 
                                           'copysetup', 'copysetupin', 'ddm', 'se', 'sepath', 'seprodpath', 'envsetup', 'envsetupin', 
                                           'region', 'copyprefix', 'copyprefixin', 'lfcpath', 'lfcprodpath', 'lfchost', 'lfcregister', 
                                           'sein', 'wntmpdir', 'proxy', 'retry', 'recoverdir', 'space', 'memory', 'cmtconfig', 'status', 
                                           'setokens', 'glexec', 'seopt', 'gatekeeper', 'pcache', 'maxinputsize', 'timefloor', 
                                           'corecount', 'faxredirector', 'allowfax', 'maxtime', 'maxwdir',],
                                'factory' : ['site', 'siteid', 'nickname', 'cloud', 'status', 'jdl', 'queue', 'localqueue', 'nqueue', 
                                             'environ', 'proxy', 'glexec', 'depthboost', 'idlepilotsupression', 'pilotlimit', 'transferringlimit', 
                                             'memory', 'maxtime', 'system', 'fairsharepolicy','autosetup_pre','autosetup_post'],
                                # None is magic here and really means "all"
                                'all' : None,
                                }


    def init(self, dbhost, dbpasswd, dbuser, dbname):
        if self.proxyS == None:
            self.proxyS = DBProxy()
            self.proxyS.connect(dbhost, dbpasswd, dbuser, dbname)

            
    def getStucturedQueueStatus(self):
        self.getQueueData()
        self.getCloudStatus()
        self.maskQueuesByCloud()
        

    def getQueueData(self, site = None, queue = None):
        # Dump schedconfig in a single query (it's not very big)
        varDict = {}
        sql = 'SELECT * from ATLAS_PANDAMETA.SCHEDCONFIG'
        if site:
            sql += ' where site=:site'
            varDict[':site'] = site
            c, r = self.proxyS.queryColumnSQL(sql, varDict)
        elif queue:
            sql += ' where nickname=:queue'
            varDict[':queue'] = queue
            c, r = self.proxyS.queryColumnSQL(sql, varDict)
        else:
            c, r = self.proxyS.queryColumnSQL(sql)
        self.queueData = self.proxyS.mapRowsToDictionary(c, r)
        
        
    def getCloudStatus(self):
        sql = 'SELECT name, status from ATLAS_PANDAMETA.CLOUDCONFIG'
        r = self.proxyS.querySQL(sql)
        self.cloudStatus = dict()
        for row in r:
            self.cloudStatus[row[0]] = row[1]

            
    def maskQueuesByCloud(self):
        '''Force queue status to offline if the cloud is offline'''
        for queue in self.queueData:
            try:
                if self.cloudStatus[queue['cloud']] == 'offline':
                    queue['status'] = 'offline'
                    print >>sys.stderr, 'Queue %s forced offline (cloud = %s is offline)' % (queue['nickname'], queue['cloud'])
            except KeyError:
                print >>sys.stderr, 'No valid cloud status for queue %s (cloud = %s)' % (queue['nickname'], queue['cloud'])


    def dumpSingleQueue(self, queueDict, dest = '/tmp', outputSet = 'all', format = 'txt'):
        try:
            file = os.path.join(dest, queueDict['nickname'] + "." + outputSet + "." + format)
            output = open(file, "w")
            outputFields = self.queueDataFields[outputSet]
            if outputFields == None:
                outputFields = queueDict.keys()
            if format == 'txt':
                for outputField in outputFields:
                    print >>output, outputField + "=" + str(queueDict[outputField])
            if format == 'pilot':
                outputStr = ''
                for outputField in outputFields:
                    if queueDict[outputField]:
                        outputStr += outputField + "=" + str(queueDict[outputField]) + "|"
                    else:
                        outputStr += outputField + "=|"
                print >>output, outputStr[:-1]
            if format == 'json':
                dumpMe = {}
                for outputField in outputFields:
                    dumpMe[outputField] = queueDict[outputField]
                print >>output, json.dumps(self.queueDictPythonise(dumpMe), sort_keys=True, indent=4)
        except:
            raise
        output.close()


    def dumpQueues(self, queueArray, dest = '/tmp', outputSet = 'all', format = 'txt'):
        for queueDict in queueArray:
            self.dumpSingleQueue(queueArray, dest, outputSet, format)


    def queueDictPythonise(self, queueDict, deepCopy = True):
        '''Turn queue dictionary with SQL text fields into a more stuctured python representation'''
        if deepCopy:
            structDict = deepcopy(queueDict)
        else:
            structDict = queueDict

        if 'releases' in structDict and structDict['releases'] != None:
            structDict['releases'] = structDict['releases'].split('|')
        # TODO - Change this into Ricardo's ISO dateTime in UTC?
        for timeKey in 'lastmod', 'tspace':
            if timeKey in structDict:
                structDict[timeKey] = structDict[timeKey].isoformat()
        return structDict


    def dumpAllSchedConfig(self, queueArray = None, dest='/tmp'):
        '''Dumps all of schedconfig into a single json file - allows clients to retrieve a
        machine readable version of schedconfig efficiently'''
        file = os.path.join(dest, "schedconfig.all.json")
        if queueArray == None:
            queueArray = self.queueData
        output = open(file, "w")
        dumpMe = {}
        for queueDict in queueArray:
            dumpMe[queueDict['nickname']] = {}
            for k,v in queueDict.iteritems():
                dumpMe[queueDict['nickname']][k] = v
            dumpMe[queueDict['nickname']] = self.queueDictPythonise(dumpMe[queueDict['nickname']])
        print >>output, json.dumps(dumpMe, sort_keys=True, indent=4)
