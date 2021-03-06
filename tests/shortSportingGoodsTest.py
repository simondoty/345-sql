# Sporting goods store test script for ReL

# Little function that prints results neatly
def neatPrint(results):
        for ii in range(0, len(results)):
                print(results[ii]);
        print;

# Connect to the database
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_demo PWORD orcl_demo CONTYPE local;
DROP TABLE RDF_DATA;

# Header from the original file:
#   Sporting_Goods Database
#
# 
#  SCRIPT - FUNCTION
#   Create and populate tables and sequences to support the Sporting Goods business scenario.
#   This database is a modified version of the database used in some of the classes of
#   the ORACLE Corporation.
# 
# NOTES
# 
# MODIFIED
# Originally created:  GDURHAM  Mar 15, 1993  -- ORACLE Corporation
#
# Modified and reprinted with permission from The ORACLE Corporation
# by Drs. Ramon A. Mata-Toledo and Pauline K. Cushman on Dec 15, 1999.
#
# Most recently modified by Andrew Oldag 29 July 2012
# NOTE: As it stands now, ReL can't create sequences, so those will be commented out, 
# perhaps for future use down the line.
# Other changes where made in the original script so that they would be understood by the existing grammar.


# Start of the creation and population of tables. Please wait.

#	************** S_CUSTOMER TABLE *********************************
#	*****************************************************************

DROP TABLE s_customer CASCADE CONSTRAINTS;
CREATE TABLE s_customer (id VARCHAR2(3), name VARCHAR2(20), phone VARCHAR2(20), address VARCHAR2(20), city VARCHAR2(20), state VARCHAR2(15), country VARCHAR2(20), zip_code VARCHAR2(15), credit_rating VARCHAR2(9), sales_rep_id VARCHAR2(3), region_id VARCHAR2(3), comments VARCHAR2(255) );

INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('301', 'Sports,Inc', '540-123-4567','72 High St','Harrisonburg', 'VA','US', '22809','EXCELLENT', '12', '1', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('302', 'Toms Sporting Goods', '540-987-6543','6741 Main St','Harrisonburg', 'VA','US', '22809','POOR', '14', '1', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('303', 'Athletic Attire', '540-123-6789','54 Market St','Harrisonburg', 'VA','US', '22808','GOOD', '14', '1', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('304', 'Athletics For All', '540-987-1234','286 Main St', 'Harrisonburg', 'VA','US', '22808','EXCELLENT', '12', '1', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('305', 'Shoes for Sports', '540-123-9876','538 High St','Harrisonburg', 'VA','US', '22809','EXCELLENT', '14', '1', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('306', 'BJ Athletics', '540-987-9999','632 Water St','Harrisonburg', 'VA','US', '22810','POOR', '12', '1', '');

INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('403', 'Athletics One', '717-234-6786','912 Columbia Rd','Lancaster', 'PA','US', '17601','GOOD', '14', '1', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('404', 'Great Athletes', '717-987-2341','121 Litiz Pike','Lancaster', 'PA','US', '17602','EXCELLENT', '12', '1', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('405', 'Athletics Two', '717-987-9875','435 High Rd','Lancaster', 'PA','US', '17602','EXCELLENT', '14', '1', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('406', 'Athletes Attic', '717-234-9888','101 Greenfield Rd','Lancaster', 'PA','US', '17601','POOR', '12', '1', '');

INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('201', 'One Sport', '55-112066222','82 Via Bahia', 'Sao Paolo','', 'Brazil', '','EXCELLENT', '12', '2', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('202', 'Deportivo Caracas', '58-28066222','31 Sabana Grande','Caracas', '', 'Venezuela', '','EXCELLENT', '12', '2', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('203', 'New Delhi Sports', '91-11903338','11368 Chanakya','New Delhi', '', 'India', '','GOOD', '11', '4', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('204', 'Ladysport', '1-206-104-0111','281 Queen Street','Seattle', 'Washington', 'US', '','EXCELLENT', '11', '1', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('205', 'Kim''s Sporting Goods', '852-3693888','15 Henessey Road','Hong Kong', '', '', '','EXCELLENT', '11', '4', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('206', 'Sportique', '33-93425722253','172 Rue de Place','Cannes', '', 'France', '','EXCELLENT', '13', '5', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('207', 'Tall Rock Sports', '234-16036222','10 Saint Antoine','Lagos', '', 'Nigeria', '','GOOD', '', '3', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('208', 'Muench Sports', '49-895274449','435 Gruenestrasse','Munich', '', 'Germany', '','GOOD', '13', '5', '');

INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('209', 'Beisbol Si!', '809-352666','415 Playa Del Mar', 'San Pedro de Macoris', '', 'Dominican Republic', '', 'EXCELLENT', '11', '6', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('210', 'Futbol Sonora', '52-404555','5 Via Saguaro', 'Nogales','', 'Mexico', '','EXCELLENT', '12', '2', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('211', 'Helmut''s Sports', '42-2111222','45 Modrany', 'Prague','', 'Czechoslovakia', '','EXCELLENT', '11', '5', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('212', 'Hamada Sport', '20-31209222','47A Corniche', 'Alexandria', '', 'Egypt', '','EXCELLENT', '13', '3', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('213', 'Sports Emporium', '1-415-555-6281','4783 168th Street','San Francisco', 'CA', 'US', '','EXCELLENT', '11', '1', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('214', 'Sports Retail', '1-716-555-7777','115 Main Street','Buffalo', 'NY', 'US', '', 'POOR', '11', '1', '');
INSERT INTO s_customer (id, name, phone, address, city, state, country, zip_code, credit_rating, sales_rep_id, region_id, comments) VALUES ('215', 'Sports Russia', '7-0953892444','7070 Yekatamina','Saint Petersburg', '', 'Russia', '','POOR', '11', '5', '');

#	************** S_CUSTOMER TABLE ********************************
#	*****************************************************************

DROP TABLE s_dept CASCADE CONSTRAINTS;
CREATE TABLE s_dept (id VARCHAR2(3), name VARCHAR2(20), region_id VARCHAR2(3));

INSERT INTO s_dept (id, name, region_id) VALUES ('10', 'Finance', '1');
INSERT INTO s_dept (id, name, region_id) VALUES ('31', 'Sales', '1');
INSERT INTO s_dept (id, name, region_id) VALUES ('32', 'Sales', '2');
INSERT INTO s_dept (id, name, region_id) VALUES ('33', 'Sales', '3');
INSERT INTO s_dept (id, name, region_id) VALUES ('34', 'Sales', '4');
INSERT INTO s_dept (id, name, region_id) VALUES ('35', 'Sales', '5');
INSERT INTO s_dept (id, name, region_id) VALUES ('41', 'Operations', '1');
INSERT INTO s_dept (id, name, region_id) VALUES ('42', 'Operations', '2');
INSERT INTO s_dept (id, name, region_id) VALUES ('43', 'Operations', '3');
INSERT INTO s_dept (id, name, region_id) VALUES ('44', 'Operations', '4');
INSERT INTO s_dept (id, name, region_id) VALUES ('45', 'Operations', '5');
INSERT INTO s_dept (id, name, region_id) VALUES ('50', 'Administration', '1');

#	************** S_TEMP TABLE ********************************
#	*****************************************************************

DROP TABLE s_emp CASCADE CONSTRAINTS;
CREATE TABLE s_emp (id VARCHAR2(3), last_name VARCHAR2(20), first_name VARCHAR2(20), userid VARCHAR2(8), start_date DATE, comments VARCHAR2(255), manager_id VARCHAR2(3), title VARCHAR2(25), dept_id VARCHAR2(3), salary NUMERIC(11,2), commission_pct NUMERIC(4,2) );

INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('1', 'Martin','Carmen','martincu','1990-03-03', '','', 'President', '50', 4500, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('2','Smith','Doris','smithdj', '1990-03-08','','1', 'VP, Operations','41', 2450, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('3', 'Norton','Michael','nortonma','1991-06-17','','1', 'VP, Sales', '31', 2400, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('4', 'Quentin', 'Mark','quentiml','1990-04-07','','1', 'VP, Finance', '10', 2450, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('5', 'Roper', 'Joseph','roperjm','1990-03-04','','1', 'VP, Administration', '50', 2550, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('6', 'Brown', 'Molly','brownmr','1991-01-18','','2', 'Warehouse Manager', '41', 1600, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('7', 'Hawkins', 'Roberta','hawkinrt','1990-05-14','','2', 'Warehouse Manager','42', 1650, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('8', 'Burns', 'Ben','burnsba','1990-04-07','','2', 'Warehouse Manager','43', 1500, 0);

INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('9', 'Catskill', 'Antoinette','catskiaw','1992-02-09','','2', 'Warehouse Manager','44', 1700, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('10', 'Jackson', 'Marta','jacksomt','1991-02-27','','2', 'Warehouse Manager','45', 1507,0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('11', 'Henderson', 'Colin','hendercs','1990-05-14','','3', 'Sales Representative', '31', 1400, 10);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('12', 'Gilson', 'Sam', 'gilsonsj','1992-01-18','','3', 'Sales Representative','32', 1490, 12.5);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('13', 'Sanders', 'Jason', 'sanderjk','1991-02-18','','3', 'Sales Representative','33', 1515, 10);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('14', 'Dameron', 'Andre', 'dameroap','1991-10-09','','3', 'Sales Representative','35', 1450, 17.5);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('15', 'Hardwick', 'Elaine', 'hardwiem','1992-02-07','','6', 'Stock Clerk','41', 1400, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('16', 'Brown', 'George', 'browngw','1990-03-08','','6', 'Stock Clerk','41', 940, 0);

INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('17', 'Washington', 'Thomas', 'washintl','1991-02-09','','7', 'Stock Clerk', '42', 1200, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('18', 'Patterson', 'Donald', 'patterdv','1991-08-06','','7', 'Stock Clerk','42', 795, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('19', 'Bell', 'Alexander', 'bellag','1991-05-26','','8', 'Stock Clerk','43', 850, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('20', 'Gantos', 'Eddie', 'gantosej','1990-11-30','','9', 'Stock Clerk','44', 800, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('21', 'Stephenson', 'Blaine', 'stephebs','1991-03-17','','10', 'Stock Clerk','45', 860, 0);

INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('22', 'Chester', 'Eddie', 'chesteek','1990-11-30', '', '9', 'Stock Clerk','44', 800, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('23', 'Pearl', 'Roger', 'pearlrg','1990-10-17', '', '9', 'Stock Clerk','34', 795, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('24', 'Dancer', 'Bonnie', 'dancerbw','1991-03-17', '', '7', 'Stock Clerk','45', 860, 0);
INSERT INTO s_emp (id, last_name, first_name, userid, start_date, comments, manager_id, title, dept_id, salary, commission_pct) VALUES ('25', 'Schmitt', 'Sandra', 'schmitss','1991-05-09', '', '8', 'Stock Clerk','45', 1100, 0);
