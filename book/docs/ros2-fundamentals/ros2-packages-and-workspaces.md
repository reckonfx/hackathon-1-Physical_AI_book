---
id: ros2-packages-and-workspaces
title: ROS2 Packages and Workspaces
sidebar_position: 5
description: Organizing ROS2 code with packages and workspaces for robotics development
---

# ROS2 Packages and Workspaces

<div className="ros2-module">
  <p>This lesson covers ROS2 packages and workspaces for organizing robotics code and dependencies.</p>
</div>

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand the structure of ROS2 packages
- Create and manage ROS2 workspaces
- Build and install ROS2 packages
- Manage dependencies and package configurations
- Validate package functionality

## Prerequisites

- Understanding of ROS2 basic concepts
- Completed previous ROS2 lessons

## Introduction to ROS2 Packages

ROS2 packages are the fundamental unit of code organization in ROS2. A package contains:

- **Source code**: Nodes, libraries, and executables
- **Configuration files**: Launch files, parameter files, URDF models
- **Documentation**: Package descriptions and usage instructions
- **Dependencies**: List of required packages and libraries

### Package Structure

A typical ROS2 package follows this structure:

```
my_robot_package/
├── CMakeLists.txt          # Build configuration for C++
├── package.xml             # Package metadata and dependencies
├── src/                    # Source code files
│   ├── my_node.cpp
│   └── my_library.cpp
├── include/                # Header files (C++)
├── launch/                 # Launch files
├── config/                 # Configuration files
├── models/                 # Robot models (URDF, SDF)
├── worlds/                 # Simulation worlds
└── scripts/                # Python scripts
```

## Creating a ROS2 Package

### Using the Command Line

```bash
# Create a new package with Python
ros2 pkg create --build-type ament_python my_robot_package

# Create a new package with C++
ros2 pkg create --build-type ament_cmake my_robot_package

# Create a package with dependencies
ros2 pkg create --build-type ament_python --dependencies rclpy std_msgs geometry_msgs my_robot_package
```

### Package.xml File

The `package.xml` file contains metadata about the package:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_robot_package</name>
  <version>0.1.0</version>
  <description>Package for my robot functionality</description>
  <maintainer email="aamir@example.com">Aamir Ahmed Shamsi</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>geometry_msgs</depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

## Python Package Structure

For Python-based packages, the structure is slightly different:

```
my_robot_package/
├── package.xml
├── setup.py
├── setup.cfg
├── my_robot_package/
│   ├── __init__.py
│   ├── my_node.py
│   └── my_library.py
└── test/
    └── test_my_robot_package.py
```

### setup.py File

```python
from setuptools import setup

package_name = 'my_robot_package'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/my_robot_package']),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Aamir Ahmed Shamsi',
    maintainer_email='aamir@example.com',
    description='Package for my robot functionality',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = my_robot_package.my_node:main',
        ],
    },
)
```

## ROS2 Workspaces

A workspace is a directory that contains multiple ROS2 packages and their build artifacts.

### Workspace Structure

```
ros2_workspace/
├── src/                    # Source packages
│   ├── my_robot_package/
│   ├── navigation_package/
│   └── perception_package/
├── build/                  # Build artifacts
├── install/                # Installed packages
└── log/                    # Build logs
```

### Creating and Building a Workspace

```bash
# Create workspace directory
mkdir -p ~/ros2_workspace/src

# Navigate to workspace
cd ~/ros2_workspace

# Build all packages in workspace
colcon build

# Source the workspace
source install/setup.bash
```

## Managing Dependencies

### Package Dependencies

Dependencies are declared in `package.xml`:

```xml
<!-- Build dependencies (needed for compilation) -->
<build_depend>rclcpp</build_depend>
<build_depend>std_msgs</build_depend>

<!-- Execution dependencies (needed at runtime) -->
<exec_depend>rclpy</exec_depend>
<exec_depend>std_msgs</exec_depend>

<!-- Test dependencies -->
<test_depend>ament_copyright</test_depend>
<test_depend>ament_flake8</test_depend>
<test_depend>ament_pep257</test_depend>
```

### Resolving Dependencies

```bash
# Install dependencies for all packages in workspace
rosdep install --from-paths src --ignore-src -r -y

# Install dependencies for a specific package
rosdep install --from-paths src/my_robot_package --ignore-src -r -y
```

## C++ Package Example

Here's a complete example of a C++ ROS2 package:

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_package)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# Create executable
add_executable(my_robot_node src/my_robot_node.cpp)
ament_target_dependencies(my_robot_node rclcpp std_msgs)

