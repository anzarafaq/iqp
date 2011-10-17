#!/bin/bash

# create the db and db user
su postgres -c "psql -f createdb.sql"

# generate the ddl file with the correct absolute paths
sed -e "s|__SQLDIR__|$PWD|g" ddl-gen.sql > ddl.sql

# generate the other ddl file with the correct absolute paths
sed -e "s|__SQLDIR__|$PWD|g" appddl-gen.sql > appddl.sql

# create the tables with the ddl file
su postgres -c "psql -d iqp -f ddl.sql"

# create the other tables with the other ddl file
su postgres -c "psql -d iqp -f appddl.sql"

# load the metadata from csv file into the category table
python loadmetadata.py
