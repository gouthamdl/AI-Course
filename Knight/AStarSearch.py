'''
Created on Sep 25, 2012

@author: gouthamdl

This is the main function implementing the A* Search.
'''
from Node import Node
from heapq import heappush,heappop
import time
import sys

def AStar(goalX,goalY):
    
    """
    The function takes as argument the location of the goal node (x,y)
    """
    
    # The initial node is at (0,0) and its path cost is 0
    initState = Node(0,0,0,None)
    
    # Maintains a list of co-ordinates on the fringe
    fringe = []
    
    # heap is a priority queue for holding the nodes in the fringe
    heap = []
    heappush(heap,(initState.f(goalX,goalY), initState))
    fringe.append(initState.getxy())
    nodesExpanded = 0
    goalNode = None
    
    while fringe :
        cell = heappop(heap)[1]
        nodesExpanded += 1
        x1,y1 = cell.getxy()
        #print str(cell) + ' f=' + str(cell.f(goalX,goalY))
        
        # If its the goal Node, then we are done
        if x1 == goalX and y1 == goalY:
            goalNode = cell
            break
        
        # Otherwise continue
        fringe.remove(cell.getxy())
        
        for sNode in cell.successors():
            x,y = sNode.getxy()  
            if (x,y) not in fringe:
                fringe.append((x,y))
                heappush(heap,(sNode.f(goalX,goalY), sNode))
    
    node = goalNode
    while node is not None:
        print node
        node = node.getParent() 
    
    print 'Nodes Expanded : ' + str(nodesExpanded)
    print 'Number of moves from Initial State to Goal : ' + str(goalNode.pathcost())

t = time.time()
x = float(sys.argv[1])
y = float(sys.argv[2])
AStar(x,y)
print 'Time taken for running the program : ' + str(time.time() - t) + ' seconds'