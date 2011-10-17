from utils import session, expose, render_template, url_for
from models import Category, SubCategory, Scenario
from models import Organization, User, AppFamilyPermission, AppPermission

from werkzeug.utils import redirect
from sqlalchemy.sql import text
from cgi import escape
import json
import hashlib
import uuid

def authenticateuser(fn):
   def wrapper(*args, **kwargs):
      request = args[0]
      c = request.client_session
      loggedinuser = None
      if "user_id" not in c:
         pass
      else:
         loggedinuser = request.client_user_object
      result = fn(*args, **kwargs)
      return result
   return wrapper

def verifyloggedin(fn):
   def wrapper(*args, **kwargs):
      request = args[0]
      c = request.client_session
      user = request.client_user_object
      if not user:
         return redirect(url_for('welcome'))
      else:
         result = fn(*args, **kwargs)
         return result
   return wrapper

def authorizeuseroncategory(fn):
   def wrapper(*args, **kwargs):
      request = args[0]
      user = request.client_user_object
      if not user:
         return redirect(url_for('welcome'))
      else:
         user_id = user.user_id
         category_name = kwargs['c_name']
         categoryquery = session.query(Category).filter(Category.category_name==category_name).all()
         if len(categoryquery) == 0:
            return redirect(url_for('overview'))
         else:
            category_id = categoryquery[0].category_id
            ## check user permission here
            appfamilypermisionquery = session.query(AppFamilyPermission).filter(AppFamilyPermission.user_id==user_id).filter(AppFamilyPermission.category_id==category_id).all()
            if len(appfamilypermisionquery) == 0:
               return redirect(url_for('setpermissions'))
            else:
               result = fn(*args, **kwargs)
               return result
   return wrapper

def authorizeuseronsubcategory(fn):
   def wrapper(*args, **kwargs):
      request = args[0]
      user = request.client_user_object
      if not user:
         return redirect(url_for('welcome'))
      else:
         user_id = user.user_id
         subcategory_name = kwargs['sc_name']
         subcategoryquery = session.query(SubCategory).filter(SubCategory.subcategory_name==subcategory_name).all()
         if len(subcategoryquery) == 0:
            return redirect(url_for('overview'))
         else:
            subcategory_id = subcategoryquery[0].subcategory_id
            ## check user permission here
            apppermisionquery = session.query(AppPermission).filter(AppPermission.user_id==user_id).filter(AppPermission.subcategory_id==subcategory_id).all()
            if len(apppermisionquery) == 0:
               return redirect(url_for('setpermissions'))
            else:
               result = fn(*args, **kwargs)
               return result
   return wrapper

@authenticateuser
@expose('/login/')
def login(request):
   c = request.client_session
   if request.method == 'POST':
      email = request.form.get('email')
      email = escape(email)
      password = request.form.get('password')
      password = escape(password)
      hashedpassword = hashlib.md5(password).hexdigest()
      userlogin = session.query(User).filter(User.user_email==email).filter(User.user_password==hashedpassword).all()
      loggedinuser = None
      for user in userlogin:
         loggedinuser = user
      if loggedinuser:
         c["user_id"] = loggedinuser.user_id
         c.modified
         return redirect(url_for('overview'))
   return render_template('login.html')

@authenticateuser
@expose('/logout/')
def logout(request):
   c = request.client_session
   if "user_id" in c:
      del c["user_id"]
   return redirect(url_for('welcome'))

