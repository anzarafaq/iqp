from utils import session, expose, render_template, Response, url_for
from models import Category, SubCategory, Scenario
from models import User, AppFamilyPermission, AppPermission
from authenticate_user import authenticateuser
from authenticate_user import verifyloggedin
from authenticate_user import authorizeuseroncategory
from authenticate_user import authorizeuseronsubcategory
from authenticate_user import login, logout
from authenticate_user import register
from authenticate_user import setpermissions
from authenticate_user import setpermissions2
from authenticate_user import setpermissions3
from uploader import get_all_scenarios, get_scenario_query
from uploader import  upload_query_result_structure
from uploader import upload_query_result_data
from uploader import upload_query_result_count

from sqlalchemy import func,over
from sqlalchemy.sql import text
from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound
from werkzeug.utils import cached_property
from werkzeug.contrib.securecookie import SecureCookie
from werkzeug.datastructures import Headers
from cgi import escape
import json
import hashlib
import uuid

from ScenarioDataTableProcessing import *
from SubCategoryDataTableProcessing import *
from ScenarioHeadersDataTableProcessing import *

@authenticateuser
@expose('/welcome/')
def welcome(request):
   return render_template('welcome.html')

@authenticateuser
@verifyloggedin
@expose('/')
def overview(request):
   user = request.client_user_object
   user_id = user.user_id
   args = json.dumps(request.args)
   categories = (session.query(Category)
                .join(AppFamilyPermission,
                    Category.category_id
                    == AppFamilyPermission.category_id)
                .filter(AppFamilyPermission.user_id == user_id)
                .order_by(Category.category_display_order.asc()))
   sub_categories = (session.query(SubCategory)
                    .join(AppPermission,
                        SubCategory.subcategory_id
                        == AppPermission.subcategory_id)
                    .filter(AppPermission.user_id == user_id))
   return render_template(
           'overview.html',
           categories=categories,
           sub_categories=sub_categories,
           user=user,
           args=args)

@authenticateuser
@verifyloggedin
@authorizeuseroncategory
@expose('/<c_name>/')
def category(request, c_name):
   if c_name == 'favicon.ico':
      return Response()
   user = request.client_user_object
   user_id = user.user_id
   args = json.dumps(request.args)
   categories = (session.query(Category)
                .join(AppFamilyPermission,
                    Category.category_id
                    == AppFamilyPermission.category_id)
                .filter(AppFamilyPermission.user_id == user_id)
                .order_by(Category.category_display_order.asc()))
   sub_categories = (session.query(SubCategory)
                    .join(AppPermission,
                        SubCategory.subcategory_id
                        == AppPermission.subcategory_id)
                    .filter(AppPermission.user_id == user_id))
   breadcrumbs = (session.query(Category)
                    .filter(Category.category_name==c_name).all()[0])
   return render_template(
           'category.html',
           categories=categories,
           sub_categories=sub_categories,
           breadcrumbs=breadcrumbs,
           category_name=c_name,
           user=user,
           args=args)

@authenticateuser
@verifyloggedin
@authorizeuseroncategory
@authorizeuseronsubcategory
@expose('/<c_name>/<sc_name>/')
def sub_category(request, c_name, sc_name):
   user = request.client_user_object
   user_id = user.user_id
   args = json.dumps(request.args)
   categories = (session.query(Category)
                .join(AppFamilyPermission,
                    Category.category_id
                    == AppFamilyPermission.category_id)
                .filter(AppFamilyPermission.user_id == user_id)
                .order_by(Category.category_display_order.asc()))
   sub_categories = (session.query(SubCategory)
                    .join(AppPermission,
                        SubCategory.subcategory_id
                        == AppPermission.subcategory_id)
                    .filter(AppPermission.user_id == user_id))
   breadcrumbs = (session.query(Category, SubCategory)
                    .join(SubCategory, Category.category_id
                        == SubCategory.category_id)
                    .filter(Category.category_name==c_name)
                    .filter(SubCategory.subcategory_name==sc_name)
                    .all()[0])
   return render_template(
           'sub_category.html',
           categories=categories,
           sub_categories=sub_categories,
           breadcrumbs=breadcrumbs,
           subcategory_name=sc_name,
           user=user,
           args=args)

