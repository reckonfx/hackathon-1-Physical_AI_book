---
id: unity-robotics-hub-integration
title: Unity Robotics Hub Integration
sidebar_position: 4
description: Integrating Unity with robotics using the Unity Robotics Hub for advanced simulation
---

# Unity Robotics Hub Integration

<div className="gazebo-module">
  <p>This lesson covers integrating Unity with robotics using the Unity Robotics Hub for advanced simulation and visualization.</p>
</div>

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand the Unity Robotics Hub ecosystem
- Set up Unity for robotics simulation
- Integrate Unity with ROS2 using ROS TCP Connector
- Create robot models and environments in Unity
- Validate Unity-ROS2 integration

## Prerequisites

- Basic understanding of Unity development
- Completed ROS2 fundamentals module
- Understanding of robot modeling concepts
- Familiarity with simulation concepts

## Introduction to Unity Robotics Hub

The Unity Robotics Hub provides a comprehensive set of tools and packages for robotics simulation and development:

- **Unity Robot Framework**: Pre-built robot models and components
- **ROS TCP Connector**: Bridge between Unity and ROS2
- **Synthetic Data Tools**: For generating training data
- **Robotics Examples**: Sample projects and use cases
- **Tutorials and Documentation**: Learning resources

### Unity vs Traditional Physics Simulators

| Feature | Unity | Gazebo |
|---------|-------|--------|
| Graphics | High-fidelity, real-time rendering | Basic visualization |
| Physics | PhysX engine | ODE, Bullet, DART |
| Robotics Focus | General game engine adapted | Purpose-built for robotics |
| Performance | Optimized for real-time | Optimized for accuracy |
| Extensibility | Extensive game development tools | Robotics-specific tools |

## Setting Up Unity for Robotics

### Prerequisites Installation

1. **Install Unity Hub and Unity Editor** (2021.3 LTS or later recommended)
2. **Install Unity Robotics packages** via Package Manager
3. **Set up ROS2 environment** for TCP communication

### Unity Robotics Packages

Required packages for robotics integration:

- **ROS TCP Connector**: Communication bridge
- **Robot Framework**: Pre-built components
- **Synthetic Data**: Data generation tools
- **URDF Importer**: Import URDF models

### ROS TCP Connector Setup

The ROS TCP Connector allows Unity to communicate with ROS2:

#### Unity Side Setup

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using Unity.Robotics.ROSTCPConnector.MessageGeneration;
using RosMessageTypes.Sensor;
using RosMessageTypes.Geometry;

public class UnityRobotController : MonoBehaviour
{
    ROSConnection ros;
    string rosIP = "127.0.0.1"; // Default IP
    int rosPort = 10000;        // Default port

    // Robot components
    public GameObject robotBase;
    public GameObject[] wheels;
    public Camera robotCamera;

    // Publishers and subscribers
    string cmdVelTopic = "/cmd_vel";
    string imageTopic = "/camera/image_raw";
    string jointStatesTopic = "/joint_states";

    void Start()
    {
        // Initialize ROS connection
        ros = ROSConnection.instance;
        ros.Initialize(rosIP, rosPort);

        // Start listening for ROS messages
        ros.Subscribe<TwistMsg>(cmdVelTopic, CmdVelCallback);

        // Start coroutine to publish data
        StartCoroutine(PublishRobotData());
    }

    void CmdVelCallback(TwistMsg cmd_vel)
    {
        // Process velocity commands
        float linearVelocity = (float)cmd_vel.linear.x;
        float angularVelocity = (float)cmd_vel.angular.z;

        // Apply movement to robot
        MoveRobot(linearVelocity, angularVelocity);
    }

    void MoveRobot(float linearVelocity, float angularVelocity)
    {
        // Apply movement to robot base
        robotBase.transform.Translate(Vector3.forward * linearVelocity * Time.deltaTime);
        robotBase.transform.Rotate(Vector3.up, angularVelocity * Time.deltaTime);

        // Update wheel rotations for visualization
        UpdateWheels(linearVelocity, angularVelocity);
    }

    void UpdateWheels(float linearVelocity, float angularVelocity)
    {
        // Simple wheel rotation based on robot movement
        foreach (GameObject wheel in wheels)
        {
            wheel.transform.Rotate(Vector3.right, linearVelocity * 60f * Time.deltaTime);
        }
    }

