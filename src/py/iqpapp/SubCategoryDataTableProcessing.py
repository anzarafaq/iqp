from utils import session, expose, render_template, Response
from models import Scenario
from sqlalchemy.sql import text
import json

def generateDataTables(request,sc_id,issue_filter):
    data = {
            "sEcho": int(request.args["sEcho"]), # we should echo it with the same no, else datatable will not genrate a table
            "iTotalDisplayRecords": 10,
            }
    columns=['name', 'description' , 'current', 'stats_total', 'stats_percentage', 'trend', 'refreshtime']
    query = """SELECT iqp_scenarios.scn_name as name, iqp_scenarios.scn_short_description as description, iqp_problem_count_recent.problem_count as current, COALESCE(iqp_problem_count_prev.problem_count, 0) as prev, (iqp_problem_count_recent.problem_count - COALESCE(iqp_problem_count_prev.problem_count, 0)) as trend, iqp_problem_count_recent.problem_time as refreshtime, COALESCE(problem_count_stats.problem_count,999999999) as stats_total, (iqp_problem_count_recent.problem_count / COALESCE(problem_count_stats.problem_count,999999999)) as stats_percentage
FROM iqp_scenarios
LEFT JOIN iqp_problem_count_recent ON (iqp_scenarios.scn_id = iqp_problem_count_recent.scn_id)
LEFT JOIN iqp_problem_count_prev ON (iqp_scenarios.scn_id = iqp_problem_count_prev.scn_id)
LEFT JOIN iqp_problem_count_recent problem_count_stats ON (iqp_scenarios.scn_totals_scn_id = problem_count_stats.scn_id)
WHERE iqp_scenarios.subcategory_id = '{sc_id}'
AND iqp_problem_count_recent.problem_count > 0
AND iqp_scenarios.scn_type NOT IN ('Stats', 'N','Feature')
AND (iqp_scenarios.scn_type = '{scen_type}' OR '{scen_type}' = '')
""".format(sc_id=sc_id, scen_type=issue_filter)
    #s = text(query)
    rs = session.execute(query).fetchall()
    data = [[str(item['name']), str(item['description']), int(item['current']), int(item['stats_total']), float(item['stats_percentage']), int(item['trend']), int(item['refreshtime'])] for item in rs]
    return json.dumps(data)
