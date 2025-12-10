---
id: ros2-services-and-actions
title: ROS2 Services and Actions
sidebar_position: 3
description: Understanding ROS2 services and actions for synchronous and goal-oriented communication
---

# ROS2 Services and Actions

<div className="ros2-module">
  <p>This lesson covers ROS2 services and actions for synchronous and goal-oriented communication between nodes.</p>
</div>

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand the difference between topics, services, and actions
- Implement ROS2 services for request-response communication
- Create actions for goal-oriented tasks
- Validate service and action communication

## Prerequisites

- Understanding of ROS2 nodes and topics
- Completed the previous lesson on nodes and topics

## Introduction to Services

Services in ROS2 provide synchronous request-response communication between nodes. Unlike topics which are asynchronous, services wait for a response before continuing.

### Service Characteristics

- **Synchronous**: Client waits for response
- **Request-Response**: One request, one response
- **Blocking**: Client blocks until response received
- **Reliable**: Request guaranteed to be received once

## Creating a Service Server

```python
#!/usr/bin/env python3
# service_server.py
# Simple ROS2 service server example

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Returning {request.a} + {request.b} = {response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Creating a Service Client

```python
#!/usr/bin/env python3
# service_client.py
# Simple ROS2 service client example

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalClient(Node):
    def __init__(self):
        super().__init__('minimal_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClient()
    response = minimal_client.send_request(1, 2)
    minimal_client.get_logger().info(f'Result of add_two_ints: {response.sum}')
    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Introduction to Actions

Actions are used for long-running tasks that require feedback and the ability to cancel. They provide:

- **Goal**: Request for a long-running task
- **Feedback**: Periodic updates during execution
- **Result**: Final outcome when task completes

### Action Characteristics

- **Goal-oriented**: Designed for tasks with specific objectives
- **Feedback**: Continuous updates during execution
- **Cancelability**: Ability to cancel long-running tasks
- **Status tracking**: Track execution status

## Creating an Action Server

```python
#!/usr/bin/env python3
# action_server.py
# Simple ROS2 action server example

import time
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_callback,
            callback_group=rclpy.callback_groups.ReentrantCallbackGroup(),
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)

    def destroy(self):
        self._action_server.destroy()
        super().destroy_node()

    def goal_callback(self, goal_request):
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1])

            self.get_logger().info(f'Publishing feedback: {feedback_msg.sequence}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info(f'Returning result: {result.sequence}')

        return result

def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(fibonacci_action_server)
    fibonacci_action_server.destroy()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Creating an Action Client

```python
#!/usr/bin/env python3
# action_client.py
# Simple ROS2 action client example

import time
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci')

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback.sequence}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()
    action_client.send_goal(10)
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
```

## Hands-on Exercise: Services and Actions

### Exercise Objective
Implement and test both service and action communication patterns.

### Steps to Complete

1. Create a service server for a custom calculation
2. Create a service client to use the service
3. Implement an action server for a long-running task
4. Create an action client to interact with the action
5. Test both communication patterns

### Validation Commands

```bash
# Terminal 1: Run the service server
ros2 run your_package_name service_server

# Terminal 2: Run the service client
ros2 run your_package_name service_client

# Terminal 3: Run the action server
ros2 run your_package_name action_server

# Terminal 4: Run the action client
ros2 run your_package_name action_client
```

## When to Use Each Communication Pattern

### Use Topics When:
- Need asynchronous communication
- Multiple publishers/subscribers needed
- Real-time streaming of data
- No need for guaranteed delivery

### Use Services When:
- Need request-response pattern
- Task is relatively quick
- Need guaranteed response
- Synchronous operation required

### Use Actions When:
- Task takes a long time
- Need feedback during execution
- Need ability to cancel
- Goal-oriented behavior required

## Summary

In this lesson, you learned:
- How services provide synchronous request-response communication
- How actions enable goal-oriented tasks with feedback
- When to use each communication pattern
- Implementation of service and action servers/clients

## References

- [ROS2 Services Documentation](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html)
- [ROS2 Actions Documentation](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)

## Author Information

<div className="author-info">
  <h3>Author: Aamir Ahmed Shamsi</h3>
  <p><strong>GIAIC ID:</strong> 00486031</p>
  <p>This lesson was created with assistance from Claude AI.</p>
</div>