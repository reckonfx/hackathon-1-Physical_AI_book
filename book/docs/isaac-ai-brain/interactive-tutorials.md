---
id: interactive-tutorials
title: Interactive Tutorials
sidebar_position: 7
description: Interactive tutorials with hands-on exercises for Isaac Sim learning
---

# Interactive Tutorials

<div className="isaac-module">
  <p>This lesson provides interactive tutorials with hands-on exercises that allow students to practice with immediate feedback in Isaac Sim environments.</p>
</div>

## Learning Objectives

By the end of this lesson, you will be able to:
- Navigate interactive tutorial framework
- Complete hands-on exercises with validation
- Apply Isaac Sim concepts in practical scenarios
- Use validation scripts to verify your work

## Prerequisites

- Completed all previous lessons in Module 3
- Isaac Sim properly installed with ROS 2 bridge
- Basic understanding of Python for validation scripts
- Completed synthetic data generation lesson

## Introduction to Interactive Learning

Interactive tutorials are designed to provide hands-on experience with Isaac Sim concepts through practical exercises. Each tutorial includes:

- Clear objectives and instructions
- Step-by-step guidance
- Validation mechanisms to check your work
- Immediate feedback on completion

### Tutorial Structure

Each interactive tutorial follows this structure:
1. **Objective**: Clear statement of what you'll learn
2. **Prerequisites**: What you need to complete the tutorial
3. **Steps**: Detailed instructions for completion
4. **Validation**: How to verify your work
5. **Summary**: Key takeaways and next steps

## Tutorial Framework

### Validation Script System

The interactive tutorial framework uses Python validation scripts to check your work:

