'''
Created on Oct 6, 2012

@author: gouthamdl
'''

'''
Created on Oct 6, 2012

@author: gouthamdl
'''

from heapq import heappop,heappush
from Cell import Cell
import copy
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
    solution = backtrack_search(grid)
    return solution

def initializevariables(grid):
    """
    Eliminates values from the domain of a variable by looking at its peers
    """
    
    global domainmap
    global gridmap
    zeroes = getinitialzeroes(grid)
    for cell in zeroes:
        row,col = cell.getxy()
        peervalues = getpeervalues(grid,cell)
        domain = set(range(1,10))
        # The updated domain of the variable will be the original one minus the values of its peers
        domain = domain - peervalues
        
        # if the length of the domain is 1, then set the variable to that value and continue the iteration
        if len(domain) == 1:
            grid[row][col] = domain.pop()
            continue
        
        cell.setDomain(domain)
        dommap = (len(domain),(row,col))
        heappush(domainmap,dommap)
        gridmap[(row,col)] = cell
    buildqueue(grid)
    #AC3(grid)

def buildqueue(grid):
    
    """
    Build the queue for AC3
    """
    
    global arcs
    global gridmap
    
    
    for cell in getzeroes(grid):
        # getvarpeers will return the zero-valued peers for the current cell as a list of the form (row,col)
        # varpeers will be a list of the corresponding cell objects
        varpeers = [rowcol for rowcol in getvarpeers(grid,cell)]
        currentrowcol = cell.getxy()
        for peer in varpeers:
            arcs.append((currentrowcol,peer))
        
def AC3(grid):
    """
    Checks for arc consistency among all the arcs
    """
    global gridmap
    global arcs
    
    temparcs = set(arcs)
    while temparcs:
        rowcol1,rowcol2 = temparcs.pop()
        cell1 = gridmap[rowcol1]
        cell2 = gridmap[rowcol2]
        result = isValueRemoved(grid,cell1,cell2)
        if result == 1:
            for rowcol in getvarpeers(grid,cell1):
                if rowcol != cell2.getxy():
                    #peerobj = gridmap[rowcol]
                    temparcs.add((rowcol,rowcol1))
        
        elif result == 0:
            return False
    return True

def isValueRemoved(grid,cell1,cell2):
    """
    Return 3 values
    0 if it finds an empty domain
    1 if it removes a value from the domain
    2 if it doesnt remove a value from the domain
    """
    global gridmap
    domain1 = cell1.getdomain()
    valueList = set()
    # Iterate over the domain of the first variable to see if we have to remove any values
    for value1 in domain1:
        flag = True
        domain2 = cell2.getdomain()
        for value2 in domain2:
            if value1 != value2:
                flag = False
                break
        if flag:
            valueList.add(value1)
    
    if len(valueList) > 0:   
        newdomain = domain1 - valueList
        if len(newdomain) == 0:
            #print 'Arc Consistency failed for ' + str(cell1.getxy()) + ' and ' + str(cell2.getxy())
            #print 'Cell 1 Domain ' + str(domain1)
            #print 'Cell2 Domain ' + str(cell2.getdomain())
            return 0
        cell1.setDomain(newdomain)
        return 1
    else:
        return 2
            
def backtrack_search(grid):
    """
    Assigns values to variables and checks for consistency in a recursive manner
    """
    
    global guesses
    global domainmap
    global gridmap
    
    if iscomplete(grid):
        return grid
    
    varmap = heappop(domainmap)
    variable = gridmap[varmap[1]]
    domainlen = varmap[0]
    domain = variable.getdomain()
    
    # Update the number of guesses
    guesses += len(domain) - 1
    
    # Loop until we've assigned and checked all 10 values to the variable
    for value in domain:
        
        # If the assignment is consistent, proceed to assign values to other variables
        if isconsistent(variable,value,grid):
            i,j = variable.getxy()      # variable is of the form (i,j)
            grid[i][j] = value
            variable.setDomain([value])
            tempgrid = copy.deepcopy(gridmap)
            #gridmap[(i,j)] = variable
            arcresult = AC3(grid)
            if not arcresult:
                # If Arc Consistency fails, then put the old values back
                grid[i][j] = 0
                rollback(tempgrid)
                variable.setDomain(domain)
                gridmap[(i,j)] = variable
                continue
            result = backtrack_search(grid)
            if not result:
                rollback(tempgrid)
                grid[i][j] = 0
                variable.setDomain(domain)
                gridmap[(i,j)] = variable
            else:
                return result
    
    # Put the variable back in the domain map and return false since the assignment is not consistent
    dommap = (domainlen,variable.getxy())
    heappush(domainmap,dommap)
    return False

def rollback(tempgrid):
    
    global gridmap
    for rowcol in gridmap.keys():
        gridmap[rowcol] = tempgrid[rowcol]

def getinitialzeroes(grid):
    """
    Returns the coordinates for all the variables in the grid
    """
    zeroes = []
    for i in range(0,9):
        for j in range(0,9):
            if grid[i][j] == 0:
                cell = Cell(i,j)
                zeroes.append(cell)
    return zeroes

def getzeroes(grid):
    """
    Returns the coordinates for all the variables in the grid
    """
    global gridmap
    zeroes = []
    for i in range(0,9):
        for j in range(0,9):
            if grid[i][j] == 0:
                cell = gridmap[(i,j)]
                zeroes.append(cell)
    return zeroes

    

def isconsistent(var,value,grid):
    
    peervalues = getpeervalues(grid,var)
    if value in peervalues:
        return False
    return True

def getpeervalues(grid,cell):
    
    """
    Returns the values of the cell's peers (Row + Column + 3*3 square)
    """
    peers = set()
    i,j = cell.getxy()
    for k in range(0,9):
        peers.add(grid[i][k])
    for k in range(0,9):
        peers.add(grid[k][j])
    squarepeers = cell.getBlockCells()
    for peer in squarepeers:
        row,col = peer
        peers.add(grid[row][col])
    return peers

def getvarpeers(grid,cell):
    """
    Returns the list of the cell's peers which are also variables
    """
    varpeers = []
    peers = cell.getpeers()
    for peer in peers:
        i,j = peer
        if grid[i][j] == 0:
            varpeers.append(peer)
    return varpeers

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

# List of Arcs at the start. Each element is a tuple of tuples of the form ((i,j),(m,n) where i,m & j,n refer to the row and column respectively
arcs = []
# Given the row and column value, this dict maps to the corresponding cell object
gridmap = {}

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