import torch
import numpy as np
import cv2
from src.model import Model

MODEL_PATH= "model.pt"
model = Model()

def classify_digits(images):
    threshold = 20
    image_count = -1
    labels = np.zeros((9,9), dtype = int)
    model.load_state_dict(torch.load(MODEL_PATH))
    model = model.to(torch.device("cpu"))
    
    for image in images:
        '''Initally we classify all blank cells as zeros so counting number of black pixels
        in an image and setting a threshold value for it can help us identify it.

        Then for every cell containing a number, we will use a pretrained model on mnist dataset
        to identify the digit'''
        
        #removing border strips of cells that might contain grid line pixel values
        image = image[10:-10, 10:-10]
        
        flat_image = np.ndarray.flatten(image)
        image_count = image_count + 1
        #count number of black pixels i.e. numbers
        count =0
        for pixel in flat_image:
            if pixel==0:
                count = count+1
        #print(count,end =" " )
        
        if count< threshold:
            #if it's a blank cell, take it as zero in the labels.
            continue
        
        #resize to standard mnist image input size
        image = cv2.resize(image, (28,28))
        image = np.expand_dims(image,axis=-1)
        image = image.reshape([1]+list(image.shape))        
        label = np.argmax(model.predict(image), axis=-1)
#         print(label)
        labels[image_count//9, image_count%9] = label
        
        
    return labels