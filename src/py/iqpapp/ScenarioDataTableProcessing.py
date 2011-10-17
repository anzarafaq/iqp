from utils import session, expose, render_template, Response
from urllib2 import unquote
from models import Scenario
from sqlalchemy import or_
from sqlalchemy.sql import text
import json

class ScenarioDataTableProcessing:
    
    def __init__(self,tableName,request):
        self.tableName = str(tableName).lower()
        self.request = request
        self.columnNames  = str(request.args["headers"]).split(",")
        self.limit = int(request.args['rp'])
        self.offset = int((int(request.args['page']) - 1) * self.limit)
        self.orderBy = request.args['sortname']
        self.sortDir = request.args['sortorder']
        self.searchColumnKey = unquote(request.args['query'])
        self.searchColumn = request.args['qtype']
        self.match = str(request.args['match'])
        self.data = {}
        
    def generateDataTables(self,userNameSpace):
        queries = self.generateQuery(userNameSpace)
        s = text(queries[0])
        rs = session.execute(s).fetchall()
        rowData = []
        for item in rs:
            tableData = {}
            tableData["cell"] = [str(item[eachColumn]) for eachColumn in self.columnNames]
            rowData.append(tableData)
            del tableData
        s = text(queries[1])
        rs = session.execute(s).fetchall()
        self.data["total"] = rs[0][0]
        self.data["page"] = self.request.args['page']
        self.data["rows"] = rowData 
        #append the headers
        return json.dumps(self.data)
    
    def generateQuery(self,userNameSpace):
        #import pdb
        #pdb.set_trace()
        countQueryList = ["""SELECT count(*) FROM {table}""".format(table = userNameSpace +'.'+ self.tableName)]
        queryList = ["""SELECT * FROM {table}""".format(table = userNameSpace +'.'+ self.tableName)]
        if self.searchColumnKey:
            if (self.match == 'like'):
                queryList.extend([" WHERE ",self.searchColumn," LIKE '%",str(self.searchColumnKey), "%' "])
            else:
                if(self.searchColumnKey == 'None'):
                    queryList.extend([" WHERE ",self.searchColumn," ISNULL"])
                else:
                    queryList.extend([" WHERE ",self.searchColumn," = '",str(self.searchColumnKey),"'"])
        countQueryList.extend(queryList[1:])
        queryList.append(""" ORDER BY {sortByColumn} """.format(sortByColumn = self.orderBy))
        queryList.append(""" {dir} """.format(dir = self.sortDir))
        queryList.append(""" limit {limit} offset {offset}; """.format(limit = self.limit,offset = self.offset))
        query = ""
        countQuery = ""
        query = query.join(queryList)
        countQuery = countQuery.join(countQueryList)
        return (query,countQuery)
        
