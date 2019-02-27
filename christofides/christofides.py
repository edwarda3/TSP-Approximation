import os
import sys
import argparse
import math
import time

#We can assume a complete graph for this program.
#Takes input from a file as described in readme.txt
# @param filepath: The path to the textfile which holds the graph information
# @return graphs: A list of graphs, with the number of graphs being equivalent to the <test cases> in the text file.
#				  Each graph is a list of vertices in the form (x,y). Because a complete graph is assumed, no edges are stored here.
def getGraphFromFile(filepath):
	starttime = time.time()
	print("Reading file... ", end = '')
	try:
		myfile = open(filepath,'r')
	except IOError:
		print("Failed to read file!")
		sys.exit()
	with myfile:
		data = myfile.read()
	print("Done! ", end='')
	data = data.strip()

	info = data.split('\n')
	graph = [0]*len(info)
	for i in range(len(info)):
		info[i] = info[i].strip()
		c = info[i].split()
		if(c[1].isdigit() and c[2].isdigit()):
			graph[i] = (int(c[1]),int(c[2]))
	endtime = time.time()
	print("(" + str(round(endtime-starttime,4)) + " seconds)")
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

def adjMatrix(graph):
	print("Building adjacency matrix... ",end='')
	starttime = time.time()
	gnodes = len(graph)
	matrix = [[0]*gnodes for _ in range(gnodes)]
	for i, v1 in enumerate(graph):
		for j, v2 in enumerate(graph):
			matrix[i][j] = getdist(v1,v2)
	endtime = time.time()
	print("Done! (" + str(round(endtime-starttime,4)) + " seconds)")
	return matrix

#From previous assignment, using Kruskal's
#Finds the MST of a complete graph given the euclidian points as vertices.
#Use Kruskal's Algorithm: https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
# @param g: A graph representation where we are given points as vertices.
# @return weight: The total weight of the MST.
# @return tree: A list of edges which make up the MST.
def findMST(g,matrix):
	# Make a list of all edges, and store them as (dist, v1, v2), and sort them
	edges = []
	for v1i in range(len(g)):
		for v2i in range(v1i+1,len(g)):
			edges.append((matrix[v1i][v2i],v1i,v2i))
			#edges.append((getdist(g[v1i],g[v2i]),v1i,v2i))
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
			if(len(tree) == len(g)-1):
				break
		progress = int(100*len(tree)/len(g))+1
		print("Finding MST... "+str(progress),end='\r')

	print()
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

#returns a pruned version of mst "tree" including ONLY vertices with odd degree.
def getOddDegrees(tree):
	odds = {}
	for node in tree:
		if(len(tree[node])%2==1):
			odds[node] = tree[node]
	return odds

#Estimate minimum perfect pairings.
#For each node, we find the closest node and then remove both as candidates.
def addPairings(graph,matrix,mst,tree,odds):
	startodds = len(odds)
	while(odds):
		(v, edges) = odds.popitem()
		min = v
		minlen = float('inf')
		for node in odds:
			d = matrix[v][node]
			#d = getdist(graph[v],graph[node])
			if(d < minlen):
				min = node
				minlen = d
		mst[v].append(min)
		mst[min].append(v)
		tree.append((v,min))
		del odds[min]

		progress = int(100*(startodds-len(odds))/startodds)
		print("Finding Pairings... "+str(progress),end='\r')

	print()
	return mst, tree

#Deletes an edge between r1,r2
def delEdge(edges,r1,r2):
	for i in range(len(edges)):
		(v1,v2) = edges[i]
		if((v1==r1 and v2==r2) or (v1==r2 and v2==r1)):
			del edges[i]
			break
	return edges
		

#Find eulerian tour
def findEulerianTour(graph,matrix,mstp,mstpe):
	startlen = len(mstpe)
	start = 0
	path = [mstp[start][0]]
	while(len(mstpe) > 0):
		for i, current in enumerate(path): #guarantees a node with unvisited neighbors
			if(len(mstp[current]) > 0):
				break
		while(len(mstp[current]) > 0):
			next = mstp[current][0]
			delEdge(mstpe,current,next)
			del mstp[current][(mstp[current].index(next))]
			del mstp[next][(mstp[next].index(current))]

			i+=1
			path.insert(i,next)
			current=next
		progress = int(100*(startlen-len(mstpe))/startlen)
		print("Finding Eulerian Tour... "+str(progress),end='\r')

	print()
	return path

#Removes the duplucate vertices from the tour
def finalizepath(graph,matrix,tour):
	cost = 0
	final = [tour[0]]
	for node in tour:
		if(not node in final): #Only add once
			#cost+=getdist(graph[node],graph[final[-1]]) #We take the cost from the last node in the final tour to this one
			cost+=matrix[node][final[-1]]
			final.append(node)
	#cost+=getdist(graph[tour[0]],graph[final[-1]])
	cost+=matrix[tour[0]][final[-1]]
	final.append(tour[0])
	return cost,final

# Runs the Christofides algorithm steps.
def gettsp(graph,matrix):
	(w, tree) = findMST(graph,matrix) #Find an MST of the graph
	mst = convertToPointRepr(tree) #For convinience, get a adjacency list repr of the mst
	oddVertices = getOddDegrees(mst) #Get the odd vertices
	mstPairings, mstPairedEdges = addPairings(graph,matrix,mst,tree,oddVertices) #Returns both the adj list and edges list after adding the perfect pairings to it (this is an estimate, greedy)
	etour = findEulerianTour(graph,matrix,mstPairings,mstPairedEdges) #Find the eulerian tour of this multigraph
	finalcost, finalpath = finalizepath(graph,matrix,etour) #remove vertices that were visited multiple times.

	return finalcost, finalpath

def writeToFile(file,weight,tour):
	s=str(weight)
	for node in tour:
		s+="\n"+str(node)
	f = open(file,'w')
	f.write(s)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("graphfile", help="Text repr of graph")
	args=parser.parse_args()
	wfile = args.graphfile
	cwd = os.getcwd()

	graph = getGraphFromFile(cwd+"/"+wfile)
	matrix = adjMatrix(graph)

	starttime = time.time()
	weight, tour = gettsp(graph,matrix)
	endtime = time.time()
	writeToFile(wfile+".tour",weight,tour)

	print("Done!\n")
	print("Runtime: "+str(round(endtime-starttime,4))+" seconds for "+str(len(graph))+" nodes, result written to \'"+wfile+".tour\'")