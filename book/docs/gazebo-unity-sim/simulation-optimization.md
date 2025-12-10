---
id: simulation-optimization
title: Simulation Optimization
sidebar_position: 6
description: Optimizing simulation performance and accuracy for efficient robotics development
---

# Simulation Optimization

<div className="gazebo-module">
  <p>This lesson covers techniques for optimizing simulation performance and accuracy for efficient robotics development.</p>
</div>

## Learning Objectives

By the end of this lesson, you will be able to:
- Identify performance bottlenecks in simulation
- Optimize physics parameters for performance vs accuracy trade-offs
- Implement efficient sensor simulation
- Balance real-time performance with simulation fidelity
- Profile and debug simulation performance issues

## Prerequisites

- Understanding of physics simulation concepts
- Experience with Gazebo and/or Unity simulation
- Basic knowledge of profiling tools

## Introduction to Simulation Optimization

Simulation optimization involves balancing performance and accuracy to meet specific requirements. The key trade-offs include:

- **Performance vs. Accuracy**: Higher accuracy typically requires more computational resources
- **Real-time vs. Speed**: Real-time simulation vs. faster-than-real-time execution
- **Visual Quality vs. Performance**: High-fidelity graphics vs. computational efficiency
- **Physics Fidelity vs. Stability**: Accurate physics vs. stable simulation

### Performance Metrics

Key metrics for simulation optimization:

- **Real-time Factor (RTF)**: Simulation time vs. wall clock time
- **Frames Per Second (FPS)**: Rendering performance
- **Update Rate**: Physics simulation frequency
- **CPU/GPU Utilization**: Resource consumption
- **Memory Usage**: RAM consumption

## Physics Optimization

### Time Step Optimization

The simulation time step is crucial for both performance and stability:

```python
#!/usr/bin/env python3
# physics_optimizer.py
# Tools for optimizing physics simulation parameters

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

class PhysicsOptimizer:
    def __init__(self):
        self.test_results = []

    def evaluate_timestep_performance(self, timesteps, simulation_time=10.0):
        """Evaluate performance across different time steps"""
        results = []

        for dt in timesteps:
            # Simulate a simple system: mass-spring-damper
            # dx/dt = v
            # dv/dt = (-k*x - c*v) / m
            def system(t, y):
                x, v = y
                m, k, c = 1.0, 10.0, 0.5  # mass, spring constant, damping
                dxdt = v
                dvdt = (-k*x - c*v) / m
                return [dxdt, dvdt]

            # Time the simulation
            import time
            start_time = time.time()

            sol = solve_ivp(system, [0, simulation_time], [1.0, 0.0],
                           method='RK45', max_step=dt)

            end_time = time.time()
            execution_time = end_time - start_time
            num_steps = len(sol.t)

            results.append({
                'timestep': dt,
                'execution_time': execution_time,
                'num_steps': num_steps,
                'steps_per_second': num_steps / simulation_time,
                'accuracy': self.estimate_accuracy(sol, dt)
            })

        return results

    def estimate_accuracy(self, solution, timestep):
        """Estimate accuracy based on solution smoothness"""
        # A simple accuracy metric based on derivative estimation
        if len(solution.y[0]) < 2:
            return 0.0

        # Calculate numerical derivatives
        dt = np.diff(solution.t)
        dx = np.diff(solution.y[0])
        vel_numeric = dx / dt

        # Compare with analytical solution for a damped oscillator
        # This is a simplified accuracy estimate
        return 1.0 / (1.0 + timestep * 100)  # Higher for smaller timesteps

    def plot_optimization_results(self, results):
        """Plot optimization results"""
        timesteps = [r['timestep'] for r in results]
        execution_times = [r['execution_time'] for r in results]
        accuracies = [r['accuracy'] for r in results]
        steps_per_sec = [r['steps_per_second'] for r in results]

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

        # Execution time vs timestep
        ax1.loglog(timesteps, execution_times, 'b-o')
        ax1.set_xlabel('Time Step (s)')
        ax1.set_ylabel('Execution Time (s)')
        ax1.set_title('Execution Time vs Time Step')
        ax1.grid(True)

        # Accuracy vs timestep
        ax2.loglog(timesteps, accuracies, 'r-o')
        ax2.set_xlabel('Time Step (s)')
        ax2.set_ylabel('Estimated Accuracy')
        ax2.set_title('Accuracy vs Time Step')
        ax2.grid(True)

        # Steps per second vs timestep
        ax3.semilogx(timesteps, steps_per_sec, 'g-o')
        ax3.set_xlabel('Time Step (s)')
        ax3.set_ylabel('Steps per Second')
        ax3.set_title('Simulation Steps per Second')
        ax3.grid(True)

        # Performance vs accuracy trade-off
        ax4.plot(execution_times, accuracies, 'm-o')
        ax4.set_xlabel('Execution Time (s)')
        ax4.set_ylabel('Estimated Accuracy')
        ax4.set_title('Performance vs Accuracy Trade-off')
        ax4.grid(True)

        plt.tight_layout()
        plt.show()

def main():
    optimizer = PhysicsOptimizer()

    # Test different time steps
    timesteps = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1]
    results = optimizer.evaluate_timestep_performance(timesteps)

    print("Physics Optimization Results:")
    print("TimeStep | ExecTime | NumSteps | Steps/s | Accuracy")
    print("-" * 55)
    for result in results:
        print(f"{result['timestep']:8.4f} | {result['execution_time']:8.4f} | "
              f"{result['num_steps']:8d} | {result['steps_per_second']:7.1f} | "
              f"{result['accuracy']:8.4f}")

    # Find optimal timestep based on weighted score
    # Weight accuracy higher (0.7) than performance (0.3)
    optimal_idx = 0
    best_score = -1
    for i, result in enumerate(results):
        # Normalize execution time (smaller is better)
        norm_time = 1.0 / (result['execution_time'] + 0.001)
        # Normalize accuracy
        norm_accuracy = result['accuracy']
        score = 0.3 * norm_time + 0.7 * norm_accuracy

        if score > best_score:
            best_score = score
            optimal_idx = i

    optimal_result = results[optimal_idx]
    print(f"\nOptimal timestep: {optimal_result['timestep']:.4f}s "
          f"(score: {best_score:.4f})")

if __name__ == "__main__":
    main()
```