```python
#!/usr/bin/env python3
# validate_isaac_sim_tutorial.py
# Generic validation framework for Isaac Sim tutorials

import sys
import os
import subprocess
import time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

class IsaacSimValidator(Node):
    def __init__(self):
        super().__init__('isaac_sim_validator')
        self.validation_results = {}

        # Publishers for validation status
        self.status_pub = self.create_publisher(String, 'tutorial_validation/status', 10)

        # Subscribers for different validation targets
        self.camera_sub = self.create_subscription(
            Image, '/camera/image_rect_color', self.camera_callback, 10)
        self.pose_sub = self.create_subscription(
            PoseStamped, '/robot/pose', self.pose_callback, 10)

        self.camera_received = False
        self.pose_received = False

    def camera_callback(self, msg):
        self.camera_received = True
        self.get_logger().info('Camera data received')

    def pose_callback(self, msg):
        self.pose_received = True
        self.get_logger().info('Pose data received')

    def validate_camera_data(self):
        """Validate that camera data is being published"""
        timeout = 10  # seconds
        start_time = time.time()

        while not self.camera_received and (time.time() - start_time) < timeout:
            rclpy.spin_once(self, timeout_sec=0.1)

        return self.camera_received

    def validate_robot_pose(self):
        """Validate that robot pose is being published"""
        timeout = 10  # seconds
        start_time = time.time()

        while not self.pose_received and (time.time() - start_time) < timeout:
            rclpy.spin_once(self, timeout_sec=0.1)

        return self.pose_received

    def run_validation(self, tutorial_name):
        """Run validation for a specific tutorial"""
        self.get_logger().info(f'Running validation for {tutorial_name}')

        if tutorial_name == 'camera_setup':
            result = self.validate_camera_data()
            return {'tutorial': tutorial_name, 'passed': result, 'details': 'Camera data validation'}
        elif tutorial_name == 'robot_control':
            result = self.validate_robot_pose()
            return {'tutorial': tutorial_name, 'passed': result, 'details': 'Robot pose validation'}

        return {'tutorial': tutorial_name, 'passed': False, 'details': 'Unknown tutorial'}

def main(args=None):
    rclpy.init(args=args)

    validator = IsaacSimValidator()

    if len(sys.argv) < 2:
        print("Usage: python3 validate_isaac_sim_tutorial.py <tutorial_name>")
        print("Available tutorials: camera_setup, robot_control")
        return

    tutorial_name = sys.argv[1]
    result = validator.run_validation(tutorial_name)

    print(f"Validation Result: {result}")

    if result['passed']:
        print(f"✓ {tutorial_name} tutorial completed successfully!")
    else:
        print(f"✗ {tutorial_name} tutorial validation failed!")

    validator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Tutorial 1: Isaac Sim Scene Setup

### Objective
Create a basic Isaac Sim scene with a humanoid robot and validate that it's properly configured.

### Prerequisites
- Isaac Sim installed and running
- Basic understanding of Isaac Sim interface

### Steps to Complete

1. **Launch Isaac Sim**:
   - Open Omniverse Launcher
   - Start Isaac Sim

2. **Create a New Scene**:
   - Go to `File` → `New Scene`
   - Clear any existing objects

3. **Add a Ground Plane**:
   - Click `Create` → `Primitive` → `Plane`
   - Scale to 10x10 units

4. **Add a Humanoid Robot**:
   - Click `Create` → `Robot` → `Astrik` (or another humanoid robot)
   - Position on the ground plane

5. **Add a Camera**:
   - Click `Create` → `Sensor` → `Camera`
   - Attach to the robot or place in the scene

6. **Configure ROS Bridge**:
   - Add ROS bridge nodes to the graph
   - Configure camera publisher to `/camera/image_rect_color`

7. **Save the Scene**:
   - Save as `tutorial_scene_1.usd`

### Validation

Run the validation script to check your scene:

```bash
# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Run validation for scene setup
python3 validate_isaac_sim_tutorial.py camera_setup
```

## Tutorial 2: Isaac ROS Integration

### Objective
Integrate Isaac Sim with ROS 2 and verify sensor data publishing.

### Prerequisites
- Completed Tutorial 1
- ROS 2 Humble installed
- Isaac ROS packages installed

### Steps to Complete

1. **Load Your Scene**:
   - Open the scene created in Tutorial 1

2. **Set Up ROS Bridge**:
   - In Isaac Sim, open the Graph tab
   - Add ROS bridge nodes:
     - Isaac Create Camera Info
     - Isaac Create RGB
     - ROS Publish Camera Info
     - ROS Publish RGB

3. **Configure Publishers**:
   - Connect camera to publisher nodes
   - Set topic names:
     - RGB: `/camera/image_rect_color`
     - Camera Info: `/camera/camera_info`

4. **Verify in ROS**:
   - In a new terminal, source ROS 2:
   ```bash
   source /opt/ros/humble/setup.bash
   ```
   - Check available topics:
   ```bash
   ros2 topic list | grep camera
   ```

5. **Test Data Flow**:
   - Play the Isaac Sim scene
   - Listen to camera topics:
   ```bash
   ros2 topic echo /camera/image_rect_color --field header.stamp -c
   ```

### Validation

```bash
# Run validation for ROS integration
python3 validate_isaac_sim_tutorial.py robot_control
```

## Tutorial 3: VSLAM Pipeline Implementation

### Objective
Implement a complete VSLAM pipeline in Isaac Sim and validate its performance.

### Prerequisites
- Completed Tutorials 1 and 2
- Understanding of VSLAM concepts
- Isaac ROS VSLAM packages installed

### Steps to Complete

1. **Install VSLAM Packages**:
   ```bash
   sudo apt install ros-humble-isaac-ros-visual-slam
   ```

2. **Configure Stereo Cameras**:
   - In Isaac Sim, create two cameras for stereo vision
   - Position them appropriately for stereo depth estimation
   - Configure camera parameters (baseline, focal length, etc.)

3. **Set Up VSLAM Pipeline**:
   - Launch the Isaac ROS VSLAM node:
   ```bash
   ros2 launch isaac_ros_visual_slam visual_slam_node.launch.py
   ```

4. **Test VSLAM**:
   - Move the robot in Isaac Sim to generate visual odometry
   - Monitor the `/visual_slam/tracking/pose` topic
   - Visualize results in RViz

5. **Validate Results**:
   - Check that pose estimates are being published
   - Verify that the map is being built correctly
   - Test loop closure detection

### Validation Script

```python
#!/usr/bin/env python3
# validate_vslam_tutorial.py
# VSLAM tutorial validation

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
import time

