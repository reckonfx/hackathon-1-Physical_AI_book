---
id: synthetic-data-generation
title: Synthetic Data Generation
sidebar_position: 6
description: Creating perception training data from Isaac Sim environments
---

# Synthetic Data Generation

<div className="isaac-module">
  <p>This lesson covers synthetic data generation workflows for training humanoid perception systems using Isaac Sim environments.</p>
</div>

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand the importance of synthetic data for perception training
- Generate various types of sensor data from Isaac Sim
- Create labeled datasets for computer vision tasks
- Implement data augmentation techniques in simulation

## Prerequisites

- Completed Nav2 Navigation Stack lesson
- Understanding of computer vision and machine learning concepts
- Isaac Sim environment with various sensors configured
- Basic Python programming skills for data processing

## Introduction to Synthetic Data for Robotics

Synthetic data generation is crucial for robotics applications because:

- **Safety**: Training in simulation avoids risks to real robots and environments
- **Cost**: No need for expensive real-world data collection campaigns
- **Variety**: Easy to create diverse scenarios and edge cases
- **Labels**: Perfect ground truth for training and evaluation
- **Scale**: Generate large datasets efficiently

For humanoid robotics perception systems, synthetic data is particularly valuable because it can simulate complex human-scale environments and interactions.

### Types of Synthetic Data

1. **RGB Images**: For object detection, segmentation, and classification
2. **Depth Maps**: For 3D understanding and obstacle detection
3. **Semantic Segmentation**: Pixel-level labeling for scene understanding
4. **Instance Segmentation**: Object-specific segmentation masks
5. **Sensor Data**: LiDAR, IMU, and other sensor modalities
6. **Trajectory Data**: For navigation and path planning

## Isaac Sim Synthetic Data Tools

### Isaac Sim Replicator

Isaac Sim Replicator is a powerful tool for generating synthetic datasets:

- **Domain Randomization**: Randomize environments, lighting, and object properties
- **Sensor Simulation**: Generate data from multiple sensor types
- **Annotation Tools**: Automatic labeling and ground truth generation
- **Variety Generation**: Create diverse scenarios efficiently

### Setting up Replicator

1. **Install Replicator components**:
   ```bash
   # Replicator is included with Isaac Sim
   # No additional installation needed
   ```

2. **Basic Replicator script**:
   ```python
   #!/usr/bin/env python3
   # synthetic_data_generator.py
   # Basic synthetic data generation script

   import omni
   import omni.replicator.core as rep
   from pxr import Usd, UsdGeom, Gf

   # Create a simple scene for data generation
   def create_data_generation_scene():
       # Create a ground plane
       ground_plane = rep.create.plane(semantics=[('class', 'ground')])

       # Create some objects with random materials
       with rep.randomizer:
           def random_objects():
               # Create random shapes
               shapes = rep.randomizer.random_choice(
                   [
                       rep.create.cube,
                       rep.create.sphere,
                       rep.create.cylinder
                   ]
               )
               return shapes(positions=rep.distribution.uniform((-100, -100, 0), (100, 100, 10)), semantics=[('class', 'object')])

       # Create random lights
       lights = rep.create.light(
           position=rep.distribution.uniform((-500, -500, 1000), (500, 500, 1000)),
           rotation=rep.distribution.uniform((-5, -5, -5), (5, 5, 5)),
           count=5
       )

       return ground_plane, random_objects, lights

   # Configure the replicator
   with rep.new_layer():
       # Create the scene
       create_data_generation_scene()

       # Create a camera for RGB and depth capture
       camera = rep.create.camera()

       # Position the camera randomly
       camera.set_position(rep.distribution.uniform((-5, -5, 5), (5, 5, 10)))

       # Create triggers for randomization
       with rep.trigger.on_frame(num_frames=100):
           rep.randomizer.randomize()

       # Define outputs
       render_product = rep.create.render_product(camera, (1024, 1024))

       # Register outputs
       rep.WriterRegistry.enable_writer("debug_file_writer")
       rep.WriterRegistry.get("debug_file_writer").initialize(
           output_dir="synthetic_data_output",
           rgb=True,
           depth=True,
           semantic_segmentation=True
       )

       # Run the replicator
       rep.run()
   ```