@authenticateuser
@verifyloggedin
@authorizeuseroncategory
@authorizeuseronsubcategory
@expose('/<c_name>/<sc_name>/<s_name>/')
def scenario(request, c_name, sc_name, s_name):  
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   args = json.dumps(request.args)
   categories = (session.query(Category)
                .join(AppFamilyPermission,
                    Category.category_id
                    == AppFamilyPermission.category_id)
                .filter(AppFamilyPermission.user_id == user_id)
                .order_by(Category.category_display_order.asc()))
   sub_categories = (session.query(SubCategory)
                    .join(AppPermission,
                        SubCategory.subcategory_id
                            == AppPermission.subcategory_id)
                    .filter(AppPermission.user_id == user_id))
   breadcrumbs = (session.query(Category, SubCategory, Scenario)
                    .join(SubCategory, Category.category_id
                        == SubCategory.category_id)
                    .join(Scenario, SubCategory.subcategory_id
                        == Scenario.subcategory_id)
                    .filter(Category.category_name==c_name)
                    .filter(SubCategory.subcategory_name==sc_name)
                    .filter(Scenario.scn_name==s_name).all()[0])
   scenario = (session.query(Scenario)
                .filter(Scenario.scn_name==s_name)
                .all()[0])
   scn_short_des = scenario.scn_short_description
   scenario_id = scenario.scn_id
   s_name_lower = s_name.lower()
   groupby = request.args.get('groupby')
   if groupby:
       clicks_count_query = ("""select insert_clicks({s_id},'{name}');"""
                            .format(s_id = scenario_id,name = groupby))
       count_query = text(clicks_count_query)
       insert = session.execute(count_query).fetchall()
       session.commit()
       
   query1 = ("""select frequent_column_name from scenario_clicks_count
                where scn_id = {s_id} order by frequency_number
                desc limit 5;""".format(s_id = scenario_id))
   s1 = text(query1)
   scenario_data_column_names_ordered1 = session.execute(s1).fetchall()
   query2 = (""" select column_name from INFORMATION_SCHEMA.COLUMNS
            where column_name not in (
                    select frequent_column_name from scenario_clicks_count
                        where scn_id = {s_id} order by frequency_number desc limit 5)
                    and table_name = '{scen_name_lower}'
                    and table_schema = '{namespace_name}' order by column_name;"""
            .format(namespace_name=org_namespace_name,
                    scen_name_lower=s_name_lower.lower(),s_id = scenario_id))
   s2 = text(query2)
   scenario_data_column_names_ordered2 = session.execute(s2).fetchall()
   return render_template(
           'scenario.html',
           categories=categories,
           sub_categories=sub_categories,
           breadcrumbs=breadcrumbs,
           scn_des=scn_short_des,
           scenario_name=s_name,
           scenario_data_column_names1=scenario_data_column_names_ordered1,
           scenario_data_column_names2=scenario_data_column_names_ordered2,
           user=user,
           args=args)

@authenticateuser
@verifyloggedin
@expose('/overview_main_chart_data_source/')
def overview_main_chart_data_source(request):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   issue_filter = request.args.get('filter')
   if not issue_filter:
      issue_filter = ''
   query = """SELECT iqp_categories.category_name, COUNT(iqp_scenarios.scn_name) as issue_count, SUM(problem_count) as problemsum
FROM iqp_categories
JOIN iqp_subcategories ON (iqp_categories.category_id = iqp_subcategories.category_id)
JOIN iqp_scenarios ON (iqp_subcategories.subcategory_id = iqp_scenarios.subcategory_id)
JOIN {namespace_name}.iqp_problem_count_recent ON (iqp_scenarios.scn_id = iqp_problem_count_recent.scn_id)
JOIN app_family_permissions ON (iqp_categories.category_id = app_family_permissions.category_id)
JOIN app_permissions ON (iqp_subcategories.subcategory_id = app_permissions.subcategory_id)
WHERE iqp_problem_count_recent.problem_count > 0
AND (iqp_scenarios.scn_type NOT IN ('Stats', 'N','Feature') OR '{filter_type}' IN ('Stats', 'N','Feature'))
AND (iqp_scenarios.scn_type = '{filter_type}' OR '{filter_type}' = '')
AND app_family_permissions.user_id = '{user_id}'
AND app_permissions.user_id = '{user_id}'
GROUP BY iqp_categories.category_name
""".format(namespace_name=org_namespace_name, filter_type=issue_filter, user_id=user_id)
   s = text(query)
   rs = session.execute(s).fetchall()
   data = [[str(item['category_name']), int(item['issue_count']), int(item['problemsum'])] for item in rs]
   result = json.dumps(data)
   return Response(result, mimetype='application/json')

