###################################
######utils for the application
###################################

from sqlalchemy import MetaData
from sqlalchemy.orm import create_session, scoped_session
from werkzeug.wrappers import Response
from werkzeug.local import Local, LocalManager
from werkzeug.routing import Map, Rule

local = Local()
local_manager = LocalManager([local])
application = local('application')

metadata = MetaData()
session = scoped_session(lambda: create_session(application.database_engine,
                         autocommit=False, autoflush=False),
                         local_manager.get_ident)

url_map = Map()
def expose(rule, **kw):
    def decorate(f):
        kw['endpoint'] = f.__name__
        url_map.add(Rule(rule, **kw))
        return f
    return decorate

def url_for(endpoint, _external=False, **values):
    return local.url_adapter.build(endpoint, values, force_external=_external)

#######################
######utils for jinja2
#######################

from os import path
from urlparse import urlparse
from werkzeug.wrappers import Response
from jinja2 import Environment, FileSystemLoader

ALLOWED_SCHEMES = frozenset(['http', 'https', 'ftp', 'ftps'])
TEMPLATE_PATH = path.join(path.dirname(__file__), 'templates')
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
jinja_env.globals['url_for'] = url_for

def render_template(template, **context):
    return Response(jinja_env.get_template(template).render(**context),
                    mimetype='text/html')

def validate_url(url):
    return urlparse(url)[0] in ALLOWED_SCHEMES

##############################################
######utils for shared data middleware
##############################################

from os import path
from werkzeug.wsgi import SharedDataMiddleware

STATIC_PATH = path.join(path.dirname(__file__), 'static')
url_map.add(Rule('/static/<file>', endpoint='static', build_only=True))

##########################
