#python 3.9.16
#Nicholas Ragano
#10/18/2023
#I wrote this one second and decided to change the structure of the adjacency lists and node lists into one new NodeDict
#   this was to make it easier to use, read and understand. it also allowed one structure to hold the the necessary information
#this program uses a custom node and graph structure that contains the essentials for an AStar program
#NodeDict info is loaded into the nodes and used to find the best path from the Class Room Building A to the Conference center


import math
#list of each node and its associated x,y value
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
    def __init__(self,name,x,y,adjList):
        self.name = name
        self.x = x
        self.y = y
        self.adj = adjList
        self.h = -1
    

class Graph:
    def __init__(self):
        self.nodes = {}

    def setHValues(self,goal):
        for node in self.nodes.values():
            node.h = math.sqrt((pow(goal.x - node.x,2) + pow(goal.y - node.y,2)))
            # print(f"node: {node.name}, {node.h}")
    

    def AStar(self, start, goal):
        self.setHValues(goal) #set all nodes h values
        parents = {}        
        parents[start] = start  #keep track of parents 
        #set makes sure we have no duplicates
        visited_incomplete = set([start])  #keep track of nodes we have visited but still have nodes to go to
        visited_completed = set([])     #keep track of nodes we have visited and went to all adjacent nodes

        distFromStart = {}      
        distFromStart[start] = 0 #we are at the start so zero
        
        while(len(visited_incomplete) > 0): #while there are more nodes to explore
            curNode = None  #set our current node to nothing

            #go through the nodes we have visited but have more to look at
            #   since we are using sets we cannot just reverse order and pop the last element to get the smallest and so must compare all elements
            for each in visited_incomplete:
                #choose a node the first loop through
                #then loop and find the node with the smallest f value
                if curNode == None or distFromStart[each] + each.h < distFromStart[curNode] + curNode.h:
                    curNode = each
            
            #if we didnt find anything then there is not path to the goal
            if curNode == None:
                return 'failure'
            
            #if we found the goal node, then we can reconstruct the path from the goal to the start by following the parents back
            if curNode == goal:
                path = []

                #loop through our chain of parents until we cant
                while parents[curNode] != curNode:
                    path.append(curNode)
                    curNode = parents[curNode]
                path.append(start)
                path.reverse()
                return path
            
            #since the adjaceny lists are tuples get both items as we iterate through each of the current nodes adjacent nodes
            for(newNode, weight) in curNode.adj:
                newNode = self.nodes[newNode] #get the node object instead of the name
                #if the newNode has not been visited at all then add it to the visited but incomplete list
                if(newNode not in visited_incomplete and newNode not in visited_completed):
                    visited_incomplete.add(newNode)
                    parents[newNode] = curNode #designate the current node as this nodes parent
                    distFromStart[newNode] = distFromStart[curNode] + weight  #compute the g distance from the start for this newNode
                else:
                    
                    #this allows us to choose the shorter of the paths if there are multiple choices
                    #if this statement isnt true then we have the shortest adjacent nodes
                    if(distFromStart[newNode] > distFromStart[curNode] + weight):
                        #then set its g distance to the current node plus the newnode weight
                        distFromStart[newNode] = distFromStart[curNode] + weight
                        parents[newNode] = curNode
                        #if its in the completed list and we found a shorter path, then we need to explore it more
                        if newNode in visited_completed:
                            visited_completed.remove(newNode)
                            visited_incomplete.add(newNode)
            #we have explored all of the current node and dealt with any adjacent nodes so we dont need to come back here for now
            visited_incomplete.remove(curNode)
            visited_completed.add(curNode)
        #if we reach here then something went wrong
        return 'failure'

        

graph = Graph()
for node in NodeDict:
    graph.nodes[node] = Node(node,NodeDict[node]['x'],NodeDict[node]['y'],NodeDict[node]['adj'])


res = graph.AStar(graph.nodes["Class Room Building A"], graph.nodes["Conference Center"])
print([x.name for x in res])


