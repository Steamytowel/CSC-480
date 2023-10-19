#python 3.9.16
#Nicholas Ragano
#10/18/2023
#this program uses a custom structure to aid with the AStar program along with complete data set that allows the nodes and paths to be mapped
#it will then output the best path from Class Room Building A to the Conference Center usingg AStar


import sys, math
#list of each node and its associated x,y value
NodeList = [
    ("Class Room Building A",0,291),
    ("Class Room Building B",0,149),
    ("Student Commons",71,220),
    ("Transportation Hub",271,220),
    ("Administration Building",306,255),
    ("Faculty Office Building",342,149),
    ("Conference Center",182,29)
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
    def __init__(self,name,x,y):
        self.name = name
        self.x = x
        self.y = y
        self.visited = False
        self.h_distance = -1
        self.parent = None
        self.adj = [] #(node name, path cost)
    

class Structure:
    def __init__(self):
        self.nodes = {}
        self.edges = []


    def addEdge(self, NodeA, NodeB, weight):
        self.edges.append((self.nodes[NodeA], self.nodes[NodeB], weight))
        #make sure the nodes themselves know they are adjacent to one another to make things easier for us
        self.nodes[NodeA].adj.append((self.nodes[NodeB],weight))
        self.nodes[NodeB].adj.append((self.nodes[NodeA],weight))

    def setHDistances(self,Goal):
        for each in self.nodes:
            node = self.node[each]
            node.h_distance = math.sqrt(pow((Goal.x - node.x),2) + pow((Goal.y - node.y),2))

    def loadFrontier(self, frontier, node):
        for each in node.adj:
            #for all adjacent nodes we have not yet visited
            if(each[0].visited == False):
                if(each[0].parent == None):
                    each[0].parent = node
                f_entry = (each[0], each[0].h_distance + each[1])
                frontier.append(f_entry)
        frontier.sort(reverse = True, key = lambda x:x[1])
        return frontier
    

    def AStar(self, start, goal):
        res = [start]
        if(start == goal):
            return res
        frontier = self.loadFrontier([],start)
        while(frontier):
            currentNode = frontier.pop()[0]
            res.append(currentNode)
            currentNode.visited = True
            if(currentNode == goal):
                return res
            frontier = self.loadFrontier(frontier, currentNode)
            if(len(frontier) > 0):
                nextSmallest = frontier[-1]
                if(nextSmallest[0] in [x[0] for x in currentNode.adj]):
                    #if the next smallest node on the frontier is adjacent to the current node
                    continue
                else:
                    #we need to go find the parent of the next frontier node
                    for each in res[::-1]:
                        if(nextSmallest[0].parent == each):
                            #our path is now corrected and we can continue
                            break
                        else:
                            res.pop()
            else:
                #no more left to try, we failed
                return 'failure'

        

struct = Structure()
for node in NodeList:
    struct.nodes[node[0]] = (Node(node[0], node[1], node[2]))

for each in AdjList:
    struct.addEdge(each[0], each[1], each[2])

res = struct.AStar(struct.nodes["Class Room Building A"], struct.nodes["Conference Center"])
if(res != 'failure'):
    print([x.name for x in res])
else:
    print(res)


