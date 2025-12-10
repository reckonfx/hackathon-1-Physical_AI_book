---
id: ros2-parameters-and-composition
title: ROS2 Parameters and Composition
sidebar_position: 6
description: Managing ROS2 parameters and node composition for flexible robotic applications
---

# ROS2 Parameters and Composition

<div className="ros2-module">
  <p>This lesson covers ROS2 parameters and node composition for creating flexible and configurable robotic applications.</p>
</div>

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand and use ROS2 parameters for node configuration
- Implement parameter declarations and callbacks
- Create parameter files in YAML format
- Understand node composition and its benefits
- Validate parameter and composition functionality

## Prerequisites

- Understanding of ROS2 nodes and packages
- Completed previous ROS2 lessons

## Introduction to ROS2 Parameters

ROS2 parameters provide a way to configure nodes at runtime without recompilation. Parameters are:

- **Type-safe**: Each parameter has a specific type (int, double, string, bool, list)
- **Dynamic**: Can be changed at runtime (if the node allows it)
- **Hierarchical**: Can be organized in namespaces
- **Persistent**: Can be saved and loaded from files

### Parameter Types

ROS2 supports the following parameter types:
- `rclpy.Parameter.Type.INTEGER`
- `rclpy.Parameter.Type.DOUBLE`
- `rclpy.Parameter.Type.STRING`
- `rclpy.Parameter.Type.BOOL`
- `rclpy.Parameter.Type.INTEGER_ARRAY`
- `rclpy.Parameter.Type.DOUBLE_ARRAY`
- `rclpy.Parameter.Type.STRING_ARRAY`
- `rclpy.Parameter.Type.BOOL_ARRAY`

## Declaring and Using Parameters

### Python Parameter Example

```python
#!/usr/bin/env python3
# parameter_node.py
# Example of ROS2 parameter usage

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_msgs.msg import String

class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')

        # Declare parameters with default values
        self.declare_parameter('robot_name', 'default_robot')
        self.declare_parameter('max_velocity', 1.0)
        self.declare_parameter('use_sim_time', False)
        self.declare_parameter('sensors', ['camera', 'lidar', 'imu'])

        # Get parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.max_velocity = self.get_parameter('max_velocity').value
        self.use_sim_time = self.get_parameter('use_sim_time').value
        self.sensors = self.get_parameter('sensors').value

        # Create publisher
        self.publisher_ = self.create_publisher(String, 'robot_info', 10)

        # Set up parameter callback
        self.add_on_set_parameters_callback(self.parameter_callback)

        # Timer for publishing info
        self.timer = self.create_timer(1.0, self.publish_info)

        self.get_logger().info(
            f'Initialized with parameters: '
            f'robot_name={self.robot_name}, '
            f'max_velocity={self.max_velocity}, '
            f'use_sim_time={self.use_sim_time}, '
            f'sensors={self.sensors}'
        )

    def parameter_callback(self, params):
        """Callback for parameter changes"""
        for param in params:
            if param.name == 'max_velocity' and param.type_ == Parameter.Type.DOUBLE:
                if param.value > 5.0:
                    return rclpy.node.SetParametersResult(successful=False, reason='Max velocity too high')
                else:
                    self.max_velocity = param.value
                    self.get_logger().info(f'Updated max_velocity to {self.max_velocity}')
            elif param.name == 'robot_name' and param.type_ == Parameter.Type.STRING:
                self.robot_name = param.value
                self.get_logger().info(f'Updated robot_name to {self.robot_name}')

        return rclpy.node.SetParametersResult(successful=True)

    def publish_info(self):
        """Publish robot information"""
        msg = String()
        msg.data = f'Robot: {self.robot_name}, Max Vel: {self.max_velocity}, Sensors: {self.sensors}'
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    parameter_node = ParameterNode()

    try:
        rclpy.spin(parameter_node)
    except KeyboardInterrupt:
        pass
    finally:
        parameter_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### C++ Parameter Example

```cpp
// parameter_node.cpp
// Example of ROS2 parameter usage in C++

#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>

