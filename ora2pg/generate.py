import os
import pdb

NAMESPACE = "TEST"
CSV_DIR = "/home/anzar/work/extracted_data"

ora_psql_map = {
 'number': 'numeric(34)',
 'number_n': 'numeric',
 'varchar2': 'varchar',
 'char': 'char',
 'long': 'text',
 'date': 'timestamp',
 'timestamp': 'timestamp',
 'clob': 'text',
 'blob': 'bytea',
 'float': 'number',
 'rowid': 'integer',
 'raw': 'bytea',
 }

all_tables = []
cols = []
start = 0
for aline in open("ora02.sql", "r"):
    aline = aline.lower().strip().replace(',', '')
    if aline.startswith("create table"):
	start = 1
        table_name = aline.split()[2].split(".")[-1]
        cols = []
    elif aline == "(":
         continue
    elif start == 1 and aline == ")":
         start = 0
         all_tables.append(dict(table_name=table_name, cols = cols))
    elif start == 1:
             col = aline.split()
             name = col[0]
             type = col[1]
             if (type.startswith("varchar") 
                or type.startswith("float(") 
                or type.startswith("char(")):
                 typ, sz = type.split("(")
                 type = "%s(%s)" % (ora_psql_map[typ], sz)
             elif type.startswith("number(") :
                 typ, sz = type.split("(")
                 sz = sz.replace(')', '')
                 type = "%s(%s)" % (ora_psql_map[typ+'_n'], sz)
             elif type.startswith("raw(") :
                 typ, sz = type.split("(")
                 sz = sz.replace(')', '')
                 type = ora_psql_map[typ]
             else:
                 type = ora_psql_map[type]
             cols.append((name, type))
    else:
          pass

schema_file_name = "%s.sql" % NAMESPACE 
sfile = open(schema_file_name, "w")

sfile.write("CREATE SCHEMA %s;" % NAMESPACE)

create_stmt = ""
copy_stmt = ""

for atable in all_tables:
    table_name = atable['table_name']
    create_stmt += "\nCREATE TABLE %s.%s" % (NAMESPACE, table_name)
    create_stmt += "\n(\n"
    create_stmt += ",\n".join(["    %s %s" %(col, typ) for col, typ in atable['cols']])
    create_stmt += "\n);\n"
    copy_stmt += "\nCOPY %s.%s FROM '%s/%s.txt' WITH CSV HEADER NULL AS 'null';" % (NAMESPACE, table_name, CSV_DIR, table_name.upper()) 

sfile.write(create_stmt)
sfile.write(copy_stmt)

sfile.close()
