from os import path, listdir
import os
import numpy as np
import cv2
from scipy.spatial.transform import Rotation as R
from numpy.linalg import inv
import time, math
import rospy
from sensor_msgs.msg import CameraInfo

class rigid_body:
    rigid_ID = 0
    tracked = True
    x = 0
    y = 0
    z = 0
    qx = 0
    qy = 0
    qz = 0
    qw = 0

#func for getting color of click pos
def click_pos(event, x, y, flags, param):
	global mouseX , mouseY
	global min_h,max_h,min_s,max_s,min_v,max_v
	if event == cv2.EVENT_LBUTTONDOWN:
		mouseX, mouseY = x, y
		print("x,y::"+str(x)+","+str(y))
	else:
		pass

def cb_once(msg):    
    print("msg:::"+str(msg))
    sub_once.unregister()

def compute_coord(obj_list,Mocap_bag_path,f):
    # print("obj_list.len::::::"+str(len(obj_list)))

    print("f:::::::::"+str(f))
    r1 = obj_list[0]   # lu frame corner
    r2 = obj_list[1]   # lu door corner
    r3 = obj_list[2]   # ru door corner
    r4 = obj_list[3]   # ru frame corner
    r5 = obj_list[4]   # rd door corner
    r6 = obj_list[5]   #camera
    image_path = Mocap_bag_path +"/Mocap_cc_test5/Mocap_color"
    depth_path = Mocap_bag_path +"/Mocap_cc_test5/Mocap_depth_test5"

    # image = cv2.imread(path.join(image_path,f))
    # cv2.imshow("image", image)
    # cv2.setMouseCallback('image', click_pos)
    # cv2.waitKey(30000) & 0xFF

    depth_file_array = f.split("_")
    depth_file_array[0] = "depth"
    depth_file = "_".join(depth_file_array)
    depth_image = cv2.imread(path.join(depth_path,depth_file))
    depth_image = cv2.cvtColor(depth_image,cv2.COLOR_BGR2GRAY)

    # print("depth_image::"+str(depth_image))

    
    r1_array = np.array([[r1.x], [r1.y], [r1.z], [1]])
    # print("r1_array::::"+str(r1_array))
    r2_array = np.array([[r2.x], [r2.y], [r2.z], [1]])
    #print("r1_array:::"+str(r1_array))
    r3_array = np.array([[r3.x], [r3.y], [r3.z], [1]])
    r4_array = np.array([[r4.x], [r4.y], [r4.z], [1]])
    r5_array = np.array([[r5.x], [r5.y], [r5.z], [1]])
    r6_array = np.array([[r6.x], [r6.y], [r6.z]])

#####
    #lfd_array = np.array([[-0.54067284], [-0.0111583145], [-0.59584385], [1]])
    #rfu_array = np.array([[-0.47726107], [-2.0054173], [-1.5429099], [1]])
    #rfd_array = np.array([[-0.52493185], [-0.0029689868], [-1.4633833], [1]])
