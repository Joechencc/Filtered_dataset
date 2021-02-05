from os import listdir
from os import path
from shutil import copyfile

def filter():
    label_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/labels"
    images_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/images"
    filter_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/filter_labels"
    not_filter_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/non_filter_labels"
    for f in listdir(label_path):
        with open(path.join(label_path,f)) as file:
            for line in file:
                if int(line[0]) == 0:
                    copyfile(path.join(label_path,f),path.join(filter_path,f))
                    break


                    

if __name__ == '__main__':
    filter()

