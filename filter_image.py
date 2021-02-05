from os import listdir
from os import path
from shutil import copyfile

def filter():
    label_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/labels"
    images_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/images"
    filter_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/filter_labels"
    filter_image_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/filter_images"
    not_filter_path = "/home/cchen_backup/Desktop/DoorDetect-Dataset/non_filter_labels"
    for f in listdir(label_path):
        with open(path.join(label_path,f)) as file:
            filename = f.split(".")[0]
            picture_name = filename + ".jpg"
            picture_name2 = filename + ".JPG"
            picture_name3 = filename + ".jpeg"
            for line in file:
                if int(line[0]) == 0:
                    try:
                        copyfile(path.join(images_path,picture_name),path.join(filter_image_path,picture_name))
                    except:
                        pass
                    try:
                        copyfile(path.join(images_path,picture_name2),path.join(filter_image_path,picture_name2))
                    except:
                        pass
                    try:
                        copyfile(path.join(images_path,picture_name3),path.join(filter_image_path,picture_name3))
                    except:
                        pass
                    break


                    

if __name__ == '__main__':
    filter()

