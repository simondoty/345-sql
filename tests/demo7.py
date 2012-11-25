from NeatPrint import neatPrintTable
		
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_ecp456 PWORD orcl_ecp456 CONTYPE local;


# working - triple table subquery projecting all columns
print "\n\n\n\n********Test7 - SELECT * FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = (SELECT PETID FROM PETS WHERE BIRTH_YEAR = 2005));"
test7=SELECT * FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = (SELECT PETID FROM PETS WHERE BIRTH_YEAR = 2005));
neatPrintTable(test7);

