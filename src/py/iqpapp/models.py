from utils import session, metadata

#from sqlalchemy import *
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base(metadata=metadata) 

class Category(Base):
    __tablename__ = 'iqp_categories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)
    category_display_order = Column(Integer)

    def __init__(self, category_name=None, category_display_order=None):
        self.category_name = category_name
        self.category_display_order = category_display_order

    def __repr__(self):
        return "<Category('%s')>" % (self.category_name)

class SubCategory(Base):
    __tablename__ = 'iqp_subcategories'
    subcategory_id = Column(Integer, primary_key=True)
    subcategory_name = Column(String)
    category_id = Column(Integer, ForeignKey("iqp_categories.category_id"))

    def __init__(self, subcategory_id=None, subcategory_name=None, category_id=None):
        self.subcategory_id = subcategory_id
        self.subcategory_name = subcategory_name
        self.category_id = category_id

    def __repr__(self):
        return "<Subcategory('%s')>" % (self.subcategory_name)

class Scenario(Base):
    __tablename__ = 'iqp_scenarios'
    scn_id = Column(Integer, primary_key=True)
    scn_name = Column(String)
    scn_long_description = Column(String)
    scn_short_description = Column(String)
    subcategory_id = Column(Integer, ForeignKey("iqp_subcategories.subcategory_id"))
    scn_type = Column(String)
    scn_query = Column(String)
    scn_totals_scn_id = Column(Integer)
    scn_dependent_flag = Column(Boolean)
    scn_dependent_on_id = Column(Integer)
    scn_dependent_filter = Column(String)
    
    def __init__(self, scn_id=None, scn_name=None, scn_long_description=None, scn_short_description=None, subcategory_id=None, scn_type=None, scn_query=None, scn_totals_scn_id=None, scn_dependent_flag=None, scn_dependent_on_id=None, scn_dependent_filter=None):
        self.scn_id = scn_id
        self.scn_name = scn_name
        self.scn_long_description = scn_long_description
        self.scn_short_description = scn_short_description
        self.subcategory_id = subcategory_id
        self.scn_type = scn_type
        self.scn_query = scn_query
        self.scn_totals_scn_id = scn_totals_scn_id
        self.scn_dependent_flag = scn_dependent_flag
        self.scn_dependent_on_id = scn_dependent_on_id
        self.scn_dependent_filter = scn_dependent_filter

    def __repr__(self):
        return "<Scn('%s')>" % (self.scn_name)

class Organization(Base):
    __tablename__ = 'organizations'
    __table_args__ = {'schema':'client'}
    organization_id = Column(Integer, primary_key=True)
    organization_name = Column(String)
    organization_namespace_name = Column(String)

    def __init__(self, organization_name=None, organization_namespace_name=None):
        self.organization_name = organization_name
        self.organization_namespace_name = organization_namespace_name

    def __repr__(self):
        return "<Organization('%s')>" % (self.organization_name)

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema':'client'}
    user_id = Column(Integer, primary_key=True)
    user_email = Column(String)
    user_password = Column(String)
    user_enabled = Column(Boolean)
    user_first_name = Column(String)
    user_last_name = Column(String)
    user_organization_id = Column(Integer)
    user_app_version = Column(String)

    def __init__(self, user_email=None, user_password=None, user_enabled=None, user_first_name=None, user_last_name=None, user_organization_id=None, user_app_version=None):
        self.user_email = user_email
        self.user_password = user_password
        self.user_enabled = user_enabled
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.user_organization_id = user_organization_id
        self.user_app_version = user_app_version

    def __repr__(self):
        return "<User('%s')>" % (self.user_email)

class ProblemCount(Base):
    __tablename__ = 'iqp_problem_count'
    __table_args__ = {}
    problem_time = Column(Integer, primary_key=True)
    scn_id = Column(Integer, primary_key=True)
    problem_count = Column(Integer)

    def __init__(self, namespace_name=None, problem_time=None, scn_id=None , problem_count=None):
        __table_args__ = {'schema':namespace_name}
        self.problem_time = problem_time
        self.scn_id = scn_id
        self.problem_count = problem_count

    def __repr__(self):
        return "<ProblemCount('%s', '%s')>" % (self.scn_id, problem_time)

class AppFamilyPermission(Base):
    __tablename__ = 'app_family_permissions'
    user_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, primary_key=True)

    def __init__(self, user_id=None, category_id=None):
        self.user_id = user_id
        self.category_id = category_id

    def __repr__(self):
        return "<AppFamilyPermissions('%s', '%s')>" % (self.user_id, self.category_id)

class AppPermission(Base):
    __tablename__ = 'app_permissions'
    user_id = Column(Integer, primary_key=True)
    subcategory_id = Column(Integer, primary_key=True)

    def __init__(self, user_id=None, subcategory_id=None):
        self.user_id = user_id
        self.subcategory_id = subcategory_id

    def __repr__(self):
        return "<AppFamilyPermissions('%s', '%s')>" % (self.user_id, self.subcategory_id)