#####
    K = np.array([[602.25927734375, 0.0, 321.3750915527344], [0.0,  603.0400390625, 240.51527404785156], [0.0, 0.0, 1.0]])  #intrinsic
    P = [[1,0,0,0],[0,1,0,0],[0,0,1,0]]

    T = R.from_quat([r6.qx, r6.qy, r6.qz, r6.qw]).as_matrix() #extrinsic rotation
    T = np.hstack((T,r6_array)) #extrinsic translation
    T = np.append(T, [[0,0,0,1]], axis=0) 
    # print("T_before::::::"+str(T))
    T = inv(T)
    # print("T::::::"+str(T))

    #T_compensate = R.from_quat([0.7071, 0 ,0.7071 ,0]).as_matrix() #extrinsic rotation
    #T_compensate = R.from_quat([0.2027, 0 ,0.7863 ,-0.5836]).as_matrix() #extrinsic rotation

    #compensate_array = np.array([[0.2], [-0.4], [-0.8]])
    #print(compensate_array)

    #T_compensate = np.hstack((T_compensate, compensate_array)) #extrinsic translation
    #T_compensate = np.append(T_compensate, [[0,0,0,1]], axis=0)
    #print("T_compensate_r1:::"+str(P @ T @ r1_array))
    #print("T_compensate_r2:::"+str(P @ T @ r2_array))

    # print("depth_image[6,337]"+str(depth_image[6,337]))
    # print("depth_image[46,432]"+str(depth_image[46,432]))
    # print("depth_image[450,340]"+str(depth_image[450,340]))

    # print("r2_array::::"+str(r2_array))
    # print("r3_array::::"+str(r3_array))
    # print("r5_array::::"+str(r5_array))
    global T0
    # print("T0::::"+str(T0))
    if T0 is None:
        r2_transform = np.array([[46],[280],[1]])* depth_image[46,280]
        r3_transform = np.array([[50],[429],[1]])* depth_image[50,429]
        r5_transform = np.array([[410],[281],[1]])* depth_image[410,281]

        b1 = np.linalg.pinv(T) @ np.linalg.pinv(P) @ np.linalg.pinv(K) @ r2_transform
        b2 = np.linalg.pinv(T) @ np.linalg.pinv(P) @ np.linalg.pinv(K) @ r3_transform
        b3 = np.linalg.pinv(T) @ np.linalg.pinv(P) @ np.linalg.pinv(K) @ r5_transform
        b1 = b1/ b1[3]
        b2 = b2/ b2[3]
        b3 = b3/ b3[3]

        b = np.vstack((b1[0:3],b2[0:3],b3[0:3]))
        A1 = [[r2.x, r2.y, r2.z, 1, 0, 0, 0, 0, 0, 0, 0, 0 ], [0, 0, 0, 0, r2.x, r2.y, r2.z, 1, 0, 0, 0, 0 ], [0, 0, 0, 0, 0, 0, 0, 0, r2.x, r2.y, r2.z, 1]]
        A2 = [[r3.x, r3.y, r3.z, 1, 0, 0, 0, 0, 0, 0, 0, 0 ], [0, 0, 0, 0, r3.x, r3.y, r3.z, 1, 0, 0, 0, 0 ], [0, 0, 0, 0, 0, 0, 0, 0, r3.x, r3.y, r3.z, 1]]
        A3 = [[r5.x, r5.y, r5.z, 1, 0, 0, 0, 0, 0, 0, 0, 0 ], [0, 0, 0, 0, r5.x, r5.y, r5.z, 1, 0, 0, 0, 0 ], [0, 0, 0, 0, 0, 0, 0, 0, r5.x, r5.y, r5.z, 1]]
        A = np.vstack((A1,A2,A3))

        # print("b1::::::"+str(b1))
        x = np.linalg.pinv(np.transpose(A) @ A) @ np.transpose(A) @ b
        T0 = np.array([[float(x[0]),float(x[1]),float(x[2]),float(x[3])],[float(x[4]),float(x[5]),float(x[6]),float(x[7])],[float(x[8]),float(x[9]),float(x[10]),float(x[11])],[0,0,0,1]])

    r2_transform = K @ P @ T @ T0 @ r2_array
    r2_transform = r2_transform/r2_transform[2]
    
    r3_transform = K @ P @ T @ T0 @ r3_array
    r3_transform = r3_transform/r3_transform[2]
    
    r5_transform = K @ P @ T @ T0 @ r5_array
    r5_transform = r5_transform/r5_transform[2]

    # print("r2_transform::"+str(r2_transform))
    # print("r3_transform::"+str(r3_transform))
    # print("r5_transform::"+str(r5_transform))

    # print("x:::::::"+str(x))

    # r2_transform = np.array([[6],[337],[1]])* depth_image[6,337]
    # r3_transform = np.array([[46],[433],[1]])* depth_image[46,432]
    # r5_transform = np.array([[450],[340],[1]])* depth_image[450,340]


    # external_2 = np.linalg.pinv(P) @ np.linalg.pinv(K) @ r2_transform @ np.linalg.pinv(r2_array)
    # external_3 = np.linalg.pinv(P) @ np.linalg.pinv(K) @ r3_transform @ np.linalg.pinv(r3_array)
    # external_5 = np.linalg.pinv(P) @ np.linalg.pinv(K) @ r5_transform @ np.linalg.pinv(r5_array)

    # r2_transform = K @ P @ external_2 @ r2_array
    # r2_transform = r2_transform/r2_transform[2]
    # print("r2_transform:::::"+str(r2_transform))

    # r3_transform = K @ P @ external_3 @ r3_array
    # r3_transform = r3_transform/r3_transform[2]
    # print("r3_transform:::::"+str(r3_transform))

    # r5_transform = K @ P @ external_5 @ r5_array
    # r5_transform = r5_transform/r5_transform[2]
    # print("r5_transform:::::"+str(r5_transform))


    # print("external_2:::"+str(external_2))
    # print("external_3:::"+str(external_3))
    # print("external_5:::"+str(external_5))

    # print("r2_transform::"+str(r2_transform))

    # r2_transform = K @ P @ T @ r1_array
    # r2_transform = r2_transform/r2_transform[2]
    
    # r3_transform = K @ P @ T @ r2_array
    # r3_transform = r3_transform/r3_transform[2]
    
    # r5_transform = K @ P @ T @ r2_array
    # r5_transform = r5_transform/r5_transform[2]

    
    
    #print("r2_transform:::"+str(r2_transform))np.linalg.pinv(P)np.linalg.pinv(P)
    """
    lfd_transform = K @ P @ T_compensate @ T @ lfd_array
    lfd_transform = lfd_transform/lfd_transform[2]

    rfu_transform = K @ P @ T_compensate @ T @ rfu_array
    rfu_transform = rfu_transform/rfu_transform[2]

    rfd_transform = K @ P @ T_compensate @ T @ rfd_array
    rfd_transform = rfd_transform/rfd_transform[2]
    """
   # print("x in camera:"+str(r1_transform))
    #print("image"+str(f))
    # print("f:::::"+str(f))
    # print("image_path::::"+str(path.join(image_path,f)))
    image = cv2.imread(path.join(image_path,f))
    #cv2.rectangle(image, (int(r2_transform[0])-10, 480- int(r2_transform[1])-10, 20, 20), (0,255,0), -1)
    # cv2.rectangle(image, (336, 5, 20, 20), (0,255,0), -1)

    #cv2.rectangle(image, (int(r1_transform[0])-10, 480- int(r1_transform[1])-10, 20, 20), (255,0,0), -1)
    print("r2_transform[0]:::::"+str(r2_transform))
    print("r3_transform[0]:::::"+str(r3_transform))
    print("r5_transform[0]:::::"+str(r5_transform))

    cv2.rectangle(image, (int(r2_transform[1,0])-4,int(r2_transform[0,0])-4,8,8), (255,0,0), -1)
    cv2.rectangle(image, (int(r3_transform[1,0])-4,int(r3_transform[0,0])-4,8,8), (255,0,0), -1)
    cv2.rectangle(image, (int(r5_transform[1,0])-4,int(r5_transform[0 ,0])-4,8,8), (255,0,0), -1)

    """
    cv2.rectangle(image, (640- int(lfd_transform[0])-10, 480- int(lfd _transform[1])-10, 20, 20), (0,255,0), -1)
    cv2.rectangle(image, (640- int(rfu_transform[0])-10, 480- int(rfu_transform[1])-10, 20, 20), (0,255,0), -1)
    cv2.rectangle(image, (640- int(rfd_transform[0])-10, 480- int(rfd_transform[1])-10, 20, 20), (0,255,0), -1)
    """
    print("image:"+str(image))
    cv2.imshow("image", image)
    cv2.setMouseCallback('image', click_pos)
    cv2.waitKey(30000) & 0xFF

    #print("r1_transform:"+str(r1_transform))