@authenticateuser
@verifyloggedin
@expose('/overview_proportion_chart_data_source/')
def overview_proportion_chart_data_source(request):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   issue_filter = request.args.get('filter')
   if not issue_filter:
      issue_filter = ''
   query = """SELECT
(CASE WHEN iqp_problem_count_recent.problem_count > 0 THEN 'Issue'
ELSE 'No_Issue'
END) as issue_or_not, COUNT(iqp_scenarios.scn_id) as issue_or_not_count
FROM iqp_categories
JOIN iqp_subcategories ON (iqp_categories.category_id = iqp_subcategories.category_id)
JOIN iqp_scenarios ON (iqp_subcategories.subcategory_id = iqp_scenarios.subcategory_id)
JOIN {namespace_name}.iqp_problem_count_recent ON (iqp_scenarios.scn_id = iqp_problem_count_recent.scn_id)
JOIN app_family_permissions ON (iqp_categories.category_id = app_family_permissions.category_id)
JOIN app_permissions ON (iqp_subcategories.subcategory_id = app_permissions.subcategory_id)
WHERE (iqp_scenarios.scn_type NOT IN ('Stats', 'N','Feature') OR '{filter_type}' IN ('Stats', 'N','Feature'))
AND (iqp_scenarios.scn_type = '{filter_type}' OR '{filter_type}' = '')
AND app_family_permissions.user_id = '{user_id}'
AND app_permissions.user_id = '{user_id}'
GROUP BY issue_or_not
""".format(namespace_name=org_namespace_name, filter_type=issue_filter, user_id=user_id)
   s = text(query)
   rs = session.execute(s).fetchall()
   data = [[str(item['issue_or_not']), int(item['issue_or_not_count'])] for item in rs]
   result = json.dumps(data)
   return Response(result, mimetype='application/json')

@authenticateuser
@verifyloggedin
@expose('/category_main_chart_data_source/<c_name>/')
def category_main_chart_data_source(request, c_name):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   this_category = session.query(Category).filter(Category.category_name==c_name).all()[0]
   c_id = this_category.category_id
   issue_filter = request.args.get('filter')
   if not issue_filter:
      issue_filter = ''
   query = """SELECT iqp_subcategories.subcategory_name, COUNT(iqp_scenarios.scn_name) issue_count, SUM(problem_count) as problemsum
FROM iqp_subcategories
JOIN iqp_scenarios ON (iqp_subcategories.subcategory_id = iqp_scenarios.subcategory_id)
JOIN {namespace_name}.iqp_problem_count_recent ON (iqp_scenarios.scn_id = iqp_problem_count_recent.scn_id)
JOIN app_permissions ON (iqp_subcategories.subcategory_id = app_permissions.subcategory_id)
WHERE iqp_problem_count_recent.problem_count > 0
AND (iqp_scenarios.scn_type NOT IN ('Stats', 'N','Feature') OR '{filter_type}' IN ('Stats', 'N','Feature'))
AND (iqp_scenarios.scn_type = '{filter_type}' OR '{filter_type}' = '')
AND iqp_subcategories.category_id = '{c_id}'
AND app_permissions.user_id = '{user_id}'
GROUP BY iqp_subcategories.subcategory_name
""".format(namespace_name=org_namespace_name, c_id=c_id, filter_type=issue_filter, user_id=user_id)
   s = text(query)
   rs = session.execute(s).fetchall()
   data = [[str(item['subcategory_name']), int(item['issue_count']), int(item['problemsum'])] for item in rs]
   result = json.dumps(data)
   return Response(result, mimetype='application/json')

