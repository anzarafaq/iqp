from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session
import csv

db_uri = 'postgresql://userapp:iqp,$$@localhost:5432/iqp'
engine = create_engine(db_uri, convert_unicode=True)
metadata = MetaData()
session = create_session(engine, autocommit=False, autoflush=False)
Base = declarative_base(metadata=metadata) 

class Category(Base):
    __tablename__ = 'iqp_categories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)
    category_display_order = Column(Integer)

    def __init__(self, category_id=None, category_name=None, category_display_order=None):
        self.category_id = category_id
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


## read from category csv and put into db
data = csv.reader(open('categories.csv'))
for row in data:
    category_name = row[0]
    category_display_order = row[1]
    category_id = row[2]
    new_category = Category(category_id, category_name, category_display_order)
    session.add(new_category)
session.commit()

## read from category csv and put into db
data = csv.reader(open('subcategories.csv'))
for row in data:
    subcategory_name = row[0]
    category_name = row[1]
    subcategory_id = row[2]
    if subcategory_id:
        category_result = session.query(Category).filter(Category.category_name==category_name).all()
        if len(category_result) > 0:
            category_id = category_result[0].category_id
            new_subcategory = SubCategory(subcategory_id, subcategory_name, category_id)
            session.add(new_subcategory)
session.commit()

## read from scenario csv and put into db
data = csv.reader(open('scenarios.csv'))
for row in data:
    scn_id = row[0]
    scn_name = row[1]
    scn_long_description = row[2]
    scn_short_description = row[3]
    subcategory_id = row[4]
    scn_type = row[5]
    scn_query = row[6]
    if row[7] == 'NULL':
        scn_totals_scn_id = scn_id;
    else:
        scn_totals_scn_id = int(row[7])
    scn_source_type = row[8]
    scn_dependent_flag = bool(row[10])
    scn_dependent_on_id = 0
    scn_dependent_filter = row[11]

    if scn_id:
        new_scenario = Scenario(scn_id, scn_name, scn_long_description, scn_short_description, subcategory_id, scn_type, scn_query, scn_totals_scn_id, scn_dependent_flag, scn_dependent_on_id, scn_dependent_filter)
        session.add(new_scenario)
session.commit()