class ParameterNode : public rclcpp::Node
{
public:
  ParameterNode() : Node("parameter_node")
  {
    // Declare parameters with default values
    this->declare_parameter<std::string>("robot_name", "default_robot");
    this->declare_parameter<double>("max_velocity", 1.0);
    this->declare_parameter<bool>("use_sim_time", false);
    this->declare_parameter<std::vector<std::string>>("sensors", {"camera", "lidar", "imu"});

    // Get parameter values
    this->robot_name_ = this->get_parameter("robot_name").as_string();
    this->max_velocity_ = this->get_parameter("max_velocity").as_double();
    this->use_sim_time_ = this->get_parameter("use_sim_time").as_bool();
    this->sensors_ = this->get_parameter("sensors").as_string_array();

    // Set up parameter callback
    this->set_on_parameters_set_callback(
      [this](const std::vector<rclcpp::Parameter> & parameters)
      {
        auto result = rcl_interfaces::msg::SetParametersResult();
        for (const auto & parameter : parameters) {
          if (parameter.get_name() == "max_velocity" && parameter.get_type() == rclcpp::ParameterType::PARAMETER_DOUBLE) {
            if (parameter.as_double() > 5.0) {
              result.successful = false;
              result.reason = "Max velocity too high";
              return result;
            } else {
              this->max_velocity_ = parameter.as_double();
              RCLCPP_INFO(this->get_logger(), "Updated max_velocity to %f", this->max_velocity_);
            }
          } else if (parameter.get_name() == "robot_name" && parameter.get_type() == rclcpp::ParameterType::PARAMETER_STRING) {
            this->robot_name_ = parameter.as_string();
            RCLCPP_INFO(this->get_logger(), "Updated robot_name to %s", this->robot_name_.c_str());
          }
        }
        result.successful = true;
        return result;
      });

    // Create publisher
    publisher_ = this->create_publisher<std_msgs::msg::String>("robot_info", 10);

    // Timer for publishing info
    timer_ = this->create_wall_timer(
      std::chrono::seconds(1),
      std::bind(&ParameterNode::publish_info, this));

    RCLCPP_INFO(this->get_logger(),
      "Initialized with parameters: robot_name=%s, max_velocity=%f, use_sim_time=%s, sensors size=%zu",
      this->robot_name_.c_str(), this->max_velocity_, this->use_sim_time_ ? "true" : "false", this->sensors_.size());
  }

private:
  void publish_info()
  {
    auto msg = std_msgs::msg::String();
    std::string sensor_str;
    for (const auto & sensor : sensors_) {
      sensor_str += sensor + ",";
    }
    if (!sensor_str.empty()) sensor_str.pop_back(); // Remove last comma

    msg.data = "Robot: " + robot_name_ + ", Max Vel: " + std::to_string(max_velocity_) + ", Sensors: " + sensor_str;
    publisher_->publish(msg);
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;

  std::string robot_name_;
  double max_velocity_;
  bool use_sim_time_;
  std::vector<std::string> sensors_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ParameterNode>());
  rclcpp::shutdown();
  return 0;
}
```

## Parameter Files (YAML)

Parameters can be organized in YAML files for easy management:

### config/robot_params.yaml

```yaml
/**:  # Applies to all nodes
  ros__parameters:
    use_sim_time: false
    log_level: "info"

robot_controller:
  ros__parameters:
    max_velocity: 1.0
    acceleration_limit: 0.5
    control_frequency: 50.0
    safety_margin: 0.5

sensor_processor:
  ros__parameters:
    camera_enabled: true
    lidar_enabled: true
    processing_rate: 30.0
    detection_threshold: 0.7

navigation_system:
  ros__parameters:
    planner_frequency: 5.0
    controller_frequency: 20.0
    recovery_enabled: true
    global_frame: "map"
    robot_base_frame: "base_link"
    footprint: [[-0.5, -0.3], [-0.5, 0.3], [0.5, 0.3], [0.5, -0.3]]
```

### Loading Parameters in Launch Files

```python
#!/usr/bin/env python3
# parameter_launch.py
# Launch file with parameter loading

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

    params_file_arg = DeclareLaunchArgument(
        'params_file',
        default_value=PathJoinSubstitution([
            FindPackageShare('my_robot_package'),
            'config',
            'robot_params.yaml'
        ]),
        description='Path to parameters file'
    )

    # Get configurations
    use_sim_time = LaunchConfiguration('use_sim_time')
    params_file = LaunchConfiguration('params_file')

    # Robot controller node
    robot_controller = Node(
        package='my_robot_package',
        executable='robot_controller',
        name='robot_controller',
        parameters=[
            params_file,
            {'use_sim_time': use_sim_time}
        ]
    )

    # Sensor processor node
    sensor_processor = Node(
        package='my_robot_package',
        executable='sensor_processor',
        name='sensor_processor',
        parameters=[
            params_file,
            {'use_sim_time': use_sim_time}
        ]
    )

    return LaunchDescription([
        use_sim_time_arg,
        params_file_arg,
        robot_controller,
        sensor_processor
    ])
```

## Node Composition

Node composition allows multiple nodes to run within a single process, providing benefits:

- **Performance**: Reduced inter-process communication overhead
- **Resource efficiency**: Shared memory and reduced context switching
- **Synchronization**: Better timing coordination between nodes
- **Deployment**: Simplified deployment with fewer processes

### Creating a Composed Node

```python

#!/usr/bin/env python3
# composed_node.py
# Example of node composition

import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import String, Int32
import threading
import time

class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')
        self.publisher_ = self.create_publisher(Int32, 'sensor_data', 10)
        self.timer = self.create_timer(0.1, self.publish_sensor_data)
        self.counter = 0

    def publish_sensor_data(self):
        msg = Int32()
        msg.data = self.counter
        self.publisher_.publish(msg)
        self.counter += 1
        self.get_logger().info(f'Published sensor data: {msg.data}')

class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')
        self.subscription = self.create_subscription(
            Int32,
            'sensor_data',
            self.sensor_callback,
            10)
        self.publisher_ = self.create_publisher(String, 'control_command', 10)

    def sensor_callback(self, msg):
        # Process sensor data and generate control command
        command = String()
        if msg.data > 10:
            command.data = f'Stop robot, sensor value: {msg.data}'
        else:
            command.data = f'Move forward, sensor value: {msg.data}'

        self.publisher_.publish(command)
        self.get_logger().info(f'Published command: {command.data}')

class ComposedNode(Node):
    """A node that composes multiple nodes within a single process"""

    def __init__(self):
        super().__init__('composed_node')

        # Create the individual nodes
        self.sensor_node = SensorNode()
        self.controller_node = ControllerNode()

        # Create a single-threaded executor to run both nodes
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(self.sensor_node)
        self.executor.add_node(self.controller_node)

        # Start the executor in a separate thread
        self.executor_thread = threading.Thread(target=self.executor.spin)
        self.executor_thread.start()

        self.get_logger().info('Composed node initialized with sensor and controller')

def main(args=None):
    rclpy.init(args=args)

    composed_node = ComposedNode()

    try:
        # Keep the main thread alive
        while rclpy.ok():
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        composed_node.executor.shutdown()
        composed_node.executor_thread.join()
        composed_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Composition with rclcpp_components

For C++, ROS2 provides the `rclcpp_components` framework for composition:

### C++ Component Example

```cpp
// components/sensor_component.hpp
#ifndef SENSOR_COMPONENT_HPP_
#define SENSOR_COMPONENT_HPP_

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"

namespace my_robot_components
{
class SensorComponent : public rclcpp::Node
{
public:
  SensorComponent(const rclcpp::NodeOptions & options);

private:
  void publish_sensor_data();

  rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  int counter_;
};
}  // namespace my_robot_components

#endif  // SENSOR_COMPONENT_HPP_
```

```cpp
// components/sensor_component.cpp
#include "sensor_component.hpp"

namespace my_robot_components
{
SensorComponent::SensorComponent(const rclcpp::NodeOptions & options)
: Node("sensor_component", options), counter_(0)
{
  publisher_ = this->create_publisher<std_msgs::msg::Int32>("sensor_data", 10);
  timer_ = this->create_wall_timer(
    std::chrono::milliseconds(100),
    std::bind(&SensorComponent::publish_sensor_data, this));
}

void SensorComponent::publish_sensor_data()
{
  auto msg = std_msgs::msg::Int32();
  msg.data = counter_++;
  publisher_->publish(msg);
  RCLCPP_INFO(this->get_logger(), "Published sensor data: %d", msg.data);
}
}  // namespace my_robot_components

#include "rclcpp_components/register_node_macro.hpp"
RCLCPP_COMPONENTS_REGISTER_NODE(my_robot_components::SensorComponent)
```

## Hands-on Exercise: Parameters and Composition

### Exercise Objective
Create a parameterized node and implement node composition.

### Steps to Complete

1. Create a parameterized node with validation
2. Create a second node that responds to parameters
3. Implement node composition
4. Test parameter changes at runtime
5. Validate the composed system

### Parameter Testing Commands

```bash
# Run the parameter node
ros2 run my_robot_package parameter_node

# List parameters
ros2 param list

# Get a specific parameter
ros2 param get /parameter_node robot_name

# Set a parameter at runtime
ros2 param set /parameter_node max_velocity 2.5

# Load parameters from file
ros2 run my_robot_package parameter_node --ros-args --params-file config/robot_params.yaml
```

## Best Practices for Parameters and Composition

### Parameter Best Practices
- Use descriptive parameter names with namespaces
- Provide sensible default values
- Validate parameter values in callbacks
- Document all parameters clearly
- Group related parameters logically

### Composition Best Practices
- Use composition for nodes that need tight coupling
- Consider performance benefits vs. complexity
- Ensure proper lifecycle management
- Test both composed and standalone modes
- Document the composition architecture

## Troubleshooting Parameters and Composition

### Common Issues
- **Parameter not found**: Check parameter names and namespaces
- **Type mismatch**: Ensure parameter types match expectations
- **Composition errors**: Verify component registration
- **Lifecycle issues**: Ensure proper node cleanup in composition

### Debugging Tips
- Use `ros2 param describe` to see parameter details
- Check parameter names with `ros2 param list`
- Use `--log-level debug` for detailed composition logs

## Summary

In this lesson, you learned:
- How to declare and use ROS2 parameters for configuration
- How to organize parameters in YAML files
- How to implement node composition for performance
- Best practices for parameter and composition design

## References

- [ROS2 Parameters Documentation](https://docs.ros.org/en/humble/How-To-Guides/Using-Parameters-In-A-Class-Python.html)
- [Node Composition Guide](https://docs.ros.org/en/humble/Tutorials/Intermediate/Composition.html)

## Author Information

<div className="author-info">
  <h3>Author: Aamir Ahmed Shamsi</h3>
  <p><strong>GIAIC ID:</strong> 00486031</p>
  <p>This lesson was created with assistance from Claude AI.</p>
</div>