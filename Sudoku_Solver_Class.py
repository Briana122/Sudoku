class Sudoku_Solver:

    def __init__(self, grid):
        self.grid = grid

    #FUNCTION - return solved grid
    def get_grid(self):
        return self.grid

    # FUNCTION - check to see if the same number is already present in the same row
    def check_row(self, row, num):
        for i in range(9):
            if (self.grid[row][i] == num):
                return False
        return True

    # FUNCTION - check to see if the same number is already present in the same column
    def check_column(self, col, num):
        for i in range(9):
            if (self.grid[i][col] == num):
                return False
        return True

    # FUNCTION - check to see if the same number is already present in the same 3x3 square
    def check_box(self, row, col, num):
        for i in range (3):
            for j in range (3):
                if self.grid[row + i][col + j] == num:
                    return False
        return True
        
    # FUNCTION - determines whether or not the empty location is suitable for potential number
    def check_number_at_location(self, row, col, num):
        if self.check_row(row, num) and self.check_column(col, num) and self.check_box(row - (row % 3), col - (col % 3), num):
            return True
        else:
            return False
        
    # FUNCTION - find_empty_location
    # - Finds empty location on Sudoku grid by searching through each row and column
    # - Reference parameter (memory location) will be set to store the coordinates of empty location, returns True
    # - If no empty location found, returns False
    def find_empty_location(self, coor):
        for row in range (9):
            for col in range (9):
                if (self.grid[row][col] == 0):
                    #store address of empty location
                    coor[0] = row
                    coor[1] = col
                    return True
        return False

    # FUNCTION - Print Sudoku grid array
    def print_grid(self):
        for i in range(9):
            for j in range(9):
                print (self.grid[i][j], end = "  ")
            print()

    def solve_Sudoku(self):
        #declare array to store coordinates of empty location on grid
        coor = [0,0] 

        #If there are no empty spots found, the Sudoku is finished
        if (not self.find_empty_location(coor)):
            return True

        #store address of empty location in variable row and col
        row = coor[0]
        col = coor[1]

        #If there is still an empty location found, recursion is used to find the missing number(s) through 1 to 9
        for num in range(1,10):
            #temporarily assigns a number to empty location
            if (self.check_number_at_location(row, col, num)):
                self.grid[coor[0]][coor[1]] = num

                #if all temporary numbers comply to the rules of Sudoku, the game is finished
                if (self.solve_Sudoku()):
                    return True

                #if temporary numbers do not comply with the rules, they are erased and a new temporary number is assigned and tested
                self.grid[coor[0]][coor[1]] = 0
        return False