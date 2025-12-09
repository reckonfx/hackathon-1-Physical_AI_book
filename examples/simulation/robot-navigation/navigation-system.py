#!/usr/bin/env python3
"""
Robot Navigation Example for VLA Systems

This script demonstrates robot navigation capabilities within the VLA framework.
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped, Point
from nav2_msgs.action import NavigateToPose
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
import time
from typing import Dict, Any, Optional
import math


class RobotNavigationSystem(Node):
    """
    Robot navigation system for VLA applications.
    """

    def __init__(self):
        super().__init__('robot_navigation_system')

        # Action client for navigation
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Publishers and subscribers
        self.status_pub = self.create_publisher(String, '/navigation_status', 10)
        self.lidar_sub = self.create_subscription(LaserScan, '/scan', self.lidar_callback, 10)

        # Navigation state
        self.current_pose = Point(x=0.0, y=0.0, z=0.0)
        self.is_navigating = False
        self.obstacles = []

        self.get_logger().info("Robot Navigation System initialized")

    def lidar_callback(self, msg: LaserScan):
        """Process lidar data to detect obstacles."""
        # Simple obstacle detection: anything closer than 0.5m is an obstacle
        obstacles = []
        for i, range_val in enumerate(msg.ranges):
            if 0.1 < range_val < 0.5:  # Valid range and close enough to be obstacle
                angle = msg.angle_min + i * msg.angle_increment
                # Convert polar to Cartesian coordinates relative to robot
                x = range_val * math.cos(angle)
                y = range_val * math.sin(angle)
                obstacles.append({'x': x, 'y': y, 'distance': range_val})

        self.obstacles = obstacles

    def navigate_to_pose(self, target_x: float, target_y: float, target_theta: float = 0.0) -> bool:
        """
        Navigate to a specific pose in the environment.

        Args:
            target_x: Target X coordinate
            target_y: Target Y coordinate
            target_theta: Target orientation (optional)

        Returns:
            True if navigation successful, False otherwise
        """
        if self.is_navigating:
            self.get_logger().warning("Navigation already in progress")
            return False

        self.get_logger().info(f"Navigating to ({target_x}, {target_y}, {target_theta})")

        # Check if navigation server is available
        if not self.nav_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error("Navigation server not available")
            return False

        # Create navigation goal
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()

        # Set target pose
        goal_msg.pose.pose.position.x = target_x
        goal_msg.pose.pose.position.y = target_y
        goal_msg.pose.pose.position.z = 0.0

        # Simple quaternion from yaw (theta)
        import math
        s = math.sin(target_theta / 2.0)
        c = math.cos(target_theta / 2.0)
        goal_msg.pose.pose.orientation.x = 0.0
        goal_msg.pose.pose.orientation.y = 0.0
        goal_msg.pose.pose.orientation.z = s
        goal_msg.pose.pose.orientation.w = c

        # Send goal
        self.is_navigating = True
        self.publish_status("Navigating to target")

        try:
            # In a real implementation, we would send the goal and wait for result
            # For this example, we'll simulate the navigation
            time.sleep(2)  # Simulate navigation time

            # Check for obstacles during navigation (simulated)
            if len(self.obstacles) > 0:
                self.get_logger().warning(f"Detected {len(self.obstacles)} obstacles during navigation")
                # In a real system, you would implement obstacle avoidance here

            self.get_logger().info("Navigation completed successfully")
            self.publish_status("Navigation completed")
            return True

        except Exception as e:
            self.get_logger().error(f"Navigation failed: {e}")
            self.publish_status(f"Navigation failed: {str(e)}")
            return False
        finally:
            self.is_navigating = False

    def navigate_to_object(self, object_info: Dict[str, Any]) -> bool:
        """
        Navigate to a specific object based on its position information.

        Args:
            object_info: Dictionary containing object information including position

        Returns:
            True if navigation successful, False otherwise
        """
        if 'position' not in object_info:
            self.get_logger().error("Object information missing position data")
            return False

        pos = object_info['position']
        target_x = pos.get('x', 0.0)
        target_y = pos.get('y', 0.0)
        target_theta = pos.get('theta', 0.0)

        return self.navigate_to_pose(target_x, target_y, target_theta)

    def navigate_to_location(self, location_name: str) -> Optional[bool]:
        """
        Navigate to a predefined location by name.

        Args:
            location_name: Name of the location to navigate to

        Returns:
            True if navigation successful, False if failed, None if location unknown
        """
        # Define known locations
        locations = {
            'kitchen': {'x': 3.0, 'y': 2.0, 'theta': 0.0},
            'living_room': {'x': -1.0, 'y': 1.5, 'theta': 1.57},
            'bedroom': {'x': -2.0, 'y': -1.0, 'theta': 3.14},
            'office': {'x': 1.5, 'y': -2.0, 'theta': -1.57}
        }

        if location_name.lower() not in locations:
            self.get_logger().error(f"Unknown location: {location_name}")
            self.publish_status(f"Unknown location: {location_name}")
            return None

        location = locations[location_name.lower()]
        self.get_logger().info(f"Navigating to {location_name} at ({location['x']}, {location['y']})")

        return self.navigate_to_pose(location['x'], location['y'], location['theta'])

    def publish_status(self, status: str):
        """Publish navigation status."""
        status_msg = String()
        status_msg.data = status
        self.status_pub.publish(status_msg)

    def get_current_position(self) -> Dict[str, float]:
        """Get the current position of the robot."""
        return {
            'x': self.current_pose.x,
            'y': self.current_pose.y,
            'z': self.current_pose.z
        }

    def calculate_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate Euclidean distance between two points."""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def main(args=None):
    """Main function to demonstrate robot navigation."""
    print("Robot Navigation System Demo")
    print("============================")
    print("This example demonstrates robot navigation capabilities for VLA systems.")
    print("It includes navigation to poses, objects, and predefined locations.")
    print()

    rclpy.init(args=args)
    nav_system = RobotNavigationSystem()

    # Example navigation scenarios
    try:
        # Navigate to a specific pose
        print("1. Navigating to specific pose (2.0, 1.5)...")
        success = nav_system.navigate_to_pose(2.0, 1.5, 0.0)
        print(f"Navigation result: {'Success' if success else 'Failed'}")
        print()

        # Navigate to a predefined location
        print("2. Navigating to kitchen...")
        result = nav_system.navigate_to_location('kitchen')
        if result is not None:
            print(f"Navigation to kitchen: {'Success' if result else 'Failed'}")
        else:
            print("Unknown location")
        print()

        # Navigate to an object (simulated)
        object_info = {
            'id': 'red_cube',
            'position': {'x': -1.0, 'y': 0.5, 'theta': 0.0}
        }
        print(f"3. Navigating to {object_info['id']} at {object_info['position']['x']}, {object_info['position']['y']}...")
        success = nav_system.navigate_to_object(object_info)
        print(f"Navigation to object result: {'Success' if success else 'Failed'}")

    except KeyboardInterrupt:
        print("\nNavigation demo interrupted by user")
    finally:
        nav_system.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()