
board = [ [ 3, 0, 6, 5, 0, 8, 4, 0, 0 ],
         [ 5, 2, 0, 0, 0, 0, 0, 0, 0 ],
         [ 0, 8, 7, 0, 0, 0, 0, 3, 1 ],
         [ 0, 0, 3, 0, 1, 0, 0, 8, 0 ],
         [ 9, 0, 0, 8, 6, 3, 0, 0, 5 ],
         [ 0, 5, 0, 0, 9, 0, 6, 0, 0 ],
         [ 1, 3, 0, 0, 0, 0, 2, 5, 0 ],
         [ 0, 0, 0, 0, 0, 0, 0, 7, 4 ],
         [ 0, 0, 5, 2, 0, 6, 3, 0, 0 ] ];

def isvalid(grid, row, col, num):
    #check row
    for i in range(9):
        if grid[row][i]== num:
            return False
    #check column
    for i in range(9):
        if grid[i][col]== num:
            return False

    #check 3x3 block of element
    for i in range(3):
        for j in range(3):
            if grid[i+ (row//3)*3][j+ (col//3)*3]== num:
                return False
    return True


def solve(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                #print(str(row)+str(col), end = "  ")
                for num in range(1,10):
                    if isvalid(grid, row, col, num):
                        
                        grid[row][col]= num
                        grid = solve(grid)
                        grid[row][col] = 0
                return grid
            
    print(grid)
    return grid


anser = solve(board)
print(anser)

    


    
