import cv2
import numpy as np
from utils import find_lane, warp_img
from steering import pid_control, get_velocity
import time
import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped

class LaneFollowNode(Node):

    def __init__(self):
        super().__init__('lane_follow_node')

        # camera settings:
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        # front_mount points (use this if camera is mounted above LIDAR)
        # points = np.float32([[160, 354], [800, 354], [0, 400], [960, 400]])


        # ROI points for warping (rear mount points)
        self.points = np.float32([[200, 433], [760, 433], [0, 500], [960, 500]])

        # creating a publisher for AckermannDriveStamped messages
        self.pub_drive = self.create_publisher(AckermannDriveStamped, '/drive', 10)

        # create a timer to publish messages at a fixed rate
        self.timer = self.create_timer(0.1, self.publish_drive)

    def publish_drive(self):
        
        ret, frame = self.cap.read()
        crop = cv2.resize(frame, (480, 270))

        # warping to the frame based on the selected points (BEV)
        bev = warp_img(frame, self.points, w=480, h=270)

        # call detect lanes to overlay lane lines, find error
        detcted_lanes, error = find_lane(bev)

        # call pid control to find the steering angle and velocity
        steering_angle = pid_control(error, time.time())
        velocity = get_velocity(steering_angle)

        # publish AckermannDriveStamped message
        drive_msg = AckermannDriveStamped()
        drive_msg.header.stamp = self.get_clock().now().to_msg()
        drive_msg.drive.steering_angle = steering_angle
        drive_msg.drive.speed = velocity
        self.pub_drive.publish(drive_msg)

        # log steering angle and velocity
        self.get_logger().info('Steering angle: %f' % steering_angle)
        self.get_logger().info('Velocity: %f' % velocity)

        cv2.imshow("frame", crop)
        cv2.imshow('lane', detcted_lanes)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = LaneFollowNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
