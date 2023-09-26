import os
f=open("data.csv", "r")
for i in f:
	s=i.split(",")
	os.system("touch " +s[2]+".csv")
f.close()

	
