#! /usr/bin/env python
#
# Dump schedconfig on a per-queue basis into cache files
#
#


from cacheschedconfig.CacheSchedConfig import cacheSchedConfig
from config import panda_config
from optparse import OptionParser


def main():
    parser = OptionParser()
    parser.add_option("-o", "--output", dest="dirname",
                      help="write cache outputs to DIR", metavar="DIR")

    (options, args) = parser.parse_args()

    cacher = cacheSchedConfig()    
    cacher.init(panda_config.dbhost, panda_config.dbpasswd, panda_config.dbuser, panda_config.dbname)
    cacher.getStucturedQueueStatus()
    
    for queue in cacher.queueData:
        cacher.dumpSingleQueue(queue, dest = options.dirname, outputSet='pilot', format='pilot')
        cacher.dumpSingleQueue(queue, dest = options.dirname, outputSet='pilot', format='json')
        cacher.dumpSingleQueue(queue, dest = options.dirname, outputSet='all', format='json')
        cacher.dumpSingleQueue(queue, dest = options.dirname, outputSet='factory', format='json')
        
    # Big dumper
    cacher.dumpAllSchedConfig(dest = options.dirname)


if __name__ == "__main__":
    main()