def compute_once(Mocap_bag_path, Mocap_file, exp_time, f):
    #print("exp_time::"+str(exp_time))
    global obj_list
    global pre_time
    global continue_flag

    with open(path.join(Mocap_bag_path, Mocap_file),'r') as infile:
        r1 = rigid_body()
        lines = infile.readlines()
        for line in lines:
            if ((line.split(" Time: ")[0] == ">> System") and (round(float(int(line.split(" Time: ")[1].split("\n")[0])),2))>0) and ((round(float(int(line.split(" Time: ")[1].split("\n")[0])),2) > exp_time) and (pre_time <= exp_time)):
                #print("exp_time::::::"+str(exp_time))
                #print("pre_time::::::"+str(pre_time))
                #print("time_duration::::::::::"+str((round(float(int(line.split(" Time: ")[1].split("\n")[0]) - init_time)/1e9,2))))
                pre_time = round(float(int(line.split(" Time: ")[1].split("\n")[0])),2)
                # print("pre_time::::::::::"+str(pre_time))
                continue_flag = 1
                print("only_once")
            
                #print("f::::"+str(f))

            elif (line.split(" Time: ")[0] == ">> System"):
                pre_time = round(float(int(line.split(" Time: ")[1].split("\n")[0])),2)
                # print("pre_time::::::::::"+str(pre_time))
                # print("exp_time::::::::"+str(exp_time))

                #print("hahahaha"+line)
            if continue_flag == 1:
                if (line.split(" of RigidBodies: ")[0] == "#"):
                    num_rigid = int(line.split(" of RigidBodies: ")[1].split("\n")[0])
                global pre_count
                global count
                if (pre_count == count):
                    if (line.split("igidBody ID: ")[0] == 'R'):
                        r1.rigid_ID = int(line.split("igidBody ID: ")[1])
                    if (line.split("Tracked : ")[0] == ""):
                        if(line.split("Tracked : ")[1].split("\n")[0] == "true"):
                            r1.tracked = True
                        else:
                            continue
                    if (line.split(": ")[0] == 'X'):
                        r1.x = float(line.split(": ")[1].split(" - ")[0])
                        r1.y = float(line.split(": ")[2].split(" - ")[0])
                        r1.z = float(line.split(": ")[3].split("\n")[0])
                    if (line.split(": ")[0] == 'qX'):
                        r1.qx = float(line.split(": ")[1].split(" - ")[0])
                        r1.qy = float(line.split(": ")[2].split(" - ")[0])
                        r1.qz = float(line.split(": ")[3].split(" - ")[0])
                        r1.qw = float(line.split(": ")[4].split("\n")[0])
                        count = count +1
                        obj_list.append(r1)
                    if (line.split(" END DATA ")[0] == "<<"):
                        compute_coord(obj_list,Mocap_bag_path,f)
                        continue_flag = 0
                        obj_list = []
                else:
                    r1 = rigid_body()
                    pre_count = pre_count +1


