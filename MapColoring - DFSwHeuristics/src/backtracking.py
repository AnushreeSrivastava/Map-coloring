
# ----------------------------------------------------
# Readme
# To run the program using test case:
#
# 1. Comment out the original test case
# 2. Put n, k, G anywhere in the region AFTER "start_time = time.time()" and BEFORE "def build():", as global variables.
# 3. Run the program, and output will be printed automatically.

# Note: the variable name for the # of variables MUST be "n"
# the variable name for the # of colors MUST be "k"
# and the variable name for the adjacency list MUST be "G"
# ------------------------------------------------------


import networkx as nx
import matplotlib.pyplot as plt
import time
import sys
# the start time
start_time = time.time()

# --------------------------------------
# Australia states mapping
#Constraints adjecency list
# (1,'SA'),(2,'WA'),(3,'NT'),(4,'Q'),(5,'NSW'),(6,'V')
#G= [[1,2,3,4,5,6],[2,1,3],[3,2,1,4],[4,1,3,5],[5,1,4,6],[6,1,5]]

# USA State mapping
# ['CA=1', 'AZ=2', 'NV=3', 'OR=4', 'WA=5', 'ID=6', 'UT=7', 'MT=8', 'WY=9', 'CO=10', 'NM=11', 'OK=12', 'TX=13', 'NE=14', 'KS=15', 'SD=16', 'ND=17',
#  'AR=18', 'LA=19', 'MO=20', 'IA=21', 'MN=22', 'MS=23', 'TN=24', 'IL=25', 'KY=26', 'WI=27', 'AL=28', 'IN=29', 'MI=30', 'FL=31', 'GA=32', 'VA=33', 'NC=34',
#  'OH=35', 'WV=36', 'SC=37', 'MD=38', 'DC=39', 'PA=40', 'DE=41', 'NY=42', 'NJ=43', 'VT=44', 'MA=45', 'CT=46', 'NH=47', 'ME=48', 'RI=49']

G = [[1,2,3,4],[2,1,3,7,11],[3,1,2,4,6,7],[4,3,1,5,6],[5,4,6],[6,5,4,3,7,9,8],[7,2,3,6,9,10],[8,6,9,16,17],
     [9,8,6,7,10,14,16],[10,9,7,11,12,14,15],[11,2,10,12,13],[12,13,11,10,15,20,18],[13,11,12,18,19],
     [14,9,10,15,20,21,16],[15,14,10,12,20],[16,17,8,9,14,21,22],[17,8,16,22],[18,12,13,19,23,24,20],[19,13,18,23],
     [20,21,14,15,12,18,24,26,25],[21,22,16,14,20,25,27],[22,17,16,21,27],[23,18,19,28,24],
     [24,26,20,18,23,28,32,34,33,26],[25,27,21,20,26,29],[26,29,25,20,24,33,35,36],[27,22,21,25,30],[28,23,24,32,31],
     [29,30,25,26,35],[30,27,29,35],[31,28,32],[32,31,28,24,34,37],[33,24,26,36,38,39,34],[34,37,32,24,33],
     [35,30,29,26,36,40],[36,35,26,33,38,40],[37,32,34],[38,39,33,36,40,41],[39,33,38],[40,35,36,38,41,43,42],
     [41,38,40,43],[42,40,43,46,45,44],[43,41,40,42],[44,42,45,47],[45,49,46,42,44,47],[46,42,45,49],[47,44,45,48]
     ,[48,47],[49,45,46]]
# #number of variables
n = 49
# Assign some random maximum chromatic number(colours)
k = 10
# ----------------------------------------


# colours
colors = []
#build the adjacency matrix
adjacency = []
#mrv list for each variable
mrv = []
legal_value = []
#degree heuristic
degree = []
# assigned variable list (0: unassigned; 1: assigned)
assign = []
#solution
solution = []
#record the search time
search = 0


def CreateGraph():
	G = nx.Graph()
	f = open(r'''..\USA.txt''')
	n = int(f.readline())
	for i in range(n):
		graph_edge_list = f.readline().split()
		G.add_edge(graph_edge_list[0], graph_edge_list[1])
	return G


def DrawGraph(G,col_val):
    pos = nx.spring_layout(G)
    col_val.sort(key=lambda x: x[0])
    values = [col[1] for col in col_val]
    nx.draw(G, pos, with_labels = True,node_size= 500, node_color = values, edge_color = 'black' ,width = 1, alpha = .7)  #with_labels=true is to show the node number in the output graph

E = CreateGraph()

# initialize colors, assign list, and build adjacency list
def build():
    i = 0
    while i < k:
        colors.append(i + 1)
        i = i + 1
    i = 0
    j = 0
    while i < n:
        legal_value.append(tuple(colors))
        mrv.append(k)
        assign.append(0)
        a_list = []
        while j < n:
            a_list.append(0)
            j = j + 1
        adjacency.append(a_list)
        j = 0
        i = i + 1
    i = 0
    j = 0
    #build adjacency by G
    while i < len(G):
        #initialize degree heuristic
        degree.append(len(G[i]) - 1)
        a_g = G[i]  #the single list inside G
        v1 = (a_g[0])
        while j < len(a_g):
            #note: the adjacency matrix is symmetry about diagonal
            adjacency[v1 - 1][int(G[i][j]) - 1] = 1
            adjacency[int(G[i][j]) - 1][v1 - 1] = 1
            j = j + 1
        j = 0
        i = i + 1

