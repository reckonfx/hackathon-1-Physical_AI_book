#!/usr/bin/env python3
"""
LLM Cognitive Planning Implementation for VLA Systems

This script demonstrates how to integrate Large Language Models (LLMs)
with robotics for cognitive planning in Vision-Language-Action (VLA) systems.
"""

import openai
import json
import time
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VLACognitivePlanner:
    """
    Cognitive planner that uses LLMs to convert natural language commands
    into structured action plans for robotics.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the cognitive planner.

        Args:
            api_key: OpenAI API key (if not set, expects OPENAI_API_KEY environment variable)
            model: LLM model to use for planning
        """
        if api_key:
            openai.api_key = api_key
        self.model = model

        self.system_prompt = """
        You are a cognitive planner for a Vision-Language-Action (VLA) robotics system.
        Your role is to interpret natural language commands and generate structured action plans.
        Each action plan should include:
        - Intent: The overall goal of the command
        - Objects: Any objects mentioned in the command
        - Locations: Any locations mentioned in the command
        - Action sequence: A series of specific actions to achieve the goal
        - Safety checks: Any safety considerations for the robot

        Respond in valid JSON format with the following structure:
        {
            "intent": "string",
            "objects": ["string"],
            "locations": ["string"],
            "actions": [
                {
                    "type": "string",
                    "target": "string",
                    "parameters": {}
                }
            ],
            "safety_checks": ["string"]
        }
        """

    def plan_actions(self, command: str, robot_state: Dict[str, Any],
                     environment_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate an action plan for the given command using LLM.

        Args:
            command: Natural language command from user
            robot_state: Current state of the robot
            environment_data: Current environmental data from sensors

        Returns:
            Structured action plan or None if planning failed
        """
        user_prompt = f"""
        Command: {command}

        Robot State: {json.dumps(robot_state, indent=2)}
        Environment Data: {json.dumps(environment_data, indent=2)}

        Generate a structured action plan in JSON format.
        """

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature for consistent, safe outputs
                max_tokens=1000,
                timeout=30
            )

            # Parse the LLM response into a structured action plan
            plan_text = response.choices[0].message['content'].strip()

            # Extract JSON from response (in case it includes explanations)
            json_start = plan_text.find('{')
            json_end = plan_text.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                plan_json = plan_text[json_start:json_end]
                plan = json.loads(plan_json)
                logger.info(f"Generated action plan: {plan['intent']}")
                return plan
            else:
                logger.error(f"Could not extract JSON from LLM response: {plan_text}")
                return None

        except openai.error.RateLimitError:
            logger.error("OpenAI API rate limit exceeded")
            return None
        except openai.error.AuthenticationError:
            logger.error("OpenAI API authentication failed")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Raw response: {plan_text}")
            return None
        except Exception as e:
            logger.error(f"Error in cognitive planning: {e}")
            return None

    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Validate the generated action plan for safety and feasibility.

        Args:
            plan: Action plan to validate

        Returns:
            True if plan is valid, False otherwise
        """
        if not plan:
            return False

        # Check for required fields
        required_fields = ['intent', 'actions']
        for field in required_fields:
            if field not in plan:
                logger.warning(f"Missing required field in plan: {field}")
                return False

        # Check for potentially dangerous actions
        for action in plan.get('actions', []):
            action_type = action.get('type', '').lower()
            if action_type in ['destroy', 'damage', 'harm']:
                logger.warning(f"Potentially dangerous action detected: {action_type}")
                return False

        # Validate action structure
        for i, action in enumerate(plan.get('actions', [])):
            if 'type' not in action:
                logger.warning(f"Action {i} missing 'type' field")
                return False

        return True


def example_usage():
    """Example usage of the cognitive planner."""
    # Initialize the planner
    planner = VLACognitivePlanner()

    # Example robot state
    robot_state = {
        "battery_level": 85,
        "current_pose": {"x": 0.0, "y": 0.0, "theta": 0.0},
        "gripper_status": "open",
        "navigation_status": "idle",
        "last_command_time": time.time()
    }

    # Example environment data
    environment_data = {
        "objects_detected": [
            {"id": "red_cube", "type": "cube", "color": "red", "position": {"x": 1.5, "y": 0.8}},
            {"id": "blue_sphere", "type": "sphere", "color": "blue", "position": {"x": -0.5, "y": 1.2}}
        ],
        "navigable_areas": ["kitchen", "living_room", "bedroom"],
        "obstacles": []
    }

    # Test commands
    test_commands = [
        "Pick up the red cube",
        "Go to the kitchen",
        "Navigate to the red cube and grasp it",
        "Find the blue sphere and bring it to me"
    ]

    for command in test_commands:
        print(f"\nProcessing command: '{command}'")
        plan = planner.plan_actions(command, robot_state, environment_data)

        if plan and planner.validate_plan(plan):
            print(f"Intent: {plan['intent']}")
            print(f"Objects: {plan['objects']}")
            print(f"Locations: {plan['locations']}")
            print(f"Actions: {len(plan['actions'])} action(s)")
            for i, action in enumerate(plan['actions']):
                print(f"  {i+1}. {action['type']} {action.get('target', '')}")
        else:
            print("Failed to generate or validate action plan")


if __name__ == '__main__':
    example_usage()