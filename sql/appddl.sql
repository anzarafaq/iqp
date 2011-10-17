DROP TABLE IF EXISTS IQP_Scenarios CASCADE;
DROP TABLE IF EXISTS IQP_SubCategories CASCADE;
DROP TABLE IF EXISTS IQP_Categories CASCADE;
DROP TABLE IF EXISTS App_Family_Permissions CASCADE;
DROP TABLE IF EXISTS App_Permissions CASCADE;
DROP TABLE IF EXISTS Scenario_Clicks_Count CASCADE;
DROP function IF EXISTS insert_clicks(key INT, data TEXT);

CREATE TABLE IQP_Categories (
Category_ID integer PRIMARY KEY,
Category_Name varchar(80),
Category_Display_Order integer
);

CREATE TABLE IQP_SubCategories (
SubCategory_ID integer PRIMARY KEY,
SubCategory_Name varchar(80),
Category_ID integer references IQP_Categories(Category_ID),
Category_Name varchar(80)
);

CREATE TABLE IQP_Scenarios (
Scn_ID integer PRIMARY KEY,
Scn_Name varchar(80),
Scn_Long_Description varchar(1000),
Scn_Short_Description varchar(500),
SubCategory_ID integer references IQP_SubCategories(SubCategory_ID),
Scn_Type varchar(50),
Scn_Query varchar(20000),
Scn_Totals_Scn_ID int,
Scn_Source_Type varchar(50),
Scn_Dependent_Flag boolean,
Scn_Dependent_On_ID int,
Scn_Dependent_Filter varchar(1000)
);

CREATE TABLE App_Family_Permissions (
User_Id integer references CLIENT.Users(User_ID),
Category_ID integer references IQP_Categories(Category_ID),
PRIMARY KEY (User_Id, Category_ID)
);

CREATE TABLE App_Permissions (
User_Id integer references CLIENT.Users(User_ID),
SubCategory_ID integer references IQP_SubCategories(SubCategory_ID),
PRIMARY KEY (User_Id, SubCategory_ID)
);

CREATE TABLE Scenario_Clicks_Count(
Scn_ID integer,
Frequent_Column_Name varchar(80),
Frequency_Number integer,
PRIMARY KEY (Scn_ID,Frequent_Column_Name)
);

CREATE FUNCTION insert_clicks(key INT, data TEXT) RETURNS VOID AS
$$
BEGIN
LOOP
UPDATE scenario_clicks_count SET frequency_number = (SELECT CASE frequency_number WHEN null THEN 0 ELSE frequency_number END FROM scenario_clicks_count where scn_id = key  AND frequent_column_name = data) + 1 WHERE scn_id = key AND frequent_column_name = data;
IF found THEN RETURN;
END IF;
BEGIN
INSERT INTO scenario_clicks_count(scn_id,frequent_column_name,frequency_number) VALUES(key,data,1);
RETURN;
EXCEPTION WHEN unique_violation THEN
END;
END LOOP;
END;
$$
LANGUAGE plpgsql;

GRANT ALL ON SCHEMA public TO userapp;
GRANT ALL ON ALL TABLES IN SCHEMA public TO userapp;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO userapp;