#backtracnking search
def solve():
    global search
    #establish the mrv list during each recursion
    #we have solution, and we want solution -- > mrv
    # func returns list of current legal values for each node
    legal = update_mrv()
    #print "MRV list is: ", mrv
    # check if assignment is completed
    #print "the mrv list is: ", mrv
    complete = True
    for item in assign:
        if item == 0:
            complete = False
    # if all variables have been assigned with its domain and no conflict
    if complete:
        #print "the # of searches is: ", search
        DrawGraph(E, solution)
        plt.show()
        print("Solution is:",solution)
        print("--- %s seconds ---" % (time.time() - start_time))
        sys.exit()
    temp_sol = []
    # ------------------------------------------------------------------------- normal backtracking search
    #select the next unassigned variable
    #var = select_var()
    #select the next unassigned variable by MRV
    var = select_by_mrv()
    # -------------------------------------------------------------------------- MRV + degree heuristic
    #print "variable is: ", var
    #print "solution is: ", solution
    # we have selected variable. Order the colour value for that variable
    # apply least constraining value
    lcv(var,legal)
    # -------------------------------------------------------------------------- least constraining value
    color = 0
    while color < k:
        safe = True
        current_color = colors[color]
        check = 0
        #check if it is safe(i.e., check the adjacent vertices of var to see if they share a color)
        while check < n:
            #if unsafe
            if var != check and adjacency[var][check] == 1 and (check + 1, current_color) in solution:
                safe = False
            check = check + 1
        # if safe
        if safe:
            #assign the current_color to var and update the solution
            remove = 0
            while remove < len(solution):
                if solution[remove][0] == var + 1:
                    solution.remove(solution[remove])
                remove = remove + 1
            mrv[var] = float('inf')
            solution.append((var + 1, current_color))
            #print "solution is: ", solution
            temp_sol.append((var + 1, current_color))
            assign[var] = 1
            #print "the assign list is: ", assign
            #depth-first search
            search = search + 1
            solve()
        search = search + 1
        color = color + 1
    #restore the solution list
    i = 0
    while i < len(temp_sol):
        if temp_sol[i] in solution:
            solution.remove(temp_sol[i])
            assign[temp_sol[i][0] - 1] = 0
        i = i + 1
    search = search + 1


def failure():
    #print "the # of searches is: ", search
    print("Solution is:",[])
    print("--- %s seconds ---" % (time.time() - start_time))

def update_mrv():
    global mrv
    #refresh mrv list
    item = 0
    temp_mrv = []
    while item < n:
        temp_mrv.append(k)
        item = item + 1
    mrv = temp_mrv
    values = list(legal_value)
    i = 0
    j = 0
    while i < len(solution):
        value = solution[i][0]
        values[value - 1] = (0,0)
        color = solution[i][1]
        mrv[value - 1] = float('inf')
        while j < n:
            if value - 1 != j and adjacency[value - 1][j] == 1 and color in values[j]:
                # remove current color from the legal_value[] for adjacent vertices
                values[j] = tuple([item for item in values[j] if item != color])
                mrv[j] = len(values[j])
            j = j + 1
        j = 0
        i = i + 1
    return values

def select_by_mrv():
    smallest = min(mrv)
    mins = [index for index, item in enumerate(mrv) if item == smallest]
    i = 0
    high_degree = degree[mins[0]]
    var_index = mins[0]
    while i < len(mins):
        if degree[mins[i]] > high_degree:
            high_degree = degree[mins[i]]
            var_index = mins[i]
        i = i + 1
    return var_index
    #-------------------------------------------------------- backtracking + mrv
    #return mrv.index(min(mrv))

#apply least constraining value heuristic
def lcv(variable,legal):
    global colors
    # initialize colors
    colors = []
    i = 0
    while i < k:
        colors.append(i + 1)
        i = i + 1
    #now we have: colors; legal values for each node; the variable to be assigned a color
    #if mrv inf, then that node has been assigned to a domain
    #the goal: order the color in colors for the one variable
    #find the adjacent nodes
    constraint = 0
    constraints = []
    adj = []
    i = 1
    while i < len(G[variable]):
        adj.append(G[variable][i] - 1)
        i = i + 1
    #get the list of unassigned adjacent nodes
    unassigned_adj = [item for item in adj if mrv[item] != float('inf')]
    i = 0
    j = 0
    while i < k:
        while j < len(unassigned_adj):
            if colors[i] in legal[unassigned_adj[j]]:
                constraint = constraint + 1
            j = j + 1
        constraints.append(constraint)
        constraint = 0
        j = 0
        i = i + 1
    #now we have colors and constraint order
    #sort the constraints
    sort_constraints = sorted(constraints)
    i = 0
    while i < len(sort_constraints):
        index = constraints.index(sort_constraints[i])
        colors[i] = index + 1
        constraints[index] = -1
        i = i + 1

def select_var():
   i = 0
   while i < len(assign):
       if assign[i] == 0:
           return i
       i = i + 1


build()
solve()
failure()

