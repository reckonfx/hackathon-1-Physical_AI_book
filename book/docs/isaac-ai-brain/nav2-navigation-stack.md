---
id: nav2-navigation-stack
title: Nav2 Navigation Stack
sidebar_position: 5
description: Nav2 navigation stack with custom bipedal plugins for humanoid robotics
---

# Nav2 Navigation Stack

<div className="isaac-module">
  <p>This lesson covers the Nav2 navigation stack with custom bipedal plugins for humanoid robotics applications.</p>
</div>

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand the Nav2 navigation stack architecture
- Configure Nav2 for humanoid robotics with bipedal constraints
- Implement custom bipedal navigation plugins
- Integrate Nav2 with Isaac Sim for navigation validation

## Prerequisites

- Completed VSLAM Implementation lesson
- Understanding of ROS 2 navigation concepts
- Isaac Sim scene with VSLAM pipeline configured
- Basic knowledge of path planning algorithms

## Introduction to Nav2 for Humanoid Robotics

The Navigation2 (Nav2) stack is the state-of-the-art navigation framework for ROS 2. For humanoid robotics, Nav2 requires special considerations due to:

- Bipedal locomotion constraints
- Balance and stability requirements
- Different kinematics compared to wheeled robots
- Complex footstep planning requirements

### Nav2 Architecture Components

1. **Navigation Server**: Main orchestrator for navigation tasks
2. **Planner Server**: Global path planning (NavFn, A*, etc.)
3. **Controller Server**: Local path following (DWB, TEB, etc.)
4. **Recovery Server**: Recovery behaviors for stuck situations
5. **Lifecycle Manager**: Manages the lifecycle of navigation components

## Nav2 Installation and Setup

### Installing Nav2 Packages

```bash
# Install Nav2 packages
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup

# Install additional tools
sudo apt install ros-humble-nav2-rviz-plugins
```

### Creating Custom Bipedal Workspace

```bash
# Create workspace for custom plugins
mkdir -p ~/nav2_bipedal_ws/src
cd ~/nav2_bipedal_ws/src

# Create custom controller package
ros2 pkg create --build-type ament_cmake nav2_bipedal_controller
```

## Configuring Nav2 for Bipedal Navigation

### Costmap Configuration

For humanoid robots, the costmap needs special parameters:

```yaml
# costmap_params.yaml
local_costmap:
  global_frame: odom
  robot_base_frame: base_link
  update_frequency: 10.0
  publish_frequency: 10.0
  width: 10
  height: 10
  resolution: 0.05
  origin_x: -5.0
  origin_y: -5.0
  plugins:
    - {name: obstacles, type: "nav2_costmap_2d::ObstacleLayer"}
    - {name: inflation, type: "nav2_costmap_2d::InflationLayer"}

global_costmap:
  global_frame: map
  robot_base_frame: base_link
  update_frequency: 1.0
  publish_frequency: 1.0
  width: 200
  height: 200
  resolution: 0.1
  origin_x: -100.0
  origin_y: -100.0
  plugins:
    - {name: static, type: "nav2_costmap_2d::StaticLayer"}
    - {name: obstacles, type: "nav2_costmap_2d::ObstacleLayer"}
    - {name: inflation, type: "nav2_costmap_2d::InflationLayer"}
```

### Bipedal-Specific Parameters

```yaml
# controller_server_params.yaml
controller_server:
  ros__parameters:
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["FollowPath"]

    # FollowPath controller
    FollowPath:
      plugin: "nav2_mppi_controller::MPPIController"
      time_steps: 50
      control_frequency: 20.0
      vx_std: 0.2
      vy_std: 0.2
      wz_std: 0.3
      model_dt: 0.05
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25
      state_reset_distance: 0.5
      max_iterations: 4
      motion_model: "DiffDriveMotionModel"
      # Custom bipedal parameters
      step_width_max: 0.3  # Maximum step width for bipedal
      step_height_max: 0.1 # Maximum step height for bipedal
      balance_constraint: 0.8 # Balance constraint factor
```

