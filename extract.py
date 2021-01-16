import cv2
import numpy as np

path = r'C:\Users\asus\Desktop\Sudoku-Solver\board.png'

def show_image(img):
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def display_contours(img, contours, color = (0,255 , 0), thickness = 2 ):
    cont_image = cv2.drawContours(img, contours, -1, color, thickness)
    show_image(cont_image)

def display_corners(img, corners, colour=(0, 0, 255),radius=10):
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for corner in corners:
        #print(corner)
        img = cv2.circle(img, tuple(corner), radius, colour, -1)
    show_image(img)
    
def read_process_image(path):
    img = cv2.imread(path, 0) #0 is flag for grayscale(cv2.IMREAD_GRAYSCALE)

    #gaussian blurring
    kernel_size = (9,9) #Tried other values but found (9,9)is the best kernel size.
    img = cv2.GaussianBlur(img.copy(), kernel_size, 0)
    
    #thresholding
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Now to make text and gridlines more bolder.we will do erosion so
    # that zero pixel values of text, gridlines will erode the non-zero
    #pixel values and text becomes bolder.
    kernel = np.ones((2,2),np.uint8)
    img = cv2.erode(img,kernel,iterations = 1)

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

    if show_contours:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        display_contours(img, ext_contours)
        display_contours(img, contours)

    # we need only external contours
    return img, ext_contours

def get_corners(img, contours, show_corners):
    contours = sorted(contours, key=cv2.contourArea)# Sorting contours by area in ascending order
    box = contours[-1]
##    print(box) #printing this box will help in understanding the code written below to find corners.
    

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
    
def get_sudoku(path, show_contours = False, show_corners = False):
    img = read_process_image(path)
    img, ext_contours = get_contours(img, show_contours)
    corners = get_corners(img.copy(), ext_contours, show_corners)
    #print(corners)
    
    
    

get_sudoku(path,show_contours = False, show_corners = False)

