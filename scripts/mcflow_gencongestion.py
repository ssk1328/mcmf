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
		placement_list = [x - 1 for x in placement_list]
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

#	return dependency_in

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

def get_commodity_src_dst (commodity) :
	## Returns source and destination nodes for a commodity

	index_s = commodity.index('s') + 1
	index_d = commodity.index('d')
	index_d1 = commodity.index('d') + 1
	index_end = len(commodity)

	src = int(commodity[index_s:index_d])
	dest = int(commodity[index_d1:index_end])

	return src , dest

def get_node_proc_mesh (node):
	index_p = node.index('p') + 1
	index_m = node.index('m')
	index_m1 = node.index('m') + 1
	index_end = len(node)
	proc_num = int ( node[index_p :index_m  ] )
	mesh_num = int ( node[index_m1:index_end] )
	return proc_num, mesh_num


def init_nodes():
	nodes = [] # start with empty list for nodes

	for i in range(len(placement)):
		string = 'p'+str(i)+'m'+str(placement[i])
		nodes.append(string)
	return nodes


def init_inflow():
	inflow = {} # start with empty dictionary for inflow specification

	for i in commodities:
		src , dest = get_commodity_src_dst(i)
		for j in nodes:
			p_num , m_num  = get_node_proc_mesh (j)
			if   p_num == src:
				inflow[(i, j)] = PACK_LENGTH 
			elif p_num == dest:
				inflow[(i, j)] = -PACK_LENGTH
			else :
				inflow[(i, j)] = 0 
	return inflow

def get_node(mesh_num):
	"Outputs the node string for a given location in mesh, using the placement list"
	proc_num = placement.index(mesh_num)
	return 'p'+str(proc_num)+'m'+str(mesh_num) 

def init_arc_list():
	arc = []
	for i in range(numMeshnodes):
		if i >= meshEdge : #up
			arc.append( ( get_node( i ) , get_node (i-meshEdge) ) )
		if i%meshEdge > 0 : #left
			arc.append( ( get_node( i ) , get_node (i-1) ) )
		if i < numMeshnodes - meshEdge :  # down
			arc.append( ( get_node( i ) , get_node (i+meshEdge) ) )
		if i%meshEdge < meshEdge-1 :  # right
			arc.append( ( get_node( i ) , get_node (i+1) ) )
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

# ****************************************************************************************************************** #
# ------------------------------------------------------------------------------------------------------------------ #
# 
# MAIN SCRIPT STARTS HERE 
# 
# ------------------------------------------------------------------------------------------------------------------ #
# ****************************************************************************************************************** #


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

# p = 2

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
CAPACITY_CONST = 215;

MAX = sys.maxsize

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
# print "placement", placement
## This means that ith value in list is location of ith processor

## Actual output from sa_qap is different 
## In the list generated, the ith value in the list is the position of ith processor in mesh

dependency = getDependencyList()	# This is the equvalent of data flow graph, here generated for the MatrixVector Application
commodities = init_commodity()		# Initiate list of commodity, data structure for lp, of the form 's2d4' source processor 2, destination 4
nodes = init_nodes()				# Initiate list of nodes, data structure for lp, of the form 'p2m4' processor 2 placed at mesh loc 4
inflow = init_inflow()				# Specify source and destination for each commodity
arc = init_arc_list()				# List of arc tuples generated from mesh network specification

multi_dict = {}
for i in arc:
	multi_dict[i] =  CAPACITY_CONST

arcs, capacity = multidict(multi_dict)	# Initiate arc and capacity data structures for lp 
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

#filename0 = "Optimize_Runtimes.txt"
#f0 = open(filename0, 'a')

# Print solution
if m.status == GRB.Status.OPTIMAL:
#	print " Runtime printed here:"
#	runtime = str(m.Runtime)
	solution = m.getAttr('x', flow)

#	f0.write( "Runtime for pg:" + str(p) + ", and numMeshnodes:" + str(numMeshnodes) + " is " + runtime + " in seconds \n" )
#    for h in commodities:
#        print('\nOptimal flows for %s:' % h)
#        for i,j in arcs:
#            if solution[h,i,j] > 0:
#                print('%s -> %s: %g' % (i, j, solution[h,i,j]))

