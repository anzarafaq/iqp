#!/usr/bin/env python
from werkzeug import script

def make_app():
    from iqpapp.application import App
    return App('postgresql://userapp:iqp,$$@localhost:5432/iqp')

action_runserver = script.make_runserver(make_app, use_reloader=True)
#action_runserver = script.make_runserver(make_app, port=8080, ssl_context='adhoc')

script.run()
