'''
Created on Oct 1, 2012

@author: gouthamdl
'''

from heapq import heappop
import sys

guesses = 0

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

def initializevariables():
    return 1

def mrv_search(grid):
    """
    Assigns values to variables and checks for consistency in a recursive manner
    """
    
    global guesses
    
    # If the zeroes list is empty, it means we have assigned values to all our variables
    zeroes = getzeroes(grid)
    if not zeroes:
        return grid
    
    domain = range(1,10)
    # Pick the first unassigned variable from zeroes (corresponds to zero values in the grid)
    variable = heappop(zeroes)
    
    # Update the number of guesses
    guesses += len(domain) - 1
    
    # Loop until we've assigned and checked all 10 values to the variable
    while domain:
        value = heappop(domain)
        
        # If the assignment is consistent, proceed to assign values to other variables
        if isconsistent(variable,value,grid):
            i,j = variable      # variable is of the form (i,j)
            grid[i][j] = value
            result = mrv_search(grid)
            if not result:
                grid[i][j] = 0
            else:
                return result
    return False

def getzeroes(grid):
    
    zeroes = []
    for i in range(0,9):
        for j in range(0,9):
            if grid[i][j] == 0:
                zeroes.append((i,j))
    return zeroes
    

def isconsistent(var,value,grid):
    
    row,col = var
    
    # Check if the value is present in the row
    for k in range(0,9):
        if grid[row][k] == value:
            return False
    
    # Check if the value is present in the column
    for k in range(0,9):
        if grid[k][col] == value:
            return False
        
    # Check if the value is present in the square
    flag = checkInSquare(var,value,grid)
    return flag

def checkInSquare(var,value,grid):
    """
    Checks if value is present in the 3*3 square its part of
    """
     
    # By now we would have checked both the row and column if value is already present
    # We only need to check the other 4 cells
    squareCells = getValues(var)
    for cell in squareCells:
        i,j = cell
        if value == grid[i][j]:
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
        return [(row+1,col-1),(row+1,col+1),(row+2,col-1),(row+2,col-1)]
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

def iscomplete(grid):
    """
    Checks for the completeness of the Sudoku grid. If there is a zero present in the grid, then the grid is incomplete.
    """
    
    for i in range(0,9):
        for j in range(0,9):
            if grid[i][j] == 0:
                return False
    return True
 
def sudokuSolver(filename):
    """
    The main program which builds the initial grid and calls the backtracking search on it
    """
    grid = readinput(filename)
    initializevariables()
    solution = mrv_search(grid)
    return solution

sol = sudokuSolver(sys.argv[1])
print 'Guesses' + ':' + str(guesses)
if sol:
    for row in sol:
        print row

else:
    print sol