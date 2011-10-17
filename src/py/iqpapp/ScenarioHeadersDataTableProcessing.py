import json
from utils import session   
from sqlalchemy.sql import text
class ScenarioHeadersDataTableProcessing:
    
    def __init__(self,tableName):
        self.tableName = tableName
        
    def generateHeaders(self,user_namespace_name):
        query = """SELECT DISTINCT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table}'""".format(table = self.tableName.lower())         
        resultset = session.execute(query).fetchall()
        headers = []
        for header in resultset:
            headers.append(str(header['column_name']))
        return json.dumps(headers)