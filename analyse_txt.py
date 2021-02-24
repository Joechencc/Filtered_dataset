from os import path
import os

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
    

def filter():
    desktop = os.path.expanduser("~/Desktop")
    align_path = desktop+"/align_file"
    time = None
    num_rigid = 0
    pre_count = 0
    count = 0
    obj_list = []
    r1 = rigid_body()
    with open(path.join(align_path,"Mocap_t1.txt"),'r') as infile:
        lines = infile.readlines()
        for line in lines:
            if (line.split(" Time: ")[0] == ">> System"):
                time = line.split(" Time: ")[1].split("\n")[0]
            if (line.split(" of RigidBodies: ")[0] == "#"):
                num_rigid = int(line.split(" of RigidBodies: ")[1].split("\n")[0])
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
                    if (len(obj_list)==3):
                        obj_list = []
            else:
                r1 = rigid_body()
                pre_count = pre_count +1
                
                
if __name__ == '__main__':
    filter()

