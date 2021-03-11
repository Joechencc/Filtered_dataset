from os import listdir
from os import path
from shutil import copyfile
import os

def filter():
    desktop = os.path.expanduser("~/Desktop")
    label_path_o = desktop + "/Filtered_dataset/fused_label"
    label_path = desktop + "/Filtered_dataset/fused_label2"
    for f in listdir(label_path_o):
        with open(path.join(label_path_o,f),'r') as infile:
            with open(path.join(label_path,f),'w') as outfile:
                lines = infile.readlines()
                for line in lines:
                    lines_array = line.split(" ")
                    element1 = lines_array[0]
                    element2 = lines_array[1]
                    element3 = lines_array[2]
                    element4 = lines_array[3]
                    element5 = lines_array[4]
                    if int(element1) == 1:
                        element1 = 0
                    elif int(element1) == 2:
                        element1 = 1
                    elif int(element1) == 3:
                        element1 = 2
                    elif int(element1) == 4:
                        element1 = 3
                    elif int(element1) == 5:
                        element1 = 4
                    elif int(element1) == 6:
                        element1 = 5
                    elif int(element1) == 7:
                        element1 = 6
                    elif int(element1) == 8:
                        element1 = 7
                    elif int(element1) == 9:
                        element1 = 8
                    elif int(element1) == 10:
                        element1 = 9
                    elif int(element1) == 11:
                        element1 = 10
                    elif int(element1) == 0:
                        continue

                    outfile.write(str(element1)+" "+ str(element2) + " "+str(element3)+" "+element4+" "+element5)
                
            

if __name__ == '__main__':
    filter()
