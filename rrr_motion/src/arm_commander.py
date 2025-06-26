#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math

class ArmCommander(Node):
    def __init__(self):
        super().__init__('arm_circular_motion_node')

        self.publisher_ = self.create_publisher(
            JointTrajectory, '/arm_controller/joint_trajectory', 10)

        self.timer_period = 0.1  # seconds (10 Hz)
        self.radius = 0.4         # adjust as per reach of your robot
        self.center_angle = 0.5   # center offset
        self.time = 0.0
        self.timer = self.create_timer(self.timer_period, self.send_trajectory)

    def send_trajectory(self):
        msg = JointTrajectory()
        msg.joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4']

        point = JointTrajectoryPoint()

        # Time-based angle for circular motion
        theta = self.time

        # Simulated circular motion in joint space (you can replace with IK later)
        joint_1 = 0.0  # keep base fixed
        joint_2 = self.center_angle + self.radius * math.cos(theta)
        joint_3 = self.center_angle + self.radius * math.sin(theta)
        joint_4 = 0.0  # optional: add twist or end-effector orientation

        point.positions = [joint_1, joint_2, joint_3, joint_4]
        point.time_from_start.sec = 1
        point.time_from_start.nanosec = 0

        msg.points.append(point)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing circular position at t={self.time:.2f}')

        self.time += self.timer_period

def main(args=None):
    rclpy.init(args=args)
    node = ArmCommander()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
