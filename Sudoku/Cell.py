'''
Created on Oct 6, 2012

@author: gouthamdl
'''

class Cell(object):
    '''
    Represents each cell of the sudoku
    '''
    def __init__(self,row,col,domain=set([])):
        '''
        Constructor
        '''
        self.row = row
        self.col = col
        self.domain = set(domain)
        self.initialize()
    
    def initialize(self):
        
        self.peers = self.getpeers()
        
    def getpeers(self):
        """
        Returns the locations of the cell's peers
        """
        row = self.row
        col = self.col
        peers = []
        peers.extend([(i,col) for i in range(0,9) if i!= row] )
        peers.extend([(row,j) for j in range(0,9) if j!=col])
        peers.extend(self.getBlockCells())
        return peers
    
    def getBlockCells(self):
        """
        Given a cell, returns the 4 elements in the 3*3 square that the cell is part of 
        These elements are the ones that are not in the cell's column and row
        """
        row = self.row
        col = self.col
    
        if row % 3 == 0 and col % 3 == 0:
            return [(row+1,col+1),(row+1,col+2),(row+2,col+1),(row+2,col+2)]
        elif row % 3 == 0 and col % 3 == 1:
            return [(row+1,col-1),(row+1,col+1),(row+2,col-1),(row+2,col+1)]
        elif row % 3 == 0 and col % 3 == 2:
            return [(row+1,col-2),(row+1,col-1),(row+2,col-2),(row+2,col-1)]
        elif row % 3 == 1 and col % 3 == 0:
            return [(row-1,col+1),(row-1,col+2),(row+1,col+1),(row+1,col+2)]
        elif row % 3 == 1 and col % 3 == 1:
            return [(row-1,col-1),(row-1,col+1),(row+1,col-1),(row+1,col+1)]
        elif row % 3 == 1 and col % 3 == 2:
            return [(row-1,col-2),(row-1,col-1),(row+1,col-2),(row+1,col-1)]
        elif row % 3 == 2 and col % 3 == 0:
            return [(row-2,col+1),(row-2,col+2),(row-1,col+1),(row-1,col+2)]
        elif row % 3 == 2 and col % 3 == 1:
            return [(row-2,col-1),(row-2,col+1),(row-1,col-1),(row-1,col+1)]
        elif row % 3 == 2 and col % 3 == 2:
            return [(row-2,col-2),(row-2,col-1),(row-1,col-2),(row-1,col-1)]
    
    def setDomain(self,domain):
        self.domain = set(domain)
    
    def getdomain(self):
        return self.domain
    
    def getxy(self):
        return (self.row,self.col)
    
    def getvalues(self):
        vallist = []
        for val in self.domain:
            vallist.append(val)
        return vallist
    
    
    
    
    
    