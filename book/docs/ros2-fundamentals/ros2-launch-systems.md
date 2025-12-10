---
id: ros2-launch-systems
title: ROS2 Launch Systems
sidebar_position: 4
description: Managing complex robotic applications with ROS2 launch systems
---

# ROS2 Launch Systems

<div className="ros2-module">
  <p>This lesson covers ROS2 launch systems for managing complex robotic applications with multiple nodes.</p>
</div>

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand the ROS2 launch system architecture
- Create launch files for multiple nodes
- Configure node parameters in launch files
- Use launch arguments and conditions
- Validate launch system functionality

## Prerequisites

- Understanding of ROS2 nodes, topics, services, and actions
- Completed previous ROS2 lessons

## Introduction to ROS2 Launch

The ROS2 launch system provides a way to start multiple nodes with specific configurations in a coordinated manner. This is essential for complex robotic applications that require multiple coordinated nodes.

### Benefits of Launch Systems

- **Coordination**: Start multiple nodes simultaneously
- **Configuration**: Set parameters for all nodes at once
- **Management**: Control lifecycle of multiple nodes
- **Repeatability**: Consistent startup across different environments

## Basic Launch File Structure

A launch file is a Python file that defines which nodes to launch and how to configure them:

```python
#!/usr/bin/env python3
# basic_launch.py
# Basic ROS2 launch file example

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='demo_nodes_py',
            executable='listener',
            name='listener',
            parameters=[
                {'use_sim_time': True}
            ],
            remappings=[
                ('chatter', 'my_chatter')
            ]
        ),
        Node(
            package='demo_nodes_py',
            executable='talker',
            name='talker',
            parameters=[
                {'use_sim_time': True}
            ],
            remappings=[
                ('chatter', 'my_chatter')
            ]
        )
    ])
```

## Launch Arguments

Launch arguments allow customization of launch files:

```python
#!/usr/bin/env python3
# argument_launch.py
# Launch file with arguments example

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='robot1',
        description='Name of the robot'
    )

    # Use launch configurations
    use_sim_time = LaunchConfiguration('use_sim_time')
    robot_name = LaunchConfiguration('robot_name')

    return LaunchDescription([
        use_sim_time_arg,
        robot_name_arg,

        Node(
            package='demo_nodes_py',
            executable='listener',
            name=[robot_name, '_listener'],
            parameters=[
                {'use_sim_time': use_sim_time}
            ]
        )
    ])
```

## Conditional Launch

Launch files can include conditional logic:

```python
#!/usr/bin/env python3
# conditional_launch.py
# Launch file with conditions example

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare arguments
    enable_gui_arg = DeclareLaunchArgument(
        'enable_gui',
        default_value='false',
        description='Enable GUI nodes'
    )

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    # Get configurations
    enable_gui = LaunchConfiguration('enable_gui')
    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([
        enable_gui_arg,
        use_sim_time_arg,

        # Always start the core node
        Node(
            package='demo_nodes_py',
            executable='listener',
            name='core_listener',
            parameters=[
                {'use_sim_time': use_sim_time}
            ]
        ),

        # Conditionally start GUI node
        Node(
            condition=IfCondition(enable_gui),
            package='rviz2',
            executable='rviz2',
            name='rviz',
            parameters=[
                {'use_sim_time': use_sim_time}
            ]
        )
    ])
```

## Complex Launch Example

Here's a more complex example that demonstrates various launch features:

```python
#!/usr/bin/env python3
# complex_robot_launch.py
# Complex robot launch file example

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Declare launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='my_robot',
        description='Name of the robot'
    )

    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=PathJoinSubstitution([
            FindPackageShare('my_robot_bringup'),
            'config',
            'robot_config.yaml'
        ]),
        description='Path to configuration file'
    )

    # Get configurations
    use_sim_time = LaunchConfiguration('use_sim_time')
    robot_name = LaunchConfiguration('robot_name')
    config_file = LaunchConfiguration('config_file')

    # Robot state publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'use_sim_time': use_sim_time},
            config_file
        ],
        remappings=[
            ('/joint_states', [robot_name, '/joint_states'])
        ]
    )

    # Joint state publisher node
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )

    # Navigation nodes
    nav_bringup_nodes = [
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            parameters=[
                {'use_sim_time': use_sim_time}
            ]
        ),
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            parameters=[
                {'use_sim_time': use_sim_time}
            ]
        ),
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            parameters=[
                {'use_sim_time': use_sim_time}
            ]
        )
    ]

    # Create launch description
    ld = LaunchDescription([
        use_sim_time_arg,
        robot_name_arg,
        config_file_arg,

        robot_state_publisher,
        joint_state_publisher
    ])

    # Add navigation nodes
    for node in nav_bringup_nodes:
        ld.add_action(node)

    return ld
```

## Launch File Best Practices

### 1. Parameter Organization
- Group related parameters in YAML files
- Use descriptive names for launch arguments
- Document all parameters and arguments

### 2. Node Naming
- Use consistent naming conventions
- Include robot names in node names for multi-robot systems
- Avoid name conflicts

### 3. Error Handling
- Validate required arguments
- Provide sensible defaults
- Use appropriate logging

## Hands-on Exercise: Launch System

### Exercise Objective
Create a launch file for a complete robotic system with multiple nodes.

### Steps to Complete

1. Create a launch file for a robot with sensors
2. Include navigation stack nodes
3. Add visualization nodes
4. Use launch arguments for configuration
5. Test the launch system

### Launch File Template

```python
#!/usr/bin/env python3
# robot_bringup_launch.py
# Complete robot launch file

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():
    # Declare launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    # Get configurations
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )

    # Sensor processing node
    sensor_processor = Node(
        package='your_sensor_package',
        executable='sensor_processor',
        parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )

    # Perception node
    perception_node = Node(
        package='your_perception_package',
        executable='perception_node',
        parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )

    return LaunchDescription([
        use_sim_time_arg,
        robot_state_publisher,
        sensor_processor,
        perception_node
    ])
```

### Running the Launch File

```bash
# Run with default parameters
ros2 launch your_package robot_bringup_launch.py

# Run with custom parameters
ros2 launch your_package robot_bringup_launch.py use_sim_time:=true
```

## Troubleshooting Launch Issues

### Common Issues
- **Node not found**: Check package name and executable name
- **Parameter issues**: Verify parameter file paths and syntax
- **Name conflicts**: Use unique names for nodes in multi-robot systems
- **Missing dependencies**: Ensure all required packages are installed

### Debugging Tips
- Use `--show-args` to see available launch arguments
- Check ROS_DOMAIN_ID if running multiple systems
- Use `ros2 launch` with `--wait` for debugging

## Summary

In this lesson, you learned:
- How to create launch files for complex robotic systems
- How to use launch arguments for customization
- How to implement conditional launching
- Best practices for organizing launch systems

## References

- [ROS2 Launch Documentation](https://docs.ros.org/en/humble/How-To-Guides/Launch-system.html)
- [Launch Files Tutorial](https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Creating-Launch-Files.html)

## Author Information

<div className="author-info">
  <h3>Author: Aamir Ahmed Shamsi</h3>
  <p><strong>GIAIC ID:</strong> 00486031</p>
  <p>This lesson was created with assistance from Claude AI.</p>
</div>