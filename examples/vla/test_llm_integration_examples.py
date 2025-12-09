#!/usr/bin/env python3
"""
Test runner for LLM integration examples
This script tests the cognitive planning functionality.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the llm-integration directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'llm-integration'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cognitive-planning'))

from llm_cognitive_planner import VLACognitivePlanner
from cognitive_planner import AdvancedCognitivePlanner


class TestVLACognitivePlanner(unittest.TestCase):
    """Test cases for the basic VLA cognitive planner."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock OpenAI API to avoid actual API calls during testing
        self.planner = VLACognitivePlanner(api_key="test-key")

    @patch('llm_cognitive_planner.openai.ChatCompletion.create')
    def test_plan_simple_command(self, mock_create):
        """Test planning for a simple command."""
        # Mock the API response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = {
            'content': '''
            {
                "intent": "move_forward",
                "objects": [],
                "locations": [],
                "actions": [
                    {
                        "type": "motion",
                        "target": "forward",
                        "parameters": {"distance": 1.0}
                    }
                ],
                "safety_checks": ["check_obstacles"]
            }
            '''
        }
        mock_create.return_value = mock_response

        # Test data
        command = "move forward"
        robot_state = {"battery_level": 80}
        environment_data = {"obstacles": []}

        # Execute test
        result = self.planner.plan_actions(command, robot_state, environment_data)

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result["intent"], "move_forward")
        self.assertEqual(len(result["actions"]), 1)
        self.assertEqual(result["actions"][0]["type"], "motion")

    @patch('llm_cognitive_planner.openai.ChatCompletion.create')
    def test_plan_complex_command(self, mock_create):
        """Test planning for a complex command."""
        # Mock the API response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = {
            'content': '''
            {
                "intent": "fetch_object",
                "objects": ["red_cube"],
                "locations": ["kitchen"],
                "actions": [
                    {
                        "type": "navigation",
                        "target": "kitchen",
                        "parameters": {"x": 1.0, "y": 2.0}
                    },
                    {
                        "type": "manipulation",
                        "target": "red_cube",
                        "parameters": {"action": "grasp"}
                    }
                ],
                "safety_checks": ["check_path_clear", "check_object_safety"]
            }
            '''
        }
        mock_create.return_value = mock_response

        # Test data
        command = "go to kitchen and pick up the red cube"
        robot_state = {"battery_level": 80, "position": {"x": 0, "y": 0}}
        environment_data = {"objects": [{"id": "red_cube", "color": "red"}]}

        # Execute test
        result = self.planner.plan_actions(command, robot_state, environment_data)

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result["intent"], "fetch_object")
        self.assertIn("red_cube", result["objects"])
        self.assertIn("kitchen", result["locations"])
        self.assertEqual(len(result["actions"]), 2)

    def test_validate_plan_safe_action(self):
        """Test validation of a safe plan."""
        safe_plan = {
            "intent": "move_forward",
            "actions": [
                {"type": "navigation", "target": "forward"}
            ]
        }
        is_valid = self.planner.validate_plan(safe_plan)
        self.assertTrue(is_valid)

    def test_validate_plan_dangerous_action(self):
        """Test validation of a dangerous plan."""
        dangerous_plan = {
            "intent": "damage_object",
            "actions": [
                {"type": "destroy", "target": "object"}
            ]
        }
        is_valid = self.planner.validate_plan(dangerous_plan)
        self.assertFalse(is_valid)


class TestAdvancedCognitivePlanner(unittest.TestCase):
    """Test cases for the advanced cognitive planner."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.planner = AdvancedCognitivePlanner(api_key="test-key")

    @patch('cognitive_planner.openai.ChatCompletion.create')
    def test_plan_complex_action(self, mock_create):
        """Test planning for a complex multi-step action."""
        # Mock the API response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = {
            'content': '''
            {
                "intent": "complex_fetch_task",
                "decomposition": {
                    "primary_goal": "fetch_and_deliver_object",
                    "subtasks": [
                        {
                            "id": "st1",
                            "description": "navigate_to_object",
                            "dependencies": [],
                            "actions": ["navigation"]
                        },
                        {
                            "id": "st2",
                            "description": "grasp_object",
                            "dependencies": ["st1"],
                            "actions": ["manipulation"]
                        }
                    ]
                },
                "objects": ["red_cube"],
                "locations": ["kitchen", "living_room"],
                "action_sequence": [
                    {
                        "id": "a1",
                        "type": "navigation",
                        "target": "kitchen",
                        "parameters": {"x": 1.0, "y": 2.0},
                        "preconditions": ["battery_sufficient"],
                        "expected_outcomes": ["at_kitchen"]
                    },
                    {
                        "id": "a2",
                        "type": "manipulation",
                        "target": "red_cube",
                        "parameters": {"action": "grasp"},
                        "preconditions": ["at_kitchen", "object_visible"],
                        "expected_outcomes": ["object_grasped"]
                    }
                ],
                "safety_checks": [
                    {
                        "check_type": "path_clear",
                        "description": "Ensure path is clear of obstacles",
                        "critical": true
                    }
                ],
                "estimated_duration": 120.5,
                "confidence": 0.85
            }
            '''
        }
        mock_create.return_value = mock_response

        # Test data
        command = "go to kitchen, pick up the red cube, and bring it to living room"
        robot_state = {"battery_level": 80, "position": {"x": 0, "y": 0}}
        environment_data = {"objects": [{"id": "red_cube", "color": "red"}]}

        # Execute test
        result = self.planner.plan_complex_action(command, robot_state, environment_data)

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result["intent"], "complex_fetch_task")
        self.assertIn("red_cube", result["objects"])
        self.assertGreater(len(result["action_sequence"]), 1)
        self.assertGreater(result["confidence"], 0.5)

    def test_validate_complex_plan(self):
        """Test validation of a complex plan."""
        valid_plan = {
            "intent": "test",
            "action_sequence": [
                {"id": "a1", "type": "navigation", "target": "location"}
            ],
            "safety_checks": [
                {"check_type": "path_clear", "critical": True}
            ],
            "decomposition": {
                "subtasks": [
                    {"id": "st1", "dependencies": []}
                ]
            }
        }

        is_valid, issues = self.planner.validate_complex_plan(valid_plan)
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)

    def test_validate_complex_plan_missing_critical_check(self):
        """Test validation of a plan without critical safety checks."""
        invalid_plan = {
            "intent": "test",
            "action_sequence": [
                {"id": "a1", "type": "navigation", "target": "location"}
            ],
            "safety_checks": [],  # No critical checks
            "decomposition": {
                "subtasks": [
                    {"id": "st1", "dependencies": []}
                ]
            }
        }

        is_valid, issues = self.planner.validate_complex_plan(invalid_plan)
        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)
        # Check if the issue is about missing critical safety checks
        critical_check_issue = any("critical safety checks" in issue.lower() for issue in issues)
        self.assertTrue(critical_check_issue)


def run_tests():
    """Run all tests."""
    print("Running LLM integration and cognitive planning tests...")

    # Create test suites
    basic_suite = unittest.TestLoader().loadTestsFromTestCase(TestVLACognitivePlanner)
    advanced_suite = unittest.TestLoader().loadTestsFromTestCase(TestAdvancedCognitivePlanner)

    # Run tests
    all_tests = unittest.TestSuite([basic_suite, advanced_suite])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(all_tests)

    # Print summary
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)