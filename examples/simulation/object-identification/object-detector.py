#!/usr/bin/env python3
"""
Object Identification Example for VLA Systems

This script demonstrates object identification capabilities within the VLA framework.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import String
from geometry_msgs.msg import Point
import numpy as np
from typing import Dict, List, Any, Optional
import cv2  # Assuming OpenCV for image processing
import time
from dataclasses import dataclass


@dataclass
class DetectedObject:
    """Class to represent a detected object."""
    id: str
    name: str
    type: str
    color: str
    position: Point
    confidence: float
    bounding_box: Dict[str, int]  # x, y, width, height


class VLAObjectDetector(Node):
    """
    Object detection system for VLA applications.
    """

    def __init__(self):
        super().__init__('vla_object_detector')

        # Publishers and subscribers
        self.image_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.camera_info_sub = self.create_subscription(CameraInfo, '/camera/camera_info', self.camera_info_callback, 10)
        self.detection_pub = self.create_publisher(String, '/object_detections', 10)
        self.status_pub = self.create_publisher(String, '/detection_status', 10)

        # Camera information
        self.camera_info = None
        self.latest_image = None

        # Known objects for simulation
        self.known_objects = {
            'red_cube': {
                'type': 'cube',
                'color': 'red',
                'position': Point(x=1.5, y=0.8, z=0.0),
                'confidence': 0.95
            },
            'blue_sphere': {
                'type': 'sphere',
                'color': 'blue',
                'position': Point(x=-0.5, y=1.2, z=0.0),
                'confidence': 0.92
            },
            'green_pyramid': {
                'type': 'pyramid',
                'color': 'green',
                'position': Point(x=2.0, y=-1.0, z=0.0),
                'confidence': 0.88
            },
            'yellow_cylinder': {
                'type': 'cylinder',
                'color': 'yellow',
                'position': Point(x=0.0, y=-1.5, z=0.0),
                'confidence': 0.90
            }
        }

        self.get_logger().info("VLA Object Detector initialized")

    def camera_info_callback(self, msg: CameraInfo):
        """Callback for camera information."""
        self.camera_info = msg

    def image_callback(self, msg: Image):
        """Callback for image data."""
        # In a real implementation, this would process the image for object detection
        # For this example, we'll store the image and use our known objects
        self.latest_image = msg
        self.get_logger().debug("Received image for processing")

    def detect_objects_in_image(self, image_msg: Optional[Image] = None) -> List[DetectedObject]:
        """
        Detect objects in the provided image or the latest image.

        Args:
            image_msg: Image to process (if None, uses latest image)

        Returns:
            List of detected objects
        """
        # For this example, we'll simulate object detection using our known objects
        # In a real implementation, this would use a computer vision model
        image_to_process = image_msg if image_to_process is not None else self.latest_image

        if image_to_process is None:
            self.get_logger().warning("No image available for object detection")
            return []

        detected_objects = []

        # Simulate detection by adding some of our known objects with some randomness
        for obj_id, obj_info in self.known_objects.items():
            # Simulate detection with some probability based on confidence
            if np.random.random() < obj_info['confidence']:
                # Create a detected object with bounding box information
                detected_obj = DetectedObject(
                    id=obj_id,
                    name=obj_id,
                    type=obj_info['type'],
                    color=obj_info['color'],
                    position=obj_info['position'],
                    confidence=obj_info['confidence'] * np.random.uniform(0.8, 1.0),  # Add some variation
                    bounding_box={
                        'x': int(np.random.uniform(0, 300)),  # Random position in image
                        'y': int(np.random.uniform(0, 200)),
                        'width': int(np.random.uniform(50, 100)),
                        'height': int(np.random.uniform(50, 100))
                    }
                )
                detected_objects.append(detected_obj)

        self.get_logger().info(f"Detected {len(detected_objects)} objects")
        return detected_objects

    def detect_objects_by_color(self, target_color: str) -> List[DetectedObject]:
        """
        Detect objects of a specific color.

        Args:
            target_color: Color to search for

        Returns:
            List of detected objects matching the color
        """
        all_objects = self.detect_objects_in_image()
        matching_objects = [
            obj for obj in all_objects
            if target_color.lower() in obj.color.lower()
        ]
        return matching_objects

    def detect_objects_by_type(self, target_type: str) -> List[DetectedObject]:
        """
        Detect objects of a specific type.

        Args:
            target_type: Type to search for

        Returns:
            List of detected objects matching the type
        """
        all_objects = self.detect_objects_in_image()
        matching_objects = [
            obj for obj in all_objects
            if target_type.lower() in obj.type.lower()
        ]
        return matching_objects

    def find_object_by_name(self, object_name: str) -> Optional[DetectedObject]:
        """
        Find a specific object by name.

        Args:
            object_name: Name of the object to find

        Returns:
            Detected object if found, None otherwise
        """
        all_objects = self.detect_objects_in_image()
        for obj in all_objects:
            if object_name.lower() in obj.name.lower():
                return obj
        return None

    def get_object_position(self, object_name: str) -> Optional[Point]:
        """
        Get the position of a specific object.

        Args:
            object_name: Name of the object

        Returns:
            Position of the object if found, None otherwise
        """
        obj = self.find_object_by_name(object_name)
        if obj:
            return obj.position
        return None

    def identify_objects_in_area(self, center_x: float, center_y: float, radius: float) -> List[DetectedObject]:
        """
        Identify objects within a specific area.

        Args:
            center_x: X coordinate of area center
            center_y: Y coordinate of area center
            radius: Radius of the area to search

        Returns:
            List of detected objects within the area
        """
        all_objects = self.detect_objects_in_image()
        area_objects = []

        for obj in all_objects:
            distance = ((obj.position.x - center_x) ** 2 + (obj.position.y - center_y) ** 2) ** 0.5
            if distance <= radius:
                area_objects.append(obj)

        return area_objects

    def publish_detections(self, objects: List[DetectedObject]):
        """Publish object detections."""
        if not objects:
            detection_msg = String()
            detection_msg.data = "No objects detected"
            self.detection_pub.publish(detection_msg)
            return

        # Create a summary of detections
        detection_data = {
            "timestamp": time.time(),
            "count": len(objects),
            "objects": [
                {
                    "id": obj.id,
                    "name": obj.name,
                    "type": obj.type,
                    "color": obj.color,
                    "confidence": obj.confidence,
                    "position": {
                        "x": obj.position.x,
                        "y": obj.position.y,
                        "z": obj.position.z
                    }
                }
                for obj in objects
            ]
        }

        detection_msg = String()
        detection_msg.data = str(detection_data)
        self.detection_pub.publish(detection_msg)

    def get_object_summary(self) -> Dict[str, Any]:
        """
        Get a summary of detected objects.

        Returns:
            Dictionary with object counts by type and color
        """
        all_objects = self.detect_objects_in_image()

        # Count by type
        type_counts = {}
        color_counts = {}

        for obj in all_objects:
            type_counts[obj.type] = type_counts.get(obj.type, 0) + 1
            color_counts[obj.color] = color_counts.get(obj.color, 0) + 1

        return {
            "total_objects": len(all_objects),
            "by_type": type_counts,
            "by_color": color_counts,
            "objects": [obj.name for obj in all_objects]
        }


def main(args=None):
    """Main function to demonstrate object identification."""
    print("VLA Object Identification Demo")
    print("===============================")
    print("This example demonstrates object identification capabilities for VLA systems.")
    print("It includes detection by color, type, name, and area.")
    print()

    rclpy.init(args=args)
    detector = VLAObjectDetector()

    try:
        # Simulate some operations
        print("Detecting all objects...")
        all_objects = detector.detect_objects_in_image()
        print(f"Found {len(all_objects)} objects")
        for obj in all_objects:
            print(f"  - {obj.name} ({obj.color} {obj.type}) at ({obj.position.x}, {obj.position.y}) with confidence {obj.confidence:.2f}")
        print()

        # Detect red objects
        print("Detecting red objects...")
        red_objects = detector.detect_objects_by_color("red")
        print(f"Found {len(red_objects)} red objects")
        for obj in red_objects:
            print(f"  - {obj.name}")
        print()

        # Detect cubes
        print("Detecting cube objects...")
        cube_objects = detector.detect_objects_by_type("cube")
        print(f"Found {len(cube_objects)} cube objects")
        for obj in cube_objects:
            print(f"  - {obj.name}")
        print()

        # Find a specific object
        print("Looking for 'red_cube'...")
        red_cube = detector.find_object_by_name("red_cube")
        if red_cube:
            print(f"Found {red_cube.name} at ({red_cube.position.x}, {red_cube.position.y})")
        else:
            print("Red cube not found")
        print()

        # Get object summary
        print("Object summary:")
        summary = detector.get_object_summary()
        print(f"  Total objects: {summary['total_objects']}")
        print(f"  By type: {summary['by_type']}")
        print(f"  By color: {summary['by_color']}")
        print()

        # Identify objects in a specific area
        print("Identifying objects near (0, 0) with radius 2.0...")
        area_objects = detector.identify_objects_in_area(0.0, 0.0, 2.0)
        print(f"Found {len(area_objects)} objects in area")
        for obj in area_objects:
            distance = ((obj.position.x - 0.0) ** 2 + (obj.position.y - 0.0) ** 2) ** 0.5
            print(f"  - {obj.name} at distance {distance:.2f}")

    except KeyboardInterrupt:
        print("\nObject identification demo interrupted by user")
    finally:
        detector.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()