@authenticateuser
@verifyloggedin
@expose('/category_proportion_chart_data_source/<c_name>/')
def category_proportion_chart_data_source(request, c_name):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   this_category = session.query(Category).filter(Category.category_name==c_name).all()[0]
   c_id = this_category.category_id
   issue_filter = request.args.get('filter')
   if not issue_filter:
      issue_filter = ''
   query = """SELECT
(CASE WHEN iqp_problem_count_recent.problem_count > 0 THEN 'Issue'
ELSE 'No_Issue'
END) as issue_or_not, COUNT(iqp_scenarios.scn_id) as issue_or_not_count
FROM iqp_subcategories
JOIN iqp_scenarios ON (iqp_subcategories.subcategory_id = iqp_scenarios.subcategory_id)
JOIN {namespace_name}.iqp_problem_count_recent ON (iqp_scenarios.scn_id = iqp_problem_count_recent.scn_id)
JOIN app_permissions ON (iqp_subcategories.subcategory_id = app_permissions.subcategory_id)
WHERE (iqp_scenarios.scn_type NOT IN ('Stats', 'N','Feature') OR '{filter_type}' IN ('Stats', 'N','Feature'))
AND (iqp_scenarios.scn_type = '{filter_type}' OR '{filter_type}' = '')
AND iqp_subcategories.category_id = '{c_id}'
AND app_permissions.user_id = '{user_id}'
GROUP BY issue_or_not
""".format(namespace_name=org_namespace_name, c_id=c_id, filter_type=issue_filter, user_id=user_id)
   s = text(query)
   rs = session.execute(s).fetchall()
   data = [[str(item['issue_or_not']), int(item['issue_or_not_count'])] for item in rs]
   result = json.dumps(data)
   return Response(result, mimetype='application/json')