# Install targets
install(TARGETS
  my_robot_node
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
```

### Source Code (src/my_robot_node.cpp)

```cpp
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MyRobotNode : public rclcpp::Node
{
public:
  MyRobotNode() : Node("my_robot_node")
  {
    publisher_ = this->create_publisher<std_msgs::msg::String>("robot_status", 10);
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(500), std::bind(&MyRobotNode::timer_callback, this));
  }

private:
  void timer_callback()
  {
    auto message = std_msgs::msg::String();
    message.data = "Robot is operational at " + std::to_string(this->now().nanoseconds());
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
    publisher_->publish(message);
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
};

int main(int argc, char * argv[])
{
  rclpy::init(argc, argv);
  rclpy::spin(std::make_shared<MyRobotNode>());
  rclpy::shutdown();
  return 0;
}
```

## Python Package Example

Here's a complete example of a Python ROS2 package:

### Python Node (my_robot_package/my_node.py)

```python
#!/usr/bin/env python3
# my_node.py
# Example ROS2 Python node

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import math

class MyRobotNode(Node):
    def __init__(self):
        super().__init__('my_robot_node')

        # Create publisher
        self.publisher_ = self.create_publisher(String, 'robot_status', 10)

        # Create subscriber
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10)

        # Create timer
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.i = 0
        self.get_logger().info('My Robot Node started')

    def timer_callback(self):
        msg = String()
        msg.data = f'Robot status update: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')
        self.i += 1

    def cmd_vel_callback(self, msg):
        linear_speed = math.sqrt(msg.linear.x**2 + msg.linear.y**2 + msg.linear.z**2)
        angular_speed = math.sqrt(msg.angular.x**2 + msg.angular.y**2 + msg.angular.z**2)

        self.get_logger().info(
            f'Received command: linear={linear_speed:.2f}, angular={angular_speed:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    my_robot_node = MyRobotNode()

    try:
        rclpy.spin(my_robot_node)
    except KeyboardInterrupt:
        pass
    finally:
        my_robot_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Hands-on Exercise: Package Creation

### Exercise Objective
Create a complete ROS2 package with nodes, dependencies, and launch files.

### Steps to Complete

1. Create a new workspace
2. Create a package with dependencies
3. Implement a Python node
4. Create a launch file
5. Build and test the package

### Package Creation Commands

```bash
# Create workspace
mkdir -p ~/robotics_ws/src
cd ~/robotics_ws

# Create package
ros2 pkg create --build-type ament_python --dependencies rclpy std_msgs geometry_msgs sensor_msgs my_robot_package

# Build the workspace
colcon build

# Source the workspace
source install/setup.bash
```

### Validation Commands

```bash
# List available packages
ros2 pkg list | grep my_robot

# Run the node
ros2 run my_robot_package my_robot_node

# Check available topics
ros2 topic list
```

## Package Management Best Practices

### 1. Version Control
- Use Git for source code management
- Tag releases with semantic versioning
- Include .gitignore for build artifacts

### 2. Documentation
- Write clear package descriptions
- Document all public interfaces
- Include usage examples

### 3. Testing
- Write unit tests for all functionality
- Use ament tools for code quality checks
- Test integration with other packages

### 4. Dependency Management
- Declare minimal required dependencies
- Avoid circular dependencies
- Use specific version ranges when needed

## Troubleshooting Package Issues

### Common Issues
- **Package not found**: Check if workspace is sourced
- **Build errors**: Verify dependencies are installed
- **Import errors**: Check Python path and module installation
- **Permission errors**: Ensure correct file permissions

### Debugging Tips
- Use `ros2 pkg executables` to list available nodes
- Check `AMENT_PREFIX_PATH` for installed packages
- Use `colcon build --packages-select package_name` for specific builds

## Summary

In this lesson, you learned:
- How to create and structure ROS2 packages
- How to manage ROS2 workspaces
- How to declare and manage dependencies
- Best practices for package organization

## References

- [ROS2 Package Documentation](https://docs.ros.org/en/humble/How-To-Guides/Creating-A-ROS2-Package.html)
- [ROS2 Workspaces Guide](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)

## Author Information

<div className="author-info">
  <h3>Author: Aamir Ahmed Shamsi</h3>
  <p><strong>GIAIC ID:</strong> 00486031</p>
  <p>This lesson was created with assistance from Claude AI.</p>
</div>