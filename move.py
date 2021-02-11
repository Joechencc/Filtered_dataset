from os import listdir
from os import path
from shutil import copyfile
import os
import cv2
from PIL import Image
import scipy

def filter():
    desktop = os.path.expanduser("~/Desktop/Filtered_dataset")
    filter_path = desktop+"/new_labels_modified"
    new_path_path = desktop+"/new_labels"
    for f in listdir(new_path_path):
        with open(path.join(new_path_path,f),'r') as infile:
            with open(path.join(filter_path,f),'w') as outfile:
                lines = infile.readlines()
                for line in lines:
                    lines_array = line.split(" ")
                    element1 = lines_array[0]
                    element4 = lines_array[3]
                    element5 = lines_array[4]
                    element2 = float(lines_array[1]) + float(element4)/2
                    element3 = float(lines_array[2]) + float(element5)/2
                    outfile.write(element1+" "+ str(element2) + " "+str(element3)+" "+element4+" "+element5)
                
        
            
        


                    

if __name__ == '__main__':
    filter()

