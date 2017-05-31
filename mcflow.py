from gurobipy import *

import math
import sys

p = 2	# Size of pg, this was specified from command line
print "Size of pg, p is %d"%p 

numPGnodes = p*p +p +1
numCores = numPGnodes
print "Number of cores in pg is %d " %numCores
#Decide Mesh Size 
meshEdge = 1
numMeshnodes = meshEdge * meshEdge
while (numPGnodes > numMeshnodes):
    meshEdge += 1
    numMeshnodes = meshEdge *meshEdge
print "numMeshnodes is %d"%numMeshnodes
print "meshEdge is %d"%meshEdge


incidenceAll = {2 : [0,1,3], 
                3 : [0,1,3,9],               
                4 : [0,1,4,14,16],           
                5 : [0,1,3,8,12,18],         
                7 : [0,1,3,13,32,36,43,52],  
                8 : [0,1,3,7,15,31,36,54,63]}

incidence = incidenceAll[p] 

#print "Incidence:",
#print incidence 


###############################################################################
## Add code to read placement routing here, this is using simulated annealing 
## based quadratic assignment problem solver
## Add code to read this from file later, add code to print this in a file in qap solver cpp file later

placementAll = {
    2: [8, 4, 7, 1, 5, 2, 0, 6, 3]
}

placement = placementAll[p]

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

print "Dependency:"
## This list basically means ith nodes is connected to pg nodes mentioned in ith row
for i in range(len(dependency)):
	print dependency[i] 



dependency_out = []
# Inserting the connections between Point Node i and all the Line nodes it is connected to, except itself 
for i in range(numCores):
    dependency_out.append([])
    for j in incidence:  
        if (i != (i+ j)%numCores ):
            dependency_out[i].append((j+i)%numCores) 

dependency_in = []
# Inserting the connections between Line node i and all the Point nodes it is connected to, except itself
for i in range(numCores):
    dependency_in.append([])
    for j in incidence:  
        if (i != (i - j)% numCores ):
            dependency_in[i].append((i - j)% numCores)

print "Data sent at t=0, x0, x1, ...: "
print "Dependency_out: "
print dependency_out 

print "Dependency sent after t = t1, y0part0, y1part0, ..... ",
print "Dependency_in: "
print dependency_in 


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

print "Communication traffic also flow matirx:"
print commTraffic


## From here on we tackle the problem at time t=t1 and hence use the dependency_in from above
## For time t=0, use dependency_out from abbove

commodities = [] # start with empty list for commodities
for i in range(len(dependency_in)):
	for j in range(len(dependency_in[i])):
		commodities.append('s'+ str(i) +'d'+ str(dependency_in[i][j]))

print "commodities:"
print commodities

nodes = [] # start with empty list for nodes
for i in range(len(dependency_in)):
	nodes.append('p'+str(i))

print "nodes:"
print nodes

inflow = {} # start with empty dictionary for inflow specification

for i in commodities:

	index_s = i.index('s') + 1
	index_d = i.index('d')
	index_d1 = i.index('d') + 1
	index_end = len(i)

	src = int(i[index_s:index_d])
	dest = int(i[index_d1:index_end])

	for j in nodes:
		if j == 'p'+str(src):
			inflow[(i, j)] = 8 
		elif j == 'p'+str(dest):
			inflow[(i, j)] = -8 
		else :
			inflow[(i, j)] = 0 

print inflow


print " "
print " "
print " "

print "numMeshnodes is %d"%numMeshnodes
print "meshEdge is %d"%meshEdge

arc = []
for i in range(numMeshnodes):
	if i >= meshEdge : #up
		arc.append(( 'p'+str(i), 'p'+str(i-meshEdge)))
	if i%meshEdge > 0 : #left
		arc.append(( 'p'+str(i), 'p'+str(i-1)))
	if i < numMeshnodes - meshEdge :  # down
		arc.append(( 'p'+str(i), 'p'+str(i+meshEdge)))
	if i%meshEdge < meshEdge-1 :  # right
		arc.append(( 'p'+str(i), 'p'+str(i+1)))


print arc
print "Length of Arc: ", 
print len(arc)

multi_dict = {}



################################
################################
## Change Capacities here


for i in arc:
	multi_dict[i] = 160	# Change to get a feasible solution

arcs, capacity = multidict(multi_dict)


print "All arcs after: "
print arcs

print "All capacities after: "
print capacity

cost = {}

for i in commodities:
	for j in arc:
		print j
		j_list = list(j)
		print j_list
		#j_tup = j_list.insert(0,i)
		j_tup = [i]+j_list
		print i
		print j_tup
		tup = tuple(j_tup)
		cost[tup] = 1

print ""
print ""
print ""

print "Cost: "
print cost

m = Model('netflow')

# Create variables
flow = m.addVars(commodities, arcs, obj=cost, name="flow")

# Arc capacity constraints
m.addConstrs(
    (flow.sum('*',i,j) <= capacity[i,j] for i,j in arcs), "cap")

# Equivalent version using Python looping
# for i,j in arcs:
#   m.addConstr(sum(flow[h,i,j] for h in commodities) <= capacity[i,j],
#               "cap[%s,%s]" % (i, j))


# Flow conservation constraints
m.addConstrs(
    (flow.sum(h,'*',j) + inflow[h,j] == flow.sum(h,j,'*')
    for h in commodities for j in nodes), "node")
# Alternate version:
# m.addConstrs(
#   (quicksum(flow[h,i,j] for i,j in arcs.select('*',j)) + inflow[h,j] ==
#     quicksum(flow[h,j,k] for j,k in arcs.select(j,'*'))
#     for h in commodities for j in nodes), "node")

# Compute optimal solution
m.optimize()

# Print solution
if m.status == GRB.Status.OPTIMAL:
    solution = m.getAttr('x', flow)
    for h in commodities:
        print('\nOptimal flows for %s:' % h)
        for i,j in arcs:
            if solution[h,i,j] > 0:
                print('%s -> %s: %g' % (i, j, solution[h,i,j]))

