#python 3.9.16
#Nicholas Ragano
#10/18/2023
#this program uses a custom graph structure along with complete data set that allows the nodes and paths to be mapped
#it will then output the best path from Class Room Building A to the Conference Center


import sys
#list of each node and its associated x,y value
NodeList = [
    ("Class Room Building A"),
    ("Class Room Building B"),
    ("Student Commons"),
    ("Transportation Hub"),
    ("Administration Building"),
    ("Faculty Office Building"),
    ("Conference Center")
]

# list of edges
AdjList = [
    ("Class Room Building A", "Student Commons", 100),
    ("Class Room Building B", "Student Commons", 100),
    ("Student Commons", "Administration Building", 275),
    ("Student Commons", "Transportation Hub", 200),
    ("Administration Building", "Transportation Hub", 50),
    ("Transportation Hub", "Faculty Office Building", 100),
    ("Faculty Office Building", "Conference Center", 200)
]


class Node:
    def __init__(self,name):
        self.name = name
        self.visited = False
        self.adj = [] #(node name, path cost)

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
    
    def addNode(self,node):
        self.nodes[node.name] = node

    def addEdge(self,NodeA,NodeB,Cost):
        self.nodes[NodeA].adj.append((NodeB,Cost))
        self.nodes[NodeB].adj.append((NodeA,Cost))

    def DLS(self,Start,Goal,Limit):
        depth = 0
        path = []     
        frontier = [Start] # level 0 depth
        Start.visited = True
        while(frontier):
            #check for our Goal on the frontier
            for nd in frontier:
                if(nd == Goal):
                    path.append(nd)
                    return path
            nextNode = frontier.pop() #pop the top of the stack, append to the path, and mark it as visited
            path.append(nextNode)
            nextNode.visited = True
            if(depth < Limit):             #check if we are at the depth limit
                if(len(nextNode.adj) > 0):  #check if our current node has unvisited adjacent nodes
                    #if it does then add the unvisited ones to frontier and increase the depth
                    for each in nextNode.adj:
                        adjNode = self.nodes[each[0]]
                        if(adjNode.visited == False):
                            frontier.append(adjNode)
                    depth += 1
                else:
                    #otherwise there is no adjacent nodes to this one so back up one and attempt the next node
                    path.pop()
                    frontier.append(path.pop()) #add the previous node back to the frontier and try again
                    depth -= 1 #dont forget to go back "up" a level
                if(len(frontier) == 0): #if the frontier is empty and we are not at depth then there is no path
                    return 'failure'
            else: #we are at the depth limit
                if(len(frontier) > 0): #but there are more to try, back up and try another
                    path.pop()
                    frontier.append(path.pop()) #add the previous node back to the frontier and try again
                    depth -= 1 #dont forget to go back "up" a level
        return 'cutoff' 


    def IDDFS(self,Start,Goal,maxDepth = sys.maxsize): #returns a list
        for i in range(0,maxDepth):
            for each in self.nodes:
                self.nodes[each].visited = False
            res = self.DLS(Start,Goal,i)
            #we found a valid path if cutoff or failure is not returned
            if res != 'cutoff' and res !='failure':
                return res
            #if cutoff is returned we will loop again
        #if we reach the max depth with no results we return no valid path
        return 'no valid path'

####ITERATIVE DEEPINING DEPTH FIRST SEARCH####
#create our graph and add each node
graph = Graph()
for n in NodeList:
    graph.addNode(Node(n))  #Node(name)

for each in AdjList:
    graph.addEdge(each[0],each[1],each[2])

#Start Node, Goal Node, OPTIONAL depth limit (default value is sys.maxsize)
res = graph.IDDFS(graph.nodes["Class Room Building A"], graph.nodes["Conference Center"])
if(res != 'no valid path'):
    print([x.name for x in res])
else:
    print("no valid path")
    


    