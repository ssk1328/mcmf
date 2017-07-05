#!/usr/bin/python

import os

p_values  = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19]

for p in p_values:

	filename = os.getcwd()+"/data/"+"qap_data_pg"+ str(p) + ".txt"
#	filename = "qap_data_pg"+ str(p) + ".txt"
	system_cmd = "python qap_pg.py " + str(p) + " -> " + filename 
	print system_cmd
	os.system(system_cmd)

print " "
print "Input data for Quadratic Assignment Generated stored in /data"
print " "

os.system('g++ sa_qap_mandar.cpp')

for p in p_values:
	os.system("./a.out " + str(p))

print "All results of qap solver stored in /results directory"


print " "
print "Python script exits with no errors"
print " "
