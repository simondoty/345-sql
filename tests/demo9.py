from NeatPrint import neatPrintTable
		
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_ecp456 PWORD orcl_ecp456 CONTYPE local;


# working - From Project Requirements Examples - triple table subquery with multiple rows returned using "IN (...)"
print "\n\n\n\n********Test9 - SELECT PETS.NAME, PETS.TYPEID FROM PETS WHERE PETS.TYPEID = (SELECT PETS.TYPEID FROM PETS WHERE PETS.BIRTH_YEAR = (SELECT PETS.BIRTH_YEAR FROM PETS WHERE PETS.PETID = 1001));"
test9=SELECT PETS.NAME, PETS.TYPEID FROM PETS WHERE PETS.TYPEID = (SELECT PETS.TYPEID FROM PETS WHERE PETS.BIRTH_YEAR = (SELECT PETS.BIRTH_YEAR FROM PETS WHERE PETS.PETID = 1001));
neatPrintTable(test9);


