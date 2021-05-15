def verify(solved_puzzle):
    for i in range(9):
        if sum(get_row(solved_puzzle, i)) != 45:
            return False
        if sum(get_column(solved_puzzle, i)) != 45:
            return False
        if sum(get_square(solved_puzzle, i, i)) != 45:
            return False
    return True

def get_row(puzzle, row_num):
    return puzzle[row_num]

def get_column(puzzle, col_num):
    return [puzzle[i][col_num] for i, _ in enumerate(puzzle[0])]

def get_square(puzzle, row_num, col_num):
    square_x = row_num // 3
    square_y = col_num // 3
    coords = []
    for i in range(3):
        for j in range(3):
            coords.append((square_x * 3 + j, square_y * 3 + i))
    return [puzzle[i[0]][i[1]] for i in coords]


N=9
def isSafe(grid, row, col, num):

	for x in range(9):
		if grid[row][x] == num:
			return False

	for x in range(9):
		if grid[x][col] == num:
			return False

	startRow = row - row % 3
	startCol = col - col % 3
	for i in range(3):
		for j in range(3):
			if grid[i + startRow][j + startCol] == num:
				return False
	return True

def solve(grid, row, col):

	if (row == 8 and col == 9):
		return True
	
	if col == 9:
		row += 1
		col = 0

	if grid[row][col] > 0:
		return solve(grid, row, col + 1)
	for num in range(1, 10):
	
		if isSafe(grid, row, col, num):
			grid[row][col] = num

			if solve(grid, row, col + 1):
				return True

		grid[row][col] = 0
	return False