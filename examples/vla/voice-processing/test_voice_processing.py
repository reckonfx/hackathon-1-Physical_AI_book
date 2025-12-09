#!/usr/bin/env python3
"""
Test script for voice processing example
This script tests the cognitive planner function from the voice processing example.
"""

import unittest
import sys
import os

# Define the cognitive_planner function here since we can't easily import it from the ROS node
def cognitive_planner(command_text: str):
    """
    Simple cognitive planner that converts natural language to action sequences.
    This is a copy of the function from the main example file.
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

    return None


class TestCognitivePlanner(unittest.TestCase):
    """Test cases for the cognitive planner function."""

    def test_cognitive_planner_move_forward(self):
        """Test cognitive planner for move forward command."""
        result = cognitive_planner("move forward")
        self.assertIsNotNone(result)
        self.assertEqual(result["intent"], "move_forward")
        self.assertIn("actions", result)
        self.assertEqual(len(result["actions"]), 1)
        self.assertEqual(result["actions"][0]["type"], "motion")

    def test_cognitive_planner_turn_left(self):
        """Test cognitive planner for turn left command."""
        result = cognitive_planner("please turn left")
        self.assertIsNotNone(result)
        self.assertEqual(result["intent"], "turn_left")
        self.assertIn("actions", result)
        self.assertEqual(len(result["actions"]), 1)
        self.assertEqual(result["actions"][0]["type"], "motion")

    def test_cognitive_planner_turn_right(self):
        """Test cognitive planner for turn right command."""
        result = cognitive_planner("turn right now")
        self.assertIsNotNone(result)
        self.assertEqual(result["intent"], "turn_right")
        self.assertIn("actions", result)
        self.assertEqual(len(result["actions"]), 1)
        self.assertEqual(result["actions"][0]["type"], "motion")

    def test_cognitive_planner_stop(self):
        """Test cognitive planner for stop command."""
        result = cognitive_planner("stop immediately")
        self.assertIsNotNone(result)
        self.assertEqual(result["intent"], "stop")
        self.assertIn("actions", result)
        self.assertEqual(len(result["actions"]), 2)

    def test_cognitive_planner_navigate_kitchen(self):
        """Test cognitive planner for navigate to kitchen command."""
        result = cognitive_planner("go to the kitchen")
        self.assertIsNotNone(result)
        self.assertEqual(result["intent"], "navigate")
        self.assertIn("destination", result)
        self.assertEqual(result["destination"], "kitchen")
        self.assertIn("actions", result)

    def test_cognitive_planner_navigate_bedroom(self):
        """Test cognitive planner for navigate to bedroom command."""
        result = cognitive_planner("navigate to bedroom")
        self.assertIsNotNone(result)
        self.assertEqual(result["intent"], "navigate")
        self.assertIn("destination", result)
        self.assertEqual(result["destination"], "bedroom")
        self.assertIn("actions", result)

    def test_cognitive_planner_unknown_command(self):
        """Test cognitive planner for unknown command."""
        result = cognitive_planner("sing me a song")
        self.assertIsNone(result)

    def test_cognitive_planner_go_forward(self):
        """Test cognitive planner for go forward command variation."""
        result = cognitive_planner("go forward slowly")
        self.assertIsNotNone(result)
        self.assertEqual(result["intent"], "move_forward")
        self.assertIn("actions", result)


def run_tests():
    """Run all tests."""
    print("Running voice processing example tests...")

    # Create a test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCognitivePlanner)

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)