@authenticateuser
@expose('/register/')
def register(request):
   c = request.client_session
   if request.method == 'POST':
      email = request.form.get('email')
      email = escape(email)
      password = request.form.get('password')
      password = escape(password)
      confirmpassword = request.form.get('confirmpassword')
      confirmpassword = escape(confirmpassword)
      firstname = request.form.get('firstname')
      firstname = escape(firstname)
      lastname = request.form.get('lastname')
      lastname = escape(lastname)
      companyname = request.form.get('companyname')
      companyname = escape(companyname)
      if password == confirmpassword:
         ## assign organizatio or create new one
         this_organization_result = session.query(Organization).filter(Organization.organization_name==companyname).all()
         if len(this_organization_result)>0:
            this_organization = this_organization_result[0]
            this_organization_id = this_organization.organization_id
         else:
            org_uuid = uuid.uuid1().hex
            namespace_name = companyname.strip().replace(' ', '') + org_uuid
            namespace_name = namespace_name.lower()
            new_organization = Organization(companyname, namespace_name)
            session.add(new_organization)
            query = """CREATE SCHEMA {u_namespace_name}
""".format(u_namespace_name=namespace_name)
            s = text(query)
            session.execute(s)
         ## create count table in user namespace
            query = """CREATE TABLE {u_namespace_name}.iqp_problem_count (
Problem_Time integer,
Scn_ID integer references IQP_Scenarios(Scn_ID),
Problem_Count integer,
PRIMARY KEY (Problem_Time, Scn_ID)
)
""".format(u_namespace_name=namespace_name)
            s = text(query)
            session.execute(s)
         ## create recent problem count view
            query = """CREATE VIEW {u_namespace_name}.IQP_Problem_Count_Recent AS
SELECT recent.problem_time, fulltable.scn_id, fulltable.problem_count
FROM {u_namespace_name}.iqp_problem_count fulltable
JOIN (
SELECT MAX(t1.problem_time) as problem_time, t1.scn_id
FROM {u_namespace_name}.iqp_problem_count t1
GROUP BY scn_id) recent
ON recent.problem_time = fulltable.problem_time
AND recent.scn_id = fulltable.scn_id
""".format(u_namespace_name=namespace_name)
            s = text(query)
            session.execute(s)
            
         ## create previous problem count view
            query = """CREATE VIEW {u_namespace_name}.IQP_Problem_Count_Prev AS
SELECT prev.problem_time, fulltable.scn_id, fulltable.problem_count
FROM {u_namespace_name}.iqp_problem_count fulltable
JOIN (
SELECT MAX(fulltable.problem_time) as problem_time, fulltable.scn_id
FROM {u_namespace_name}.iqp_problem_count fulltable
JOIN (
SELECT MAX(t1.problem_time) as problem_time, t1.scn_id
FROM {u_namespace_name}.iqp_problem_count t1
GROUP BY scn_id) prev
ON prev.scn_id = fulltable.scn_id
WHERE prev.problem_time > fulltable.problem_time
GROUP BY fulltable.scn_id
) prev
ON prev.problem_time = fulltable.problem_time
AND prev.scn_id = fulltable.scn_id
""".format(u_namespace_name=namespace_name)
            s = text(query)
            session.execute(s)
            this_organization = new_organization
            ## commit changes
            session.commit()
            this_organization_id = this_organization.organization_id
         
         ## create new user
         hashedpassword = hashlib.md5(password).hexdigest()
         new_user = User(email, hashedpassword, '0', firstname, lastname, this_organization_id, '0')
         session.add(new_user)
         ## commit changes
         session.commit()
         ## set user id in cookie
         c["user_id"] = new_user.user_id
         c.modified
         return redirect(url_for('overview'))
   return render_template('register.html')

@authenticateuser
@verifyloggedin
@expose('/setpermissions/')
def setpermissions(request):
   user = request.client_user_object
   user_id = user.user_id
   categories = session.query(Category).order_by(Category.category_display_order.asc())
   return render_template('setpermissions.html', categories=categories)

@authenticateuser
@verifyloggedin
@expose('/setpermissions2/')
def setpermissions2(request):
   user = request.client_user_object
   user_id = user.user_id
   if request.method == 'POST':
      selectedcategory_ids = request.form.getlist('category')
      session.query(AppFamilyPermission).filter(AppFamilyPermission.user_id==user_id).delete()
      for selectedcategory_id in selectedcategory_ids:
         selectedcategory = session.query(Category).filter(Category.category_id==selectedcategory_id)
         newappfamilypermission = AppFamilyPermission(user_id, selectedcategory_id)
         session.add(newappfamilypermission)
      session.commit()

      categories = session.query(Category).filter(Category.category_id.in_(selectedcategory_ids)).order_by(Category.category_display_order.asc()).all()
      subcategories = session.query(SubCategory, Category).join(Category, Category.category_id == SubCategory.category_id).all()
   else:
      return redirect(url_for('setpermissions'))
   return render_template('setpermissions2.html', categories=categories, subcategories=subcategories)

@authenticateuser
@verifyloggedin
@expose('/setpermissions3/')
def setpermissions3(request):
   user = request.client_user_object
   user_id = user.user_id
   if request.method == 'POST':
      selectedsubcategory_ids = request.form.getlist('subcategory')
      session.query(AppPermission).filter(AppPermission.user_id==user_id).delete()
      for selectedsubcategory_id in selectedsubcategory_ids:
         selectedsubcategory = session.query(SubCategory).filter(SubCategory.subcategory_id==selectedsubcategory_id)
         newapppermission = AppPermission(user_id, selectedsubcategory_id)
         session.add(newapppermission)
      session.commit()
   else:
      return redirect(url_for('setpermissions'))
   return render_template('setpermissions3.html')
