import sys, os
sys.path.append(os.path.dirname(__file__))
from utils import local, local_manager, metadata, session, url_map, SharedDataMiddleware, STATIC_PATH
import views
from custom_request import CustomRequest

from sqlalchemy import create_engine
from werkzeug.wrappers import Request
from werkzeug.wsgi import ClosingIterator
from werkzeug.exceptions import HTTPException
from werkzeug.utils import cached_property
from werkzeug.contrib.securecookie import SecureCookie


class App(object):

    def __init__(self, db_uri):
        local.application = self
        self.database_engine = create_engine(db_uri, convert_unicode=True)
        self.dispatch = SharedDataMiddleware(self.dispatch, {
                '/static':  STATIC_PATH
                })

    def dispatch(self, environ, start_response):
        local.application = self
        request = CustomRequest(environ)
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            response = handler(request, **values)
        except HTTPException, e:
            response = e
        request.client_session.save_cookie(response)
        return ClosingIterator(response(environ, start_response),
                               [session.remove, local_manager.cleanup])

    def __call__(self, environ, start_response):
        return self.dispatch(environ, start_response)