### Gazebo Physics Optimization

Optimize Gazebo physics parameters for your specific use case:

```xml
<!-- Optimized physics configuration -->
<physics type="ode">
  <!-- Performance-oriented configuration -->
  <max_step_size>0.01</max_step_size>  <!-- Larger for performance -->
  <real_time_factor>1.0</real_time_factor>
  <real_time_update_rate>100.0</real_time_update_rate>  <!-- Lower for performance -->

  <ode>
    <solver>
      <type>quick</type>  <!-- Fast solver -->
      <iters>20</iters>   <!-- Balance between speed and stability -->
      <sor>1.3</sor>
    </solver>
    <constraints>
      <cfm>0.0</cfm>
      <erp>0.2</erp>
      <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>

<!-- For accuracy-oriented simulation -->
<physics type="ode">
  <max_step_size>0.001</max_step_size>  <!-- Smaller for accuracy -->
  <real_time_factor>0.5</real_time_factor>  <!-- Allow slower than real-time -->
  <real_time_update_rate>1000.0</real_time_update_rate>

  <ode>
    <solver>
      <type>quick</type>
      <iters>100</iters>  <!-- More iterations for stability -->
      <sor>1.0</sor>
    </solver>
    <constraints>
      <cfm>1e-5</cfm>    <!-- Smaller CFM for accuracy -->
      <erp>0.9</erp>     <!-- Higher ERP for accuracy -->
      <contact_max_correcting_vel>10.0</contact_max_correcting_vel>
      <contact_surface_layer>0.0001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

## Collision Optimization

### Simplified Collision Models

Use simplified geometries for collision detection:

```xml
<!-- In URDF or SDF -->
<link name="complex_link">
  <!-- Visual model (detailed) -->
  <visual>
    <geometry>
      <mesh filename="complex_model.dae"/>
    </geometry>
  </visual>

  <!-- Collision model (simplified) -->
  <collision>
    <geometry>
      <!-- Use simpler shape for collision -->
      <cylinder radius="0.1" length="0.2"/>
      <!-- Or use multiple simple shapes -->
      <!-- <box size="0.2 0.2 0.1"/> -->
    </geometry>
  </collision>