## Creating Perception Training Data

### RGB Image Generation

```python
#!/usr/bin/env python3
# rgb_data_generator.py
# Generate RGB images with domain randomization

import omni.replicator.core as rep
import numpy as np

# Create a domain randomization function
def create_domain_randomization():
    # Randomize materials
    with rep.randomizer:
        def randomize_materials():
            # Get all materials in the scene
            materials = rep.get.materials()

            # Randomize their properties
            with materials:
                rep.randomizer.random_material_params(
                    roughness=rep.distribution.uniform(0.1, 1.0),
                    metallic=rep.distribution.uniform(0.0, 1.0),
                    color=rep.distribution.uniform((0, 0, 0), (1, 1, 1))
                )

    # Randomize lighting
    def randomize_lighting():
        lights = rep.get.lights()
        with lights:
            rep.randomizer.randomize_lights(
                intensity=rep.distribution.log_uniform(100, 10000),
                color=rep.distribution.uniform((0.5, 0.5, 0.5), (1, 1, 1))
            )

    # Randomize environment
    def randomize_environment():
        # Randomize fog, exposure, etc.
        rep.randomizer.randomize_post_process(
            exposure=rep.distribution.uniform(-1, 1),
            contrast=rep.distribution.uniform(0.8, 1.2),
            saturation=rep.distribution.uniform(0.8, 1.2)
        )

    return randomize_materials, randomize_lighting, randomize_environment

# Configure the replicator for RGB generation
with rep.new_layer():
    # Create domain randomization
    randomize_materials, randomize_lighting, randomize_environment = create_domain_randomization()

    # Create triggers
    with rep.trigger.on_frame(num_frames=1000):
        randomize_materials()
        randomize_lighting()
        randomize_environment()

    # Create camera
    camera = rep.create.camera()
    render_product = rep.create.render_product(camera, (640, 480))

    # Register RGB output
    rep.WriterRegistry.enable_writer("debug_file_writer")
    rep.WriterRegistry.get("debug_file_writer").initialize(
        output_dir="rgb_training_data",
        rgb=True
    )

    # Run the replicator
    rep.run()
```

### Semantic Segmentation Data

```python
#!/usr/bin/env python3
# segmentation_data_generator.py
# Generate semantic segmentation data

import omni.replicator.core as rep

def create_segmentation_scene():
    # Create objects with semantic labels
    with rep.randomizer:
        def create_objects():
            # Create objects with specific semantic classes
            cubes = rep.create.cube(
                position=rep.distribution.uniform((-100, -100, 0), (100, 100, 10)),
                semantics=[('class', 'obstacle')]
            )

            spheres = rep.create.sphere(
                position=rep.distribution.uniform((-100, -100, 0), (100, 100, 10)),
                semantics=[('class', 'target')]
            )

            planes = rep.create.plane(
                position=rep.distribution.uniform((-200, -200, 0), (200, 200, 0)),
                semantics=[('class', 'ground')]
            )

            return cubes, spheres, planes

# Configure for segmentation
with rep.new_layer():
    create_segmentation_scene()

    # Create camera
    camera = rep.create.camera()
    render_product = rep.create.render_product(camera, (640, 480))

    # Register segmentation output
    rep.WriterRegistry.enable_writer("debug_file_writer")
    rep.WriterRegistry.get("debug_file_writer").initialize(
        output_dir="segmentation_training_data",
        semantic_segmentation=True,
        instance_segmentation=True,
        rgb=True  # Include RGB for visualization
    )

    # Run the replicator
    rep.run()
```

## Data Pipeline Implementation

### Data Processing Script

