from taskbuffer.OraDBProxy import DBProxy

class NewDBProxy(DBProxy):
    '''
    Class extending OraDBProxy to add some column name mapping utilites
    '''

    def queryColumnSQL(self, sql, varMap = None, arraySize = 10, lowerCase = True):
        comment = ' /* cacheSchedConfig Connection test */'
        if self.conn == None:
            return None, None
        try:
            self.conn.begin()
            self.cur.arraysize = arraySize
            if varMap == None:
                ret = self.cur.execute(sql+comment)
            else:
                ret = self.cur.execute(sql+comment,varMap)
            res = self.cur.fetchall()
            # Iterate over the result arrays
            #print self.cur.description
            columnNames = []
            for descriptionTuple in self.cur.description:
                if lowerCase:
                    columnNames.append(descriptionTuple[0].lower())
                else:
                    columnNames.append(descriptionTuple[0])
            return columnNames, res
        except:
            # roll back
            self._rollback(self.useOtherError)
            type, value, traceBack = sys.exc_info()
            _logger.error("querySQLS : %s %s" % (sql,str(varMap)))
            _logger.error("querySQLS : %s %s" % (type,value))
            return None, None

    def mapRowsToDictionary(self, columnNames, rows):
        resDictArray = []
        for row in rows:
            tmpDict = {}
            for i in range(len(columnNames)):
                tmpDict[columnNames[i]] = row[i]
            resDictArray.append(tmpDict)
        return resDictArray

