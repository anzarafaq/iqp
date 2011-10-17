from utils import session, expose, render_template, url_for, Response
from models import Category, SubCategory, Scenario
from models import User, AppFamilyPermission, AppPermission
from authenticate_user import authenticateuser, verifyloggedin

from werkzeug.utils import redirect
from sqlalchemy.sql import text
from cgi import escape
import json
import hashlib
import uuid

@authenticateuser
@verifyloggedin
@expose('/get_all_scenarios/')
def get_all_scenarios(request):
   all_scenarios = session.query(Scenario).all()
   #data = [n for n in range(20)]
   data = [scenario.scn_id for scenario in all_scenarios]
   result = json.dumps(data)
   return Response(result, mimetype='application/json')

@authenticateuser
@verifyloggedin
@expose('/get_scenario_query/<scn_id>/')
def get_scenario_query(request, scn_id):
   this_scenario = session.query(Scenario).filter(Scenario.scn_id==scn_id).all()[0]
   #data = [n for n in range(20)]
   data = [this_scenario.scn_query]
   result = json.dumps(data)
   return Response(result, mimetype='application/json')

oracleToPostgresDataTypes = dict()
#oracleToPostgresDataTypes['number'] = 'integer'
#oracleToPostgresDataTypes['number'] = 'bigint'
oracleToPostgresDataTypes['number'] = 'double precision'
oracleToPostgresDataTypes['varchar2'] = 'varchar'
oracleToPostgresDataTypes['char'] = 'varchar'
oracleToPostgresDataTypes['long'] = 'text'
oracleToPostgresDataTypes['date'] = 'timestamp'
oracleToPostgresDataTypes['timestamp'] = 'timestamp'
oracleToPostgresDataTypes['raw'] = 'bytea'
oracleToPostgresDataTypes['clob'] = 'text'
oracleToPostgresDataTypes['blob'] = 'bytea'

@authenticateuser
@verifyloggedin
@expose('/upload_query_result_structure/<scn_id>/')
def upload_query_result_structure(request, scn_id):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   this_scenario = session.query(Scenario).filter(Scenario.scn_id==scn_id).all()[0]
   scn_name = this_scenario.scn_name
   scn_name_lower = scn_name.lower()
   if request.method == 'POST':

      def columnTypeIfExists(dataType):
         if dataType not in oracleToPostgresDataTypes:
            return "varchar"
         else:
            return oracleToPostgresDataTypes[dataType]

      ## get get argument
      query_result_structure = request.form.get('query_result_structure')

      ## decode JSON back into python list
      structure_decoded = json.loads(query_result_structure)

      ## drop old table in user namespace if it exists
      droptable_query = """DROP TABLE IF EXISTS {namespace_name}.{scn_name_lower}
""".format(namespace_name=org_namespace_name, scn_name_lower=scn_name_lower)
      droptable_s = text(droptable_query)
      session.execute(droptable_s)

      ## create new table in user namespace
      columns = structure_decoded['columns']
      column_definition_string = ','.join([column['name'] + ' ' + columnTypeIfExists(column['type']) for column in columns])
      newtable_query = """CREATE TABLE {namespace_name}.{scn_name_lower} (
""".format(namespace_name=org_namespace_name, scn_name_lower=scn_name_lower)
      newtable_query = newtable_query + column_definition_string + """)"""
      newtable_s = text(newtable_query)
      session.execute(newtable_s)

      ## commit all changes to db
      session.commit()
   return render_template('welcome.html')

@authenticateuser
@verifyloggedin
@expose('/upload_query_result_data/<scn_id>/')
def upload_query_result_data(request, scn_id):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   this_scenario = session.query(Scenario).filter(Scenario.scn_id==scn_id).all()[0]
   scn_name = this_scenario.scn_name
   scn_name_lower = scn_name.lower()
   if request.method == 'POST':
      query_result_data = request.form.get('query_result_data')

      ## decode JSON
      data_decoded = json.loads(query_result_data)

      ## get column names for table
      column_names_query = """SELECT DISTINCT column_name
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_name = '{scn_name_lower}'
AND table_schema = '{namespace_name}'
""".format(namespace_name=org_namespace_name, scn_name_lower=scn_name_lower)
      column_names_s = text(column_names_query)
      column_names_result = session.execute(column_names_s).fetchall()
      column_names = [row[0] for row in column_names_result]

      if len(column_names) > 0:
         ## insert all data into the new table
         def columnValueIfExists(columnName):
            if columnName not in field_values:
               return "null"
            elif field_values[columnName] == '\x00':
               return "null"
            else:
               return "'" + field_values[columnName].replace("'", "''") + "'"
         rows = data_decoded['rows']
         for row in rows:
            field_values = row['fieldValues']
            column_names_string = ','.join([columnName for columnName in column_names])
            column_values_string = ','.join([columnValueIfExists(columnName) for columnName in column_names])
            
            ## make insert statement
            insert_query = """INSERT INTO {namespace_name}.{scn_name_lower}""".format(namespace_name=org_namespace_name, scn_name_lower=scn_name_lower)
            insert_query = insert_query + """({column_names_string}) VALUES""".format(column_names_string=column_names_string)
            insert_query = insert_query + "(" + column_values_string + ")"
            insert_s = text(insert_query)
            session.execute(insert_s)

         ## commit all changes to db
         session.commit()
   return render_template('welcome.html')

@authenticateuser
@verifyloggedin
@expose('/upload_query_result_count/<scn_id>/')
def upload_query_result_count(request, scn_id):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   this_scenario = session.query(Scenario).filter(Scenario.scn_id==scn_id).all()[0]
   scn_name = this_scenario.scn_name
   scn_name_lower = scn_name.lower()
   if request.method == 'POST':
      query_result_count = request.form.get('query_result_count')

      ## decode JSON
      count_decoded = json.loads(query_result_count)
      
      ## insert count data into problem count table
      row_count = count_decoded['rowCount']
      new_count_query = """INSERT INTO {namespace_name}.iqp_problem_count
(Problem_Time, Scn_ID, Problem_Count)
VALUES ((select extract(epoch from now())), {scn_id}, {row_count})
""".format(namespace_name=org_namespace_name, scn_id=scn_id, row_count=row_count)
      new_count_s = text(new_count_query)
      session.execute(new_count_s)
      
      ## commit all changes to db
      session.commit()
   return render_template('welcome.html')
