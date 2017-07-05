#!/usr/bin/python

import math
import sys

######### GETTING PG SIZE FROM COMMAND LINE ############
         
if len(sys.argv) >= 2:
    p = int(sys.argv[1])
    reportFileName = "report_lp_hungarian_fixedPG"+str(p)+".txt"
    if (p < 2 or p > 19):
        print "Size of PG has to be between 2 and 19\n"
        exit()
else : 
    print "Specify Size of PG to be evaluated with random mappings to be generated for mesh \n "
    exit()


######### NETWORK SIZE DEFINITION ############

#p = 3
numPGnodes = p*p +p +1
numCores = numPGnodes
numVariables = 2*numCores*numCores + 2*numCores

#Decide Mesh Size 
meshEdge = 1
numMeshnodes = meshEdge * meshEdge
while (numPGnodes > numMeshnodes):
    meshEdge += 1
    numMeshnodes = meshEdge *meshEdge
#print "numMeshnodes is %d"%numMeshnodes
#print "meshEdge is %d"%meshEdge

incidenceAll = {2  : [0,1,3], 
                3  : [0,1,3,9],               
                4  : [0,1,4,14,16],           
                5  : [0,1,3,8,12,18],         
                7  : [0,1,3,13,32,36,43,52],  
                8  : [0,1,3,7,15,31,36,54,63],
                9  : [0,1,3,9,27,49,56,61,77,81],
                11 : [0,1,3,12,20,34,38,81,88,94,104,109],
                13 : [0,1,3,16,23,28,42,76,82,86,119,137,154,175],
                16 : [0,1,3,7,15,31,63,90,116,127,136,181,194,204,233,238,255],
                17 : [0,1,3,30,37,50,55,76,98,117,129,133,157,189,199,222,293,299],
                19 : [0,1,19,28,96,118,151,153,176,202,240,254,290,296,300,307,337,361,366,369]

                }

incidence = incidenceAll[p] 
#print "Incidence:",
#print incidence 

###################

## Dependency generically means the nodes with which given node communicates. In matrix vector product, we 
## communicate only with the Nodes containing : Line Nodes of the given point node and the point nodes of the given 
## line node.
## Hence : 
## Dependency contains the list of nodes which need to be close to a node in Mesh (Basically list of Line Nodes 
## connected to Point Node and list of Point Nodes connected to Line Node, for a given node)

dependency = []
# Inserting the connections between Point Node i and all the Line nodes it is connected to, except itself 
for i in range(numCores):
    dependency.append([])
    for j in incidence:  
        if (i != (i+ j)%numCores ):
            dependency[i].append((j+i)%numCores) 

# Inserting the connections between Line node i and all the Point nodes it is connected to, except itself
for i in range(numCores):
    for j in incidence:  
        if (i != (i - j)% numCores ):
            dependency[i].append((i - j)% numCores)

#print "Dependency:",
#print dependency 

#Number of variables in the LP = 126
#xij -> 49 (0 to 48)
#yij -> 49 (49 to 97)
#xi  -> 7  (98 to 104)
#yi  -> 7  (112 to 118) 


#Setting up the commTraffic matrix
commTraffic = [[0] * numCores for i in range(numCores)]

for i in range(numCores):
    for j in dependency[i]:
        srclines = [(x+i)%numCores for x in incidence]
        destlines = [(x+j)%numCores for x in incidence]
        matchline = 0
        for a in srclines:
            done = 0 # to indicate whether matched or not
            for b in destlines:
                if a == b:
                    done =1
                    matchline = a #src and dest lines matched
                    break
            if done is 1:
                break
        commTraffic[i][matchline] += 1
        commTraffic[matchline][j] += 1


dist_matrix = [[None]*numMeshnodes]*numMeshnodes

print numMeshnodes
print ''

#print "FLOW COST MATRIX"
#print "BEGIN"

for i in range(numCores):
    commTraffic[i][i] = 0

for i in range(numMeshnodes):
    for j in range(numMeshnodes):
        if ((i<numCores) and (j<numCores)):
            print commTraffic[i][j],
        else :
            print "0" ,
    print ''

#print "END"

print ''

#print "DISTANCE COST MATRIX "
#print "BEGIN "

for i in range(numMeshnodes):
    for j in range(numMeshnodes):
        xi = i%meshEdge
        yi = (i/meshEdge)
        xj = (j%meshEdge)
        yj = (j/meshEdge)
        dist_matrix[i][j] = abs(xi-xj) + abs(yi-yj)
        print dist_matrix[i][j] , 
    print ''
#print "END"