@authenticateuser
@verifyloggedin
@expose('/sub_category_table_data_source/<sc_name>/')
def sub_category_table_data_source(request,sc_name):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   this_sub_category = session.query(SubCategory).filter(SubCategory.subcategory_name==sc_name).all()[0]
   sc_id = this_sub_category.subcategory_id
   issue_filter = request.args.get('filter')
   sortkey = request.args['sortname']
   sortDir = request.args['sortorder']
   limit = int(request.args['rp'])
   offset = int((int(request.args['page']) - 1) * limit)
   data = None
   if not issue_filter:
      issue_filter = ''
   if issue_filter == ('Stats' or 'Features'):
       query = """SELECT iqp_scenarios.scn_name as name, iqp_scenarios.scn_short_description as description, iqp_problem_count_recent.problem_count as current, iqp_problem_count_recent.problem_time as refreshtime, COALESCE(problem_count_stats.problem_count,999999999) as stats_total, (100*iqp_problem_count_recent.problem_count / COALESCE(problem_count_stats.problem_count,999999999)) as stats_percentage
FROM iqp_scenarios
LEFT JOIN {namespace_name}.iqp_problem_count_recent ON (iqp_scenarios.scn_id = iqp_problem_count_recent.scn_id)
LEFT JOIN {namespace_name}.iqp_problem_count_prev ON (iqp_scenarios.scn_id = iqp_problem_count_prev.scn_id)
LEFT JOIN {namespace_name}.iqp_problem_count_recent problem_count_stats ON (iqp_scenarios.scn_totals_scn_id = problem_count_stats.scn_id)
WHERE iqp_scenarios.subcategory_id = '{sc_id}'
AND iqp_problem_count_recent.problem_count > 0
AND (iqp_scenarios.scn_type NOT IN ('Stats', 'N','Feature') OR '{filter_type}' IN ('Stats', 'N','Feature'))
AND (iqp_scenarios.scn_type = '{filter_type}' OR '{filter_type}' = '')
ORDER BY {sortby} {dir} limit {limit} offset {offset}
""".format(namespace_name=org_namespace_name,sc_id=sc_id, filter_type=issue_filter, sortby = sortkey, dir = sortDir,limit = limit,offset = offset )
       s = text(query)
       rs = session.execute(s).fetchall()
       data = [[str(item['name']), str(item['description']), int(item['current']), int(item['refreshtime'])] for item in rs]
   else:
       query = """SELECT iqp_scenarios.scn_name as name, iqp_scenarios.scn_short_description as description, iqp_problem_count_recent.problem_count as current, COALESCE(iqp_problem_count_prev.problem_count, 0) as prev, (iqp_problem_count_recent.problem_count - COALESCE(iqp_problem_count_prev.problem_count, 0)) as trend, iqp_problem_count_recent.problem_time as refreshtime, COALESCE(problem_count_stats.problem_count,999999999) as stats_total, (100*iqp_problem_count_recent.problem_count / COALESCE(problem_count_stats.problem_count,999999999)) as stats_percentage
FROM iqp_scenarios
LEFT JOIN {namespace_name}.iqp_problem_count_recent ON (iqp_scenarios.scn_id = iqp_problem_count_recent.scn_id)
LEFT JOIN {namespace_name}.iqp_problem_count_prev ON (iqp_scenarios.scn_id = iqp_problem_count_prev.scn_id)
LEFT JOIN {namespace_name}.iqp_problem_count_recent problem_count_stats ON (iqp_scenarios.scn_totals_scn_id = problem_count_stats.scn_id)
WHERE iqp_scenarios.subcategory_id = '{sc_id}'
AND iqp_problem_count_recent.problem_count > 0
AND (iqp_scenarios.scn_type NOT IN ('Stats', 'N','Feature') OR '{filter_type}' IN ('Stats', 'N','Feature'))
AND (iqp_scenarios.scn_type = '{filter_type}' OR '{filter_type}' = '')
ORDER BY {sortby} {dir} limit {limit} offset {offset}
""".format(namespace_name=org_namespace_name,sc_id=sc_id, filter_type=issue_filter, sortby = sortkey, dir = sortDir,limit = limit,offset = offset )
       s = text(query)
       rs = session.execute(s).fetchall()
       data = [[str(item['name']), str(item['description']), int(item['current']), int(item['stats_total']), float(item['stats_percentage']), int(item['trend']), int(item['refreshtime'])] for item in rs]
   countQuery = """SELECT count(*)
FROM iqp_scenarios
LEFT JOIN {namespace_name}.iqp_problem_count_recent ON (iqp_scenarios.scn_id = iqp_problem_count_recent.scn_id)
LEFT JOIN {namespace_name}.iqp_problem_count_prev ON (iqp_scenarios.scn_id = iqp_problem_count_prev.scn_id)
LEFT JOIN {namespace_name}.iqp_problem_count_recent problem_count_stats ON (iqp_scenarios.scn_totals_scn_id = problem_count_stats.scn_id)
WHERE iqp_scenarios.subcategory_id = '{sc_id}'
AND iqp_problem_count_recent.problem_count > 0
AND (iqp_scenarios.scn_type NOT IN ('Stats', 'N','Feature') OR '{filter_type}' IN ('Stats', 'N','Feature'))
AND (iqp_scenarios.scn_type = '{filter_type}' OR '{filter_type}' = '')
""".format(namespace_name=org_namespace_name,sc_id=sc_id, filter_type=issue_filter)
   cs = text(countQuery)
   rs2 = session.execute(cs).fetchall()
   jsond = { "total" : rs2[0][0], "page" : request.args['page'], "rows" : []}
   for row in data:
       eachRow = {}
       eachRow["cell"] = row
       jsond["rows"].append(eachRow)
       del eachRow
   result = json.dumps(jsond)
   return Response(result, mimetype='application/json')

@authenticateuser
@verifyloggedin
@expose('/sub_category_proportion_chart_data_source/<sc_name>/')
def sub_category_proportion_chart_data_source(request, sc_name):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   this_sub_category = session.query(SubCategory).filter(SubCategory.subcategory_name==sc_name).all()[0]
   sc_id = this_sub_category.subcategory_id
   issue_filter = request.args.get('filter')
   if not issue_filter:
      issue_filter = ''
   query = """SELECT
(CASE WHEN iqp_problem_count_recent.problem_count > 0 THEN 'Issue'
ELSE 'No_Issue'
END) as issue_or_not, COUNT(iqp_scenarios.scn_id) as issue_or_not_count
FROM iqp_scenarios
JOIN {namespace_name}.iqp_problem_count_recent ON (iqp_scenarios.scn_id = iqp_problem_count_recent.scn_id)
WHERE (iqp_scenarios.scn_type NOT IN ('Stats', 'N','Feature') OR '{filter_type}' IN ('Stats', 'N','Feature'))
AND (iqp_scenarios.scn_type = '{filter_type}' OR '{filter_type}' = '')
AND iqp_scenarios.subcategory_id = '{sc_id}'
GROUP BY issue_or_not
""".format(namespace_name=org_namespace_name, sc_id=sc_id, filter_type=issue_filter)
   s = text(query)
   rs = session.execute(s).fetchall()
   data = [[str(item['issue_or_not']), int(item['issue_or_not_count'])] for item in rs]
   result = json.dumps(data)
   return Response(result, mimetype='application/json')

