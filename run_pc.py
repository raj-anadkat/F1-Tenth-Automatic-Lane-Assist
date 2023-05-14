# Code to test on PC

import cv2
import numpy as np
from utils import find_lane, warp_img
from steering import pid_control,get_velocity
import time

# camera settings:
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
cap.set(cv2.CAP_PROP_FPS, 30)


# front_mount points (use this if camera is mounted above LIDAR)
# points = np.float32([[160, 354], [800, 354], [0, 400], [960, 400]])

# Region of interest points for warping (rear mount points)
# change these based on camera mounting position, refer find_ROI
points = np.float32([[200, 433], [760, 433], [0, 500], [960, 500]])


while True:

    ret,frame = cap.read()
    crop = cv2.resize(frame,(480,270))
   

    # warping to the frame based on the selected points (BEV)
    bev = warp_img(frame, points, w=480, h=270)
    
    # call detect lanes to overlay lane lines, find error
    detcted_lanes,error = find_lane(bev)

    # call pid control to find the steering angle and velocity
    steering_angle = pid_control(error,time.time())
    velocity = get_velocity(steering_angle)

    # print steering angle and velocity
    print("Steering angle:", steering_angle)
    print("Velocity:",velocity)
    

    cv2.imshow("frame",crop)
    cv2.imshow('lane',detcted_lanes)
    cv2.waitKey(1)