## Implementing Custom Bipedal Plugins

### Creating a Bipedal Controller

Let's create a custom controller that considers bipedal constraints:

```cpp
// nav2_bipedal_controller/src/bipedal_controller.cpp
#include <math.h>
#include <memory>
#include <string>
#include <vector>

#include "nav2_core/controller.hpp"
#include "nav2_util/odometry_utils.hpp"
#include "nav2_util/geometry_utils.hpp"
#include "nav_2d_utils/parameters.hpp"
#include "nav_2d_utils/path_ops.hpp"
#include "nav_msgs/msg/path.hpp"
#include "geometry_msgs/msg/twist.hpp"

namespace nav2_bipedal_controller
{

class BipedalController : public nav2_core::Controller
{
public:
  BipedalController() = default;
  ~BipedalController() override = default;

  void configure(
    const rclcpp_lifecycle::LifecycleNode::WeakPtr & parent,
    std::string name, const std::shared_ptr<tf2_ros::Buffer> & tf,
    const std::shared_ptr<nav2_costmap_2d::Costmap2DROS> & costmap_ros) override
  {
    node_ = parent.lock();
    name_ = name;
    tf_ = tf;
    costmap_ros_ = costmap_ros;
    costmap_ = costmap_ros_->getCostmap();

    // Bipedal-specific parameters
    node_->declare_parameter(name_ + ".step_width_max", 0.3);
    node_->declare_parameter(name_ + ".step_height_max", 0.1);
    node_->declare_parameter(name_ + ".balance_constraint", 0.8);

    step_width_max_ = node_->get_parameter(name_ + ".step_width_max").as_double();
    step_height_max_ = node_->get_parameter(name_ + ".step_height_max").as_double();
    balance_constraint_ = node_->get_parameter(name_ + ".balance_constraint").as_double();
  }

  void cleanup() override
  {
    RCLCPP_INFO(node_->get_logger(), "Cleaning up controller");
  }

  void activate() override
  {
    RCLCPP_INFO(node_->get_logger(), "Activating controller");
  }

  void deactivate() override
  {
    RCLCPP_INFO(node_->get_logger(), "Deactivating controller");
  }

  geometry_msgs::msg::TwistStamped computeVelocityCommands(
    const geometry_msgs::msg::PoseStamped & pose,
    const geometry_msgs::msg::Twist & velocity,
    nav2_core::GoalChecker * goal_checker) override
  {
    geometry_msgs::msg::TwistStamped cmd_vel;
    cmd_vel.header.frame_id = pose.header.frame_id;
    cmd_vel.header.stamp = node_->now();

    // Bipedal-specific velocity computation
    // This is a simplified example - real implementation would be more complex
    cmd_vel.twist.linear.x = computeBipedalLinearVelocity(pose, velocity);
    cmd_vel.twist.angular.z = computeBipedalAngularVelocity(pose, velocity);

    // Apply bipedal constraints
    applyBipedalConstraints(cmd_vel.twist);

    return cmd_vel;
  }

private:
  double computeBipedalLinearVelocity(
    const geometry_msgs::msg::PoseStamped & pose,
    const geometry_msgs::msg::Twist & velocity)
  {
    // Simplified bipedal velocity computation
    // Consider step constraints, balance, etc.
    return 0.5; // Placeholder value
  }

  double computeBipedalAngularVelocity(
    const geometry_msgs::msg::PoseStamped & pose,
    const geometry_msgs::msg::Twist & velocity)
  {
    // Simplified bipedal angular velocity computation
    return 0.2; // Placeholder value
  }

  void applyBipedalConstraints(geometry_msgs::msg::Twist & cmd_vel)
  {
    // Apply maximum velocity constraints based on bipedal capabilities
    double max_linear = step_width_max_ * 2.0; // Simplified constraint
    double max_angular = balance_constraint_ * 0.5; // Simplified constraint

    if (cmd_vel.linear.x > max_linear) {
      cmd_vel.linear.x = max_linear;
    } else if (cmd_vel.linear.x < -max_linear) {
      cmd_vel.linear.x = -max_linear;
    }

    if (cmd_vel.angular.z > max_angular) {
      cmd_vel.angular.z = max_angular;
    } else if (cmd_vel.angular.z < -max_angular) {
      cmd_vel.angular.z = -max_angular;
    }
  }

  rclcpp_lifecycle::LifecycleNode::SharedPtr node_;
  std::string name_;
  std::shared_ptr<tf2_ros::Buffer> tf_;
  std::shared_ptr<nav2_costmap_2d::Costmap2DROS> costmap_ros_;
  nav2_costmap_2d::Costmap2D * costmap_;
  double step_width_max_;
  double step_height_max_;
  double balance_constraint_;
};

}  // namespace nav2_bipedal_controller

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(
  nav2_bipedal_controller::BipedalController,
  nav2_core::Controller)
```