@authenticateuser
@verifyloggedin
@expose('/scenario_main_chart_data_source/<s_name>/')
def scenario_main_chart_data_source(request, s_name):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   groupby = request.args.get('groupby')
   data = {}
   if groupby:
      query = """SELECT {group_by}, COUNT(*) as groupsum FROM {namespace_name}.{scen_name}
GROUP BY {group_by}
""".format(namespace_name=org_namespace_name, scen_name=s_name, group_by=groupby) 
      s = text(query)
      rs = session.execute(s).fetchall()
      data['groupby'] = groupby
      data['data'] = [[str(item[groupby]), int(item['groupsum'])] for item in rs]
   else:
      scenario = session.query(Scenario).filter(Scenario.scn_name==s_name).all()[0]
      scenario_id = scenario.scn_id
      s_name_lower = s_name.lower()
      query1 = """select frequent_column_name from scenario_clicks_count where scn_id = {s_id} order by frequency_number desc limit 1;""".format(s_id = scenario_id)
      s1 = text(query1)
      mostly_used = session.execute(s1).fetchall()
      if mostly_used:
          query = """SELECT {mostly_used}, COUNT(*) as groupsum FROM {namespace_name}.{scen_name} GROUP BY {mostly_used}""".format(namespace_name=org_namespace_name, scen_name=s_name, mostly_used=mostly_used[0][0])
      else:
          query = """SELECT COUNT(*) as groupsum FROM {namespace_name}.{scen_name}""".format(namespace_name=org_namespace_name, scen_name=s_name) 
      s = text(query)
      rs = session.execute(s).fetchall()
      if mostly_used:
          data['groupby'] = mostly_used[0][0]
          data['data'] = [[str(item[mostly_used[0][0]]), int(item['groupsum'])] for item in rs]
      else:
          data['groupby'] = 'All Rows'
          data['data'] = [[str('All Rows'), int(item['groupsum'])] for item in rs]
   result = json.dumps(data)
   return Response(result, mimetype='application/json')

#this is not used any more
@authenticateuser
@verifyloggedin
@expose('/scenario_main_chart_options_data_source/<s_name>/')
def scenario_main_chart_options_data_source(request, s_name):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   s_name_lower = s_name.lower()
   for scenario in session.query(Scenario).filter(Scenario.scn_name==s_name).all():
      this_scenario = scenario
   s_id = this_scenario.scn_id
   data = {}
   query = """select frequent_column_name from scenario_clicks_count where scn_id = {sid} order by frequency_number desc limit 5;""".format(sid = s_id)
   s = text(query)
   rs = session.execute(s).fetchall()
   data["most-five"] = [[str(item['frequent_column_name'])] for item in rs]
   query2 = """select column_name from INFORMATION_SCHEMA.COLUMNS where column_name not in (select frequent_column_name from scenario_clicks_count order by  frequency_number desc limit 5) and table_name = '{scen_name_lower}' and table_schema = '{namespace_name}'  order by column_name;""".format(namespace_name=org_namespace_name, scen_name_lower=s_name_lower.lower())
   s2 = text(query2)
   rs2 = session.execute(s2).fetchall()
   data["others"] = [[str(item['column_name'])] for item in rs2]
   result = json.dumps(data)
   return Response(result, mimetype='application/json')

