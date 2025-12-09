#!/usr/bin/env python3
"""
Cognitive Planning Implementation for VLA Systems

This script demonstrates advanced cognitive planning techniques
for Vision-Language-Action (VLA) systems using LLMs.
"""

import openai
import json
import time
from typing import Dict, List, Any, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedCognitivePlanner:
    """
    Advanced cognitive planner with multi-step reasoning and memory.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize the advanced cognitive planner.

        Args:
            api_key: OpenAI API key (if not set, expects OPENAI_API_KEY environment variable)
            model: LLM model to use for planning
        """
        if api_key:
            openai.api_key = api_key
        self.model = model
        self.conversation_history = []

        self.system_prompt = """
        You are an advanced cognitive planner for a Vision-Language-Action (VLA) robotics system.
        Your role is to interpret complex natural language commands and generate detailed action plans
        with multi-step reasoning, context awareness, and safety considerations.

        Your planning process should include:
        1. Command interpretation and intent recognition
        2. Environment analysis and context understanding
        3. Multi-step action decomposition
        4. Safety validation and risk assessment
        5. Plan optimization for efficiency

        Respond in valid JSON format with the following structure:
        {
            "intent": "string",
            "decomposition": {
                "primary_goal": "string",
                "subtasks": [
                    {
                        "id": "string",
                        "description": "string",
                        "dependencies": ["string"],
                        "actions": ["string"]
                    }
                ]
            },
            "objects": ["string"],
            "locations": ["string"],
            "action_sequence": [
                {
                    "id": "string",
                    "type": "string",
                    "target": "string",
                    "parameters": {},
                    "preconditions": ["string"],
                    "expected_outcomes": ["string"]
                }
            ],
            "safety_checks": [
                {
                    "check_type": "string",
                    "description": "string",
                    "critical": true/false
                }
            ],
            "estimated_duration": "float",  # in seconds
            "confidence": "float"  # 0.0 to 1.0
        }
        """

    def plan_complex_action(self, command: str, robot_state: Dict[str, Any],
                          environment_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate a complex action plan for the given command using advanced LLM reasoning.

        Args:
            command: Complex natural language command from user
            robot_state: Current state of the robot
            environment_data: Current environmental data from sensors

        Returns:
            Detailed action plan or None if planning failed
        """
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": command,
            "timestamp": time.time()
        })

        # Include conversation history for context
        history_context = "\n".join([
            f"Previous command: {item['content']}"
            for item in self.conversation_history[-3:]  # Last 3 interactions
        ])

        user_prompt = f"""
        Command: {command}

        Conversation History:
        {history_context}

        Robot State: {json.dumps(robot_state, indent=2)}
        Environment Data: {json.dumps(environment_data, indent=2)}

        Generate a detailed action plan in JSON format with multi-step reasoning.
        """

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,  # Slightly higher for creativity while maintaining safety
                max_tokens=1500,
                timeout=45
            )

            # Parse the LLM response into a structured action plan
            plan_text = response.choices[0].message['content'].strip()

            # Extract JSON from response (in case it includes explanations)
            json_start = plan_text.find('{')
            json_end = plan_text.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                plan_json = plan_text[json_start:json_end]
                plan = json.loads(plan_json)

                # Add to conversation history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": f"Planned action for: {command}",
                    "plan_intent": plan.get("intent", "unknown"),
                    "timestamp": time.time()
                })

                logger.info(f"Generated complex action plan: {plan['intent']}")
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
            logger.error(f"Error in advanced cognitive planning: {e}")
            return None

    def validate_complex_plan(self, plan: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate the generated complex action plan for safety and feasibility.

        Args:
            plan: Action plan to validate

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        if not plan:
            issues.append("Plan is None")
            return False, issues

        # Check for required fields
        required_fields = ['intent', 'action_sequence']
        for field in required_fields:
            if field not in plan:
                issues.append(f"Missing required field in plan: {field}")

        # Check for potentially dangerous actions
        for action in plan.get('action_sequence', []):
            action_type = action.get('type', '').lower()
            if action_type in ['destroy', 'damage', 'harm', 'injure']:
                issues.append(f"Potentially dangerous action detected: {action_type}")

        # Validate action structure
        for i, action in enumerate(plan.get('action_sequence', [])):
            if 'type' not in action:
                issues.append(f"Action {i} missing 'type' field")
            if 'id' not in action:
                issues.append(f"Action {i} missing 'id' field")

        # Check subtask dependencies
        subtasks = plan.get('decomposition', {}).get('subtasks', [])
        for subtask in subtasks:
            for dep_id in subtask.get('dependencies', []):
                if not any(st['id'] == dep_id for st in subtasks):
                    issues.append(f"Subtask dependency '{dep_id}' does not exist")

        # Validate safety checks
        safety_checks = plan.get('safety_checks', [])
        critical_safety_failures = [sc for sc in safety_checks if sc.get('critical', False)]
        if not critical_safety_failures:
            issues.append("No critical safety checks defined")

        is_valid = len(issues) == 0
        return is_valid, issues

    def update_plan_based_on_feedback(self, plan: Dict[str, Any], feedback: str) -> Optional[Dict[str, Any]]:
        """
        Update a plan based on execution feedback.

        Args:
            plan: Original action plan
            feedback: Feedback from plan execution

        Returns:
            Updated plan or None if update failed
        """
        user_prompt = f"""
        Original Plan: {json.dumps(plan, indent=2)}

        Execution Feedback: {feedback}

        Based on the feedback, update the plan to address the issues encountered.
        Return the updated plan in the same JSON format.
        """

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=1200,
                timeout=30
            )

            plan_text = response.choices[0].message['content'].strip()
            json_start = plan_text.find('{')
            json_end = plan_text.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                plan_json = plan_text[json_start:json_end]
                updated_plan = json.loads(plan_json)
                logger.info(f"Updated plan based on feedback: {updated_plan['intent']}")
                return updated_plan
            else:
                logger.error(f"Could not extract JSON from feedback response: {plan_text}")
                return None

        except Exception as e:
            logger.error(f"Error updating plan based on feedback: {e}")
            return None


def example_usage():
    """Example usage of the advanced cognitive planner."""
    # Initialize the planner
    planner = AdvancedCognitivePlanner()

    # Example robot state
    robot_state = {
        "battery_level": 75,
        "current_pose": {"x": 0.0, "y": 0.0, "theta": 0.0},
        "gripper_status": "open",
        "navigation_status": "idle",
        "manipulation_capability": True,
        "last_command_time": time.time()
    }

    # Example environment data
    environment_data = {
        "objects_detected": [
            {"id": "red_cube", "type": "cube", "color": "red", "position": {"x": 1.5, "y": 0.8}},
            {"id": "blue_sphere", "type": "sphere", "color": "blue", "position": {"x": -0.5, "y": 1.2}},
            {"id": "green_pyramid", "type": "pyramid", "color": "green", "position": {"x": 2.0, "y": -1.0}}
        ],
        "navigable_areas": ["kitchen", "living_room", "bedroom", "office"],
        "obstacles": [
            {"type": "furniture", "position": {"x": 1.0, "y": 0.5}, "size": {"width": 0.8, "height": 1.2}}
        ],
        "navigation_map": "available"
    }

    # Test complex commands
    test_commands = [
        "Go to the kitchen, find the red cup on the table, pick it up, and bring it to the living room",
        "Identify all blue objects in the office and move them to the storage area",
        "Navigate to the person, ask what they need help with, and assist them appropriately"
    ]

    for command in test_commands:
        print(f"\nProcessing complex command: '{command}'")
        plan = planner.plan_complex_action(command, robot_state, environment_data)

        if plan:
            is_valid, issues = planner.validate_complex_plan(plan)
            if is_valid:
                print(f"Intent: {plan['intent']}")
                print(f"Estimated Duration: {plan.get('estimated_duration', 'unknown')} seconds")
                print(f"Confidence: {plan.get('confidence', 0.0):.2f}")
                print(f"Subtasks: {len(plan.get('decomposition', {}).get('subtasks', []))}")
                print(f"Action Sequence: {len(plan['action_sequence'])} actions")

                # Show first few actions
                for i, action in enumerate(plan['action_sequence'][:3]):
                    print(f"  {i+1}. {action['type']} {action.get('target', '')}")

                if len(plan['action_sequence']) > 3:
                    print(f"  ... and {len(plan['action_sequence']) - 3} more actions")
            else:
                print(f"Plan validation failed with {len(issues)} issues:")
                for issue in issues[:5]:  # Show first 5 issues
                    print(f"  - {issue}")
                if len(issues) > 5:
                    print(f"  ... and {len(issues) - 5} more issues")
        else:
            print("Failed to generate action plan")


if __name__ == '__main__':
    example_usage()