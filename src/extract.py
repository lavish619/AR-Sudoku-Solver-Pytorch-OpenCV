import cv2
import numpy as np
from math import floor

from src.classify import classify_digits

def show_image(img):
    '''function to show an image'''
    
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def display_contours(img, contours, color = (0,255 , 0), thickness = 2 ):
    '''function to display identified contours of sudoku board'''
    
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    cont_image = cv2.drawContours(img, contours, -1, color, thickness)
    show_image(cont_image)


def display_corners(img, corners, colour=(0, 0, 255),radius=7):
    '''function to display corners of sudoku board'''
    
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    for corner in corners:
        img = cv2.circle(img, tuple(corner), radius, colour, -1)
    show_image(img)

    
def read_process_image(path):
    img = cv2.imread(path, 0) #0 is flag for grayscale(cv2.IMREAD_GRAYSCALE)

    #gaussian blurring
    kernel_size = (9,9) #Tried other values but found (9,9)is the best kernel size.
    img = cv2.GaussianBlur(img, kernel_size, 0)
    
    #thresholding
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Now to make text and gridlines more bolder.we will do erosion so
    # that zero(black) pixel values of text and gridlines will erode the non-zero(white)
    #pixel values and text becomes bolder.
    kernel = np.ones((2,2),np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel) #erosion followed by dilation (cv2.MORPH_OPEN)

    return img
    
def get_contours(img, show_contours):

    #for contour detection, it needs object to be white present in a black background.
    # so, first we will invert the image.
    img = cv2.bitwise_not(img,img)
    
    # now find contours
    #outer contours(boundry of sudoku)
    ext_contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #all contours(numbers, grid lines)
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Now invert the image again after finding contours
    img = cv2.bitwise_not(img,img)
    
    if show_contours:
        display_contours(img, ext_contours)
        display_contours(img, contours)

    # we need only external contours
    return img, ext_contours

def get_corners(img, contours, show_corners):
    contours = sorted(contours, key=cv2.contourArea)# Sorting contours by area in ascending order
    box = contours[-1]
##    print(box) #printing the box will help in understanding the code written below to find corners.
    

    #A function to obtain the element at 1st position of an element
    #because 1st element will be used as a key to for finding max/min of points below.
    def func(x):
        return x[1]

    # Bottom-right point has the largest (x + y) value
    # Top-left has point smallest (x + y) value
    # Bottom-left point has smallest (x - y) value
    # Top-right point has largest (x - y) value
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in box]), key=func)
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in box]), key=func)
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in box]), key=func)
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in box]), key=func)

    #x, y coordinates of 4 corner points
    bottom_right = box[bottom_right][0]
    top_left = box[top_left][0]
    bottom_left = box[bottom_left][0]
    top_right = box[top_right][0]

    corners = (top_left, top_right, bottom_left, bottom_right)

    if show_corners:
        display_corners(img, corners)

    return corners

def get_cropimage(img, corners):

    top_left, top_right, bottom_left, bottom_right = corners
    
    def distance_between(p1, p2):
        #Gives the distance between two pixels
        a = p2[0] - p1[0]
        b = p2[1] - p1[1]
        return np.sqrt((a ** 2) + (b ** 2))
    
    input_pts = np.array([top_left+3, top_right, bottom_left, bottom_right], dtype= 'float32')

    # Get the longest length in the rectangle
    length = max([
            distance_between(bottom_right, top_right),
            distance_between(top_left, bottom_left),
            distance_between(bottom_right, bottom_left),
            distance_between(top_left, top_right)
            ])
    
    length = length -5 #this is done to slightly compensate for the thick outer gridline

    output_pts = np.array([[0,0],[length,0],[0,length],[length,length]], dtype= 'float32')

    # Gets the transformation matrix for skewing the image to
    # fit a square by comparing the 4 before and after points
    m = cv2.getPerspectiveTransform(input_pts, output_pts)

    # Performs the transformation on the original image
    warped = cv2.warpPerspective(img, m, (int(length), int(length)))
##    warped = cv2.cvtColor(warped, cv2.COLOR_GRAY2BGR)
    return warped

def display_gridlines(img, color = (255,0,0)):
    
    side = img.shape[0]/9
    side = int(side)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for i in range(9):
        img = cv2.line(img, (floor(side*(i+1)),0),(floor(side*(i+1)),floor(side*9)), color)
        img = cv2.line(img, (0,floor(side*(i+1))),(floor(side*9),floor(side*(i+1))), color)
    show_image(img)
    
def obtain_grid(img, show_grid):
    """Infers 81 cell grid from a square image."""
    grid_nums = []
    side = img.shape[0]/9
    side = int(side)
    for i in range(9):
        for j in range(9):
            cell = img[side*i:side*(i+1), side*j:side*(j+1)]
            grid_nums.append(cell)
    
    if show_grid:
        display_gridlines(img)
    
    return grid_nums        
        
def get_sudoku(path, show_contours = False, show_corners = False, show_grid = False):
    img = read_process_image(path)
    img, ext_contours = get_contours(img, show_contours)
    corners = get_corners(img, ext_contours, show_corners)
    image = get_cropimage(img, corners)
    num_imgs = obtain_grid(image, show_grid)
    
    labels = classify_digits(num_imgs)
    
    return labels