@authenticateuser
@verifyloggedin
@expose('/scenario_table_data_source/<s_name>/')#for table data
def scenario_table_data_source(request, s_name):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   s_name = str(s_name)
   s_name = escape(s_name)
   processTable = ScenarioDataTableProcessing(s_name,request)
   return Response(processTable.generateDataTables(org_namespace_name), mimetype='application/json')

#not used
@authenticateuser
@verifyloggedin
@expose('/scenario_header_table_data_source/<s_name>/')#for table column names
def scenario_header_table_data_source(request, s_name):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   s_name = str(s_name)
   s_name = escape(s_name)
   headers = ScenarioHeadersDataTableProcessing(s_name)
   return Response(headers.generateHeaders(org_namespace_name),mimetype='application/json')

@authenticateuser
@verifyloggedin
@expose('/scenario_trend_chart_data_source/<s_name>/')
def scenario_trend_chart_data_source(request, s_name):
   user = request.client_user_object
   user_id = user.user_id
   org = request.client_organization_object
   org_namespace_name = org.organization_namespace_name
   s_name = str(s_name)
   s_name = escape(s_name)
   for scenario in session.query(Scenario).filter(Scenario.scn_name==s_name).all():
      this_scenario = scenario
   s_id = this_scenario.scn_id
   query = """SELECT iqp_problem_count.problem_time, iqp_problem_count.problem_count
FROM {namespace_name}.iqp_problem_count
WHERE iqp_problem_count.scn_id = '{s_id}' ORDER BY iqp_problem_count.problem_time DESC LIMIT 100 OFFSET 0
""".format(namespace_name=org_namespace_name, s_id=s_id)
   s = text(query)
   rs = session.execute(s).fetchall()
   data = []
   for item in rs:
      data.append([int(item['problem_time']*1000), int(item['problem_count'])])
   result = json.dumps(data)
   return Response(result, mimetype='application/json')

