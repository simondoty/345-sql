from NeatPrint import neatPrintTable
		
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_ecp456 PWORD orcl_ecp456 CONTYPE local;


# basic select with criteria
print "\n********Test0a - SELECT * FROM VISITS WHERE PRICE < 80; "
test0a=SELECT * FROM VISITS WHERE PRICE < 80;
neatPrintTable(test0a);

# basic select with multiple criteria
print "\n********Test0b - SELECT * FROM PETS WHERE BIRTH_YEAR >= 2010 AND TYPEID = 2002; "
test0b=SELECT * FROM PETS WHERE BIRTH_YEAR >= 2010 AND TYPEID = 2002;
neatPrintTable(test0b);


# multi-table subquery projecting one column
print "\n\n\n\n********Test1 - SELECT NAME FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = 1001); "
test1=SELECT NAME FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = 1001); 
neatPrintTable(test1);

# working - multi-table subquery projecting multiple columns
print "\n\n\n\n********Test2 - SELECT VETID, NAME FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = 1001); "
test2=SELECT VETID, NAME FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = 1001);
neatPrintTable(test2);

# working - multi-table subquery projecting all columns
print "\n\n\n\n********Test3 - SELECT * FROM PETS WHERE PETID = (SELECT PETID FROM VISITS WHERE TIME = 2.9); "
test3=SELECT * FROM PETS WHERE PETID = (SELECT PETID FROM VISITS WHERE TIME = 2.9);
neatPrintTable(test3);

# working - multi-table subquery with two criteria in the subquery
print "\n\n\n\n********Test4 - SELECT * FROM VISITS WHERE PETID = (SELECT PETID FROM PETS WHERE PETS.TYPEID > 2001 AND NAME = 'NEMO';"
test4=SELECT * FROM VISITS WHERE PETID = (SELECT PETID FROM PETS WHERE PETS.TYPEID > 2001 AND NAME = 'NEMO');
neatPrintTable(test4);

#working - multi-table subquery with two criteria in WHERE and two criteria in subquery
print "\n\n\n\n********Test5 - SELECT * FROM VISITS WHERE PRICE > 80 AND PETID = (SELECT PETID FROM PETS WHERE PETS.TYPEID > 2001 AND NAME = 'NEMO');"
test5=SELECT * FROM VISITS WHERE PRICE > 80 AND PETID = (SELECT PETID FROM PETS WHERE PETS.TYPEID > 2001 AND NAME = 'NEMO');
neatPrintTable(test5);

# working - triple table subquery projecting one column
print "\n\n\n\n********Test7 - SELECT NAME FROM VETS WHERE VETS.VETID = (SELECT VISITS.VETID FROM VISITS WHERE VISITS.VETID = (SELECT VETS.VETID FROM VETS WHERE VETS.VETID = 4001));"
test6=SELECT NAME FROM VETS WHERE VETS.VETID = (SELECT VISITS.VETID FROM VISITS WHERE VISITS.VETID = (SELECT VETS.VETID FROM VETS WHERE VETS.VETID = 4001));
neatPrintTable(test6);

# working - triple table subquery projecting all columns
print "\n\n\n\n********Test7 - SELECT * FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = (SELECT PETID FROM PETS WHERE BIRTH_YEAR = 2005));"
test7=SELECT * FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = (SELECT PETID FROM PETS WHERE BIRTH_YEAR = 2005));
neatPrintTable(test7);

# working - triple table subquery with multiple rows returned using "IN (...)"
print "\n\n\n\n********Test8 - SELECT * FROM ANIMALTYPES WHERE TYPEID = (SELECT TYPEID FROM PETS WHERE PETID = (SELECT PETID FROM VISITS WHERE TIME = 2));"
test8=SELECT * FROM ANIMALTYPES WHERE TYPEID = (SELECT TYPEID FROM PETS WHERE PETID = (SELECT PETID FROM VISITS WHERE TIME = 2));
neatPrintTable(test8);

# working - From Project Requirements Examples - triple table subquery with multiple rows returned using "IN (...)"
print "\n\n\n\n********Test9 - SELECT PETS.NAME, PETS.TYPEID FROM PETS WHERE PETS.TYPEID = (SELECT PETS.TYPEID FROM PETS WHERE PETS.BIRTH_YEAR = (SELECT PETS.BIRTH_YEAR FROM PETS WHERE PETS.PETID = 1001));"
test9=SELECT PETS.NAME, PETS.TYPEID FROM PETS WHERE PETS.TYPEID = (SELECT PETS.TYPEID FROM PETS WHERE PETS.BIRTH_YEAR = (SELECT PETS.BIRTH_YEAR FROM PETS WHERE PETS.PETID = 1001));
neatPrintTable(test9);