class VSLAMValidator(Node):
    def __init__(self):
        super().__init__('vslam_validator')

        self.pose_sub = self.create_subscription(
            PoseStamped,
            '/visual_slam/tracking/pose',
            self.pose_callback,
            10)

        self.odom_sub = self.create_subscription(
            Odometry,
            '/visual_slam/odometry',
            self.odom_callback,
            10)

        self.pose_received = False
        self.odom_received = False

        self.poses = []
        self.odoms = []

    def pose_callback(self, msg):
        self.pose_received = True
        self.poses.append(msg.pose.position)
        self.get_logger().info('VSLAM pose received')

    def odom_callback(self, msg):
        self.odom_received = True
        self.odoms.append(msg.pose.pose.position)
        self.get_logger().info('VSLAM odometry received')

    def validate_vslam(self):
        """Validate VSLAM pipeline"""
        timeout = 30  # seconds
        start_time = time.time()

        while (not self.pose_received or not self.odom_received) and (time.time() - start_time) < timeout:
            rclpy.spin_once(self, timeout_sec=0.1)

        # Check that we have movement data
        if len(self.poses) > 5:
            return True
        else:
            return False

def main(args=None):
    rclpy.init(args=args)
    validator = VSLAMValidator()

    print("Validating VSLAM pipeline...")
    result = validator.validate_vslam()

    if result:
        print("✓ VSLAM tutorial completed successfully!")
        print(f"  - Received {len(validator.poses)} pose estimates")
        print(f"  - Received {len(validator.odoms)} odometry messages")
    else:
        print("✗ VSLAM tutorial validation failed!")
        print("  - Check that the robot moved in Isaac Sim")
        print("  - Verify VSLAM nodes are running correctly")

    validator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Tutorial 4: Nav2 Navigation with Bipedal Constraints

### Objective
Configure and test Nav2 navigation with custom bipedal plugins in Isaac Sim.

### Prerequisites
- Completed VSLAM tutorial
- Custom bipedal controller built
- Isaac Sim scene with navigation map

### Steps to Complete

1. **Build Custom Controller**:
   ```bash
   cd ~/nav2_bipedal_ws
   colcon build --packages-select nav2_bipedal_controller
   source install/setup.bash
   ```

2. **Launch Navigation Stack**:
   ```bash
   ros2 launch isaac_nav2_bringup bipedal_nav2.launch.xml
   ```

3. **Configure Navigation Parameters**:
   - Set bipedal-specific parameters in the config files
   - Adjust step width and height constraints
   - Configure balance constraints

4. **Test Navigation**:
   - Send navigation goals to the robot
   - Observe path planning and execution
   - Verify bipedal constraints are enforced

5. **Validate Performance**:
   - Check that the robot follows the planned path
   - Verify that balance constraints are maintained
   - Test obstacle avoidance behavior

### Validation

```bash
# Run navigation validation
# This would involve sending goals and checking execution
ros2 run nav2_test_launch send_goal.py 1.0 1.0 0.0
```

## Tutorial 5: Synthetic Data Generation Pipeline

### Objective
Create a complete synthetic data generation pipeline for perception training.

### Prerequisites
- Understanding of Isaac Sim Replicator
- Python programming skills
- Completed previous tutorials

### Steps to Complete

1. **Create Domain Randomization Scene**:
   - Set up a scene with multiple object types
   - Configure materials for randomization
   - Add lighting with randomization

2. **Configure Data Generation**:
   - Set up RGB, depth, and segmentation outputs
   - Configure annotation generation
   - Set output directory and format

3. **Run Data Generation**:
   - Execute the replicator script
   - Monitor data generation progress
   - Verify output quality

4. **Process Generated Data**:
   - Run quality assurance checks
   - Create dataset splits
   - Validate data alignment

