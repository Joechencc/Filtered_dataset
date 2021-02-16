from os import listdir
from os import path
from shutil import copyfile
import os

def filter():
    desktop = os.path.expanduser("~/Desktop")
    label_path1 = desktop + "/Filtered_dataset/filter_labels"
    label_path2 = desktop + "/Filtered_dataset/new_labels2"
    outlabel_path = desktop + "/Filtered_dataset/fused_label"
    for f in listdir(label_path1):
        with open(path.join(label_path1,f),'r') as infile_1:
            with open(path.join(label_path2,f),'r') as infile_2:
                with open(path.join(outlabel_path,f),'w') as outfile:
                    lines1 = infile_1.readlines()
                    lines2 = infile_2.readlines()
                    for line1 in lines1:
                        outfile.write(line1)
                    for line2 in lines2:
                        outfile.write(line2)

           
            

if __name__ == '__main__':
    filter()
