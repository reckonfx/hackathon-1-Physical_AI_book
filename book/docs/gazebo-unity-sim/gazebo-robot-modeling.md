---
id: gazebo-robot-modeling
title: Gazebo Robot Modeling
sidebar_position: 2
description: Creating robot models for physics simulation in Gazebo
---

# Gazebo Robot Modeling

<div className="gazebo-module">
  <p>This lesson covers creating robot models for physics simulation in Gazebo, including URDF and SDF formats.</p>
</div>

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand the URDF and SDF robot description formats
- Create basic robot models with links and joints
- Add physical properties to robot models
- Validate robot models for simulation
- Integrate models with ROS2

## Prerequisites

- Basic understanding of robotics concepts
- Completed ROS2 fundamentals module
- Understanding of coordinate systems and transformations

## Introduction to Robot Modeling

Robot modeling in Gazebo involves creating digital representations of physical robots that accurately simulate their kinematics, dynamics, and physical properties. Two primary formats are used:

- **URDF (Unified Robot Description Format)**: XML-based format commonly used in ROS
- **SDF (Simulation Description Format)**: More flexible format used by Gazebo

### URDF vs SDF

| Feature | URDF | SDF |
|---------|------|-----|
| Primary Use | ROS ecosystem | Gazebo simulation |
| Flexibility | Limited | High |
| Complexity | Simpler | More complex |
| Gazebo Integration | Requires conversion | Native support |

## URDF Robot Model Structure

A URDF robot model consists of:

- **Links**: Rigid bodies with mass, inertia, and visual/collision properties
- **Joints**: Connections between links with specific degrees of freedom
- **Transmissions**: Mapping between actuators and joints
- **Gazebo plugins**: Simulation-specific extensions

### Basic URDF Example

```xml
<?xml version="1.0"?>
<robot name="simple_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Wheel links -->
  <link name="wheel_front_left">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.002"/>
    </inertial>
  </link>

  <!-- Joint connecting wheel to base -->
  <joint name="wheel_front_left_joint" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_front_left"/>
    <origin xyz="0.2 0.2 -0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

  <!-- Additional joints and links would follow -->
</robot>
```

## Advanced URDF Features

### Using Xacro for Complex Models

Xacro (XML Macros) allows for more complex and reusable robot models:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="advanced_robot">

  <!-- Properties -->
  <xacro:property name="M_PI" value="3.1415926535897931" />
  <xacro:property name="wheel_radius" value="0.1" />
  <xacro:property name="wheel_width" value="0.05" />
  <xacro:property name="base_width" value="0.5" />
  <xacro:property name="base_length" value="0.5" />
  <xacro:property name="base_height" value="0.2" />

  <!-- Macro for wheels -->
  <xacro:macro name="wheel" params="prefix *origin">
    <link name="${prefix}_wheel">
      <visual>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
        <material name="black">
          <color rgba="0 0 0 1"/>
        </material>
      </visual>
      <collision>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="0.2"/>
        <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.002"/>
      </inertial>
    </link>

    <joint name="${prefix}_wheel_joint" type="continuous">
      <parent link="base_link"/>
      <child link="${prefix}_wheel"/>
      <xacro:insert_block name="origin"/>
      <axis xyz="0 1 0"/>
    </joint>
  </xacro:macro>

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="${base_width} ${base_length} ${base_height}"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="${base_width} ${base_length} ${base_height}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="0.416" ixy="0" ixz="0" iyy="0.416" iyz="0" izz="0.833"/>
    </inertial>
  </link>

  <!-- Create wheels using macro -->
  <xacro:wheel prefix="front_left">
    <origin xyz="${base_length/2} ${base_width/2} -${wheel_radius}" rpy="${M_PI/2} 0 0"/>
  </xacro:wheel>

  <xacro:wheel prefix="front_right">
    <origin xyz="${base_length/2} -${base_width/2} -${wheel_radius}" rpy="${M_PI/2} 0 0"/>
  </xacro:wheel>

  <!-- Additional wheels -->
  <xacro:wheel prefix="rear_left">
    <origin xyz="-${base_length/2} ${base_width/2} -${wheel_radius}" rpy="${M_PI/2} 0 0"/>
  </xacro:wheel>

  <xacro:wheel prefix="rear_right">
    <origin xyz="-${base_length/2} -${base_width/2} -${wheel_radius}" rpy="${M_PI/2} 0 0"/>
  </xacro:wheel>

