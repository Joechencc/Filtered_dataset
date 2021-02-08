from os import listdir, path
from shutil import copyfile

def filter():
    desktop = path.join(path.join(path.expanduser('~')), 'Desktop') 
    label_path = desktop+"/Filtered_dataset/labels"
    images_path = desktop+"/Filtered_dataset/images"
    new_label_path = desktop+"/Filtered_dataset/new_labels"

    for f in listdir(images_path):
        new_label = f.split(".")[0] + ".txt"
        print("new_label::::::::::"+str(new_label))
        with open(path.join(new_label_path,f), "w") as output: 
            pass

if __name__ == '__main__':
    filter()

