from os import listdir
from os import path
from shutil import copyfile
import os

def filter():
    desktop = os.path.expanduser("~/Desktop")
    images_path = desktop + "/Filtered_dataset/scaled_images"
    label_path = desktop + "/Filtered_dataset/new_labels"
    for f in listdir(images_path):
        text_msg = f.split(".")[0]+".txt"
        if not os.path.isfile(path.join(label_path,text_msg)):
            #print("os.path.isfile(path.join(label_path,text_msg):"+str(not os.path.isfile(path.join(label_path,text_msg))))
            os.remove(path.join(images_path,f))
            

if __name__ == '__main__':
    filter()