```python
#!/usr/bin/env python3
# process_synthetic_data.py
# Process and validate synthetic data

import os
import json
import numpy as np
from PIL import Image
import cv2

def validate_synthetic_dataset(dataset_path):
    """Validate the structure and content of a synthetic dataset"""

    # Check required directories exist
    required_dirs = ['rgb', 'depth', 'segmentation', 'annotations']
    for dir_name in required_dirs:
        dir_path = os.path.join(dataset_path, dir_name)
        if not os.path.exists(dir_path):
            print(f"Warning: Missing directory {dir_path}")
            continue

    # Count files in each directory
    rgb_count = len([f for f in os.listdir(os.path.join(dataset_path, 'rgb')) if f.endswith(('.png', '.jpg'))])
    depth_count = len([f for f in os.listdir(os.path.join(dataset_path, 'depth')) if f.endswith('.png')])
    seg_count = len([f for f in os.listdir(os.path.join(dataset_path, 'segmentation')) if f.endswith('.png')])

    print(f"Dataset validation:")
    print(f"  RGB images: {rgb_count}")
    print(f"  Depth maps: {depth_count}")
    print(f"  Segmentation: {seg_count}")

    # Check for alignment (same number of files)
    if rgb_count == depth_count == seg_count:
        print("  ✓ All modalities aligned")
    else:
        print("  ⚠ Modality count mismatch")

    return rgb_count, depth_count, seg_count

def generate_training_splits(dataset_path, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    """Generate train/validation/test splits for the dataset"""

    # Get all file IDs
    rgb_dir = os.path.join(dataset_path, 'rgb')
    file_ids = [os.path.splitext(f)[0] for f in os.listdir(rgb_dir) if f.endswith(('.png', '.jpg'))]

    # Shuffle and split
    np.random.shuffle(file_ids)
    n_files = len(file_ids)

    train_end = int(n_files * train_ratio)
    val_end = int(n_files * (train_ratio + val_ratio))

    splits = {
        'train': file_ids[:train_end],
        'validation': file_ids[train_end:val_end],
        'test': file_ids[val_end:]
    }

    # Create split files
    for split_name, split_ids in splits.items():
        split_file = os.path.join(dataset_path, f'{split_name}_split.txt')
        with open(split_file, 'w') as f:
            for file_id in split_ids:
                f.write(f"{file_id}\n")

    print(f"Created splits:")
    for split_name, split_ids in splits.items():
        print(f"  {split_name}: {len(split_ids)} samples")

    return splits

def create_dataset_config(dataset_path, config_name="dataset_config.json"):
    """Create a configuration file for the dataset"""

    config = {
        "dataset_name": "Isaac_Sim_Humanoid_Perception",
        "version": "1.0",
        "description": "Synthetic perception dataset for humanoid robotics",
        "modalities": ["rgb", "depth", "segmentation"],
        "classes": {
            "0": "background",
            "1": "obstacle",
            "2": "target",
            "3": "ground"
        },
        "image_size": [640, 480],
        "data_splits": {
            "train": "train_split.txt",
            "validation": "validation_split.txt",
            "test": "test_split.txt"
        },
        "created_with": "Isaac Sim Replicator",
        "license": "MIT"
    }

    config_path = os.path.join(dataset_path, config_name)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"Created dataset config at {config_path}")

# Example usage
if __name__ == "__main__":
    dataset_path = "synthetic_perception_data"

    # Validate dataset
    validate_synthetic_dataset(dataset_path)

    # Generate splits
    splits = generate_training_splits(dataset_path)

    # Create config
    create_dataset_config(dataset_path)
```

## Training Data Workflows

### Perception Model Training Script

