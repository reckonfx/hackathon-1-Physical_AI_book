---
id: ros2-nodes-and-topics
title: ROS2 Nodes and Topics
sidebar_position: 2
description: Understanding ROS2 nodes and topics for robotics communication
---

# ROS2 Nodes and Topics

<div className="ros2-module">
  <p>This lesson covers the fundamental concepts of ROS2 nodes and topics for robotics communication.</p>
</div>

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand the concept of ROS2 nodes
- Implement topics for inter-node communication
- Create publishers and subscribers
- Validate node communication

## Prerequisites

- Basic understanding of robotics concepts
- Completed the introduction to ROS2

## Introduction to ROS2 Nodes

ROS2 nodes are the fundamental building blocks of any ROS2 application. Each node is a separate process that performs a specific task and communicates with other nodes through topics, services, and actions.

### Key Characteristics of Nodes

- **Modularity**: Each node performs a specific function
- **Communication**: Nodes communicate through ROS2 middleware
- **Discovery**: Nodes can discover each other automatically
- **Lifecycle**: Nodes have a well-defined lifecycle

## Topics and Message Passing

Topics are the primary mechanism for asynchronous communication between nodes in ROS2. They use a publish-subscribe pattern where:

- Publishers send messages to topics
- Subscribers receive messages from topics
- Multiple publishers and subscribers can exist for the same topic

### Topic Communication Pattern

```
Publisher Node → Topic → Subscriber Node
     ↓                        ↑
Publisher Node → Topic → Subscriber Node
```

## Creating a Simple Publisher

```python
#!/usr/bin/env python3
# publisher_example.py
# Simple ROS2 publisher example

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Creating a Simple Subscriber

```python
#!/usr/bin/env python3
# subscriber_example.py
# Simple ROS2 subscriber example

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Hands-on Exercise: Node Communication

### Exercise Objective
Create and test a publisher-subscriber pair to understand ROS2 communication.

### Steps to Complete

1. Create a new ROS2 package for the exercise
2. Implement the publisher node
3. Implement the subscriber node
4. Test the communication between nodes
5. Validate the message exchange

### Validation Commands

```bash
# Terminal 1: Run the publisher
ros2 run your_package_name publisher_example

# Terminal 2: Run the subscriber
ros2 run your_package_name subscriber_example
```

## Quality of Service (QoS) Settings

QoS settings control the delivery behavior of messages:

- **Reliability**: Whether messages must be delivered
- **Durability**: Whether late-joining subscribers receive old messages
- **History**: How many messages to store

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

# Create a QoS profile
qos_profile = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE
)
```

## Summary

In this lesson, you learned:
- How ROS2 nodes function as fundamental building blocks
- The publish-subscribe communication pattern
- How to implement publishers and subscribers
- Quality of Service settings for message delivery

## References

- [ROS2 Documentation](https://docs.ros.org/en/humble/)
- [ROS2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)

## Author Information

<div className="author-info">
  <h3>Author: Aamir Ahmed Shamsi</h3>
  <p><strong>GIAIC ID:</strong> 00486031</p>
  <p>This lesson was created with assistance from Claude AI.</p>
</div>