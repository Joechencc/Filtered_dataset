from sensor_msgs.msg import CameraInfo, Image
import message_filters
import rospy
from cv_bridge import CvBridge
import cv2
from os import path
import numpy as np

count = 0
init_sec = 0
init_nsec = 0
sec = 0
nsec = 0


def map_uint16_to_uint8(img, lower_bound=None, upper_bound=None):
    '''
    Map a 16-bit image trough a lookup table to convert it to 8-bit.

    Parameters
    ----------
    img: numpy.ndarray[np.uint16]
        image that should be mapped
    lower_bound: int, optional
        lower bound of the range that should be mapped to ``[0, 255]``,
        value must be in the range ``[0, 65535]`` and smaller than `upper_bound`
        (defaults to ``numpy.min(img)``)
    upper_bound: int, optional
       upper bound of the range that should be mapped to ``[0, 255]``,
       value must be in the range ``[0, 65535]`` and larger than `lower_bound`
       (defaults to ``numpy.max(img)``)

    Returns
    -------
    numpy.ndarray[uint8]
    '''
    print(img.encoding)
    if not(0 <= lower_bound < 2**16) and lower_bound is not None:
        raise ValueError(
            '"lower_bound" must be in the range [0, 65535]')
    if not(0 <= upper_bound < 2**16) and upper_bound is not None:
        raise ValueError(
            '"upper_bound" must be in the range [0, 65535]')
    if lower_bound is None:
        lower_bound = np.min(img)
    if upper_bound is None:
        upper_bound = np.max(img)
    if lower_bound >= upper_bound:
        raise ValueError(
            '"lower_bound" must be smaller than "upper_bound"')
    lut = np.concatenate([
        np.zeros(lower_bound, dtype=np.uint16),
        np.linspace(0, 255, upper_bound - lower_bound).astype(np.uint16),
        np.ones(2**16 - upper_bound, dtype=np.uint16) * 255
    ])
    return lut[img].astype(np.uint8)

def detect(image, depth, image_info, depth_info):
    global count
    global init_sec, init_nsec
    #cv_image = CvBridge().imgmsg_to_cv2(image, desired_encoding='bgr8')
    cv_image = map_uint16_to_uint8(depth,0,255)  

    if (init_sec == 0):
        init_sec = image_info.header.stamp.secs
        init_nsec = image_info.header.stamp.nsecs
    sec = image_info.header.stamp.secs
    nsec = image_info.header.stamp.nsecs

    time = (sec - init_sec) + 1e-9 * (nsec - init_nsec)

    #file_path = "/home/chen1804/Desktop/align_file/save_file_1"
    file_path = "/home/chen1804/Desktop/align_file/save_file_1_depth"
    #file_name = "image_"+str(count)+ "_"+ str(round(time,2)) + ".jpg"
    file_name = "depth_"+str(count)+ "_"+ str(round(time,2)) + ".jpg"
    print("image::"+str(cv_image))
    cv2.imwrite(path.join(file_path, file_name), cv_image)
    count = count + 1
    cv2.waitKey(30)


if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    while not rospy.is_shutdown():
        depth_sub = message_filters.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, queue_size = 1, buff_size=2**24)
        image_sub = message_filters.Subscriber("/camera/color/image_raw", Image, queue_size = 1, buff_size=2**24)
        depth_info = message_filters.Subscriber("/camera/aligned_depth_to_color/camera_info", CameraInfo, queue_size = 1, buff_size=2**24)
        images_info = message_filters.Subscriber("/camera/color/camera_info", CameraInfo, queue_size = 1, buff_size=2**24)
        ats = message_filters.ApproximateTimeSynchronizer([image_sub, depth_sub, images_info, depth_info], 10,1 )
        ats.registerCallback(detect)
        rospy.spin()
