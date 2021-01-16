import cv2
import numpy as np

path = r'C:\Users\asus\Desktop\Sudoku-Solver\board.png'
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
    

def get_contours(img):
    pass
    
def get_sudoku(path):
    img = read_process_image(path)
    get_contours(img)
    
    

get_sudoku(path)

