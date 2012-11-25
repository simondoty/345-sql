from NeatPrint import neatPrintTable
		
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_ecp456 PWORD orcl_ecp456 CONTYPE local;

#working - multi-table subquery with two criteria in WHERE and two criteria in subquery
print "\n\n\n\n********Test5 - SELECT * FROM VISITS WHERE PRICE > 80 AND PETID = (SELECT PETID FROM PETS WHERE PETS.TYPEID > 2001 AND NAME = 'NEMO');"
test5=SELECT * FROM VISITS WHERE PRICE > 80 AND PETID = (SELECT PETID FROM PETS WHERE PETS.TYPEID > 2001 AND NAME = 'NEMO');
neatPrintTable(test5);

