from NeatPrint import neatPrintTable
		
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_ecp456 PWORD orcl_ecp456 CONTYPE local;

# working - triple table subquery with multiple rows returned using "IN (...)"
print "\n\n\n\n********Test8 - SELECT * FROM ANIMALTYPES WHERE TYPEID = (SELECT TYPEID FROM PETS WHERE PETID = (SELECT PETID FROM VISITS WHERE TIME = 2));"
test8=SELECT * FROM ANIMALTYPES WHERE TYPEID = (SELECT TYPEID FROM PETS WHERE PETID = (SELECT PETID FROM VISITS WHERE TIME = 2));
neatPrintTable(test8);

