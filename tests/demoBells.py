print "\n\n#############################   Bells (Inequality) Theorem   #############################\n"
PRO ?>>[CLEAR]. 
PRO ?[points.pl].



#Creating Datapoints
MAKECONNECT URL jdbc:oracle:thin:@rising-sun.microlab.cs.utexas.edu:1521:orcl UNAME CS345_demo PWORD orcl_demo CONTYPE local;
DROP TABLE DATAPOINTS;
CREATE TABLE DATAPOINTS (DATA VARCHAR(255), C1 NUMBER, C2 NUMBER, C3 NUMBER);
i = 1
while (i < 16):
	c = 0
	for j in range(4):
		c1 = 0
		for k in range(4):
			INSERT INTO  DATAPOINTS (DATA,C1,C2,C3) VALUES ('data',i,c,c1);
			#ASP ?->'data'(i,c,c1).
			c1 = c1 + 30
			i = i + 1
		c = c + 30

#Creating facts for Bells Theorem
facts = []

for i in ASPSELECT * FROM DATAPOINTS;:
	print "\nRaw return: "	
	print i
	x = str(i).strip("'").split(",")
	print x
	if(int(x[1])<6):
		facts.append( x[0]+"("+x[1]+", "+x[2]+", "+x[3]+")" )
	
print "\nShowing data:\n"
for i in facts:
	print i + "."
	PRO ?->i.
	
print "Bells (Inequality) Theorem, for disagree1\n"

print "\nDisagree1: "
x=PRO ?-'disagree1'('A').
for i in x:
    print i


print "\nDisagree2: "
x=PRO ?-'disagree2'('A').
for i in x:
    print i

print "\nDisagree3: "
x=PRO ?-'disagree3'('A').
for i in x:
    print i
