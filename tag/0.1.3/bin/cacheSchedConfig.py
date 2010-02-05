#! /usr/bin/env python
#
# Dump schedconfig on a per-queue basis into cache files
#
#

# Temporary configuration
queueDataFields = {
    'pilot' : ['appdir', 'datadir', 'dq2url', 'copytool', 'copytoolin', 'copysetup', 'copysetupin', 'ddm', 'se', 'sepath', 'seprodpath', 'envsetup', 'envsetupin', 'region', 'copyprefix', 'copyprefixin', 'lfcpath', 'lfcprodpath', 'lfchost', 'sein', 'wntmpdir', 'proxy', 'retry', 'recoverdir', 'space', 'memory', 'cmtconfig', 'status', 'setokens', 'glexec', 'seopt', 'gatekeeper', 'pcache', 'maxinputsize'],
    'factory' : ['site', 'siteid', 'nickname', 'cloud', 'status', 'jdl', 'localqueue', 'nqueue', 'environ', 'glexec'],
    'all' : None,
}

# DB Connection
from cacheschedconfig.OraDBProxy2 import NewDBProxy as DBProxy
from config import panda_config
from copy import deepcopy
from datetime import datetime
from optparse import OptionParser
import calendar
import sys

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


    def init(self, dbhost, dbpasswd, dbuser, dbname):
        if self.proxyS == None:
            self.proxyS = DBProxy()
            self.proxyS.connect(dbhost, dbpasswd, dbuser, dbname)


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


    def dumpSingleQueue(self, queueDict, dest = '/tmp', outputSet = 'all', format = 'txt'):
        try:
            file = dest + "/" + queueDict['nickname'] + "." + outputSet + "." + format
            output = open(file, "w")
            outputFields = queueDataFields[outputSet]
            if outputFields == None:
                outputFields = queueDict.keys()
            outputFields.sort()
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
                structDict[timeKey] = calendar.timegm(structDict[timeKey].utctimetuple())
        return structDict



def main():
    parser = OptionParser()
    parser.add_option("-o", "--output", dest="dirname",
                      help="write cache outputs to DIR", metavar="DIR")

    (options, args) = parser.parse_args()

    cacher = cacheSchedConfig()    
    cacher.init(panda_config.dbhost, panda_config.dbpasswd, panda_config.dbuser, panda_config.dbname)
    cacher.getQueueData()
    
    for queue in cacher.queueData:
        cacher.dumpSingleQueue(queue)
        cacher.dumpSingleQueue(queue, dest = options.dirname, outputSet='pilot', format='pilot')
        cacher.dumpSingleQueue(queue, dest = options.dirname, outputSet='all', format='json')
        cacher.dumpSingleQueue(queue, dest = options.dirname, outputSet='factory', format='json')


if __name__ == "__main__":
    main()

