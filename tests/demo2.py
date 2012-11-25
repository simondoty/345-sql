from NeatPrint import neatPrintTable
		
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_ecp456 PWORD orcl_ecp456 CONTYPE local;


# working - multi-table subquery projecting multiple columns
print "\n\n\n\n********Test2 - SELECT VETID, NAME FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = 1001); "
test2=SELECT VETID, NAME FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = 1001);
neatPrintTable(test2);

