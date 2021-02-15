from os import listdir, path
import cv2
import os
import numpy as np

def visualize():
    desktop = path.join(path.join(path.expanduser('~')), 'Desktop') 
    images_path = desktop+"/Filtered_dataset/scaled_images_backup"
    new_label_path = desktop+"/Filtered_dataset/labels"
    image_p =path.join(images_path,"91abd3f94ecdf3bb.jpg")
    image = cv2.imread(image_p)
    height = image.shape[0]
    width = image.shape[1]
    with open(path.join(new_label_path,"91abd3f94ecdf3bb.txt")) as fp:
        line = fp.readline()
        while line:
            x = line.split(" ")[1]
            y = line.split(" ")[2]
            wid = line.split(" ")[3]
            hgt = line.split(" ")[4]

            #print("line::"+str(line.split(" ")))
            cv2.rectangle(image, (int(float(x)*width-float(wid)/2*width),int(float(y)*height-float(hgt)*height/2)), (int(float(x)*width+float(wid)/2*width),int(float(y)*height+float(hgt)*height/2)), (255,0,0), -1)
            line = fp.readline()

    cv2.namedWindow("image")
    cv2.imshow("image", image)
    cv2.waitKey(30000) & 0xFF

    
if __name__ == '__main__':
    visualize()

