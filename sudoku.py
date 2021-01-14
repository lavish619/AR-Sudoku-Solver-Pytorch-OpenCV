
grid = [ [ 3, 0, 6, 5, 0, 8, 4, 0, 0 ],
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
            if grid[i+ (row - row%3)][j+ (col - col%3)]== num:
                return False

    return True
    
def solve(grid, x, y):
    print(x,y)
   # print(grid)
    if y==8 and x==9:
        print("yesss")
        #print(grid)
        return True
    
    if x==9:
        x=0
        y=y+1
        
    if grid[x][y]>0:
        solve(grid, x+1 , y)
    
    for i in range(1,10):
        if isvalid(grid, x, y, i):
            grid[x][y] = i
        
            if solve(grid, x+1, y):
                return True
        
        grid[x][y]=0

    return False

def main():
    solve(grid,0,0)
    

if __name__ == '__main__':
    main()
    