    IEnumerator PublishRobotData()
    {
        // Publish data at 30Hz
        WaitForSeconds wait = new WaitForSeconds(1f / 30f);

        while (true)
        {
            // Publish camera image
            if (robotCamera != null)
            {
                Texture2D image = CaptureCameraImage(robotCamera);
                if (image != null)
                {
                    // Convert to ROS image message and publish
                    // Implementation depends on your specific needs
                }
            }

            yield return wait;
        }
    }

    Texture2D CaptureCameraImage(Camera cam)
    {
        // Capture camera image for publishing
        RenderTexture currentRT = RenderTexture.active;
        RenderTexture.active = cam.targetTexture;
        cam.Render();

        Texture2D image = new Texture2D(cam.targetTexture.width, cam.targetTexture.height);
        image.ReadPixels(new Rect(0, 0, cam.targetTexture.width, cam.targetTexture.height), 0, 0);
        image.Apply();

        RenderTexture.active = currentRT;
        return image;
    }
}
```

#### ROS2 Side Setup

```python
#!/usr/bin/env python3
# unity_robot_bridge.py
# Bridge between ROS2 and Unity

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import Image, JointState
from std_msgs.msg import Header
import socket
import json
import threading
import time
import numpy as np
from cv_bridge import CvBridge

class UnityROSBridge(Node):
    def __init__(self):
        super().__init__('unity_ros_bridge')

        # ROS2 publishers and subscribers
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.image_pub = self.create_publisher(
            Image, '/unity_camera/image_raw', 10)
        self.joint_state_pub = self.create_publisher(
            JointState, '/joint_states', 10)

        # Unity connection
        self.unity_socket = None
        self.unity_ip = '127.0.0.1'
        self.unity_port = 10000

        # Setup Unity connection
        self.connect_to_unity()

        # Timer for periodic updates
        self.timer = self.create_timer(0.1, self.update_unity)

        # Bridge
        self.bridge = CvBridge()

        self.get_logger().info('Unity-ROS bridge initialized')

    def connect_to_unity(self):
        """Connect to Unity via TCP"""
        try:
            self.unity_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.unity_socket.connect((self.unity_ip, self.unity_port))
            self.get_logger().info(f'Connected to Unity at {self.unity_ip}:{self.unity_port}')
        except Exception as e:
            self.get_logger().error(f'Failed to connect to Unity: {e}')

    def cmd_vel_callback(self, msg):
        """Send velocity commands to Unity"""
        if self.unity_socket:
            cmd_data = {
                'type': 'cmd_vel',
                'linear_x': msg.linear.x,
                'linear_y': msg.linear.y,
                'linear_z': msg.linear.z,
                'angular_x': msg.angular.x,
                'angular_y': msg.angular.y,
                'angular_z': msg.angular.z
            }

            try:
                self.unity_socket.send(json.dumps(cmd_data).encode() + b'\n')
            except Exception as e:
                self.get_logger().error(f'Failed to send command to Unity: {e}')

    def update_unity(self):
        """Periodically update Unity with ROS data"""
        if not self.unity_socket:
            return

        # Request sensor data from Unity
        sensor_request = {'type': 'request_sensors'}

        try:
            self.unity_socket.send(json.dumps(sensor_request).encode() + b'\n')
        except Exception as e:
            self.get_logger().error(f'Failed to request sensors from Unity: {e}')

    def send_joint_states(self, joint_positions, joint_names):
        """Publish joint states to ROS"""
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.name = joint_names
        msg.position = joint_positions

        self.joint_state_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    bridge = UnityROSBridge()

    try:
        rclpy.spin(bridge)
    except KeyboardInterrupt:
        pass
    finally:
        if bridge.unity_socket:
            bridge.unity_socket.close()
        bridge.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Creating Robot Models in Unity

### Importing URDF Models

Unity provides a URDF Importer for importing ROS robot models:

1. **Install URDF Importer** from Unity Package Manager
2. **Import URDF file** into Unity project
3. **Configure joints** and physics properties
4. **Add ROS components** for communication

### Unity Robot Component Script

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using RosMessageTypes.Geometry;

public class UnityRobot : MonoBehaviour
{
    [Header("Robot Configuration")]
    public float maxLinearVelocity = 1.0f;
    public float maxAngularVelocity = 1.0f;

    [Header("Sensor Configuration")]
    public Camera mainCamera;
    public GameObject lidarSensor;
    public GameObject imuSensor;

    // Internal components
    ROSConnection ros;
    string robotNamespace = "unity_robot";

    void Start()
    {
        ros = ROSConnection.instance;

        // Subscribe to command topics
        ros.Subscribe<TwistMsg>($"{robotNamespace}/cmd_vel", OnCmdVelReceived);

        // Start sensor publishing coroutines
        StartCoroutine(PublishCameraImage());
        StartCoroutine(PublishLidarData());
        StartCoroutine(PublishImuData());
    }