#    print "Solution:"
#    print "Solution type:",
#    print type(solution)
#    print len(solution)

#	f0.close()
	
	congestion = {}
	
	for i,j in arcs :
		congestion[(i,j)] = 0

	for i,j in arcs :
		for h in commodities:
			congestion[(i,j)] = congestion[(i,j)] + solution[h,i,j]

	count_cong = 0
	val_cong = 0
	max_arc = 0 
	for i,j in arcs :
		count_cong = count_cong + 1
		val_cong = congestion[(i,j)] + val_cong
		if congestion[(i,j)] > max_arc:
			max_arc = congestion[(i,j)]

	avg_arc = val_cong/count_cong

	print "Average arc congestion is", avg_arc
	print "Max arc congestion is", max_arc


def get_src_dst (commodity) :
	## Returns source and destination nodes (in string form) for a commodity
	src , dest = get_commodity_src_dst(commodity)
	for j in nodes:
		p_num , m_num  = get_node_proc_mesh (j)
		if src == p_num :
			src_nd = j
		if dest == p_num :
			dest_nd = j
	return src_nd , dest_nd

def get_node_from_mesh(mesh_num):

	for i in range(len(placement)):
		if placement[i] == mesh_num:
			proc_num = i

	node_op = 'p' + str(proc_num) +'m' + str(mesh_num)
	return node_op


def xypath_gen(src_mesh_num, dest_mesh_num):
	pack = [src_mesh_num]

	while (src_mesh_num != dest_mesh_num):

		if(src_mesh_num%3 == dest_mesh_num%3):	# check if x is same

			if(src_mesh_num/3 == dest_mesh_num/3): # check if y is same
				pack.append(src_mesh_num)

			else:
				if(src_mesh_num/3 > dest_mesh_num/3):
					src_mesh_num = src_mesh_num-3
				elif(src_mesh_num/3 < dest_mesh_num/3):
					src_mesh_num = src_mesh_num+3
				pack.append(src_mesh_num)

		else:	
			if(src_mesh_num%3 > dest_mesh_num%3):
				src_mesh_num = src_mesh_num-1
			elif(src_mesh_num%3 < dest_mesh_num%3):
				src_mesh_num = src_mesh_num+1
			pack.append(src_mesh_num)
	
	return pack


def init_xy_list():

	arc_list = []
	# arc_list [3]  = ['p0m6', 'p4m4', 8.0, ['p0m6', 'p1m3', 'p7m0', 'p8m1', 'p4m4']]
	# arc_list[arc_id] = [ src_node, dest_node, count, path_list]

	for h in commodities:
		src_node, dest_node = get_src_dst(h)
		path_list = []
			
		src_pnum, src_mnum = get_node_proc_mesh(src_node)
		dest_pnum, dest_mnum = get_node_proc_mesh(dest_node)

		mesh_list = xypath_gen(src_mnum, dest_mnum)

		for i in mesh_list:
			path_list.append(get_node_from_mesh(i) )
		arc_list.append( [src_node, dest_node, PACK_LENGTH, path_list] )

	return arc_list


l0 = init_xy_list()

congestion_xy = {}

for path in l0:
#	print path
	arc_path = path[3]

	for i in range(len(arc_path)-1):
		sr = arc_path[i]
		ds = arc_path[i+1]
		if (sr,ds) not in congestion_xy.keys():
			congestion_xy[(sr,ds)] = 0
		else:			
			congestion_xy[(sr,ds)] = congestion_xy[(sr,ds)] + path[2]

# print congestion_xy

count_cong = 0
val_cong = 0
max_xy = 0

#print congestion_xy

for key in congestion_xy.keys():
	count_cong = count_cong + 1
	val_cong = congestion_xy[key] + val_cong
	if congestion_xy[key] > max_xy:
		max_xy = congestion_xy[key]

avg_xy = val_cong/count_cong

print "Average XY congestion is", avg_xy
print "Max XY Congestion is ", max_xy