def process_file_time(file,offset_time):
    time_array = file.split("_")[1].split(".")[0]
    time_array_2 = file.split("_")[2].split(".")[0]

    camera_time = float(time_array) + float(time_array_2)/1e9
    system_time = camera_time - offset_time
    return system_time

def filter(offset_time):
    global num_count
    desktop = os.path.expanduser("~/Desktop")
    Mocap_color_path = desktop+"/Filtered_dataset/Lab_data/lab_data_March/Mocap_cc_test5/Mocap_color_test5"
    Mocap_bag_path = desktop+"/Filtered_dataset/Lab_data/lab_data_March"
    Mocap_file = "Mocap_cc_5.txt"

    # image_path = align_path +"/save_file_bkup"
    listd = sorted(listdir(Mocap_color_path))

    # print("listd:::"+str(listd))


    for f in listd:
        exp_time = process_file_time(f,offset_time)
        # print("exp_time::::"+str(exp_time))
        compute_once(Mocap_bag_path, Mocap_file, exp_time, f)        

                
if __name__ == '__main__':
    pre_count = 0
    count = 0
    pre_time = 0
    A_matrix = []
    b_vector = []
    time = None
    num_rigid = 0
    obj_list = []
    continue_flag =0
    offset_time = -4200.45485186
    T0 = None
    filter(offset_time)