### Package Configuration

```xml
<!-- nav2_bipedal_controller/package.xml -->
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>nav2_bipedal_controller</name>
  <version>0.0.0</version>
  <description>Custom Nav2 controller for bipedal humanoid robots</description>
  <maintainer email="aamir@example.com">Aamir Ahmed Shamsi</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <depend>nav2_core</depend>
  <depend>nav2_util</depend>
  <depend>nav2_costmap_2d</depend>
  <depend>nav_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>tf2_ros</depend>
  <depend>pluginlib</depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

```cmake
# nav2_bipedal_controller/CMakeLists.txt
cmake_minimum_required(VERSION 3.8)
project(nav2_bipedal_controller)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(nav2_core REQUIRED)
find_package(nav2_util REQUIRED)
find_package(nav2_costmap_2d REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(pluginlib REQUIRED)

set(dependencies
  nav2_core
  nav2_util
  nav2_costmap_2d
  nav_msgs
  geometry_msgs
  tf2_ros
  pluginlib
)

add_library(bipedal_controller SHARED
  src/bipedal_controller.cpp
)

target_include_directories(bipedal_controller PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)

ament_target_dependencies(bipedal_controller ${dependencies})

pluginlib_export_plugin_description_file(nav2_core plugins.xml)

install(TARGETS bipedal_controller
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
```

```xml
<!-- nav2_bipedal_controller/plugins.xml -->
<class_libraries>
  <library path="bipedal_controller">
    <class type="nav2_bipedal_controller::BipedalController" base_class_type="nav2_core::Controller">
      <description>Custom controller for bipedal humanoid robots</description>
    </class>
  </library>
</class_libraries>
```

## Integrating Nav2 with Isaac Sim

### Launch File Configuration

```xml
<!-- isaac_nav2_bringup/launch/bipedal_nav2.launch.xml -->
<launch>
  <!-- Arguments -->
  <arg name="namespace" default=""/>
  <arg name="use_sim_time" default="true"/>
  <arg name="autostart" default="true"/>
  <arg name="params_file" default="$(find-pkg-share isaac_nav2_bringup)/params/bipedal_nav2_params.yaml"/>
  <arg name="map" default="$(find-pkg-share isaac_nav2_bringup)/maps/example_map.yaml"/>

  <!-- Map Server -->
  <node pkg="nav2_map_server" exec="map_server" name="map_server" output="screen">
    <param name="yaml_filename" value="$(var map)"/>
    <param name="topic" value="map"/>
    <param name="frame_id" value="map"/>
    <param name="use_sim_time" value="$(var use_sim_time)"/>
  </node>

  <!-- Local & Global Costmap -->
  <node pkg="nav2_costmap_2d" exec="nav2_costmap_2d" name="local_costmap" output="screen">
    <param from="$(var params_file)"/>
    <param name="use_sim_time" value="$(var use_sim_time)"/>
    <param name="local_costmap.global_frame" value="odom"/>
    <param name="local_costmap.robot_base_frame" value="base_link"/>
  </node>

  <node pkg="nav2_costmap_2d" exec="nav2_costmap_2d" name="global_costmap" output="screen">
    <param from="$(var params_file)"/>
    <param name="use_sim_time" value="$(var use_sim_time)"/>
    <param name="global_costmap.global_frame" value="map"/>
    <param name="global_costmap.robot_base_frame" value="base_link"/>
  </node>

  <!-- Navigation Server -->
  <node pkg="nav2_planner" exec="planner_server" name="planner_server" output="screen">
    <param from="$(var params_file)"/>
    <param name="use_sim_time" value="$(var use_sim_time)"/>
  </node>

  <node pkg="nav2_controller" exec="controller_server" name="controller_server" output="screen">
    <param from="$(var params_file)"/>
    <param name="use_sim_time" value="$(var use_sim_time)"/>
  </node>

  <node pkg="nav2_recoveries" exec="recoveries_server" name="recoveries_server" output="screen">
    <param from="$(var params_file)"/>
    <param name="use_sim_time" value="$(var use_sim_time)"/>
  </node>

  <node pkg="nav2_bt_navigator" exec="bt_navigator" name="bt_navigator" output="screen">
    <param from="$(var params_file)"/>
    <param name="use_sim_time" value="$(var use_sim_time)"/>
  </node>

  <!-- Lifecycle Manager -->
  <node pkg="nav2_lifecycle_manager" exec="lifecycle_manager" name="lifecycle_manager" output="screen">
    <param name="use_sim_time" value="$(var use_sim_time)"/>
    <param name="autostart" value="$(var autostart)"/>
    <param name="node_names" value="[map_server, local_costmap, global_costmap, planner_server, controller_server, recoveries_server, bt_navigator]"/>
  </node>
</launch>
```

## Hands-on Exercise: Nav2 Bipedal Navigation

### Exercise Objective
Configure and test Nav2 with custom bipedal plugins in Isaac Sim.

### Steps to Complete

1. Build the custom bipedal controller package
2. Configure Nav2 parameters for bipedal navigation
3. Integrate with Isaac Sim using ROS bridge
4. Test navigation in a simulated environment
5. Validate path planning and execution with bipedal constraints

### Validation Commands

```bash
# Build the custom controller
cd ~/nav2_bipedal_ws
colcon build --packages-select nav2_bipedal_controller
source install/setup.bash

# Launch Isaac Sim with ROS bridge
# Then in another terminal:
source /opt/ros/humble/setup.bash
source ~/nav2_bipedal_ws/install/setup.bash
ros2 launch isaac_nav2_bringup bipedal_nav2.launch.xml

# Send a navigation goal
ros2 run nav2_test_launch send_goal.py 1.0 1.0 0.0
```

## Performance Considerations

### Computational Requirements
- Path planning algorithms can be computationally intensive
- Real-time bipedal control requires high-frequency updates
- Consider computational budget for humanoid robots

### Stability and Safety
- Ensure balance constraints are properly enforced
- Implement safety fallback behaviors
- Test extensively in simulation before real-world deployment

## Troubleshooting Nav2 Issues

### Common Issues
- **TF issues**: Verify all coordinate frames are properly published
- **Costmap issues**: Check sensor data is being received and processed
- **Controller issues**: Validate custom controller is loaded and configured correctly
- **Planning issues**: Ensure global planner is finding valid paths

## Summary

In this lesson, you learned:
- Nav2 architecture and components
- How to configure Nav2 for humanoid robotics
- Implementation of custom bipedal navigation plugins
- Integration of Nav2 with Isaac Sim

This navigation system will be essential for autonomous humanoid robot operation.

## References

- [Nav2 Documentation](https://navigation.ros.org/)
- [Isaac ROS Navigation Integration](https://docs.nvidia.com/isaac/packages/ros_navigation/index.html)

## Author Information

<div className="author-info">
  <h3>Author: Aamir Ahmed Shamsi</h3>
  <p><strong>GIAIC ID:</strong> 00486031</p>
  <p>This lesson was created with assistance from Claude AI.</p>
</div>