```python
#!/usr/bin/env python3
# train_perception_model.py
# Example training script for perception model using synthetic data

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image
import os
import numpy as np

class SyntheticPerceptionDataset(Dataset):
    """Dataset class for synthetic perception data"""

    def __init__(self, data_path, split='train', transform=None):
        self.data_path = data_path
        self.transform = transform

        # Load split file
        split_file = os.path.join(data_path, f"{split}_split.txt")
        with open(split_file, 'r') as f:
            self.file_ids = [line.strip() for line in f.readlines()]

        self.rgb_path = os.path.join(data_path, 'rgb')
        self.seg_path = os.path.join(data_path, 'segmentation')

    def __len__(self):
        return len(self.file_ids)

    def __getitem__(self, idx):
        file_id = self.file_ids[idx]

        # Load RGB image
        rgb_path = os.path.join(self.rgb_path, f"{file_id}.png")
        rgb_image = Image.open(rgb_path).convert('RGB')

        # Load segmentation
        seg_path = os.path.join(self.seg_path, f"{file_id}.png")
        seg_image = Image.open(seg_path).convert('L')  # Grayscale for segmentation

        if self.transform:
            rgb_image = self.transform(rgb_image)
            seg_image = self.transform(seg_image)

        # Convert segmentation to tensor
        seg_tensor = torch.tensor(np.array(seg_image), dtype=torch.long)

        return rgb_image, seg_tensor

def train_segmentation_model(data_path, num_epochs=10):
    """Train a segmentation model using synthetic data"""

    # Define transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Create datasets
    train_dataset = SyntheticPerceptionDataset(data_path, split='train', transform=transform)
    val_dataset = SyntheticPerceptionDataset(data_path, split='validation', transform=transform)

    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)

    # Simple segmentation model (using a pre-trained backbone)
    model = torch.hub.load('pytorch/vision:v0.10.0', 'fcn_resnet50', pretrained=True)
    # Modify the classifier for our number of classes
    model.classifier[-1] = nn.Conv2d(512, 4, kernel_size=(1, 1))  # 4 classes

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    model.train()
    for epoch in range(num_epochs):
        running_loss = 0.0
        for i, (images, targets) in enumerate(train_loader):
            images, targets = images.to(device), targets.to(device)

            optimizer.zero_grad()
            outputs = model(images)['out']
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            if i % 10 == 9:  # Print every 10 mini-batches
                print(f'Epoch {epoch+1}, Batch {i+1}, Loss: {running_loss/10:.4f}')
                running_loss = 0.0

    print('Training completed!')

    # Save the model
    torch.save(model.state_dict(), 'synthetic_perception_model.pth')
    print('Model saved as synthetic_perception_model.pth')

if __name__ == "__main__":
    data_path = "synthetic_perception_data"

    # Train the model
    train_segmentation_model(data_path)
```

## Hands-on Exercise: Complete Synthetic Data Pipeline

### Exercise Objective
Create a complete synthetic data generation and processing pipeline for humanoid perception training.

### Steps to Complete

1. Set up Isaac Sim Replicator for data generation
2. Create a diverse scene with domain randomization
3. Generate RGB, depth, and segmentation data
4. Process and validate the generated dataset
5. Create train/validation/test splits
6. Train a simple perception model with the data

### Implementation Commands

```bash
# Create necessary directories
mkdir -p synthetic_perception_data/{rgb,depth,segmentation,annotations}

# Run the data generation scripts (these would be executed in Isaac Sim)
# python3 rgb_data_generator.py
# python3 segmentation_data_generator.py

# Process the generated data
python3 process_synthetic_data.py

# Train the perception model
python3 train_perception_model.py
```

## Quality Assurance for Synthetic Data

### Data Quality Checks