    void OnCmdVelReceived(TwistMsg cmd_vel)
    {
        // Clamp velocities to safe limits
        float linear = Mathf.Clamp((float)cmd_vel.linear.x, -maxLinearVelocity, maxLinearVelocity);
        float angular = Mathf.Clamp((float)cmd_vel.angular.z, -maxAngularVelocity, maxAngularVelocity);

        // Apply movement
        ApplyDifferentialDrive(linear, angular);
    }

    void ApplyDifferentialDrive(float linear, float angular)
    {
        // Simple differential drive model
        float leftWheelVel = linear - angular * 0.5f;  // 0.5m wheelbase
        float rightWheelVel = linear + angular * 0.5f;

        // Apply to robot's rigidbody or transform
        transform.Translate(Vector3.forward * linear * Time.deltaTime);
        transform.Rotate(Vector3.up, angular * Time.deltaTime);
    }

    System.Collections.IEnumerator PublishCameraImage()
    {
        // Publish camera images at 30 FPS
        WaitForSeconds wait = new WaitForSeconds(1f / 30f);

        while (true)
        {
            if (mainCamera != null)
            {
                // Capture and publish camera image
                CaptureAndPublishCameraImage();
            }

            yield return wait;
        }
    }

    void CaptureAndPublishCameraImage()
    {
        // Implementation for capturing and publishing camera data
        // This would convert Unity camera output to ROS Image message
    }

    System.Collections.IEnumerator PublishLidarData()
    {
        // Publish LiDAR data at 10 Hz
        WaitForSeconds wait = new WaitForSeconds(1f / 10f);

        while (true)
        {
            PublishLidarScan();
            yield return wait;
        }
    }

    void PublishLidarScan()
    {
        // Implementation for simulating and publishing LiDAR data
        // This would use Unity's raycasting to simulate LiDAR
    }

    System.Collections.IEnumerator PublishImuData()
    {
        // Publish IMU data at 100 Hz
        WaitForSeconds wait = new WaitForSeconds(1f / 100f);

        while (true)
        {
            PublishImuReading();
            yield return wait;
        }
    }

    void PublishImuReading()
    {
        // Implementation for publishing IMU data based on Unity physics
    }
}
```

## Advanced Unity Robotics Features

### Synthetic Data Generation

Unity's Synthetic Data package enables generation of training data:

```csharp
using UnityEngine;
using Unity.SyntheticData;
using Unity.Barracuda;

public class SyntheticDataGenerator : MonoBehaviour
{
    [Header("Synthetic Data Configuration")]
    public Camera dataCamera;
    public GameObject[] objectsToRandomize;
    public Material[] materialsToRandomize;

    [Header("Output Configuration")]
    public string outputDirectory = "synthetic_data";
    public int datasetSize = 1000;

    void Start()
    {
        StartCoroutine(GenerateDataset());
    }

    System.Collections.IEnumerator GenerateDataset()
    {
        for (int i = 0; i < datasetSize; i++)
        {
            // Randomize environment
            RandomizeEnvironment();

            // Capture data
            CaptureSyntheticData(i);

            // Wait for next capture
            yield return new WaitForSeconds(0.1f);
        }

        Debug.Log($"Dataset generation completed: {datasetSize} samples");
    }

    void RandomizeEnvironment()
    {
        // Randomize object positions, rotations, materials
        foreach (GameObject obj in objectsToRandomize)
        {
            obj.transform.position = new Vector3(
                Random.Range(-5f, 5f),
                Random.Range(0f, 2f),
                Random.Range(-5f, 5f)
            );

            obj.transform.rotation = Random.rotation;
        }

        // Randomize materials
        foreach (Material mat in materialsToRandomize)
        {
            mat.color = Random.ColorHSV();
        }
    }

