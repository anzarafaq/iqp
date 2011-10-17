DROP Schema IF EXISTS CLIENT CASCADE;

CREATE SCHEMA CLIENT;

CREATE TABLE CLIENT.Organizations (
Organization_ID SERIAL PRIMARY KEY,
Organization_Name varchar(80),
Organization_Namespace_Name varchar(80)
);

CREATE TABLE CLIENT.Users (
User_ID SERIAL PRIMARY KEY,
User_Email varchar(80) UNIQUE,
User_Password varchar(80),
User_Enabled boolean,
User_First_Name varchar(80),
User_Last_Name varchar(80),
User_Organization_ID integer references CLIENT.Organizations(Organization_ID),
User_App_Version integer,
User_Data_Source_Type varchar(80)
);

DROP USER userapp;
CREATE USER userapp WITH PASSWORD 'iqp,$$';
GRANT ALL ON DATABASE iqp TO userapp;
GRANT ALL ON SCHEMA CLIENT TO userapp;
GRANT ALL ON ALL TABLES IN SCHEMA CLIENT TO userapp;
GRANT ALL ON ALL SEQUENCES IN SCHEMA CLIENT TO userapp;