```python
#!/usr/bin/env python3
# quality_assurance.py
# Quality checks for synthetic data

import os
import cv2
import numpy as np
from PIL import Image

def check_image_quality(image_path):
    """Check basic image quality metrics"""
    img = cv2.imread(image_path)

    # Check for blur using Laplacian variance
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Check for proper exposure
    mean_brightness = np.mean(gray)

    # Check for proper contrast
    std_dev = np.std(gray)

    quality_metrics = {
        'laplacian_variance': laplacian_var,
        'mean_brightness': mean_brightness,
        'std_deviation': std_dev
    }

    return quality_metrics

def validate_data_alignment(rgb_path, depth_path, seg_path):
    """Validate that modalities are properly aligned"""

    # Load images
    rgb_img = cv2.imread(rgb_path)
    depth_img = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED)
    seg_img = cv2.imread(seg_path, cv2.IMREAD_UNCHANGED)

    # Check dimensions
    if rgb_img.shape[:2] != depth_img.shape[:2] or rgb_img.shape[:2] != seg_img.shape[:2]:
        return False, "Dimension mismatch"

    # Check if all images exist and have data
    if rgb_img is None or depth_img is None or seg_img is None:
        return False, "Missing image"

    return True, "Aligned"

def generate_quality_report(dataset_path):
    """Generate a quality report for the dataset"""

    rgb_dir = os.path.join(dataset_path, 'rgb')
    depth_dir = os.path.join(dataset_path, 'depth')
    seg_dir = os.path.join(dataset_path, 'segmentation')

    quality_report = {
        'total_samples': 0,
        'quality_issues': [],
        'average_metrics': {
            'laplacian_variance': 0,
            'mean_brightness': 0,
            'std_deviation': 0
        }
    }

    file_ids = [os.path.splitext(f)[0] for f in os.listdir(rgb_dir) if f.endswith(('.png', '.jpg'))]
    quality_report['total_samples'] = len(file_ids)

    total_laplacian = 0
    total_brightness = 0
    total_std = 0

    for file_id in file_ids:
        rgb_path = os.path.join(rgb_dir, f"{file_id}.png")
        depth_path = os.path.join(depth_dir, f"{file_id}.png")
        seg_path = os.path.join(seg_dir, f"{file_id}.png")

        # Check alignment
        aligned, msg = validate_data_alignment(rgb_path, depth_path, seg_path)
        if not aligned:
            quality_report['quality_issues'].append(f"{file_id}: {msg}")

        # Check image quality
        metrics = check_image_quality(rgb_path)
        total_laplacian += metrics['laplacian_variance']
        total_brightness += metrics['mean_brightness']
        total_std += metrics['std_deviation']

    if len(file_ids) > 0:
        quality_report['average_metrics']['laplacian_variance'] = total_laplacian / len(file_ids)
        quality_report['average_metrics']['mean_brightness'] = total_brightness / len(file_ids)
        quality_report['average_metrics']['std_deviation'] = total_std / len(file_ids)

    return quality_report

# Example usage
if __name__ == "__main__":
    dataset_path = "synthetic_perception_data"
    report = generate_quality_report(dataset_path)

    print("Quality Report:")
    print(f"Total samples: {report['total_samples']}")
    print(f"Quality issues: {len(report['quality_issues'])}")
    print(f"Average Laplacian variance: {report['average_metrics']['laplacian_variance']:.2f}")
    print(f"Average brightness: {report['average_metrics']['mean_brightness']:.2f}")
    print(f"Average std deviation: {report['average_metrics']['std_deviation']:.2f}")
```

## Performance Considerations

### Computational Requirements
- High-resolution synthetic data generation can be computationally intensive
- Consider GPU requirements for both generation and processing
- Batch processing can improve efficiency

### Data Diversity
- Ensure synthetic data covers the full range of real-world scenarios
- Include edge cases and challenging conditions
- Balance between diversity and realism

## Troubleshooting Data Generation Issues

### Common Issues
- **Memory errors**: Reduce batch size or resolution
- **Alignment problems**: Check camera calibration and synchronization
- **Quality issues**: Adjust lighting and material parameters
- **Labeling errors**: Verify semantic annotation setup

## Summary

In this lesson, you learned:
- The importance of synthetic data for perception training
- How to use Isaac Sim Replicator for data generation
- Techniques for domain randomization and data augmentation
- How to process and validate synthetic datasets
- Implementation of a complete training pipeline

Synthetic data generation is essential for creating robust perception systems for humanoid robots.

## References

- [Isaac Sim Replicator Documentation](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorial_replicator.html)
- [Synthetic Data for Robotics](https://docs.nvidia.com/isaac/packages/replicator/index.html)

## Author Information

<div className="author-info">
  <h3>Author: Aamir Ahmed Shamsi</h3>
  <p><strong>GIAIC ID:</strong> 00486031</p>
  <p>This lesson was created with assistance from Claude AI.</p>
</div>