@authenticateuser
@verifyloggedin
@expose('/export/browser_data/')
def export(request):
    import csv
    #Response.headers['Content-Type'] = "application/CSV"
    #Response.headers['Content-Disposition'] = 'attachment; filename= sample.csv'
    d = Headers()
    #write the headers
    #d.add("Pragma", "public")
    #d.add("Expires","0")
    #d.add("Cache-Control", must-revalidate, post-check=0, pre-check=0")
    #d.add('Content-Type', "application/force-download")
    #d.add("Content-Type","application/octet-stream")
    d.add("Content-Type","application/octet-stream")
    d.add('Content-Disposition', 'attachment;filename=iqpgenerated.csv')
    headers = ["Application","No of Scenarios","No of Issues"]
    ofile  = open('/home/ubuntu/iqp/sample.csv', "wb")
    
    #write column names first
    writer = csv.writer(ofile, delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(headers)
    tableData = json.loads(request.args['tableData'])
    #write table data
    for eachRow in tableData:
        writer.writerow(eachRow)
    return Response(open('/home/ubuntu/iqp/sample.csv', 'r'),headers = d)

@authenticateuser
@verifyloggedin
@expose('/export/subcategory/<sc_name>')
def exportSubcategoryTable(request,sc_name):
    import csv
    #Response.headers['Content-Type'] = "application/CSV"
    #Response.headers['Content-Disposition'] = 'attachment; filename= sample.csv'
    d = Headers()
    #write the headers
    #d.add("Pragma", "public")
    #d.add("Expires","0")
    #d.add("Cache-Control", must-revalidate, post-check=0, pre-check=0")
    #d.add('Content-Type', "application/force-download")
    #d.add("Content-Type","application/octet-stream")
    d.add("Content-Type","application/octet-stream")
    d.add('Content-Disposition', 'attachment;filename=iqpgenerated.csv')
    headers = ["Scenario","Current Count","Total Count","Percentage of Total","Trend","Last Refreshed"]
    ofile  = open('/home/ubuntu/iqp/sample.csv', "wb")
    
    #write column names first
    writer = csv.writer(ofile, delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(headers)
    
    user = request.client_user_object
    user_id = user.user_id
    org = request.client_organization_object
    org_namespace_name = org.organization_namespace_name
    this_sub_category = session.query(SubCategory).filter(SubCategory.subcategory_name==sc_name).all()[0]
    sc_id = this_sub_category.subcategory_id
    issue_filter = request.args.get('filter')
    if not issue_filter:
        issue_filter = ''
    query = """SELECT iqp_scenarios.scn_name as name, iqp_scenarios.scn_short_description as description, iqp_problem_count_recent.problem_count as current, COALESCE(iqp_problem_count_prev.problem_count, 0) as prev, (iqp_problem_count_recent.problem_count - COALESCE(iqp_problem_count_prev.problem_count, 0)) as trend, iqp_problem_count_recent.problem_time as refreshtime, COALESCE(problem_count_stats.problem_count,999999999) as stats_total, (iqp_problem_count_recent.problem_count / COALESCE(problem_count_stats.problem_count,999999999)) as stats_percentage
FROM iqp_scenarios
LEFT JOIN {namespace_name}.iqp_problem_count_recent ON (iqp_scenarios.scn_id = iqp_problem_count_recent.scn_id)
LEFT JOIN {namespace_name}.iqp_problem_count_prev ON (iqp_scenarios.scn_id = iqp_problem_count_prev.scn_id)
LEFT JOIN {namespace_name}.iqp_problem_count_recent problem_count_stats ON (iqp_scenarios.scn_totals_scn_id = problem_count_stats.scn_id)
WHERE iqp_scenarios.subcategory_id = '{sc_id}'
AND iqp_problem_count_recent.problem_count > 0
AND (iqp_scenarios.scn_type NOT IN ('Stats', 'N','Feature') OR '{filter_type}' IN ('Stats', 'N','Feature'))
AND (iqp_scenarios.scn_type = '{filter_type}' OR '{filter_type}' = '')
""".format(namespace_name=org_namespace_name,sc_id=sc_id, filter_type=issue_filter)
    s = text(query)
    rs = session.execute(s).fetchall()
    data = [[str(item['description']), int(item['current']), int(item['stats_total']), float(item['stats_percentage']), int(item['trend']), int(item['refreshtime'])] for item in rs]
    #tableData = json.loads(request.args['tableData'])
    #write table data
    for eachRow in data:
        writer.writerow(eachRow)
    return Response(open('/home/ubuntu/iqp/sample.csv', 'r'),headers = d)

@authenticateuser
@verifyloggedin
@expose('/export/scenario/<s_name>')
def exportScenarioTable(request,s_name):
    import csv
    #Response.headers['Content-Type'] = "application/CSV"
    #Response.headers['Content-Disposition'] = 'attachment; filename= sample.csv'
    d = Headers()
    #write the headers
    #d.add("Pragma", "public")
    #d.add("Expires","0")
    #d.add("Cache-Control", must-revalidate, post-check=0, pre-check=0")
    #d.add('Content-Type', "application/force-download")
    #d.add("Content-Type","application/octet-stream")
    d.add("Content-Type","application/octet-stream")
    d.add('Content-Disposition', 'attachment;filename=iqpgenerated.csv')
    
    #get the name space
    user = request.client_user_object
    user_id = user.user_id
    org = request.client_organization_object
    org_namespace_name = org.organization_namespace_name

    
    #get the get arguments
    headers = str(request.args["headers"]).split(",")
    tableName = s_name
    
    ofile  = open('/home/ubuntu/iqp/sample.csv', "wb")
    #write column names first
    writer = csv.writer(ofile, delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(headers)
    
    #write the data
    query = """SELECT * FROM {table}""".format(table = org_namespace_name +'.'+tableName)
    s = text(query)
    rs = session.execute(s).fetchall()
    for item in rs:
        lis = [str(item[eachColumn]) for eachColumn in headers]
        writer.writerow(lis)
    return Response(open('/home/ubuntu/iqp/sample.csv', 'r'),headers = d)

@authenticateuser
@verifyloggedin
@expose('/export/sendemail/')
def export_sendEmail(request):
    #get the name space
    d = Headers()
    d.add('Access-Control-Allow-Origin', 'http://localhost:5000')
    d.add('Access-Control','allow <*>')
    user = request.client_user_object
    user_id = user.user_id
    user_namespace_name = user.user_namespace_name
    svg = str(request.args["svg"])
    tableData = request.args["tableData"]
    return Response("ok",headers = d)
