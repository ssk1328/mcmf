from gurobipy import *
import math
import sys
import copy

def read_placement_files () :
	placementAll = {}
	for p in p_values:
		fileobj = open("qap_scripts/qap_sol_pg"+ str(p) +".txt")
		file_string = fileobj.read()
		placement_list = map(int, file_string.split())
		placementAll[p] = placement_list
		fileobj.close()

	return placementAll

def getDependencyList():
	## This list basically means ith nodes is connected to pg nodes mentioned in the list dependency[i]
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

	return dependency
	#dependency_out = []
	# Inserting the connections between Point Node i and all the Line nodes it is connected to, except itself 
	#for i in range(numCores):
	#    dependency_out.append([])
	#    for j in incidence:  
	#        if (i != (i+ j)%numCores ):
	#            dependency_out[i].append((j+i)%numCores) 

	#dependency_in = []
	# Inserting the connections between Line node i and all the Point nodes it is connected to, except itself
	#for i in range(numCores):
	#    dependency_in.append([])
	#    for j in incidence:  
	#        if (i != (i - j)% numCores ):
	#            dependency_in[i].append((i - j)% numCores)

	# print "Data sent at t=0, x0, x1, ...: "
	# print "Dependency_out: "
	# print dependency_out 

	# print "Dependency sent after t = t1, y0part0, y1part0, ..... ",
	# print "Dependency_in: "
	# print dependency_in 


def init_commodity():
	commodities = [] # start with empty list for commodities
	for i in range(len(dependency)):
		for j in range(len(dependency[i])):
			commodities.append('s'+ str(i) +'d'+ str(dependency[i][j]))

	return commodities

def init_nodes():
	nodes = [] # start with empty list for nodes

	for i in range(len(placement)):
		string = 'p'+str(placement[i])+'m'+str(i)
		nodes.append(string)
	return nodes

def init_inflow():
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
				inflow[(i, j)] = PACK_LENGTH 
			elif p_num == 'p'+str(dest):
				inflow[(i, j)] = -PACK_LENGTH
			else :
				inflow[(i, j)] = 0 

	return inflow

def init_arc_list():
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

	return arc

def init_cost():
	cost = {}
	for i in commodities:
		for j in arc:
			j_list = list(j)
			j_tup = [i]+j_list
			tup = tuple(j_tup)
			cost[tup] = 1
	return cost

# ------------------------------------------------------------------------------------------------------------------ #
# MAIN SCRIPT STARTS HERE 
# ------------------------------------------------------------------------------------------------------------------ #

p = 2	# Size of pg, this was specified from command line
p_values  = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19]

numPGnodes = p*p +p +1
numCores = numPGnodes
# Decide Mesh Size here, largest perfect square number greater than numCores
meshEdge = 1
numMeshnodes = meshEdge * meshEdge
while (numPGnodes > numMeshnodes):
    meshEdge += 1
    numMeshnodes = meshEdge *meshEdge


## This is the inflow and outflow at source and destination respectively for all comoodities
## This represents how many parts the packet can be broken into
PACK_LENGTH = 8;

## This is the fixed capacity for all arcs
## This has to be changed to get a feasible soluton usually
CAPACITY_CONST = 16;

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

###############################################################################
placementAll = read_placement_files()
placement = placementAll[p]
print "placement", placement
## 2: [8, 4, 7, 1, 5, 2, 0, 6, 3] , TODO: Fix this
placement = [8, 4, 7, 1, 5, 2, 0, 6, 3] 
## This means that at the ith location in mesh we put up the placement[i]th processor
## Example here processor 8 is placed at 0th location in mesh
## Example here processor 4 is placed at 1st location in mesh

## Actual output from sa_qap is different 
## In the list generated, the ith value in the list is the position of ith processor in mesh


dependency = getDependencyList()
commodities = init_commodity()
nodes = init_nodes()
inflow = init_inflow()
arc = init_arc_list()

multi_dict = {}
for i in arc:
	multi_dict[i] =  CAPACITY_CONST

arcs, capacity = multidict(multi_dict)
cost = init_cost()

m = Model('netflow')

# Create variables
flow = m.addVars(commodities, arcs, obj=cost, name="flow")

# Arc capacity constraints
m.addConstrs(
    (flow.sum('*',i,j) <= capacity[i,j] for i,j in arcs), "cap")

# Flow conservation constraints
m.addConstrs(
    (flow.sum(h,'*',j) + inflow[h,j] == flow.sum(h,j,'*')
    for h in commodities for j in nodes), "node")

# Dont print log to console
m.Params.LogToConsole = 0

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