</link>
```

### Collision Filtering

Implement collision filtering to reduce unnecessary collision checks:

```xml
<!-- In URDF with Gazebo plugins -->
<gazebo reference="link_name">
  <collision>
    <surface>
      <contact>
        <collide_without_contact>0</collide_without_contact>
        <collide_without_contact_bitmask>255</collide_without_contact_bitmask>
      </contact>
    </surface>
  </collision>
</gazebo>
```

## Sensor Optimization

### Efficient Sensor Configuration

Optimize sensor parameters for performance:

```xml
<!-- Optimized camera configuration -->
<sensor type="camera" name="optimized_camera">
  <update_rate>15.0</update_rate>  <!-- Lower rate for performance -->
  <camera name="head">
    <horizontal_fov>1.047</horizontal_fov>  <!-- 60 degrees -->
    <image>
      <width>320</width>  <!-- Lower resolution for performance -->
      <height>240</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>5.0</far>  <!-- Shorter range for performance -->
    </clip>
  </camera>
</sensor>

<!-- Optimized LiDAR configuration -->
<sensor type="ray" name="optimized_lidar">
  <update_rate>10.0</update_rate>  <!-- Lower update rate -->
  <ray>
    <scan>
      <horizontal>
        <samples>360</samples>  <!-- Lower resolution -->
        <resolution>1</resolution>
        <min_angle>-1.570796</min_angle>  <!-- 90 degrees FOV instead of 180 -->
        <max_angle>1.570796</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>10.0</max>  <!-- Shorter range -->
      <resolution>0.01</resolution>
    </range>
  </ray>
</sensor>
```

### Sensor Performance Profiling

```python
#!/usr/bin/env python3
# sensor_profiler.py
# Profile sensor performance in simulation

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan, Imu
from std_msgs.msg import Float64
import time
from collections import deque
import statistics

class SensorProfiler(Node):
    def __init__(self):
        super().__init__('sensor_profiler')

        # Sensor data storage
        self.image_times = deque(maxlen=100)
        self.lidar_times = deque(maxlen=100)
        self.imu_times = deque(maxlen=100)

        # Subscribers
        self.image_sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 1)
        self.lidar_sub = self.create_subscription(
            LaserScan, '/lidar/scan', self.lidar_callback, 1)
        self.imu_sub = self.create_subscription(
            Imu, '/imu/data', self.imu_callback, 1)

        # Timer for reporting
        self.report_timer = self.create_timer(5.0, self.report_performance)

        self.get_logger().info('Sensor profiler initialized')

    def image_callback(self, msg):
        """Profile image sensor performance"""
        current_time = self.get_clock().now().nanoseconds / 1e9
        self.image_times.append(current_time)

    def lidar_callback(self, msg):
        """Profile LiDAR sensor performance"""
        current_time = self.get_clock().now().nanoseconds / 1e9
        self.lidar_times.append(current_time)

    def imu_callback(self, msg):
        """Profile IMU sensor performance"""
        current_time = self.get_clock().now().nanoseconds / 1e9
        self.imu_times.append(current_time)

    def report_performance(self):
        """Report sensor performance metrics"""
        self.get_logger().info('\n' + '='*50)
        self.get_logger().info('SENSOR PERFORMANCE REPORT')
        self.get_logger().info('='*50)

        if len(self.image_times) > 1:
            image_intervals = [self.image_times[i] - self.image_times[i-1]
                              for i in range(1, len(self.image_times))]
            avg_interval = statistics.mean(image_intervals)
            avg_rate = 1.0 / avg_interval if avg_interval > 0 else 0

            self.get_logger().info(f'Camera: Avg rate: {avg_rate:.2f} Hz, '
                                 f'Avg interval: {avg_interval*1000:.2f} ms')

        if len(self.lidar_times) > 1:
            lidar_intervals = [self.lidar_times[i] - self.lidar_times[i-1]
                              for i in range(1, len(self.lidar_times))]
            avg_interval = statistics.mean(lidar_intervals)
            avg_rate = 1.0 / avg_interval if avg_interval > 0 else 0

            self.get_logger().info(f'LiDAR: Avg rate: {avg_rate:.2f} Hz, '
                                 f'Avg interval: {avg_interval*1000:.2f} ms')

        if len(self.imu_times) > 1:
            imu_intervals = [self.imu_times[i] - self.imu_times[i-1]
                            for i in range(1, len(self.imu_times))]
            avg_interval = statistics.mean(imu_intervals)
            avg_rate = 1.0 / avg_interval if avg_interval > 0 else 0

            self.get_logger().info(f'IMU: Avg rate: {avg_rate:.2f} Hz, '
                                 f'Avg interval: {avg_interval*1000:.2f} ms')

