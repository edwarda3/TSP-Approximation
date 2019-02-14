import os
import sys
import argparse
import math

#We can assume a complete graph for this program.
#Takes input from a file as described in readme.txt
# @param filepath: The path to the textfile which holds the graph information
# @return graphs: A list of graphs, with the number of graphs being equivalent to the <test cases> in the text file.
#				  Each graph is a list of vertices in the form (x,y). Because a complete graph is assumed, no edges are stored here.
def getGraphFromFile(filepath):
	print("Reading file... ", end = '')
	try:
		myfile = open(filepath,'r')
	except IOError:
		print("Failed to read file!")
		sys.exit()
	with myfile:
		data = myfile.read()
	print("Done!")
	data = data.strip()

	info = data.split('\n')
	graph = [0]*len(info)
	for i in range(len(info)):
		info[i] = info[i].strip()
		c = info[i].split()
		if(c[1].isdigit() and c[2].isdigit()):
			graph[i] = (int(c[1]),int(c[2]))
	return graph

#A representation of the graph to print out.
# @param graph: The graph to print
# @param n: The number, or index of this graph according to the graphs array.
# @return s: A string which holds the representation
def grepr(graph):
	s = ""
	for v in range(len(graph)):
		s+="\t"+str(v)+": "+str(graph[v]) +"\n"
	return s

#A representation of the MST to print out.
# @param weight: Total weight of the MST
# @param tree: The tree of the MST, listed as the edges which make up the tree. Each edge is (u,v) = ((x1,y1),(x2,y2))
# @return s: A string which holds the representation
def mstrepr(weight,tree):
	s=""
	s+="Minimum Spanning Tree:\n"
	s+="Weight: "+str(weight)+"\n"
	s+="Tree edges:\n"
	for edge in tree:
		s+="\t"+str(edge)+"\n"
	return s

#Returns the euclidian distance between two points rounded to the nearest integer.
# @param v1: The first point as (x,y)
# @param v2: The second point as (x,y)
# @return value: The distance between v1, v2 to the nearest integer.
def getdist(v1, v2):
	(x1,y1) = v1
	(x2,y2) = v2
	return round(math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2)))

#Checks to see if all vertices are part of the same component.
#This acts as a premature end, because in a connected graph, most edges are going to be useless. (time savings)
# @param sets: The dictionary which contains information about the connected components of the tree.
# @return: True if there is only a single connected component (a full tree). False otherwise.
def isDone(sets):
	val = None
	for key in sets:
		if(val == None):
			val = sets[key]
		else:
			if(not val == sets[key]):
				return False
	return True

#Finds the MST of a complete graph given the euclidian points as vertices.
#Use Kruskal's Algorithm: https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
# @param g: A graph representation where we are given points as vertices.
# @return weight: The total weight of the MST.
# @return tree: A list of edges which make up the MST.
def findMST(g):
	# Make a list of all edges, and store them as (dist, v1, v2), and sort them
	edges = []
	for v1i in range(len(g)):
		for v2i in range(v1i+1,len(g)):
			edges.append((getdist(g[v1i],g[v2i]),v1i,v2i))
	edges.sort()

	# Set up a dictionary "sets", which assigns a value to each vertex.
	# This value will become representative of the connected component that each vertex belongs to.
	# Each vertex will have a unique value to start (as there are no edges yet).
	sets = {}
	for v in range(len(g)):
		sets[v] = v
	tree = []
	weight = 0

	# Traverse through the sorted list of edges (lowest first)
	# At each edge, If both vertices are part of different components, then join them.
	# When joining two components, change all vertices that share that component number and change it to the component number that we merge with. 
	for edge in edges:
		if(not sets[edge[1]] == sets[edge[2]]):
			setnum = sets[edge[1]]
			setnumchange = sets[edge[2]] 
			# Go through and change all keys connected to the second vertex of this edge.
			for key in sets:
				if(sets[key]==setnumchange):
					sets[key] = setnum
			tree.append((edge[1],edge[2]))
			weight+=edge[0]
			if(isDone(sets)):
				break
		progress = int(100*len(tree)/len(g))
		print("Finding MST... "+str(progress),end='\r')
	print("\n")

	return (weight,tree)

def convertToPointRepr(tree):
	mst = {}
	for i in range(len(tree)+1):
		mst[i]= []
	for edge in tree:
		(v1,v2) = edge
		mst[v1].append(v2)
		mst[v2].append(v1)
	return mst

#We traverse the MST in preorder.
#root->left->right, where left denotes the closest node to the last one.
def preorderTraversal(mst):
	curnode = 0
	visited = []
	vweight = 0
	backtrack = {}
	backtrack[0] = None
	visited.append(curnode)

	while(len(visited) < len(graph)):
		traversed = False #True if we do deeper into tree

		#We try to sort the list first
		nodes = mst[curnode]
		sortednodes = []
		for node in nodes:
			sortednodes.append((getdist(graph[node],graph[visited[-1]]),node))
		sortednodes.sort()

		#Preorder traversal
		for n in sortednodes:
			(d,node) = n
			if(not node in visited):
				backtrack[node] = curnode
				vweight+=d
				visited.append(node)
				curnode = node
				traversed = True
				break

		if(not traversed): #backtrack if no available nodes
			curnode = backtrack[curnode]

		progress = int(100*len(visited)/len(graph))
		print("Running traversal... "+str(progress),end='\r')
	vweight+=getdist(graph[0],graph[visited[-1]])
	visited.append(0)
	print("\n")

	return vweight,visited

def gettsp(graph):
	(w, tree) = findMST(graph)
	mst = convertToPointRepr(tree)
	weight, tour = preorderTraversal(mst)

	return weight,tour

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("graphfile", help="Text repr of graph")
	args=parser.parse_args()
	wfile = args.graphfile
	cwd = os.getcwd()

	graph = getGraphFromFile(cwd+"/"+wfile)

	weight, tour = gettsp(graph)
	print("Weight: "+str(weight))
	print("Tour: "+str(tour))