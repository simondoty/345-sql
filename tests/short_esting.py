from NeatPrint import neatPrintTable
		
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_ecp456 PWORD orcl_ecp456 CONTYPE local;
"""
Printing PETS table: 
 ---------------- ---------------- ---------------- ----------------
| PETID          | TYPEID         | BIRTH_YEAR     | NAME           | 
| -------------- + -------------- + -------------- + -------------- |
| 1007           | 2003           | 2006           | JERRY          | 
| 1004           | 2002           | 2007           | MIKE           | 
| 1005           | 2002           | 2000           | BARKLY         | 
| 1001           | 2001           | 2005           | COUSCOUS       | 
| 1006           | 2002           | 2010           | NEMO           | 
| 1003           | 2001           | 2009           | MAPLE          | 
| 1008           | 2003           | 2010           | LOLA           | 
| 1002           | 2001           | 2009           | PUMPKIN        | 
 ---------------- ---------------- ---------------- ----------------

	
Printing VISITS table: 
 ---------------- ---------------- ---------------- ----------------
| VETID          | PETID          | TIME           | PRICE          | 
| -------------- + -------------- + -------------- + -------------- |
| 4001           | 1006           | 2              | 100            | 
| 4005           | 1005           | 1              | 80             | 
| 4003           | 1002           | 24             | 20             | 
| 4003           | 1002           | 2              | 200            | 
| 4002           | 1003           | 2.9            | 95             | 
| 4004           | 1008           | 1              | 15             | 
| 4005           | 1001           | 5              | 50             | 
 ---------------- ---------------- ---------------- ----------------

	
Printing VETS table: 
 ---------------- ---------------- ----------------
| VETID          | NAME           | HIRED_YEAR     | 
| -------------- + -------------- + -------------- |
| 4002           | BOBBY          | 2008           | 
| 4001           | ANDREW         | 2011           | 
| 4004           | DHARMA         | 2010           | 
| 4003           | CATHY          | 2007           | 
| 4005           | ELIZABETH      | 2004           | 
 ---------------- ---------------- ----------------


Pritning ANIMALTYPES table: 
 ---------------- ----------------
| SPECIES        | TYPEID         | 
| -------------- + -------------- |
| CAT            | 2001           | 
| RABBIT         | 2003           | 
| DOG            | 2002           | 
 ---------------- ----------------
"""
########## still isn't working. get string out of bounds at index -14. doesn't appear to be from birth_year either####
#output6=SELECT PETS.NAME, PETS.TYPEID FROM PETS WHERE PETS.TYPEID = (SELECT PETS.TYPEID FROM PETS WHERE PETS.BIRTH_YEAR = (SELECT PETS.BIRTH_YEAR FROM PETS WHERE PETS.PETID = 1001));

# ours is working
#output7=SELECT NAME FROM VETS WHERE VETS.VETID = (SELECT VISITS.VETID FROM VISITS WHERE VISITS.VETID = (SELECT VETS.VETID FROM VETS WHERE VETS.VETID = 4001));

# ours is working
#output8=SELECT VETID, NAME FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = 1001);

# ours is working
#output=SELECT NAME FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = 1001); 

# ours is working
#output1=SELECT * FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = (SELECT PETID FROM PETS WHERE NAME = 'NEMO')); 

# ours is working
#output9=SELECT * FROM PETS WHERE PETS.TYPEID = (SELECT ANIMALTYPES.TYPEID FROM ANIMALTYPES WHERE ANIMALTYPES.SPECIES = 'CAT');
# our is working
#output2=SELECT * FROM PETS, VISITS WHERE PETS.TYPEID = (SELECT ANIMALTYPES.TYPEID FROM ANIMALTYPES WHERE ANIMALTYPES.SPECIES = 'CAT');

#ours is working
#output4=SELECT * FROM VISITS WHERE PRICE = 80;

########### isn't working, need to add second wherefrag?...############################
#output5=SELECT * FROM VISITS WHERE PRICE > 80 AND PETID = (SELECT PETID FROM PETS WHERE NAME = 'NEMO');

# ours is working - so birth_year seems to be working for single queries
#output10=SELECT * FROM PETS WHERE BIRTH_YEAR = 2006;

# ours is working, so birth_year works fine...
#output11=SELECT * FROM VETS WHERE VETID = (SELECT VETID FROM VISITS WHERE PETID = (SELECT PETID FROM PETS WHERE BIRTH_YEAR = 2005));

#ours is working;  this returns multipls rows of correct answers. is it even supposed to be able to do this?
#output12=SELECT * FROM ANIMALTYPES WHERE TYPEID = (SELECT TYPEID FROM PETS WHERE PETID = (SELECT PETID FROM VISITS WHERE TIME = 2));


#print "Printing PETS table: "
#neatPrintTable(outputPETS);
#print "Printing VISITS table: "
#neatPrintTable(outputVISITS);
#print "Printing VETS table: "
#neatPrintTable(outputVETS);
#print "Pritning ANIMALTYPES table: "
#neatPrintTable(outputANIMALTYPES);

#neatPrintTable(output1);
#neatPrintTable(output2);
#neatPrintTable(output3);   
#neatPrintTable(output4);
#neatPrintTable(output5);   # not working
#neatPrintTable(output6);   # not working string out of bounds
#neatPrintTable(output7);
#neatPrintTable(output8);
#neatPrintTable(output9);
#neatPrintTable(output10);
#neatPrintTable(output11);
#neatPrintTable(output12);


#output=SELECT * FROM PETS	WHERE PETS.TYPEID = (SELECT	PETS.TYPEID	FROM PETS WHERE	PETS.BIRTH_YEAR	= (SELECT PETS.BIRTH_YEAR FROM PETS WHERE PETS.PETID = 1001));
#output= SELECT PETS.NAME, PETS.TYPEID FROM PETS WHERE PETS.PETID = (SELECT PETS.PETID FROM PETS WHERE PETS.PETID = 1001);
#output= SELECT PETS.NAME, PETS.TYPEID FROM PETS WHERE PETS.PETID = (SELECT PETS.PETID FROM PETS WHERE PETS.PETID = (SELECT PETS.PETID FROM PETS WHERE PETS.PETID = 1001));

#output=SELECT * FROM VISITS WHERE VETID = (SELECT VETID FROM VISITS WHERE VETID = (SELECT VETID FROM VETS WHERE NAME = 'BOBBY'));

#neatPrintTable(output);


#output=SELECT VETS.NAME FROM VETS WHERE VETS.HIRED_YEAR = 2011;
#output=SELECT * FROM VISITS WHERE VETID = (SELECT VETID FROM VETS WHERE HIRED_YEAR = 2011);
#output=SELECT ANIMALTYPES.TYPEID FROM ANIMALTYPES WHERE ANIMALTYPES.SPECIES = 'CAT';
#output=SELECT * FROM ANIMALTYPES;
#output=SELECT SPECIES FROM ANIMALTYPES WHERE ANIMALTYPES.SPECIES = "CAT";
#output=SELECT * FROM PETS WHERE PETS.TYPEID = (SELECT ANIMALTYPES.TYPEID FROM ANIMALTYPES WHERE ANIMALTYPES.SPECIES = "CAT");  #(SELECT PRICE FROM VISITS WHERE PETID = 1006); #works

#output=SELECT * FROM PETS, VETS WHERE PRICE = (SELECT PRICE FROM VISITS WHERE VISITS.PETID = 1006); #works
#print  output
#neatPrintTable(output);

#output=SELECT TIME, PRICE, VETID, PETID FROM VISITS WHERE PRICE = 80; #works
#neatPrintTable(output);

