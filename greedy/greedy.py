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

#Returns the euclidian distance between two points rounded to the nearest integer.
# @param v1: The first point as (x,y)
# @param v2: The second point as (x,y)
# @return value: The distance between v1, v2 to the nearest integer.
def getdist(v1, v2):
	(x1,y1) = v1
	(x2,y2) = v2
	return round(math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2)))

def greedy(graph):
	curidx = 0
	visited = []
	vweight = 0
	visited.append(curidx)
	while(len(visited) < len(graph)):
		min = 9999999
		minnode = curidx
		for node in range(len(graph)):
			distn = getdist(graph[curidx],graph[node])
			if(not curidx == node and not node in visited and distn < min):
				min = distn
				minnode = node
		vweight+=min
		visited.append(minnode)
		curidx = minnode
	visited.append(0)
	return vweight,visited


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("graphfile", help="Text repr of graph")
	args=parser.parse_args()
	wfile = args.graphfile
	cwd = os.getcwd()

	graph = getGraphFromFile(cwd+"/"+wfile)

	weight, tour = greedy(graph)
	print("Weight: "+str(weight))
	print("Tour: "+str(tour))