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

NodeDict = {
    'Class Room Building A': {'adj': [('Student Commons', 100)], 'x': 0, 'y': 291},
    'Class Room Building B': {'adj': [('Student Commons', 100)], 'x': 0, 'y': 149},
    'Student Commons': {'adj': [('Class Room Building A',100),('Class Room Building B',100),('Transportation Hub',200),('Administration Building',275)], 'x': 71, 'y': 220},
    'Transportation Hub': {'adj': [('Student Commons',200), ('Administration Building', 50), ('Faculty Office Building', 100)], 'x': 271, 'y': 220},
    'Administration Building': {'adj': [('Student Commons', 275),('Transportation Hub', 50)], 'x': 306, 'y': 255},
    'Faculty Office Building': {'adj': [('Transportation Hub',100), ('Conference Center', 200)], 'x': 342, 'y': 149},
    'Conference Center': {'adj': [('Faculty Office Building', 200)], 'x': 182, 'y': 29}
}

class Node:
    def __init__(self,name,x,y):
        self.name = name
        self.x = x
        self.y = y
        self.visited = False
        self.h_distance = -1
        self.parent = []
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
            node = self.nodes[each]
            node.h_distance = math.sqrt(pow((Goal.x - node.x),2) + pow((Goal.y - node.y),2))

    def loadFrontier(self, frontier, node):
        for each in node.adj:
            #for all adjacent nodes we have not yet visited that are not already in the frontier
            if(each[0].visited == False and (each[0] not in [n[0] for n in frontier])):
                each[0].parent.append(node)
                f_entry = (each[0], each[0].h_distance + each[1])
                frontier.append(f_entry)
        frontier.sort(reverse = True, key = lambda x:x[1])
        return frontier
    

    def AStar(self, start, goal):
        self.setHDistances(goal)
        res = [start]       #add our start to the path
        if(start == goal):  #check that we didnt start at the goal
            return res
        start.visited = True
        frontier = self.loadFrontier([],start) #load the frontier with nodes adjacent to the current node
        while(frontier):
            currentNode = frontier.pop()[0] #get the smallest from the pqueue
            res.append(currentNode) #add it to the current path and mark visited
            currentNode.visited = True
            if(currentNode == goal):    #check if we are at the goal
                return res
            #if we arent then we should go about selecting the next smallest frontier node
            frontier = self.loadFrontier(frontier, currentNode) #load the frontier with nodes adjacent to the current node

            if(len(frontier) > 0):  #if the frontier pqueue is empty then we cant make it to the goal
                nextSmallest = frontier[-1] #peek at the next smallest node on the frontier
                if(nextSmallest[0] in [x[0] for x in currentNode.adj]):
                    #if the next smallest node on the frontier is adjacent to the current node
                    #   then we can continue right along as normal
                    continue
                else:
                    #if it isnt then we need to go to the next smallest node and reconstruct the path back to start
                    
                    at_start = False
                    tempNode = nextSmallest[0]
                    res = []
                    while(at_start == False):
                        if(len(tempNode.parent) == 0):
                            at_start = True
                        else:
                            if(len(tempNode.parent) > 1):
                                #if there is more than one node that could be a parent
                                #choose the parent with the smallest g distance
                                tempNode = min(tempNode.parent, key = lambda x: x.h_distance)
                                    
                            else:
                                tempNode = tempNode.parent[0]
                                res.append(tempNode)
                    res.reverse()

            else:
                #no more left to try, we failed
                return 'failure'

        

struct = Structure()
for node in NodeList:
    struct.nodes[node[0]] = (Node(node[0], node[1], node[2]))

for each in AdjList:
    struct.addEdge(each[0], each[1], each[2])

res = struct.AStar(struct.nodes["Class Room Building A"], struct.nodes["Administration Building"])
if(res != 'failure'):
    print([x.name for x in res])
else:
    print(res)


