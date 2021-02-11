from os import listdir, path
from shutil import copyfile
import cv2
import os
import signal
import sys

count = 0

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    global label_path
    os.remove(global_label)
    sys.exit(0)

# param contains the center and the color of the circle 
def click_and_crop(event, x, y, flags, param):
    global count
    global width
    global height
    if event ==cv2.EVENT_LBUTTONDOWN:
        #count : 1-7 hinge frameOT frameOB doorHT doorHB doorOT doorOB
        if count == 4:
            #1 0.521094 0.727778 0.028125 0.033333
            print("frame Open top, current mode count:"+str(count))
            cv2.rectangle(image,(x-10,y-10),(x+10,y+10),(255,0,0),-1)
            #print("x:::::"+str(x/width))
            #print("y:::::"+str(y/height))
            output.write("4 "+str((x)/width)+" "+str((y)/height)+" "+str(20/width)+" "+str(20/height)+"\n")
        elif count == 5:
            print("frame Open Bottom, current mode count:"+str(count))
            cv2.rectangle(image,(x-10,y-10),(x+10,y+10),(255,0,0),-1)
            output.write("5 "+str((x)/width)+" "+str((y)/height)+" "+str(20/width)+" "+str(20/height)+"\n")
        elif count == 6:
            print("Door Hinge Top, current mode count:"+str(count))
            cv2.rectangle(image,(x-10,y-10),(x+10,y+10),(255,0,0),-1)
            output.write("6 "+str((x)/width)+" "+str((y)/height)+" "+str(20/width)+" "+str(20/height)+"\n")
        elif count == 7:
            print("Door Hinge Bottom, current mode count:"+str(count))
            cv2.rectangle(image,(x-10,y-10),(x+10,y+10),(255,0,0),-1)
            output.write("7 "+str((x)/width)+" "+str((y)/height)+" "+str(20/width)+" "+str(20/height)+"\n")
        elif count == 8:
            print("Door Open Top, current mode count:"+str(count))
            cv2.rectangle(image,(x-10,y-10),(x+10,y+10),(255,0,0),-1)
            output.write("8 "+str((x)/width)+" "+str((y)/height)+" "+str(20/width)+" "+str(20/height)+"\n")
        elif count == 9:
            print("Door Open Bottom, current mode count:"+str(count))
            cv2.rectangle(image,(x-10,y-10),(x+10,y+10),(255,0,0),-1)
            output.write("9 "+str((x)/width)+" "+str((y)/height)+" "+str(20/width)+" "+str(20/height)+"\n")
        elif count == 0:
            print("frame Hinge top, current mode count:"+str(count))
            cv2.rectangle(image,(x-10,y-10),(x+10,y+10),(255,0,0),-1)
            output.write("10 "+str((x)/width)+" "+str((y)/height)+" "+str(20/width)+" "+str(20/height)+"\n")
        elif count == 1:
            print("frame Hinge Bottom, current mode count:"+str(count))
            cv2.rectangle(image,(x-10,y-10),(x+10,y+10),(255,0,0),-1)
            output.write("11 "+str((x)/width)+" "+str((y)/height)+" "+str(20/width)+" "+str(20/height)+"\n")
        elif count == 2:
            print("label hinge left upper, current mode count:"+str(count))
            global hinge_x_l,hinge_y_r
            hinge_x_l=x
            hinge_y_r=y
        elif count == 3:
            print("label hinge lower bottom, current mode count:"+str(count))
            output.write("3 "+str(x/width+(x-hinge_x_l)/(2*width))+" "+str(y/height+(y-hinge_y_r)/(2*height))+" ")
            output.write(str((x-hinge_x_l)/width)+" "+str((y-hinge_y_r)/height)+"\n")
        else:
            print("count::"+str(count))
            print("error")
       # print("image::::"+str(image))
       # print("x::::::::::"+str(x))
       # print("y::::::::::"+str(y))
       # print("flags::::::::::"+str(flags))
       # print("param::::::::::"+str(param))



def filter():
    desktop = path.join(path.join(path.expanduser('~')), 'Desktop') 
    label_path = desktop+"/Filtered_dataset/labels"
    images_path = desktop+"/Filtered_dataset/scaled_images"
    new_label_path = desktop+"/Filtered_dataset/new_labels"
    mode = "view"

    for f in listdir(images_path):
        new_label = f.split(".")[0] + ".txt"
        image_p =path.join(images_path,f)
        global image
        global output
        global height,width
        global global_label
        global_label = path.join(new_label_path,new_label)
        image = cv2.imread(image_p)
        height = image.shape[0]
        width = image.shape[1]
        with open(path.join(new_label_path,new_label), "w") as output: 
            cv2.namedWindow("image")
            cv2.setMouseCallback("image", click_and_crop)
            global count
            count = 0
            print("------------------------------------------------------")
            print("The current image is "+str(f))
            print("Click on frame Open top please")
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
                elif key == ord("4"):
                    count = 4
                elif key == ord("5"):
                    count = 5
                elif key == ord("6"):
                    count = 6
                elif key == ord("7"):
                    count = 7
                elif key == ord("8"):
                    count = 8
                elif key == ord("9"):
                    count = 9
                elif key == ord("2"):
                    count = 2
                elif key == ord("3"):
                    count = 3
                elif key == ord("0"):
                    count = 0
                elif key == ord("1"):
                    count = 1
        print("saved as "+str(new_label))
        done_flag = input("Are you satisfy with this labelling? y/n:::")
        if done_flag == 'y':
            os.remove(path.join(images_path,f))
        else:
            os.remove(path.join(new_label_path,new_label))
            
        print("------------------------------------------------------")  

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    filter()

