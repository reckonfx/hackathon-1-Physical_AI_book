# Worked Examples: Full VLA Pipeline

This document provides detailed worked examples showing the complete Vision-Language-Action (VLA) pipeline from voice input to robot execution.

## Example 1: Pick Up Red Cube

### Scenario
User says: "Pick up the red cube"

### Complete Pipeline Walkthrough

#### Step 1: Voice Input Processing
- **Input**: Audio containing "Pick up the red cube"
- **Processing**: Whisper transcribes audio to text
- **Output**: "Pick up the red cube"
- **Code Reference**:
  ```python
  # From examples/vla/voice-processing/voice-command-to-ros2-action.py
  text = recognizer.recognize_whisper(audio, model="base")
  ```

#### Step 2: Natural Language Understanding
- **Input**: "Pick up the red cube"
- **Processing**: LLM interprets command and extracts entities
- **Entities Identified**:
  - Action: "pick up" / "grasp"
  - Object: "red cube"
  - Color: "red"
  - Type: "cube"
- **Code Reference**:
  ```python
  # From examples/vla/llm-integration/llm-cognitive-planner.py
  plan = planner.plan_actions(command, robot_state, environment_data)
  ```

#### Step 3: Environment Analysis
- **Current Robot State**:
  - Position: (0.0, 0.0, 0.0)
  - Battery: 85%
  - Gripper: Open
- **Environment Data**:
  - Objects detected: red cube at (1.5, 0.8, 0.0), blue sphere at (-0.5, 1.2, 0.0)
  - Navigable areas: kitchen, living room
  - Obstacles: furniture at (1.0, 0.5)

#### Step 4: Cognitive Planning
- **Generated Action Plan**:
  ```json
  {
    "intent": "grasp_red_cube",
    "objects": ["red_cube"],
    "locations": [],
    "actions": [
      {
        "id": "nav_to_cube",
        "type": "navigation",
        "target": {"x": 1.5, "y": 0.8, "z": 0.0},
        "parameters": {}
      },
      {
        "id": "align_with_cube",
        "type": "manipulation",
        "target": "red_cube",
        "parameters": {"action": "align"}
      },
      {
        "id": "grasp_cube",
        "type": "manipulation",
        "target": "red_cube",
        "parameters": {"action": "grasp"}
      }
    ],
    "safety_checks": ["path_clear", "object_verification"]
  }
  ```

#### Step 5: Action Execution
- **Navigation Phase**:
  - Robot moves from (0.0, 0.0) to (1.5, 0.8)
  - Avoids obstacle at (1.0, 0.5)
  - Uses `NavigateToPose` action client
- **Manipulation Phase**:
  - Manipulator controller positions gripper near red cube
  - Gripper closes to grasp the cube
  - Force sensors verify successful grasp

#### Step 6: Verification and Feedback
- **Status**: "Successfully picked up the red cube"
- **Updated Robot State**:
  - Gripper: Closed with object
  - Carried object: red cube