def main(args=None):
    rclpy.init(args=args)
    profiler = SensorProfiler()

    try:
        rclpy.spin(profiler)
    except KeyboardInterrupt:
        pass
    finally:
        profiler.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Rendering and Graphics Optimization

### Gazebo Rendering Optimization

```bash
# Gazebo command line options for performance
gz sim -r --iterations 1000 --profile performance

# Or with specific rendering options
export GZ_GUI_PLUGIN_INFO_VISIBLE=0
export GZ_SIM_HEADLESS=1  # For headless operation
gz sim -s HeadlessSystem
```

### Unity Rendering Optimization

For Unity-based simulation, implement these optimizations:

```csharp
using UnityEngine;

public class RenderingOptimizer : MonoBehaviour
{
    [Header("LOD Configuration")]
    public LODGroup lodGroup;
    public int targetFramerate = 60;

    [Header("Quality Settings")]
    public int targetQualityLevel = 2;  // Medium
    public bool useOcclusionCulling = true;
    public bool useLOD = true;

    void Start()
    {
        OptimizeRendering();
    }

    void OptimizeRendering()
    {
        // Set target frame rate
        Application.targetFrameRate = targetFramerate;

        // Set quality level
        QualitySettings.SetQualityLevel(targetQualityLevel, true);

        // Enable occlusion culling if available
        if (useOcclusionCulling)
        {
            StaticOcclusionCulling.Compute();
        }

        // Configure LOD if available
        if (lodGroup != null && useLOD)
        {
            ConfigureLOD();
        }

        Debug.Log($"Rendering optimized: {targetFramerate} FPS target, Quality: {QualitySettings.names[targetQualityLevel]}");
    }

    void ConfigureLOD()
    {
        // Configure LOD distances
        LOD[] lods = new LOD[3];
        lods[0] = new LOD(0.5f, GetLODMeshes(0)); // High detail
        lods[1] = new LOD(0.2f, GetLODMeshes(1)); // Medium detail
        lods[2] = new LOD(0.05f, GetLODMeshes(2)); // Low detail

        lodGroup.SetLODs(lods);
        lodGroup.RecalculateBounds();
    }

    Renderer[] GetLODMeshes(int lodLevel)
    {
        // Return appropriate renderers for each LOD level
        // Implementation depends on your specific model structure
        return new Renderer[0];
    }
}
```

## Memory and Resource Optimization

### Resource Management Script

```python
#!/usr/bin/env python3
# resource_optimizer.py
# Optimize simulation resource usage

import psutil
import os
import time
import gc
from collections import defaultdict

class ResourceManager:
    def __init__(self):
        self.resource_usage = defaultdict(list)
        self.optimization_thresholds = {
            'cpu_percent': 80,
            'memory_percent': 80,
            'disk_percent': 90
        }

    def monitor_resources(self):
        """Monitor system resource usage"""
        usage = {
            'timestamp': time.time(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'memory_available_gb': psutil.virtual_memory().available / (1024**3),
            'process_count': len(psutil.pids())
        }

        # Store usage data
        for key, value in usage.items():
            if key != 'timestamp':
                self.resource_usage[key].append(value)

        return usage

    def check_optimization_needed(self, usage):
        """Check if optimization is needed based on thresholds"""
        optimization_needed = {}
        for resource, threshold in self.optimization_thresholds.items():
            if usage[resource] > threshold:
                optimization_needed[resource] = True
            else:
                optimization_needed[resource] = False

        return optimization_needed

    def suggest_optimizations(self, optimization_needed):
        """Suggest optimizations based on resource usage"""
        suggestions = []

        if optimization_needed.get('cpu_percent', False):
            suggestions.append("Reduce physics update rate")
            suggestions.append("Simplify collision geometries")
            suggestions.append("Reduce sensor update rates")

        if optimization_needed.get('memory_percent', False):
            suggestions.append("Use lower resolution textures/models")
            suggestions.append("Implement object pooling")
            suggestions.append("Reduce simulation world size")

        if optimization_needed.get('disk_percent', False):
            suggestions.append("Clean up old simulation logs")
            suggestions.append("Use compressed sensor data formats")

        return suggestions

    def optimize_simulation(self):
        """Apply optimizations based on current resource usage"""
        usage = self.monitor_resources()
        optimization_needed = self.check_optimization_needed(usage)
        suggestions = self.suggest_optimizations(optimization_needed)

        print(f"\nResource Usage Report:")
        print(f"CPU: {usage['cpu_percent']:.1f}%")
        print(f"Memory: {usage['memory_percent']:.1f}%")
        print(f"Available Memory: {usage['memory_available_gb']:.2f} GB")
        print(f"Disk: {usage['disk_percent']:.1f}%")

        if suggestions:
            print(f"\nOptimization Suggestions:")
            for suggestion in suggestions:
                print(f"  - {suggestion}")
        else:
            print(f"\nResources look good! No optimizations needed.")

def main():
    manager = ResourceManager()

    # Monitor resources for a period
    for i in range(5):
        manager.optimize_simulation()
        time.sleep(2)

    # Print final summary
    print(f"\nFinal Resource Summary:")
    for resource, values in manager.resource_usage.items():
        if values:
            avg_value = sum(values) / len(values)
            print(f"Average {resource}: {avg_value:.2f}")

if __name__ == "__main__":
    main()
```