    void CaptureSyntheticData(int sampleIndex)
    {
        // Capture RGB, depth, segmentation data
        // Save to output directory with proper naming
    }
}
```

### Perception Simulation

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

public class PerceptionSimulator : MonoBehaviour
{
    [Header("Perception Sensors")]
    public Camera rgbCamera;
    public Camera depthCamera;
    public Camera segmentationCamera;

    [Header("Simulation Parameters")]
    public float perceptionRange = 10f;
    public int detectionProbability = 95; // Percentage

    void Start()
    {
        // Initialize perception system
    }

    public PerceptionData SimulatePerception(Vector3 robotPosition)
    {
        PerceptionData data = new PerceptionData();

        // Perform object detection simulation
        Collider[] hits = Physics.OverlapSphere(robotPosition, perceptionRange);

        foreach (Collider hit in hits)
        {
            if (Random.Range(0, 100) < detectionProbability)
            {
                // Add detected object to perception data
                DetectedObject obj = new DetectedObject();
                obj.name = hit.name;
                obj.position = hit.transform.position;
                obj.type = GetObjectType(hit.tag);

                data.detectedObjects.Add(obj);
            }
        }

        return data;
    }

    ObjectType GetObjectType(string tag)
    {
        // Map Unity tags to object types
        switch (tag)
        {
            case "Obstacle": return ObjectType.Obstacle;
            case "Target": return ObjectType.Target;
            case "Landmark": return ObjectType.Landmark;
            default: return ObjectType.Unknown;
        }
    }
}

[System.Serializable]
public class PerceptionData
{
    public System.Collections.Generic.List<DetectedObject> detectedObjects =
        new System.Collections.Generic.List<DetectedObject>();
    public float timestamp;
}

[System.Serializable]
public class DetectedObject
{
    public string name;
    public Vector3 position;
    public ObjectType type;
}

public enum ObjectType
{
    Unknown,
    Obstacle,
    Target,
    Landmark,
    Human
}
```

## Hands-on Exercise: Unity-ROS Integration

### Exercise Objective
Create a Unity scene with a robot that receives commands from ROS2 and publishes sensor data.

### Steps to Complete

1. Set up Unity project with Robotics packages
2. Create a simple robot model in Unity
3. Implement ROS TCP Connector communication
4. Test command reception and sensor publishing
5. Validate integration with ROS2 tools

### Testing Commands

```bash
# Terminal 1: Start the Unity-ROS bridge
source /opt/ros/humble/setup.bash
python3 unity_robot_bridge.py

# Terminal 2: Send velocity commands to Unity
source /opt/ros/humble/setup.bash
ros2 topic pub /cmd_vel geometry_msgs/Twist "{linear: {x: 1.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}"

# Terminal 3: Monitor sensor data
source /opt/ros/humble/setup.bash
ros2 topic echo /unity_camera/image_raw

# Terminal 4: Check available topics
source /opt/ros/humble/setup.bash
ros2 topic list
```

## Best Practices for Unity Robotics

### 1. Performance Optimization
- Use appropriate Level of Detail (LOD) systems
- Optimize rendering for real-time performance
- Limit physics calculations to essential elements
- Use occlusion culling for large environments

### 2. Communication Reliability
- Implement proper error handling for TCP connections
- Use appropriate message rates for real-time control
- Implement reconnection logic for robust operation
- Validate data integrity in communication

### 3. Simulation Accuracy
- Calibrate Unity physics to match real-world behavior
- Use realistic sensor noise models
- Validate simulation results against real hardware
- Implement proper time synchronization

### 4. Development Workflow
- Use version control for Unity scenes and assets
- Document robot configurations and parameters
- Create reusable robot components
- Test incrementally with simple scenarios

## Troubleshooting Unity-ROS Integration

### Common Issues
- **Connection failures**: Check IP addresses and ports
- **Performance issues**: Optimize Unity scene complexity
- **Synchronization problems**: Ensure consistent time bases
- **Data format mismatches**: Verify message type compatibility

### Debugging Tips
- Use Unity's console for Unity-side debugging
- Check ROS2 logs for communication issues
- Monitor network traffic for connection problems
- Use simple test messages to verify communication

## Summary

In this lesson, you learned:
- How to set up Unity for robotics simulation with the Robotics Hub
- How to integrate Unity with ROS2 using TCP communication
- How to create and configure robot models in Unity
- How to implement perception and sensor simulation
- Best practices for Unity-ROS integration

Unity Robotics Hub provides powerful capabilities for high-fidelity simulation and visualization, complementing traditional physics simulators like Gazebo.

## References

- [Unity Robotics Hub Documentation](https://github.com/Unity-Technologies/Unity-Robotics-Hub)
- [ROS TCP Connector Guide](https://github.com/Unity-Technologies/ROS-TCP-Connector)
- [Unity Robot Framework](https://github.com/Unity-Technologies/Unity-Robotics-Framework)

## Author Information

<div className="author-info">
  <h3>Author: Aamir Ahmed Shamsi</h3>
  <p><strong>GIAIC ID:</strong> 00486031</p>
  <p>This lesson was created with assistance from Claude AI.</p>
</div>