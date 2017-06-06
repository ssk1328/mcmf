from gurobipy import *

import math
import sys
import copy

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


## This is the inflow and outflow at source and destination respectively for all comoodities
## This represents how many parts the packet can be broken into
pack_lenght = 1;

## This is the fixed capacity for all arcs
## This has to be changed to get a feasible soluton usually
capacity_const = 2;

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
    2: [8, 4, 7, 1, 5, 2, 0, 6, 3] ,
    3: [13, 1, 11, 2, 14, 0, 10, 12, 9, 5, 8, 6, 15, 4, 7, 3] 
}

placement = placementAll[p]

## This means that at the ith location in mesh we put up the placement[i]th processor
## Example here processor 8 is placed at 0th location in mesh
## Example here processor 4 is placed at 1st location in mesh

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
for i in range(len(dependency)):
	for j in range(len(dependency[i])):
		commodities.append('s'+ str(i) +'d'+ str(dependency[i][j]))

print "commodities:"
print commodities

nodes = [] # start with empty list for nodes

for i in range(len(placement)):
    string = 'p'+str(placement[i])+'m'+str(i)
    nodes.append(string)

#   for i in range(len(dependency_in)):
#	  nodes.append('p'+str(i))

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

		n_index_p = j.index('p')
		n_index_m = j.index('m')

		p_num = j[n_index_p:n_index_m]

		if   p_num == 'p'+str(src):
			inflow[(i, j)] = pack_lenght 
		elif p_num == 'p'+str(dest):
			inflow[(i, j)] = -pack_lenght
		else :
			inflow[(i, j)] = 0 

print "Inflow: "
print inflow
print "Lenght of inflow dictionary: "
print len(inflow)

print " "
print " "
print " "

print "numMeshnodes is %d"%numMeshnodes
print "meshEdge is %d"%meshEdge

arc = []
for i in range(numMeshnodes):
	if i >= meshEdge : #up
		arc.append(( 'p'+str(placement[i])+'m'+str(i), 'p'+ str(placement[i-meshEdge]) +'m'+str(i-meshEdge)))
	if i%meshEdge > 0 : #left
		arc.append(( 'p'+str(placement[i])+'m'+str(i), 'p'+ str(placement[i-1]) +'m'+str(i-1)))
	if i < numMeshnodes - meshEdge :  # down
		arc.append(( 'p'+str(placement[i])+'m'+str(i), 'p'+ str(placement[i+meshEdge]) +'m'+str(i+meshEdge)))
	if i%meshEdge < meshEdge-1 :  # right
		arc.append(( 'p'+str(placement[i])+'m'+str(i), 'p'+ str(placement[i+1]) +'m'+str(i+1)))


print arc
print "Length of Arc: ", 
print len(arc)

multi_dict = {}



################################
################################
## Change Capacities here


for i in arc:
	multi_dict[i] =  capacity_const	# Change to get a feasible solution

arcs, capacity = multidict(multi_dict)


print "All arcs after: "
print type(arcs)
print arcs

# print "All capacities after: "
# print capacity

cost = {}

for i in commodities:
	for j in arc:
#		print j
		j_list = list(j)
#		print j_list
		#j_tup = j_list.insert(0,i)
		j_tup = [i]+j_list
#		print i
#		print j_tup
		tup = tuple(j_tup)
		cost[tup] = 1

print ""
print ""
print ""

# print "Cost: "
# print cost

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

    print "Solution:"
    print "Solution type:",
    print type(solution)
    print len(solution)

arc_solution = copy.copy(solution)

arc_list = []
# add info about convention in ths data structure

def check_flow ( commodity ):
	minimum_flow = 9999 # supposed to be infinity

	for i,j in arcs:
		if (arc_solution[commodity, i, j] > 0) & (arc_solution[commodity, i, j]  < minimum_flow) :
			minimum_flow = arc_solution[commodity, i, j]

	if minimum_flow == 9999:	# Means no non-zero flow was found
		minimum_flow = 0

	return minimum_flow

def get_src_dst (commodity) :
	## Returns source and destination nodes for a commodity

	index_s = commodity.index('s') + 1
	index_d = commodity.index('d')
	index_d1 = commodity.index('d') + 1
	index_end = len(commodity)

	src = int(commodity[index_s:index_d])
	dest = int(commodity[index_d1:index_end])

#	print "In get_src_dst function:"
#	print "For commodity:", commodity

#	print "Source and Destination processor ids are respectively"

	for j in nodes:
		n_index_p = j.index('p')+1
		n_index_m = j.index('m')

		p_num = int(j[n_index_p:n_index_m])

#		print "Nodes is:", j
#		print "p_num is:", p_num
		
		if src == p_num :
			src_nd = j

		if dest == p_num :
			dest_nd = j


	return src_nd , dest_nd

def get_next_node (commodity, previous_node):

#	print " "
#	print "Inside get_next_node function"
	min_val = 9999

#	print "previous_node is ", previous_node

	for x,y in arcs:
		if (x==previous_node):
#			print 'x is', x
#			print 'y is', y
			sol_tmp = arc_solution[commodity, x, y]
#			print "sol_temp", sol_tmp 
#			print "(sol_tmp > 0) :" , (sol_tmp > 0) 
#			print "(sol_tmp < min_val)" , (sol_tmp < min_val)
			if  (sol_tmp > 0) & (sol_tmp < min_val) :
#				print "Value of next node", y
				min_val = arc_solution[commodity, x, y]
				min_dst = y

#	print "min_dst before return of function", min_dst
	return min_dst


print ""
print ""
print "Arc solutions start from here"

