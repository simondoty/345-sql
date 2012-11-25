from NeatPrint import neatPrintTable
		
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_ecp456 PWORD orcl_ecp456 CONTYPE local;



# working - multi-table subquery projecting all columns
print "\n\n\n\n********Test3 - SELECT * FROM PETS WHERE PETID = (SELECT PETID FROM VISITS WHERE TIME = 2.9); "
test3=SELECT * FROM PETS WHERE PETID = (SELECT PETID FROM VISITS WHERE TIME = 2.9);
neatPrintTable(test3);

