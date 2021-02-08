from os import listdir, path
from shutil import copyfile
import cv2

def filter():
    desktop = path.join(path.join(path.expanduser('~')), 'Desktop') 
    label_path = desktop+"/Filtered_dataset/labels"
    images_path = desktop+"/Filtered_dataset/images"
    new_label_path = desktop+"/Filtered_dataset/new_labels"
    mode = "view"

    for f in listdir(images_path):
        new_label = f.split(".")[0] + ".txt"
        image_p =path.join(images_path,f)
        image = cv2.imread(image_p)
        with open(path.join(new_label_path,f), "w") as output: 
            while True:
		# display the image and wait for a keypress
                cv2.imshow("image", image)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q") and mode == "view":
                    return
                elif (key == ord("n") or key == ord(" ")) and mode == "view":
                    break
                elif key == ord("e"):
                    mode = "edit"
                elif key == ord("v"):
                    mode = "view"

if __name__ == '__main__':
    filter()

