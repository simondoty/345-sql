from NeatPrint import neatPrintTable
		
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_dotysn PWORD orcl_dotysn CONTYPE local;

# !!! need to run tests/fillTestTables.py before running this
#output=SELECT TIME TIME_1, p.PRICE, p.VETID AS VETID_P, p.PETID FROM VISITS AS p WHERE PRICE = 80; #works
#neatPrintTable(output);

#output=SELECT * FROM VISITS; #works
#neatPrintTable(output);


#output=SELECT * FROM  PETS;
#output=SELECT * FROM PETS, VETS WHERE PRICE = 80;; #, PETS, VETS; # WHERE PRICE = (SELECT PRICE FROM VISITS WHERE PETID = 1006) ; #works
#neatPrintTable(output);



#output=SELECT * FROM PETS, VETS WHERE VETS.PRICE = 80; #(SELECT PRICE FROM VISITS WHERE PETID = 1006); #works

output=SELECT * FROM PETS, VETS WHERE PRICE = (SELECT PRICE FROM VISITS WHERE VISITS.PETID = 1006); #works
#print  output
#neatPrintTable(output);


#output=SELECT TIME, PRICE, VETID, PETID FROM VISITS WHERE PRICE = 80; #works
#neatPrintTable(output);


