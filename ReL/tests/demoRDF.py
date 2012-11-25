print "###############################CREATING SQL TABLE###############################"
#Connection is remote because creating SQL table then RDF from SQl
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_demo PWORD orcl_demo CONTYPE remote;

#Creating table to be use as ASP facts for diners problem
DROP TABLE DINERS;

CREATE TABLE DINERS (SUBJECT VARCHAR(255), PREDICATE VARCHAR(255), OBJECT VARCHAR(255));
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrAstor','gender','male');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrBlake','gender','male');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrCrane','gender','male');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrDavis','gender','male');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrAstor','person','NA');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrsAstor','person','NA');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrBlake','person','NA');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrsBlake','person','NA');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrCrane','person','NA');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrsCrane','person','NA');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrDavis','person','NA');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrsDavis','person','NA');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrAstor','married','mrsAstor');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrBlake','married','mrsBlake');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrCrane','married','mrsCrane');
INSERT INTO  DINERS (SUBJECT,PREDICATE,OBJECT) VALUES ('mrDavis','married','mrsDavis');

#In case RDF table exists drop it(for demo purposes)
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_demo PWORD orcl_demo CONTYPE local;
DROP TABLE DINERS;

#Going back to remote connection
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_demo PWORD orcl_demo CONTYPE remote;

#Doing RDFSELECT, if table exits it will return the SQL tuples
#RDFSELECT returns the SQL tuples used to construct RDF
print RDFSELECT * FROM DINERS;
