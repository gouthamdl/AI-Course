'''
Created on Oct 6, 2012

@author: gouthamdl
'''

from heapq import heappop,heappush
import sys

def readinput(filename):
    
    inpfile = open(filename,'r')
    inpt = inpfile.read()
    
    # Grid is a 2d list which stores our problem
    grid = [[0] * 9 for i in range(1,10)]
    
    # Location of all the zeroes in the grid.
    #zeroes = []
    
    i = 0
    j = 0
    
    for x in inpt:
        if x != ' ' and x != '\n':

            if x == '-':
                grid[i][j] = 0
                #heappush(zeroes,(i,j))
                
            else:
                grid[i][j] = int(x)
                
            j += 1
            if j == 9:
                i += 1
                j = 0
    
    return grid

def sudokuSolver(filename):
    """
    The main program which builds the initial grid and calls the backtracking search on it
    """
    grid = readinput(filename)
    initializevariables(grid)
    solution = mrv_search(grid)
    return solution

def initializevariables(grid):
    """
    Eliminates values from the domain of a variable by looking at its peers
    """
    
    global domainmap
    zeroes = getzeroes(grid)
    for cell in zeroes:
        peervalues = getpeervalues(grid,cell)
        domain = set(range(1,10))
        # The updated domain of the variable will be the original one minus the values of its peers
        domain = domain - peervalues
        
        # if the length of the domain is 1, then set the variable to that value and continue the iteration
        if len(domain) == 1:
            row,col = cell
            grid[row][col] = domain.pop()
            continue
        
        map = (len(domain),(cell,domain))
        heappush(domainmap,map)
        


def mrv_search(grid):
    """
    Assigns values to variables and checks for consistency in a recursive manner
    """
    
    global guesses
    global domainmap
    
    if iscomplete(grid):
        return grid
    
    varmap = heappop(domainmap)
    variable,domain = varmap[1]
    domainlen = varmap[0]
    
    # Update the number of guesses
    guesses += len(domain) - 1
    
    # Loop until we've assigned and checked all 10 values to the variable
    for value in domain:
        
        # If the assignment is consistent, proceed to assign values to other variables
        if isconsistent(variable,value,grid):
            i,j = variable      # variable is of the form (i,j)
            grid[i][j] = value
            result = mrv_search(grid)
            if not result:
                grid[i][j] = 0
            else:
                return result
    
    # Put the variable back in the domain map and return false since the assignment is not consistent
    map = (domainlen,(variable,domain))
    heappush(domainmap,map)
    return False

def getzeroes(grid):
    """
    Returns the coordinates for all the variables in the grid
    """
    zeroes = []
    for i in range(0,9):
        for j in range(0,9):
            if grid[i][j] == 0:
                zeroes.append((i,j))
    return zeroes
    

def isconsistent(var,value,grid):
    
    peervalues = getpeervalues(grid, var)
    if value in peervalues:
        return False
    return True

def getValues(var):
    """
    Given a cell, returns the 4 elements in the 3*3 square that the cell is part of 
    These elements are the ones that are not in the cell's column and row
    """
    row,col = var
    
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
    
def getpeervalues(grid,cell):
    
    """
    Returns the values of the cell's peers (Row + Column + 3*3 square)
    """
    peers = set()
    i,j = cell
    for k in range(0,9):
        peers.add(grid[i][k])
    for k in range(0,9):
        peers.add(grid[k][j])
    squarepeers = getValues(cell)
    for peer in squarepeers:
        row,col = peer
        peers.add(grid[row][col])
    return peers

def getpeers(cell):
    """
    Returns the locations of the cell's peers
    """
    row,col = cell
    peers = []
    peers.extend([(i,col) for i in range(0,9)])
    peers.extend([(row,j) for j in range(0,9)])
    peers.extend(getValues(cell))
    return peers

def iscomplete(grid):
    """
    Checks for the completeness of the Sudoku grid. If there is a zero present in the grid, then the grid is incomplete.
    """
    
    for i in range(0,9):
        for j in range(0,9):
            if grid[i][j] == 0:
                return False
    return True

guesses = 0

# The domain map is a list of tuples of the form (A,(B,C)) where A is the variable's domain size,
# B is the variable (of the form (i,j)) and C is the domain of the variable
domainmap = []
sol = sudokuSolver(sys.argv[1])
print 'Guesses' + ':' + str(guesses)
if sol:
    for row in sol:
        print row

else:
    print sol