import torch
import numpy as np
import cv2
from src.model import Model

MODEL_PATH= "model.pt"

def classify_digits(images):
    threshold = 20
    image_count = -1
    labels = np.zeros((9,9), dtype = int)
    model = Model(1,10)
    model.load_state_dict(torch.load(MODEL_PATH, map_location = torch.device("cpu")))
    
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
        image = cv2.resize(image, (32,32))/255.0
        image = torch.tensor(image, dtype = torch.float)
        image = image.unsqueeze(0)
        image = image.unsqueeze(1)
        label = np.argmax(model(image).detach().numpy(), axis=-1)
#         print(label)
        labels[image_count//9, image_count%9] = label
        
        
    return labels