## Real-time Performance Optimization

### Real-time Factor (RTF) Optimization

```python
#!/usr/bin/env python3
# rtf_optimizer.py
# Optimize for real-time performance

import time
import subprocess
import signal
import sys

class RTFOptimizer:
    def __init__(self):
        self.target_rtf = 1.0  # Real-time
        self.current_rtf = 0.0
        self.optimization_parameters = {
            'max_step_size': 0.001,
            'real_time_update_rate': 1000.0,
            'solver_iterations': 20,
            'contact_surface_layer': 0.001
        }

    def measure_rtf(self, simulation_time=10):
        """Measure current Real-Time Factor"""
        # This is a simplified measurement
        # In practice, you'd measure simulation time vs wall clock time
        wall_start = time.time()

        # Simulate for specified time
        time.sleep(simulation_time)

        wall_end = time.time()
        wall_duration = wall_end - wall_start

        # RTF = simulation time / wall clock time
        self.current_rtf = simulation_time / wall_duration
        return self.current_rtf

    def optimize_for_rtf(self, target_rtf=1.0):
        """Adjust parameters to achieve target RTF"""
        print(f"Optimizing for RTF: {target_rtf}")

        # Start with conservative parameters
        params = self.optimization_parameters.copy()

        # Adjust parameters based on current performance
        if self.current_rtf > target_rtf:
            # Running too fast, can increase accuracy
            params['max_step_size'] *= 0.8  # Smaller steps for accuracy
            params['solver_iterations'] = min(100, params['solver_iterations'] + 10)
        else:
            # Running too slow, need to improve performance
            params['max_step_size'] *= 1.2  # Larger steps for performance
            params['solver_iterations'] = max(5, params['solver_iterations'] - 5)

        print(f"Adjusted parameters: {params}")
        return params

    def adaptive_optimization(self, duration=60):
        """Continuously optimize during simulation"""
        start_time = time.time()

        while time.time() - start_time < duration:
            # Measure current RTF
            current_rtf = self.measure_rtf(simulation_time=1)

            print(f"Current RTF: {current_rtf:.3f}, Target: {self.target_rtf:.3f}")

            # Adjust if needed
            if abs(current_rtf - self.target_rtf) > 0.1:
                self.optimization_parameters = self.optimize_for_rtf(self.target_rtf)

            time.sleep(0.1)  # Small delay to prevent overwhelming

def main():
    optimizer = RTFOptimizer()

    print("Starting RTF optimization...")
    print("This would normally connect to a running simulation")

    # Simulate the optimization process
    for i in range(10):
        # Simulate measuring RTF
        import random
        simulated_rtf = 0.8 + random.random() * 0.4  # 0.8 to 1.2
        optimizer.current_rtf = simulated_rtf

        print(f"Iteration {i+1}: Measured RTF = {simulated_rtf:.3f}")

        if abs(simulated_rtf - optimizer.target_rtf) > 0.1:
            params = optimizer.optimize_for_rtf(optimizer.target_rtf)
            print(f"  Adjusted parameters for RTF optimization")

        time.sleep(0.5)

if __name__ == "__main__":
    main()
```

