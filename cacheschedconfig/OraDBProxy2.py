from taskbuffer.OraDBProxy import DBProxy
import sys
import json

class NewDBProxy(DBProxy):
    '''
    Class extending OraDBProxy to add some column name mapping utilites
    '''

    def queryColumnSQL(self, sql, varMap = None, arraySize = 100, lowerCase = True):
        comment = ' /* cacheSchedConfig column query */'
        if self.conn == None:
            return None, None
        try:
            self.conn.begin()
            self.cur.arraysize = arraySize
            sys.stderr.write("querySQL : %s, %s, %s \n" % (sql, varMap, comment))
            if varMap == None:
                ret = self.cur.execute(sql+comment)
            else:
                ret = self.cur.execute(sql+comment,varMap)
            res = self.cur.fetchall()
            self.conn.commit()
            retList = []
            for panda_queue, data, in res:
                if isinstance(data, str):
                    dictData = json.loads(data)
                else:
                    dictData = json.loads(data.read())
                dictData['siteid'] = panda_queue
                retList.append(dictData)
            return retList
        except:
            raise

    def querySQL(self, sql, varMap = None, arraySize=100):
        comment = ' /* cacheSchedConfig standard query */'
        if self.conn == None:
            return None
        try:
            self.conn.begin()
            self.cur.arraysize = arraySize
            sys.stderr.write("querySQL : %s, %s, %s \n" % (sql, varMap, comment))
            if varMap == None:
                ret = self.cur.execute(sql+comment)
            else:
                ret = self.cur.execute(sql+comment,varMap)
            res = self.cur.fetchall()
            self.conn.commit()
            return res
        except:
            # roll back
            raise

    def mapRowsToDictionary(self, columnNames, rows):
        resDictArray = []
        for row in rows:
            tmpDict = {}
            for i in range(len(columnNames)):
                tmpDict[columnNames[i]] = row[i]
            resDictArray.append(tmpDict)
        return resDictArray
