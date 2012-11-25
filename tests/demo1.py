from NeatPrint import neatPrintTable
		
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_ecp456 PWORD orcl_ecp456 CONTYPE local;


# multi-table subquery projecting one column
print "\n\n\n\n********Test1 - SELECT NAME FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = 1001); "
test1=SELECT NAME FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = 1001); 
neatPrintTable(test1);

