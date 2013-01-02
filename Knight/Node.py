'''
Created on Sep 25, 2012

@author: gouthamdl
'''

from math import ceil

class Node(object):
    '''
    The Node class is for representing each position of the chessboard 
    '''


    def __init__(self,x,y,g,parent):
        
        self.x = float(x)
        self.y = float(y)
        
        # g represents the path cost from the initial state to the current node
        self.g = float(g) 
        # A tuple representing the previous position of the knight before it came o the current node
        self.parent = parent
        
    
    def heuristic(self,x1,y1):
        """
        Returns the heuristic estimate to go from the current Node to the Node (x1,y1)
        """
        absXDiff = abs(self.x - x1)
        absYDiff = abs(self.y - y1)
        h = ceil((absXDiff + absYDiff) / 3)
        return h
    
    def f(self,x1,y1):
        # Returns the f value for the current node with (x1,y1) as the goal node
        return self.g + self.heuristic(x1,y1)
    
    def pathcost(self):
        # Return the path cost for this node from the initial state
        return self.g
    
    def successors(self):
        # From any given Cell, a Knight can move to 8 other cells in a single step
        # This function returns all the nodes the knight can goto from the current Node
        
        x = self.x
        y = self.y
        g = self.g
        p = self
        
        node1 = Node(x - 2, y+1, g+1, p)
        node2 = Node(x - 2, y-1, g+1, p)
        node3 = Node(x - 1, y+2, g+1, p)
        node4 = Node(x - 1, y-2, g+1, p)
        
        node5 = Node(x + 1, y+2, g+1, p)
        node6 = Node(x + 1, y-2, g+1, p)
        node7 = Node(x + 2, y+1, g+1, p)
        node8 = Node(x + 2, y-1, g+1, p)
        
        return [node1,node2,node3,node4,node5,node6,node7,node8]
    
    def getxy(self):        
        return (self.x,self.y) 
    
    def getParent(self):
        #if self.parent is None:
        #    return (self.x,self.y) # In case of the initial State, just return its own coordinates since it wont have a parent node
        return self.parent
    
    def __str__(self):
        return str(self.getxy())
        
        
        
        