## Hands-on Exercise: Simulation Optimization

### Exercise Objective
Optimize a simulation for performance while maintaining required accuracy.

### Steps to Complete

1. Set up a basic simulation with performance monitoring
2. Measure baseline performance metrics
3. Apply optimization techniques
4. Validate that accuracy requirements are still met
5. Document performance improvements

### Optimization Validation Script

```python
#!/usr/bin/env python3
# optimization_validator.py
# Validate optimization results

import numpy as np
import matplotlib.pyplot as plt

class OptimizationValidator:
    def __init__(self):
        self.metrics = {
            'baseline': {},
            'optimized': {}
        }

    def run_baseline_test(self):
        """Run simulation with default parameters"""
        print("Running baseline simulation test...")

        # Simulate baseline performance
        baseline_metrics = {
            'rtf': 0.5,  # Real-time factor
            'cpu_usage': 75.0,  # Percent
            'memory_usage': 2.5,  # GB
            'simulation_steps_per_sec': 50000,
            'accuracy_score': 0.95  # 0-1 scale
        }

        self.metrics['baseline'] = baseline_metrics
        return baseline_metrics

    def run_optimized_test(self):
        """Run simulation with optimized parameters"""
        print("Running optimized simulation test...")

        # Simulate optimized performance
        optimized_metrics = {
            'rtf': 0.8,  # Improved real-time factor
            'cpu_usage': 45.0,  # Reduced CPU usage
            'memory_usage': 1.8,  # Reduced memory usage
            'simulation_steps_per_sec': 80000,  # Increased throughput
            'accuracy_score': 0.92  # Slightly reduced accuracy (acceptable trade-off)
        }

        self.metrics['optimized'] = optimized_metrics
        return optimized_metrics

    def calculate_improvement(self):
        """Calculate improvement metrics"""
        baseline = self.metrics['baseline']
        optimized = self.metrics['optimized']

        if not baseline or not optimized:
            print("Error: Missing baseline or optimized metrics")
            return {}

        improvements = {}

        # Calculate improvements
        improvements['rtf_improvement'] = (optimized['rtf'] - baseline['rtf']) / baseline['rtf'] * 100
        improvements['cpu_improvement'] = (baseline['cpu_usage'] - optimized['cpu_usage']) / baseline['cpu_usage'] * 100
        improvements['memory_improvement'] = (baseline['memory_usage'] - optimized['memory_usage']) / baseline['memory_usage'] * 100
        improvements['throughput_improvement'] = (optimized['simulation_steps_per_sec'] - baseline['simulation_steps_per_sec']) / baseline['simulation_steps_per_sec'] * 100
        improvements['accuracy_change'] = optimized['accuracy_score'] - baseline['accuracy_score']

        return improvements

    def validate_acceptance_criteria(self):
        """Validate that optimization meets acceptance criteria"""
        improvements = self.calculate_improvement()

        # Define acceptance criteria
        criteria = {
            'min_rtf_improvement': 10,  # Percent improvement in RTF
            'min_cpu_improvement': 10,  # Percent improvement in CPU usage
            'min_accuracy_threshold': 0.90  # Minimum acceptable accuracy
        }

        print(f"\nAcceptance Criteria Validation:")
        print(f"  Min RTF improvement: {criteria['min_rtf_improvement']}%")
        print(f"  Min CPU improvement: {criteria['min_cpu_improvement']}%")
        print(f"  Min accuracy threshold: {criteria['min_accuracy_threshold']}")

        rtf_ok = improvements.get('rtf_improvement', 0) >= criteria['min_rtf_improvement']
        cpu_ok = improvements.get('cpu_improvement', 0) >= criteria['min_cpu_improvement']
        accuracy_ok = self.metrics['optimized'].get('accuracy_score', 0) >= criteria['min_accuracy_threshold']

        print(f"\nValidation Results:")
        print(f"  RTF improvement OK: {rtf_ok} ({improvements.get('rtf_improvement', 0):.1f}%)")
        print(f"  CPU improvement OK: {cpu_ok} ({improvements.get('cpu_improvement', 0):.1f}%)")
        print(f"  Accuracy threshold OK: {accuracy_ok} ({self.metrics['optimized'].get('accuracy_score', 0):.2f})")

        overall_success = rtf_ok and cpu_ok and accuracy_ok
        print(f"\nOverall Optimization Success: {overall_success}")

        return overall_success

    def generate_report(self):
        """Generate optimization report"""
        print(f"\n{'='*60}")
        print(f"SUPSIMULATION OPTIMIZATION REPORT")
        print(f"{'='*60}")

        baseline = self.metrics['baseline']
        optimized = self.metrics['optimized']
        improvements = self.calculate_improvement()

        print(f"Baseline Performance:")
        for key, value in baseline.items():
            print(f"  {key}: {value}")

        print(f"\nOptimized Performance:")
        for key, value in optimized.items():
            print(f"  {key}: {value}")

        print(f"\nImprovements:")
        for key, value in improvements.items():
            if 'improvement' in key:
                print(f"  {key}: {value:+.2f}%")
            else:
                print(f"  {key}: {value:+.3f}")

        # Create visualization
        metrics = ['RTF', 'CPU Usage (%)', 'Memory (GB)', 'Steps/Sec']
        baseline_values = [
            baseline['rtf'],
            baseline['cpu_usage'],
            baseline['memory_usage'],
            baseline['simulation_steps_per_sec']
        ]
        optimized_values = [
            optimized['rtf'],
            optimized['cpu_usage'],
            optimized['memory_usage'],
            optimized['simulation_steps_per_sec']
        ]

        x = np.arange(len(metrics))
        width = 0.35

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(x - width/2, baseline_values, width, label='Baseline', alpha=0.8)
        ax.bar(x + width/2, optimized_values, width, label='Optimized', alpha=0.8)

        ax.set_xlabel('Metrics')
        ax.set_ylabel('Values')
        ax.set_title('Simulation Performance: Baseline vs Optimized')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

def main():
    validator = OptimizationValidator()

    # Run tests
    validator.run_baseline_test()
    validator.run_optimized_test()

    # Validate results
    success = validator.validate_acceptance_criteria()

    # Generate report
    validator.generate_report()

    print(f"\nOptimization {'successful' if success else 'failed'}!")

if __name__ == "__main__":
    main()
```

