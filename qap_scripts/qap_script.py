#!/usr/bin/python

import os

p_values  = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16]

for p in p_values:

	filename = "qap_data_pg"+ str(p) + ".txt"
	system_cmd = "python qap_lp_algo.py " + str(p) + " -> " + filename 
	print system_cmd
	os.system(system_cmd)


os.system('g++ sa_qap_mandar.cpp')

for p in p_values:
	os.system("./a.out " + str(p))
