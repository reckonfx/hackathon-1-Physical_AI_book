#!/usr/bin/env python3
"""
Manipulation Workflows Example for VLA Systems

This script demonstrates robotic manipulation workflows within the VLA framework.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64MultiArray
from geometry_msgs.msg import Pose, Point, Vector3
from sensor_msgs.msg import JointState
import time
from typing import Dict, List, Any, Optional
import math
import numpy as np


class ManipulatorController(Node):
    """
    Manipulation controller for VLA applications.
    """

    def __init__(self):
        super().__init__('manipulator_controller')

        # Publishers and subscribers
        self.joint_command_pub = self.create_publisher(Float64MultiArray, '/joint_commands', 10)
        self.gripper_command_pub = self.create_publisher(Float64MultiArray, '/gripper_command', 10)
        self.manipulation_status_pub = self.create_publisher(String, '/manipulation_status', 10)
        self.joint_state_sub = self.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10)

        # Manipulation state
        self.current_joint_positions = [0.0] * 6  # Example: 6 DOF arm
        self.gripper_position = 0.0  # 0.0 = open, 1.0 = closed
        self.is_moving = False
        self.manipulation_history = []

        self.get_logger().info("Manipulator Controller initialized")

    def joint_state_callback(self, msg: JointState):
        """Callback for joint state updates."""
        if len(msg.position) >= 6:  # Assuming at least 6 joints
            self.current_joint_positions = list(msg.position[:6])
        if 'gripper' in msg.name:
            gripper_idx = msg.name.index('gripper')
            self.gripper_position = msg.position[gripper_idx]

    def move_to_joint_positions(self, joint_positions: List[float], duration: float = 2.0) -> bool:
        """
        Move manipulator to specified joint positions.

        Args:
            joint_positions: List of target joint angles (in radians)
            duration: Time to complete the movement (seconds)

        Returns:
            True if successful, False otherwise
        """
        if len(joint_positions) != len(self.current_joint_positions):
            self.get_logger().error(f"Joint position list length mismatch: expected {len(self.current_joint_positions)}, got {len(joint_positions)}")
            return False

        if self.is_moving:
            self.get_logger().warning("Manipulator is already moving")
            return False

        self.is_moving = True
        self.publish_status(f"Moving to joint positions: {joint_positions}")

        try:
            # Create and send joint command
            command_msg = Float64MultiArray()
            command_msg.data = joint_positions
            self.joint_command_pub.publish(command_msg)

            # Simulate movement time
            time.sleep(duration)

            # Update current positions
            self.current_joint_positions = joint_positions
            self.publish_status("Movement completed")

            # Record in history
            self.manipulation_history.append({
                'action': 'move_to_joint_positions',
                'target': joint_positions,
                'timestamp': time.time()
            })

            return True

        except Exception as e:
            self.get_logger().error(f"Error moving to joint positions: {e}")
            self.publish_status(f"Movement failed: {str(e)}")
            return False
        finally:
            self.is_moving = False

    def move_to_pose(self, target_pose: Pose, approach_vector: Vector3 = Vector3(x=0.0, y=0.0, z=-1.0)) -> bool:
        """
        Move manipulator to a specific Cartesian pose.

        Args:
            target_pose: Target pose for the end effector
            approach_vector: Direction vector for approach (optional)

        Returns:
            True if successful, False otherwise
        """
        self.publish_status(f"Moving to pose: ({target_pose.position.x}, {target_pose.position.y}, {target_pose.position.z})")

        # In a real implementation, this would perform inverse kinematics
        # For this example, we'll simulate the movement
        try:
            # Simulate IK calculation and joint movement
            # This is a simplified approach - real IK would be more complex
            simulated_joints = self._simulate_inverse_kinematics(target_pose)

            if simulated_joints:
                success = self.move_to_joint_positions(simulated_joints)
                if success:
                    self.manipulation_history.append({
                        'action': 'move_to_pose',
                        'target_pose': target_pose,
                        'timestamp': time.time()
                    })
                return success
            else:
                self.get_logger().error("Could not calculate inverse kinematics for target pose")
                self.publish_status("Could not reach target pose")
                return False

        except Exception as e:
            self.get_logger().error(f"Error moving to pose: {e}")
            self.publish_status(f"Pose movement failed: {str(e)}")
            return False

    def grasp_object(self, object_info: Dict[str, Any], grasp_type: str = "power") -> bool:
        """
        Grasp an object using appropriate grasp strategy.

        Args:
            object_info: Dictionary containing object information
            grasp_type: Type of grasp ('power', 'pinch', 'suction', etc.)

        Returns:
            True if successful, False otherwise
        """
        object_name = object_info.get('name', 'unknown')
        object_size = object_info.get('size', 0.1)  # Default size 10cm
        object_weight = object_info.get('weight', 0.1)  # Default weight 100g

        self.publish_status(f"Grasping {object_name} (size: {object_size}m, weight: {object_weight}kg)")

        try:
            # Adjust gripper based on object properties and grasp type
            if grasp_type == "power":
                # Power grasp - close gripper firmly
                grip_force = min(0.8, object_weight * 2)  # Adjust grip based on weight
                grip_position = max(0.3, 1.0 - object_size)  # Adjust based on object size
            elif grasp_type == "pinch":
                # Pinch grasp - partial closure
                grip_force = min(0.5, object_weight)
                grip_position = max(0.5, 0.8 - object_size)
            else:
                # Default grasp
                grip_force = min(0.6, object_weight * 1.5)
                grip_position = max(0.4, 1.0 - object_size * 0.5)

            # Move to object position first
            obj_pose = Pose()
            if 'position' in object_info:
                pos = object_info['position']
                obj_pose.position.x = pos.get('x', 0.0)
                obj_pose.position.y = pos.get('y', 0.0)
                obj_pose.position.z = pos.get('z', 0.0) + 0.1  # Approach from above

            # Move to approach position
            approach_success = self.move_to_pose(obj_pose)
            if not approach_success:
                self.get_logger().error("Could not reach approach position")
                return False

            # Close gripper to grasp object
            self.close_gripper(grip_position)
            time.sleep(0.5)  # Wait for grasp

            # Lift object slightly
            lift_pose = obj_pose
            lift_pose.position.z += 0.05  # Lift 5cm
            lift_success = self.move_to_pose(lift_pose)

            if lift_success:
                self.manipulation_history.append({
                    'action': 'grasp_object',
                    'object': object_name,
                    'grasp_type': grasp_type,
                    'timestamp': time.time()
                })

            return lift_success

        except Exception as e:
            self.get_logger().error(f"Error during grasping: {e}")
            self.publish_status(f"Grasping failed: {str(e)}")
            return False

    def release_object(self, release_height: Optional[float] = None) -> bool:
        """
        Release the currently grasped object.

        Args:
            release_height: Height at which to release the object (optional)

        Returns:
            True if successful, False otherwise
        """
        self.publish_status("Releasing object")

        try:
            # If release height specified, move to that height first
            if release_height is not None:
                current_pose = self.get_current_end_effector_pose()
                if current_pose:
                    current_pose.position.z = release_height
                    self.move_to_pose(current_pose)

            # Open gripper to release
            self.open_gripper()
            time.sleep(0.3)  # Wait for release

            # Move up slightly to clear the object
            current_pose = self.get_current_end_effector_pose()
            if current_pose:
                current_pose.position.z += 0.05
                self.move_to_pose(current_pose)

            self.manipulation_history.append({
                'action': 'release_object',
                'timestamp': time.time()
            })

            self.publish_status("Object released")
            return True

        except Exception as e:
            self.get_logger().error(f"Error during release: {e}")
            self.publish_status(f"Release failed: {str(e)}")
            return False

    def open_gripper(self, position: float = 1.0) -> bool:
        """Open the gripper to the specified position."""
        try:
            command_msg = Float64MultiArray()
            command_msg.data = [position]  # 1.0 = fully open
            self.gripper_command_pub.publish(command_msg)
            self.gripper_position = position
            self.publish_status(f"Gripper opened to position {position}")
            return True
        except Exception as e:
            self.get_logger().error(f"Error opening gripper: {e}")
            return False

    def close_gripper(self, position: float = 0.0) -> bool:
        """Close the gripper to the specified position."""
        try:
            command_msg = Float64MultiArray()
            command_msg.data = [position]  # 0.0 = fully closed
            self.gripper_command_pub.publish(command_msg)
            self.gripper_position = position
            self.publish_status(f"Gripper closed to position {position}")
            return True
        except Exception as e:
            self.get_logger().error(f"Error closing gripper: {e}")
            return False

    def _simulate_inverse_kinematics(self, target_pose: Pose) -> Optional[List[float]]:
        """
        Simulate inverse kinematics calculation.

        Args:
            target_pose: Target pose for the end effector

        Returns:
            List of joint angles if solution found, None otherwise
        """
        # This is a simplified simulation of IK
        # In a real implementation, you would use a proper IK solver

        # For this example, we'll generate a random but plausible joint configuration
        # that roughly achieves the target position
        try:
            # Generate random joint angles that are likely to reach the target
            joint_angles = [
                np.random.uniform(-1.57, 1.57),  # Joint 1: -90° to 90°
                np.random.uniform(-1.0, 1.0),    # Joint 2: -57° to 57°
                np.random.uniform(-2.0, 2.0),    # Joint 3: -114° to 114°
                np.random.uniform(-3.14, 3.14), # Joint 4: full rotation
                np.random.uniform(-1.57, 1.57), # Joint 5: -90° to 90°
                np.random.uniform(-3.14, 3.14)  # Joint 6: full rotation
            ]
            return joint_angles
        except Exception:
            return None

    def get_current_end_effector_pose(self) -> Optional[Pose]:
        """Get the current pose of the end effector based on joint positions."""
        # In a real implementation, this would perform forward kinematics
        # For this example, we'll return a simulated pose
        try:
            # Simulate pose based on current joint positions
            pose = Pose()
            pose.position.x = 0.5 + self.current_joint_positions[0] * 0.1
            pose.position.y = 0.0 + self.current_joint_positions[1] * 0.1
            pose.position.z = 0.3 + self.current_joint_positions[2] * 0.1
            # Add simple orientation simulation
            pose.orientation.z = self.current_joint_positions[3]
            pose.orientation.w = 1.0  # Simplified orientation
            return pose
        except Exception:
            return None

    def execute_manipulation_sequence(self, sequence: List[Dict[str, Any]]) -> bool:
        """
        Execute a sequence of manipulation actions.

        Args:
            sequence: List of manipulation actions to execute

        Returns:
            True if all actions completed successfully, False otherwise
        """
        self.publish_status(f"Executing manipulation sequence with {len(sequence)} actions")

        for i, action in enumerate(sequence):
            self.get_logger().info(f"Executing action {i+1}/{len(sequence)}: {action.get('type', 'unknown')}")

            action_type = action.get('type', '')
            success = False

            if action_type == 'move_to_joint_positions':
                positions = action.get('positions', [])
                duration = action.get('duration', 2.0)
                success = self.move_to_joint_positions(positions, duration)
            elif action_type == 'move_to_pose':
                pose = action.get('pose')
                if pose:
                    success = self.move_to_pose(pose)
            elif action_type == 'grasp':
                object_info = action.get('object', {})
                grasp_type = action.get('grasp_type', 'power')
                if object_info:
                    success = self.grasp_object(object_info, grasp_type)
            elif action_type == 'release':
                release_height = action.get('height')
                success = self.release_object(release_height)
            elif action_type == 'open_gripper':
                position = action.get('position', 1.0)
                success = self.open_gripper(position)
            elif action_type == 'close_gripper':
                position = action.get('position', 0.0)
                success = self.close_gripper(position)
            else:
                self.get_logger().error(f"Unknown action type: {action_type}")
                continue

            if not success:
                self.get_logger().error(f"Action {i+1} failed: {action_type}")
                self.publish_status(f"Manipulation sequence failed at action {i+1}")
                return False

        self.publish_status("Manipulation sequence completed successfully")
        return True

    def publish_status(self, status: str):
        """Publish manipulation status."""
        status_msg = String()
        status_msg.data = status
        self.manipulation_status_pub.publish(status_msg)

    def get_manipulation_history(self) -> List[Dict[str, Any]]:
        """Get the history of manipulation actions."""
        return self.manipulation_history.copy()


def main(args=None):
    """Main function to demonstrate manipulation workflows."""
    print("VLA Manipulation Workflows Demo")
    print("===============================")
    print("This example demonstrates robotic manipulation capabilities for VLA systems.")
    print("It includes joint control, pose control, grasping, and manipulation sequences.")
    print()

    rclpy.init(args=args)
    manipulator = ManipulatorController()

    try:
        # Example 1: Move to joint positions
        print("1. Moving to home position...")
        home_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        success = manipulator.move_to_joint_positions(home_positions)
        print(f"Move to home: {'Success' if success else 'Failed'}")
        print()

        # Example 2: Grasp an object
        print("2. Grasping an object...")
        object_info = {
            'name': 'red_cube',
            'size': 0.05,  # 5cm cube
            'weight': 0.05,  # 50g
            'position': {'x': 0.5, 'y': 0.2, 'z': 0.1}
        }
        success = manipulator.grasp_object(object_info, 'power')
        print(f"Grasp object: {'Success' if success else 'Failed'}")
        print()

        # Example 3: Release the object
        print("3. Releasing the object...")
        success = manipulator.release_object(release_height=0.15)
        print(f"Release object: {'Success' if success else 'Failed'}")
        print()

        # Example 4: Execute a manipulation sequence
        print("4. Executing manipulation sequence...")
        sequence = [
            {
                'type': 'move_to_joint_positions',
                'positions': [0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                'duration': 1.0
            },
            {
                'type': 'open_gripper',
                'position': 1.0
            },
            {
                'type': 'move_to_pose',
                'pose': Pose(position=Point(x=0.4, y=0.0, z=0.2))
            },
            {
                'type': 'close_gripper',
                'position': 0.3
            }
        ]
        success = manipulator.execute_manipulation_sequence(sequence)
        print(f"Sequence execution: {'Success' if success else 'Failed'}")
        print()

        # Print manipulation history
        print("5. Manipulation history:")
        history = manipulator.get_manipulation_history()
        for i, action in enumerate(history):
            print(f"  {i+1}. {action['action']} at {time.ctime(action['timestamp'])}")

    except KeyboardInterrupt:
        print("\nManipulation demo interrupted by user")
    finally:
        manipulator.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()