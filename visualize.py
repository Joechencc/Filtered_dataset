from os import listdir, path
import cv2
import os
import numpy as np

def visualize():
    desktop = path.join(path.join(path.expanduser('~')), 'Desktop') 
    images_path = desktop+"/Filtered_dataset/save_file_1_bk"
    new_label_path = desktop+"/Filtered_dataset/lab_label"
    image_p =path.join(images_path,"image_26_2.08.jpg")
    image = cv2.imread(image_p)
    height = image.shape[0]
    width = image.shape[1]
    with open(path.join(new_label_path,"image_26_2.08.txt")) as fp:
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

