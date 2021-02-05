from os import listdir
from os import path
from shutil import copyfile

def filter():
    label_path = "/home/cchen_backup/Desktop/Filtered_dataset/labels"
    images_path = "/home/cchen_backup/Desktop/Filtered_dataset/images"
    new_label_path = "/home/cchen_backup/Desktop/Filtered_dataset/new_labels"

    for f in listdir(label_path):
        with open(path.join(label_path,f), "r") as file:
            with open(path.join(new_label_path,f), "w") as output: 
                for line in file:
                    if int(line[0]) == 0:
                        output.write(line)
                    elif int(line[0]) == 1:
                        output.write(line)


                    

if __name__ == '__main__':
    filter()

