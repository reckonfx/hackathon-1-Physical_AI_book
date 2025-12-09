#!/usr/bin/env python3
"""
Voice Command to ROS 2 Action Translation Example

This script demonstrates the basic pipeline for converting voice commands
into ROS 2 action sequences using OpenAI Whisper for speech recognition
and cognitive planning for action generation.
"""

import sys
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav2_msgs.action import NavigateToPose
from sensor_msgs.msg import LaserScan
import speech_recognition as sr
import openai
import json
from typing import Dict, Any, Optional


class VoiceCommandProcessor(Node):
    """
    A ROS 2 node that processes voice commands and translates them into ROS 2 actions.
    """

    def __init__(self):
        super().__init__('voice_command_processor')

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_pub = self.create_publisher(String, '/voice_command_status', 10)

        # Subscribers
        self.lidar_sub = self.create_subscription(LaserScan, '/scan', self.lidar_callback, 10)

        # Action clients
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Audio recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize recognizer settings
        with self.microphone as source:
            self.get_logger().info("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source)

        self.get_logger().info("Voice Command Processor initialized")
        self.current_environment_data = {}

    def lidar_callback(self, msg: LaserScan):
        """Callback for lidar data to maintain environment awareness."""
        self.current_environment_data = {
            'ranges': msg.ranges[:10],  # Sample first 10 readings
            'min_range': min(msg.ranges) if msg.ranges else float('inf'),
            'max_range': max(msg.ranges) if msg.ranges else 0.0
        }

    def listen_for_command(self) -> Optional[str]:
        """Listen for a voice command and return the recognized text."""
        try:
            self.get_logger().info("Listening for voice command...")

            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5.0)

            self.get_logger().info("Processing audio...")

            # Using Whisper for speech recognition
            try:
                text = self.recognizer.recognize_whisper(audio, model="base")
                self.get_logger().info(f"Recognized: {text}")
                return text
            except sr.RequestError as e:
                self.get_logger().error(f"Whisper API error: {e}")
                return None
            except sr.UnknownValueError:
                self.get_logger().error("Whisper could not understand audio")
                return None

        except sr.WaitTimeoutError:
            self.get_logger().warning("No speech detected within timeout")
            return None
        except Exception as e:
            self.get_logger().error(f"Error listening for command: {e}")
            return None

    def cognitive_planner(self, command_text: str) -> Optional[Dict[str, Any]]:
        """
        Simple cognitive planner that converts natural language to action sequences.
        In a real implementation, this would use an LLM to generate structured plans.
        """
        # This is a simplified version - in reality, you'd use an LLM API
        command_lower = command_text.lower()

        # Simple rule-based planning for demo purposes
        if "move forward" in command_lower or "go forward" in command_lower:
            return {
                "intent": "move_forward",
                "actions": [
                    {"type": "motion", "command": "linear_x", "value": 0.5, "duration": 2.0}
                ]
            }
        elif "turn left" in command_lower:
            return {
                "intent": "turn_left",
                "actions": [
                    {"type": "motion", "command": "angular_z", "value": 0.5, "duration": 1.0}
                ]
            }
        elif "turn right" in command_lower:
            return {
                "intent": "turn_right",
                "actions": [
                    {"type": "motion", "command": "angular_z", "value": -0.5, "duration": 1.0}
                ]
            }
        elif "stop" in command_lower:
            return {
                "intent": "stop",
                "actions": [
                    {"type": "motion", "command": "linear_x", "value": 0.0, "duration": 0.0},
                    {"type": "motion", "command": "angular_z", "value": 0.0, "duration": 0.0}
                ]
            }
        elif "navigate to" in command_lower or "go to" in command_lower:
            # Extract destination from command (simplified)
            if "kitchen" in command_lower:
                return {
                    "intent": "navigate",
                    "destination": "kitchen",
                    "pose": {"x": 1.0, "y": 2.0, "theta": 0.0},
                    "actions": [
                        {"type": "navigation", "target_pose": {"x": 1.0, "y": 2.0, "theta": 0.0}}
                    ]
                }
            elif "bedroom" in command_lower:
                return {
                    "intent": "navigate",
                    "destination": "bedroom",
                    "pose": {"x": -1.0, "y": 1.0, "theta": 1.57},
                    "actions": [
                        {"type": "navigation", "target_pose": {"x": -1.0, "y": 1.0, "theta": 1.57}}
                    ]
                }

        self.get_logger().warning(f"Unknown command: {command_text}")
        return None

    def execute_action_sequence(self, action_plan: Dict[str, Any]):
        """Execute the planned actions."""
        if not action_plan:
            self.get_logger().error("No action plan to execute")
            return

        self.get_logger().info(f"Executing action plan: {action_plan['intent']}")

        for action in action_plan.get('actions', []):
            action_type = action.get('type')

            if action_type == 'motion':
                self.execute_motion_action(action)
            elif action_type == 'navigation':
                self.execute_navigation_action(action)
            else:
                self.get_logger().warning(f"Unknown action type: {action_type}")

    def execute_motion_action(self, action: Dict[str, Any]):
        """Execute a motion action (e.g., move forward, turn)."""
        cmd_msg = Twist()

        if 'linear_x' in action:
            cmd_msg.linear.x = action['linear_x']
        if 'angular_z' in action:
            cmd_msg.angular.z = action['angular_z']

        # Publish the command
        self.cmd_vel_pub.publish(cmd_msg)
        self.get_logger().info(f"Published motion command: linear.x={cmd_msg.linear.x}, angular.z={cmd_msg.angular.z}")

        # Duration-based execution (in a real system, you'd use action feedback)
        duration = action.get('duration', 1.0)
        self.get_clock().sleep_for(rclpy.duration.Duration(seconds=duration))

        # Stop after movement
        cmd_msg.linear.x = 0.0
        cmd_msg.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd_msg)

    def execute_navigation_action(self, action: Dict[str, Any]):
        """Execute a navigation action using Nav2."""
        if not self.nav_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error("Navigation action server not available")
            return

        # Create navigation goal
        goal_msg = NavigateToPose.Goal()
        # Note: In a real implementation, you'd properly construct the PoseStamped message
        # This is simplified for the example

        self.get_logger().info("Sending navigation goal...")
        # send_goal_future = self.nav_client.send_goal_async(goal_msg)
        # For this example, we'll just log the intent
        self.get_logger().info(f"Navigation to pose: {action.get('target_pose')}")

    def run_voice_loop(self):
        """Main loop for continuously listening for voice commands."""
        self.get_logger().info("Starting voice command processing loop...")

        while rclpy.ok():
            try:
                # Listen for a command
                command_text = self.listen_for_command()

                if command_text:
                    # Plan actions based on the command
                    action_plan = self.cognitive_planner(command_text)

                    if action_plan:
                        # Execute the planned actions
                        self.execute_action_sequence(action_plan)

                        # Publish status
                        status_msg = String()
                        status_msg.data = f"Executed: {command_text}"
                        self.status_pub.publish(status_msg)
                    else:
                        status_msg = String()
                        status_msg.data = f"Could not understand command: {command_text}"
                        self.status_pub.publish(status_msg)
                else:
                    # No command detected, continue loop
                    continue

            except KeyboardInterrupt:
                self.get_logger().info("Interrupted by user")
                break
            except Exception as e:
                self.get_logger().error(f"Error in voice loop: {e}")
                continue


def main(args=None):
    """Main function to run the voice command processor node."""
    rclpy.init(args=args)

    # Initialize OpenAI API (you would set your API key here)
    # openai.api_key = os.getenv("OPENAI_API_KEY")  # Uncomment and set in production

    node = VoiceCommandProcessor()

    try:
        node.run_voice_loop()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()