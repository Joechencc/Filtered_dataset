from os import listdir
from os import path
from shutil import copyfile

def filter():
    label_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/labels"
    images_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/images"
    filter_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/filter_labels"
    not_filter_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/non_filter_labels"
    total_count =0
    for f in listdir(label_path):
        with open(path.join(label_path,f)) as file:
            count =0
            for line in file:
                if int(line[0]) == 0:
                    count+=1
                    total_count +=1
            copyfile(path.join(label_path,f),path.join(filter_path,f))

    print("count:"+str(total_count))
                    

if __name__ == '__main__':
    filter()