</robot>
```

## SDF Robot Model

SDF provides more flexibility and native Gazebo support:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_robot">
    <!-- Base link -->
    <link name="base_link">
      <pose>0 0 0.1 0 0 0</pose>
      <inertial>
        <mass>1.0</mass>
        <inertia>
          <ixx>0.1</ixx>
          <ixy>0</ixy>
          <ixz>0</ixz>
          <iyy>0.1</iyy>
          <iyz>0</iyz>
          <izz>0.1</izz>
        </inertia>
      </inertial>

      <visual name="base_visual">
        <geometry>
          <box>
            <size>0.5 0.5 0.2</size>
          </box>
        </geometry>
        <material>
          <ambient>0 0 1 1</ambient>
          <diffuse>0 0 1 1</diffuse>
        </material>
      </visual>

      <collision name="base_collision">
        <geometry>
          <box>
            <size>0.5 0.5 0.2</size>
          </box>
        </geometry>
      </collision>
    </link>

    <!-- Wheel link -->
    <link name="wheel_front_left">
      <pose>0.2 0.2 0 0 0 0</pose>
      <inertial>
        <mass>0.2</mass>
        <inertia>
          <ixx>0.001</ixx>
          <ixy>0</ixy>
          <ixz>0</ixz>
          <iyy>0.001</iyy>
          <iyz>0</iyz>
          <izz>0.002</izz>
        </inertia>
      </inertial>

      <visual name="wheel_visual">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.05</length>
          </cylinder>
        </geometry>
      </visual>

      <collision name="wheel_collision">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.05</length>
          </cylinder>
        </geometry>
      </collision>
    </link>

    <!-- Joint -->
    <joint name="wheel_front_left_joint" type="continuous">
      <parent>base_link</parent>
      <child>wheel_front_left</child>
      <axis>
        <xyz>0 1 0</xyz>
      </axis>
    </joint>

    <!-- Gazebo plugin for ROS2 control -->
    <plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">
      <ros>
        <namespace>simple_robot</namespace>
        <remapping>cmd_vel:=cmd_vel</remapping>
        <remapping>odom:=odom</remapping>
      </ros>
      <left_joint>wheel_front_left_joint</left_joint>
      <right_joint>wheel_front_right_joint</right_joint>
      <wheel_separation>0.4</wheel_separation>
      <wheel_diameter>0.2</wheel_diameter>
      <max_wheel_torque>20</max_wheel_torque>
      <max_wheel_acceleration>1.0</max_wheel_acceleration>
    </plugin>
  </model>
</sdf>
```

## Adding Sensors to Robot Models

### Camera Sensor Example

```xml
<!-- In URDF -->
<gazebo reference="camera_link">
  <sensor type="camera" name="camera1">
    <update_rate>30.0</update_rate>
    <camera name="head">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>600</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <ros>
        <namespace>camera</namespace>
        <remapping>image_raw:=image_color</remapping>
        <remapping>camera_info:=camera_info</remapping>
      </ros>
      <camera_name>camera</camera_name>
      <image_topic_name>image_raw</image_topic_name>
      <camera_info_topic_name>camera_info</camera_info_topic_name>
      <frame_name>camera_link_optical</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

### LiDAR Sensor Example

```xml
<!-- In URDF -->
<gazebo reference="lidar_link">
  <sensor type="ray" name="lidar_sensor">
    <pose>0 0 0 0 0 0</pose>
    <visualize>true</visualize>
    <update_rate>10</update_rate>
    <ray>
      <scan>
        <horizontal>
          <samples>720</samples>
          <resolution>1</resolution>
          <min_angle>-1.570796</min_angle>
          <max_angle>1.570796</max_angle>
        </horizontal>
      </scan>
      <range>
        <min>0.10</min>
        <max>30.0</max>
        <resolution>0.01</resolution>
      </range>
    </ray>
    <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
      <ros>
        <namespace>lidar</namespace>
        <remapping>scan:=scan</remapping>
      </ros>
      <output_type>sensor_msgs/LaserScan</output_type>
      <frame_name>lidar_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

## Hands-on Exercise: Robot Model Creation

### Exercise Objective
Create a complete robot model with base, wheels, and sensors.

### Steps to Complete

