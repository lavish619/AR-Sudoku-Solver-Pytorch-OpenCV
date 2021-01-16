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

    #for contour detection, it needs object to be found as white in a black background.
    # so, first we will invert the image.
    img = cv2.bitwise_not(img,img)
    
    # now find contours
    #outer contours(boundry of sudoku)
    ext_contours, heirarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #all contours(numbers, grid lines)
    contours, heirarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

##    img2 = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
##    ext_cont_image = cv2.drawContours(img2.copy(), ext_contours, -1, (0, 255, 0), 2)
##    all_cont_image = cv2.drawContours(img2.copy(), contours, -1, (0, 255, 0), 2)
    
##    cv2.imshow("external_contours",ext_cont_image)
##    cv2.imshow("all_contours",all_cont_image)
##    
##    cv2.waitKey(0)
    
    return img, ext_contours 
    
def get_sudoku(path):
    img = read_process_image(path)
    img, ext_contours = get_contours(img)
    
    

get_sudoku(path)