### Complete Code Implementation
```python
#!/usr/bin/env python3
"""
Worked Example 1: Pick Up Red Cube
Complete implementation of the full VLA pipeline.
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

import speech_recognition as sr
import openai
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Image
from nav2_msgs.action import NavigateToPose

from llm_cognitive_planner import VLACognitivePlanner


class WorkedExample1(Node):
    """
    Complete implementation of 'Pick up the red cube' example.
    """

    def __init__(self):
        super().__init__('worked_example_1')

        # Initialize components
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.cognitive_planner = VLACognitivePlanner(api_key="your-api-key")

        # Publishers and subscribers
        self.status_pub = self.create_publisher(String, '/vla_status', 10)
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Environment data simulation
        self.environment_data = {
            'objects': [
                {'id': 'red_cube', 'color': 'red', 'type': 'cube', 'position': {'x': 1.5, 'y': 0.8}},
                {'id': 'blue_sphere', 'color': 'blue', 'type': 'sphere', 'position': {'x': -0.5, 'y': 1.2}}
            ]
        }

    def run_example(self):
        """Execute the complete 'Pick up red cube' example."""
        command = "Pick up the red cube"
        self.get_logger().info(f"Processing command: {command}")

        # Step 1: Process command through cognitive planner
        robot_state = self.get_robot_state()
        action_plan = self.cognitive_planner.plan_actions(command, robot_state, self.environment_data)

        if action_plan and self.cognitive_planner.validate_plan(action_plan):
            # Step 2: Execute the action plan
            success = self.execute_action_plan(action_plan)

            if success:
                self.get_logger().info("Example completed successfully!")
                self.status_pub.publish(String(data="Successfully picked up the red cube"))
            else:
                self.get_logger().error("Example execution failed")
                self.status_pub.publish(String(data="Failed to pick up the red cube"))
        else:
            self.get_logger().error("Failed to generate valid action plan")

    def get_robot_state(self):
        """Get current robot state."""
        return {
            'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
            'battery': 85,
            'gripper_status': 'open'
        }

    def execute_action_plan(self, plan):
        """Execute the planned actions."""
        success = True
        for action in plan.get('actions', []):
            action_success = self.execute_single_action(action)
            success = success and action_success
            if not action_success:
                break
        return success

    def execute_single_action(self, action):
        """Execute a single action."""
        action_type = action.get('type')
        if action_type == 'navigation':
            return self.execute_navigation_action(action)
        elif action_type == 'manipulation':
            return self.execute_manipulation_action(action)
        else:
            self.get_logger().warning(f"Unknown action type: {action_type}")
            return False

    def execute_navigation_action(self, action):
        """Execute navigation action."""
        target = action.get('target', {})
        self.get_logger().info(f"Navigating to {target}")
        # In a real implementation, this would call the navigation action server
        return True  # Simulated success

    def execute_manipulation_action(self, action):
        """Execute manipulation action."""
        target = action.get('target', 'unknown')
        act = action.get('parameters', {}).get('action', 'unknown')
        self.get_logger().info(f"Performing {act} on {target}")
        # In a real implementation, this would control the manipulator
        return True  # Simulated success


def main():
    rclpy.init()
    example = WorkedExample1()
    example.run_example()
    example.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Example 2: Navigate to Kitchen and Fetch Item

### Scenario
User says: "Go to the kitchen and bring me the blue mug"

### Pipeline Walkthrough

#### Step 1: Voice Processing
- **Input**: Audio with "Go to the kitchen and bring me the blue mug"
- **Output**: Text transcript

#### Step 2: Command Decomposition
- **Intent**: Fetch specific object from specific location
- **Location**: kitchen
- **Object**: blue mug
- **Action sequence**: navigate → detect → grasp → return

#### Step 3: Environment Context
- **Known locations**: kitchen at (3.0, 2.0, 0.0), living room at (-1.0, 1.5, 0.0)
- **Objects in environment**: blue mug, red cup, green bottle

#### Step 4: Action Plan
1. Navigate to kitchen (3.0, 2.0)
2. Detect blue mug in kitchen area
3. Grasp blue mug
4. Return to user location

#### Step 5: Execution
- Navigation to kitchen with obstacle avoidance
- Object detection in kitchen
- Grasping with appropriate force
- Safe return navigation

## Example 3: Complex Multi-Step Task

### Scenario
User says: "Find all red objects in the living room and move them to the kitchen"

### Pipeline Walkthrough

#### Step 1: Command Analysis
- **Action**: Find → Move
- **Objects**: red objects
- **Source**: living room
- **Destination**: kitchen

#### Step 2: Multi-Step Planning
1. Navigate to living room
2. Scan for red objects
3. For each red object: grasp and move to kitchen
4. Repeat until no more red objects found

#### Step 3: Execution Loop
- Iterative detection and manipulation
- Continuous environment monitoring
- Adaptive planning based on discoveries

### Key Implementation Patterns

#### Pattern 1: Error Handling
```python
def execute_with_retry(action, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = execute_action(action)
            if result.success:
                return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1)  # Wait before retry
    return None
```

#### Pattern 2: Safety Validation
```python
def validate_action_safety(action, robot_state, environment):
    # Check for collision risks
    # Verify robot capabilities
    # Confirm environmental constraints
    return safety_check_passed
```

#### Pattern 3: Feedback Integration
```python
def update_plan_based_on_feedback(plan, feedback):
    # Adjust plan based on execution results
    # Learn from successes and failures
    # Improve future planning
    return updated_plan
```

## Performance Considerations

### Latency Optimization
- Cache frequently accessed information
- Use lightweight models for real-time tasks
- Implement asynchronous processing where possible

### Reliability Measures
- Comprehensive error handling
- Graceful degradation when components fail
- Continuous monitoring and status reporting

### Safety Protocols
- Multiple validation steps before action execution
- Emergency stop capabilities
- Collision avoidance systems

These worked examples demonstrate the complete VLA pipeline integration, showing how voice commands are transformed into physical robot actions through the coordinated operation of voice processing, cognitive planning, and robot control systems.