## Best Practices for Simulation Optimization

### 1. Progressive Optimization
- Start with default parameters
- Optimize one aspect at a time
- Measure impact of each change
- Document the optimization process

### 2. Use Case-Driven Optimization
- Identify the primary use case (real-time control, batch simulation, etc.)
- Optimize for the specific requirements
- Balance performance and accuracy appropriately

### 3. Monitoring and Profiling
- Continuously monitor performance metrics
- Use profiling tools to identify bottlenecks
- Establish baseline performance for comparison
- Set up automated performance regression tests

### 4. Validation After Optimization
- Verify that simulation behavior is still correct
- Check that accuracy requirements are met
- Test edge cases and corner scenarios
- Validate results against known benchmarks

## Troubleshooting Performance Issues

### Common Performance Issues
- **Low RTF**: Increase time step, reduce solver iterations
- **High CPU usage**: Simplify collision models, reduce sensor rates
- **Memory leaks**: Check for proper resource cleanup
- **Instability**: Decrease time step, increase solver iterations

### Debugging Tools
- Use simulation profiler tools
- Monitor system resources during simulation
- Check for error messages in logs
- Validate physics parameters

## Summary

In this lesson, you learned:
- How to optimize physics parameters for performance vs accuracy trade-offs
- Techniques for efficient collision detection and sensor simulation
- How to monitor and profile simulation performance
- Best practices for maintaining accuracy while improving performance

Simulation optimization is crucial for efficient robotics development, allowing you to run more complex simulations within your computational constraints.

## References

- [Gazebo Performance Tuning](http://gazebosim.org/tutorials?tut=performance_tuning&cat=simulation)
- [Unity Performance Optimization](https://docs.unity3d.com/Manual/OptimizingGraphicsPerformance.html)
- [Physics Simulation Optimization](http://gazebosim.org/tutorials?tut=physics_params&cat=simulation)

## Author Information

<div className="author-info">
  <h3>Author: Aamir Ahmed Shamsi</h3>
  <p><strong>GIAIC ID:</strong> 00486031</p>
  <p>This lesson was created with assistance from Claude AI.</p>
</div>