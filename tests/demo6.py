from NeatPrint import neatPrintTable
		
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_ecp456 PWORD orcl_ecp456 CONTYPE local;


# working - triple table subquery projecting one column
print "\n\n\n\n********Test6 - SELECT NAME FROM VETS WHERE VETS.VETID = (SELECT VISITS.VETID FROM VISITS WHERE VISITS.VETID = (SELECT VETS.VETID FROM VETS WHERE VETS.VETID = 4001));"
test6=SELECT NAME FROM VETS WHERE VETS.VETID = (SELECT VISITS.VETID FROM VISITS WHERE VISITS.VETID = (SELECT VETS.VETID FROM VETS WHERE VETS.VETID = 4001));
neatPrintTable(test6);

