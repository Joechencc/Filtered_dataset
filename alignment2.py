from os import listdir
from os import path
from shutil import copyfile
import os

def filter():
    desktop = os.path.expanduser("~/Desktop")
    label_path_old = desktop + "/Filtered_dataset/filter_labels"
    label_path = desktop + "/Filtered_dataset/new_labels"
    for f in listdir(label_path_old):
        if not os.path.isfile(path.join(label_path,f)):
            print("f"+str(f))
            #print("os.path.isfile(path.join(label_path,text_msg):"+str(not os.path.isfile(path.join(label_path,text_msg))))
            os.remove(path.join(label_path_old,f))
            

if __name__ == '__main__':
    filter()
