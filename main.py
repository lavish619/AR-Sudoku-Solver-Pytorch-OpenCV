from src.extract import get_sudoku
from src.sudoku import solve, verify
import numpy as np
import copy
import cv2
import math

def write_solution_on_image(image, grid, user_grid):
    # Write grid on image
    SIZE = 9
    width = image.shape[1] // 9
    height = image.shape[0] // 9
    for i in range(SIZE):
        for j in range(SIZE):
            if user_grid[i][j] != 0 :    
                continue          
            text = str(grid[i][j])
            off_set_x = width // 15
            off_set_y = height // 15
            font = cv2.FONT_HERSHEY_SIMPLEX
            (text_height, text_width), baseLine = cv2.getTextSize(text, font, fontScale=1, thickness=3)
            marginX = math.floor(width / 7)
            marginY = math.floor(height / 7)
        
            font_scale = 0.6 * min(width, height) / max(text_height, text_width)
            text_height *= font_scale
            text_width *= font_scale
            bottom_left_corner_x = width*j + math.floor((width - text_width) / 2) + off_set_x
            bottom_left_corner_y = height*(i+1) - math.floor((height - text_height) / 2) + off_set_y
            image = cv2.putText(image, text, (bottom_left_corner_x, bottom_left_corner_y), 
                                                  font, font_scale, (0,0,255), thickness=3, lineType=cv2.LINE_AA)
    return image

def inverse_perspective(img, dst_img, pts):
    pts_source = np.array([[0, 0],  [img.shape[1] - 1, 0], [img.shape[1] - 1, img.shape[0] - 1], [0, img.shape[0] - 1]],
                          dtype='float32')
    
    h, status = cv2.findHomography(pts_source, pts)
    warped = cv2.warpPerspective(img, h, (dst_img.shape[1], dst_img.shape[0]))
    cv2.fillConvexPoly(dst_img, np.ceil(pts).astype(int), 0, 16)
    dst_img = dst_img + warped
    return dst_img


if __name__ == "__main__":
    path1 = r'./images/board.png'
    board, corners, img, warped_img = get_sudoku(path1, show_contours = False, 
                                                show_corners = False, show_grid = False)
    print(board)

    unsolved = copy.deepcopy(board)

    solve(board, 0, 0)
    assert verify(board) == True
    print(np.array(board))

    warped_soln = write_solution_on_image(warped_img, board, unsolved)
    output = inverse_perspective(warped_soln, img, np.array(corners))
    cv2.imwrite("./output/output.jpg", output)