for h in commodities:
#	print "Addition of arc info for commodity:", h
	src_node, dest_node = get_src_dst(h)

#	print "Source Node: ", src_node
#	print "Destination Node: ", dest_node

	while check_flow(h)>0 :
		min_flow = check_flow(h)
#		print "Min Flow Value is:" , min_flow
		path_list = []
		path_list.append(src_node)
		
		prev_node = src_node
		next_node = src_node

		while (next_node != dest_node ):
#			print "Prev Node is:" , prev_node
			next_node = get_next_node(h, prev_node)
#			print "Next node is;" , next_node
			path_list.append(next_node)
#			print path_list
			arc_solution[h, prev_node, next_node] = arc_solution[h, prev_node, next_node]  - min_flow 

			prev_node = next_node

#		print "Outside while now"

		path_length = len(path_list)
		path_source = path_list[0]
		path_dest = path_list[path_length-1]

		arc_list.append([ path_source, path_dest, min_flow, path_list ])

#	print "Commodity done:", h
#	print ""



print "Arc_list generated:"

for j in range(len(arc_list)):
	print "arc_id", j ,
	print ":",
	print arc_list[j]


print "Lets populate data structure at source:"


print ""
print "**********************************************"
print "PACKET SPECIFICATION AT INPUT NODES"
print "**********************************************"
for j in nodes:
	print ""
	print "Input packet specifications at node:", j

	for arc_id in range (len(arc_list)):
		if arc_list[arc_id][0]== j :
			print "For Destination: ", arc_list[arc_id][1] ,
			print "arc_id is", arc_id, 
			print "count is", arc_list[arc_id][2]

## ***************************************************** ##
## FILE WRITING STARTS HERE
## ***************************************************** ##

filename = "Lookup.bsv"
f = open(filename, 'w')

f.write("import MemTypes::*;\n")
f.write("import ProcTypes::*;\n")
f.write("\n")
f.write("// Python generated code which returns arc_id for each pair of source and destination of packets \n")
f.write("\n")
f.write("function NoCArcId lookupNoCArcId(ProcID srcProcId, ProcID destProcID);\n")

for j in nodes:

	index0 = j.index('p')+1
	index1 = j.index('m')
	pnum = j[index0:index1]

	f.write("  if (srcProcId == " + pnum + ") begin\n")	

	for arc_id in range (len(arc_list)):
		if arc_list[arc_id][0]== j :
			dest_node = arc_list[arc_id][1]

			index_0 = dest_node.index('p')+1
			index_1 = dest_node.index('m')
			pnum_0 = dest_node[index_0:index_1]

			ret_arc_id = str(arc_id)

			f.write("    if(destProcID == "+ pnum_0 +") return " + ret_arc_id + ";\n")
#	f.write("    else return 0;\n")
	f.write("  end\n")

f.write("  else return 0;\n")

f.write("endfunction\n")


print ""
print "**********************************************"
print "PACKET ROUTING AT INTERMEDIATE NODES"
print "**********************************************"

f.write("\n")
f.write("\n")

f.write("// Lookup function for destination node at each mesh node corresponding to the arc id and source mesh \n")
f.write("function String lookupArcDest ( NoCAddr2D thisRowAddr, NoCAddr2D thisColAddr, NoCArcId arc_index); \n")


f.write ("endfunction \n")


for j in nodes:

	print ""
	print "Packet routing direction at node:", j

	index0 = j.index('m')+1
	index1 = len(j)
	mesh_num = int(j[index0:index1])

	mesh_row = int(mesh_num/meshEdge)
	mesh_col = mesh_num%meshEdge

	f.write("  if ((thisRowAddr == " + str(mesh_row) + ") & (thisColAddr == " + str(mesh_col) + ")) begin \n")

	for arc_id in range (len(arc_list)):
		arc_path = arc_list[arc_id][3]
		len_arc_path = len(arc_path)
		for i in range(len_arc_path):

			if arc_path[i]==j:


				if i == len_arc_path-1 :
					direction = 'H'
				else :
					current_node_in_path = arc_path[i]
					next_node_in_path = arc_path[i+1]
					


					curr_index_m = current_node_in_path.index('m')
					curr_index_last = len(current_node_in_path)

					next_index_m = next_node_in_path.index('m')
					next_index_last = len(next_node_in_path)

					current_node_mesh = int(current_node_in_path[curr_index_m+1:curr_index_last])
					next_node_mesh = int(next_node_in_path[next_index_m+1:next_index_last])

					if(next_node_mesh == current_node_mesh +1 ):
						direction = 'E'
					elif (next_node_mesh == current_node_mesh - 1 ):
						direction = 'W'
					elif ((next_node_mesh/3) == (current_node_mesh/3)+1):
						direction = 'S'
					elif ((next_node_mesh/3) == (current_node_mesh/3)-1):
						direction = 'N'

				print "For arc_id: ", arc_id ,
				print "direction is", direction  
				f.write("    if (arc_index == "+ str(arc_id)+") return \"" + direction+"\"  ;\n")
	f.write("  end \n")
f.write("endfunction\n")


f.write("\n")
f.write("\n")
f.write("// This is device placement generated from the qap solver used before hardcoded in mcmf.py file right now  \n")
f.write("function MeshID lookupNoCAddr(ProcID currProcId); \n")
f.write("  case (currProcId)\n")

for i in range(numCores):
	for j in range(len(placement)):
		if placement[j] == i :
			f.write("    "+ str(i) + ": return " + str(j) + "; \n")


f.write("  endcase \n")
f.write("endfunction \n")
f.close()




