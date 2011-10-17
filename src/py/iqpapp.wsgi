import sys, os
sys.path.append(os.path.dirname(__file__)) 

from iqpapp.application import App
application = App('postgresql://userapp:iqp,$$@localhost:5432/iqp')
