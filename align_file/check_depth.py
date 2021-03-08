from os import path, listdir
import os
import cv2


#func for getting color of click pos
def click_pos(event, x, y, flags, param):
	global mouseX , mouseY
	global min_h,max_h,min_s,max_s,min_v,max_v, image
	if event == cv2.EVENT_LBUTTONDOWN:
		mouseX, mouseY = x, y
		print("x::"+str(x))
		print("y::"+str(y))
		print("image::"+str(image[y,x]))
	else:
		pass


if __name__ == '__main__':
    desktop = os.path.expanduser("~/Desktop")
    align_path = desktop+"/align_file"
    image_path = align_path +"/save_file_1_depth"
    image_path_color = align_path +"/save_file_bkup"

    for f in listdir(image_path_color):
        if (f == "image_153_14.41.jpg"):
            array = f.split("_")
            array[0] = "depth"
            f = "_".join(array)
            image = cv2.imread(path.join(image_path,f))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow("image",image)
            print("depth:::"+str(image[160,16]))
            cv2.setMouseCallback('image', click_pos)
            cv2.waitKey(30000)