1. Create a URDF file for a simple differential drive robot
2. Add visual and collision properties
3. Include inertial properties for physics simulation
4. Add Gazebo plugins for ROS2 integration
5. Validate the model in Gazebo

### Model Validation Script

```python
#!/usr/bin/env python3
# validate_robot_model.py
# Script to validate robot model

import xml.etree.ElementTree as ET
import sys
import subprocess

def validate_urdf_model(urdf_file):
    """Validate URDF model using check_urdf tool"""
    try:
        result = subprocess.run(['check_urdf', urdf_file],
                                capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ URDF model {urdf_file} is valid")
            return True
        else:
            print(f"✗ URDF model {urdf_file} validation failed:")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("check_urdf tool not found. Install ros-humble-urdfdom-py")
        return False
    except subprocess.TimeoutExpired:
        print("Validation timed out")
        return False

def check_model_properties(urdf_file):
    """Check basic properties of the URDF model"""
    try:
        tree = ET.parse(urdf_file)
        root = tree.getroot()

        # Count links and joints
        links = root.findall('.//link')
        joints = root.findall('.//joint')

        print(f"Model contains {len(links)} links and {len(joints)} joints")

        # Check for essential elements
        has_base = any(link.get('name') == 'base_link' for link in links)
        has_inertial = any(link.find('inertial') is not None for link in links)
        has_visual = any(link.find('visual') is not None for link in links)
        has_collision = any(link.find('collision') is not None for link in links)

        print(f"Has base link: {has_base}")
        print(f"Has inertial properties: {has_inertial}")
        print(f"Has visual properties: {has_visual}")
        print(f"Has collision properties: {has_collision}")

        return has_base and has_inertial and has_visual and has_collision

    except ET.ParseError as e:
        print(f"Error parsing URDF file: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_robot_model.py <urdf_file>")
        return

    urdf_file = sys.argv[1]

    print(f"Validating robot model: {urdf_file}")

    # Check basic properties
    basic_valid = check_model_properties(urdf_file)

    # Validate with URDF tool
    urdf_valid = validate_urdf_model(urdf_file)

    if basic_valid and urdf_valid:
        print("✓ Robot model validation completed successfully!")
    else:
        print("✗ Robot model validation failed!")

if __name__ == "__main__":
    main()
```

### Running the Validation

```bash
# Validate the robot model
python3 validate_robot_model.py simple_robot.urdf

# Load the model in Gazebo (if Gazebo is installed)
gz sim -r simple_robot.sdf
```

## Best Practices for Robot Modeling

### 1. Mass and Inertia Properties
- Use realistic mass values based on actual robot components
- Calculate inertia tensors accurately for stable simulation
- Use CAD tools to compute mass properties when possible

### 2. Visual and Collision Models
- Use simplified collision models for performance
- Ensure visual models match physical dimensions
- Use appropriate level of detail for simulation requirements

### 3. Joint Configuration
- Use appropriate joint types (revolute, continuous, prismatic)
- Set proper joint limits and dynamics
- Configure joint friction and damping for realistic behavior

### 4. Sensor Integration
- Position sensors accurately on the robot model
- Configure sensor parameters to match real hardware
- Validate sensor data in simulation

## Troubleshooting Model Issues

### Common Issues
- **Model not loading**: Check XML syntax and required elements
- **Physics instability**: Verify mass and inertia properties
- **Joint issues**: Check joint types and limits
- **Collision problems**: Ensure collision geometries are properly defined

### Debugging Tips
- Use `check_urdf` to validate model syntax
- Check Gazebo console for error messages
- Verify that all referenced files exist
- Use RViz to visualize the robot model

## Summary

In this lesson, you learned:
- How to create robot models using URDF and SDF formats
- How to define links, joints, and physical properties
- How to add sensors and actuators to robot models
- Best practices for robot modeling and validation

Robot modeling is fundamental for simulation-based robotics development and provides the foundation for testing and validating robotic systems before deployment on real hardware.

## References

- [URDF Documentation](http://wiki.ros.org/urdf)
- [SDF Documentation](http://sdformat.org/)
- [Gazebo Robot Modeling Tutorial](http://gazebosim.org/tutorials?tut=ros2_overview)

## Author Information

<div className="author-info">
  <h3>Author: Aamir Ahmed Shamsi</h3>
  <p><strong>GIAIC ID:</strong> 00486031</p>
  <p>This lesson was created with assistance from Claude AI.</p>
</div>