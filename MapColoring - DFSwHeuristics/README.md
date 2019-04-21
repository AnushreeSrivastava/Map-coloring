# Backtracking search
The program solves the instances of map colouring problem

### Course
<dt>2018 Spring, SFU</dt>
<dt>CMPT 310: Artificial Intelligence Survey</dt>

### Author
James(Yuhao) He

### Description
A map-colouring problem is made up of a set of vertices that represent the regions (variables), edges that represent the adjacency between each pair of vertices, and a set of colours (domains). The program aims to find a valid assignment of colours to vertices such that no vertice shares the same color with its adjacent vertices (neighbours). 

### Inputs
Given n vertices which are numbered 1 through n, and a set of m colours numbered 1 through m. Also a adjacency list is given, where each list element (v1,v2,...,vi) represents that the vertices v1, v2, ..., vi are connencted to each other. 

### Output
The output is a list of n tuples, where each tuple indicates the vertice and the colour to be assigned. For example, the list [(1,2), (2,5)] indicates that vertice 1 is assigned colour 2 and vertice 2 is assigned colour 5.

### Additionals
The back tracking search is implemented along with the MRV, degree, and least constraining value heuristic, for the purpose of search efficiency. 
