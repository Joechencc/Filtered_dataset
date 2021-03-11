from os import listdir
from os import path
from shutil import copyfile
import os
import cv2
from PIL import Image
import scipy

def filter():
    desktop = os.path.expanduser("~/Desktop/Filtered_dataset")
    label_path = desktop+"/labels"
    images_path = desktop+"/images"
    scaled_images_path = desktop+"/scaled_images"
    filter_path = desktop+"/filter_labels"
    new_path_path = desktop+"/new_labels"
    for f in listdir(images_path):
        src = cv2.imread(path.join(images_path,f),cv2.IMREAD_UNCHANGED)
        scale_percent = 50
        width = int(src.shape[1] * scale_percent / 100)
        height = int(src.shape[0] * scale_percent / 100) 
        dsize = (width, height)
        while height > 480:
            src = cv2.resize(src, dsize)
            height = int(src.shape[0] * scale_percent / 100) 
            width = int(src.shape[1] * scale_percent / 100)
            dsize = (width, height)
        cv2.imwrite(path.join(scaled_images_path,f),src)
            
        


                    

if __name__ == '__main__':
    filter()