5. **Train a Model**:
   - Use the generated data to train a simple model
   - Validate model performance
   - Compare with real-world data if available

### Validation Script

```python
#!/usr/bin/env python3
# validate_synthetic_data_tutorial.py
# Synthetic data tutorial validation

import os
import json
from PIL import Image

def validate_synthetic_data_tutorial(dataset_path):
    """Validate the synthetic data generation tutorial"""

    required_dirs = ['rgb', 'depth', 'segmentation', 'annotations']
    required_files = ['dataset_config.json', 'train_split.txt', 'validation_split.txt', 'test_split.txt']

    # Check directories
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = os.path.join(dataset_path, dir_name)
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_name)

    # Check files
    missing_files = []
    for file_name in required_files:
        file_path = os.path.join(dataset_path, file_name)
        if not os.path.exists(file_path):
            missing_files.append(file_name)

    # Count samples
    if os.path.exists(os.path.join(dataset_path, 'rgb')):
        sample_count = len(os.listdir(os.path.join(dataset_path, 'rgb')))
    else:
        sample_count = 0

    validation_result = {
        'missing_directories': missing_dirs,
        'missing_files': missing_files,
        'sample_count': sample_count,
        'tutorial_passed': len(missing_dirs) == 0 and len(missing_files) == 0 and sample_count > 0
    }

    return validation_result

def main():
    dataset_path = "synthetic_perception_data"

    print("Validating synthetic data generation tutorial...")
    result = validate_synthetic_data_tutorial(dataset_path)

    if result['tutorial_passed']:
        print(f"✓ Synthetic data tutorial completed successfully!")
        print(f"  - Generated {result['sample_count']} samples")
    else:
        print("✗ Synthetic data tutorial validation failed!")
        if result['missing_directories']:
            print(f"  - Missing directories: {result['missing_directories']}")
        if result['missing_files']:
            print(f"  - Missing files: {result['missing_files']}")
        if result['sample_count'] == 0:
            print("  - No samples generated")

if __name__ == "__main__":
    main()
```

## Hands-on Exercise: Complete Isaac Sim Workflow

### Exercise Objective
Complete a full workflow from scene creation to navigation in Isaac Sim.

### Steps to Complete

1. Create a new Isaac Sim scene with humanoid robot
2. Set up Isaac ROS bridge for sensor data
3. Implement VSLAM pipeline for localization
4. Configure Nav2 with bipedal constraints
5. Generate synthetic data for perception training
6. Validate each component using the tutorial framework

### Validation Commands

```bash
# Complete workflow validation
source /opt/ros/humble/setup.bash
source ~/nav2_bipedal_ws/install/setup.bash

# Validate each component
python3 validate_isaac_sim_tutorial.py camera_setup
python3 validate_isaac_sim_tutorial.py robot_control
python3 validate_vslam_tutorial.py
python3 validate_synthetic_data_tutorial.py
```

## Troubleshooting Interactive Tutorials

### Common Issues
- **ROS connection issues**: Verify ROS environment is sourced
- **Isaac Sim not responding**: Check GPU resources and restart if needed
- **Validation script errors**: Ensure all dependencies are installed
- **Scene setup problems**: Verify Isaac Sim installation and extensions

### Getting Help
- Check the Isaac Sim documentation for specific error messages
- Verify that all required packages are installed
- Ensure Isaac Sim and ROS 2 are properly configured

## Summary

In this lesson, you learned:
- How to use the interactive tutorial framework
- How to complete hands-on exercises with validation
- How to validate your work at each step
- How to troubleshoot common issues

These interactive tutorials provide practical experience with Isaac Sim concepts and validate your understanding through hands-on exercises.

## References

- [Isaac Sim Interactive Tutorials](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorial_isaac_sim_basics.html)
- [ROS 2 Integration Tutorials](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorial_ros_bridge.html)

## Author Information

<div className="author-info">
  <h3>Author: Aamir Ahmed Shamsi</h3>
  <p><strong>GIAIC ID:</strong> 00486031</p>
  <p>This lesson was created with assistance from Claude AI.</p>
</div>