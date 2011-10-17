from utils import session, expose, render_template, Response
from models import Scenario
from sqlalchemy import or_
import json

def generateDataTables(request,sc_id,issue_filter):
    data = {
    "sEcho": int(request.args["sEcho"]), # we should echo it with the same no, else datatable will not genrate a table
    "iTotalDisplayRecords": 10,
    }
    
    columns=['name', 'description' , 'current', 'stats_total', 'stats_percentage', 'trend', 'refreshtime']
    rowdata = []
    rowCounter = 0
    fromRow = 0
    toRow = 5
    sortByColumn = 0
    sortDir = "asc"
    
    if (request.args['iDisplayStart'] and request.args['iDisplayLength'] != '-1' ): # set the from and to
        fromRow = int(request.args['iDisplayStart'])
        toRow = int(fromRow + int(request.args['iDisplayLength']))
        
    # ordering
    if(request.args['iSortCol_0']):
        sortByColumn = int(request.args['iSortCol_0'])
        if(request.args['sSortDir_0']):
            sortDir = str(request.args['sSortDir_0'])
        
        
    if(request.args['sSearch']):
        jsonData = generateTablesWithSearch(request.args['sSearch'],data,sortByColumn,sortDir,columns)
    else: 
        for row in session.query(Scenario.scn_name.label("name"),Scenario.scn_short_description.label("desc"),Scenario.scn_type.label("type")).order_by(columns[sortByColumn])[fromRow:toRow]:
            rowdata.append([])
            rowdata[rowCounter].append(row.name)
            rowdata[rowCounter].append(row.desc)
            rowdata[rowCounter].append(row.type)
            rowCounter += 1
        jsonData = (rowdata,rowCounter)
        
    data["aaData"] = jsonData[0]
    data["iTotalRecords"] = jsonData[1]
    return json.dumps(data)

def generateTablesWithSearch(search,data,sortByColumn,sortDir,columns):
    rowdata = []
    rowCounter = 0
    fromRow = 0
    toRow = 5
    aFilter1 = "lower(iqp_scenarios.scn_name) LIKE '%"+search+"%'"
    aFilter2 = "lower(iqp_scenarios.scn_short_description) LIKE '%"+search+"%'"
    aFilter3 = "lower(iqp_scenarios.scn_type) LIKE '%"+search+"%'"
    
    for row in session.query(Scenario.scn_name.label("name"),Scenario.scn_short_description.label("desc"),Scenario.scn_type.label("type")).filter(or_(aFilter1,aFilter2,aFilter3)).order_by(columns[sortByColumn])[fromRow:toRow]:
        rowdata.append([])
        rowdata[rowCounter].append(row.name)
        rowdata[rowCounter].append(row.desc)
        rowdata[rowCounter].append(row.type)
        rowCounter += 1
        
    return (rowdata,rowCounter) # here rowCounter will be the no of rows
    
        
    
    
    