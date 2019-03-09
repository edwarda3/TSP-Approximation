# TSP-Approximation
3 Algorithms to approximate a path for the Travelling Salesman Problem.

Written for CS420: Graph Theory class at Oregon State University (W2019).

The problem takes an input graph of format:

*test-input.txt*
```
city# x y
city# x y
...
```

Outputs to:
*test-input.txt.tour*
```
cost
city#1
city#2
...
```

This problem assumes a complete graph given the vertices, and edge weights are euclidian distances between the (x,y) points.

## Greedy Algorithm:
Start at some node, and take the shortest path. Runs in O(V^2).

Run using:
```
$ python3 greedy/greedy.py <test file>
```

## Spanning-Tree Heuristic:
Build an MST, and traverse that MST in pre-order.
See: http://demonstrations.wolfram.com/TheTravelingSalesmanProblem4SpanningTreeHeuristic/

Run using:
```
$ python3 euclidian-approx/preorder-traversal.py <test file>
```

## Christofides Algorithm:
Builds an MST, finds minimum pairs of odd-degree vertices (approximate), adds those edges of the pairs to the MST for a multigraph. Find an eulerian tour of the multigraph and prune duplicate vertices.
See: https://en.wikipedia.org/wiki/Christofides_algorithm

Run using:
```
$ python3 christofides/christofides.py <test file>
```
