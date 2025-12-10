# Quickstart Guide: Module 3: The AI-Robot Brain (NVIDIA Isaac™)

## Prerequisites

- Ubuntu 22.04 LTS (recommended)
- RTX 4090 or equivalent GPU for optimal Isaac Sim rendering
- NVIDIA GPU drivers with CUDA support
- Isaac Sim powered by Omniverse installed
- ROS 2 Humble Hawksbill LTS installed
- Python 3.10+ with pip
- Git for version control
- 32GB+ RAM recommended for complex humanoid simulations

## System Setup

1. **Install NVIDIA drivers and CUDA**
   ```bash
   # Update system packages
   sudo apt update && sudo apt upgrade -y

   # Install NVIDIA drivers (adjust version as needed)
   sudo apt install nvidia-driver-535 nvidia-utils-535

   # Install CUDA toolkit
   sudo apt install nvidia-cuda-toolkit

   # Reboot to apply changes
   sudo reboot
   ```

2. **Install Isaac Sim powered by Omniverse**
   - Download and install Omniverse Launcher from NVIDIA Developer website
   - Launch Omniverse Launcher and sign in with your NVIDIA account
   - Install Isaac Sim extension
   - Verify installation by launching Isaac Sim and checking for errors

3. **Install ROS 2 Humble Hawksbill**
   ```bash
   # Setup locale
   sudo locale-gen en_US en_US.UTF-8
   sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

   # Setup sources
   sudo apt install software-properties-common
   sudo add-apt-repository universe

   # Add ROS 2 apt repository
   sudo apt update && sudo apt install curl gnupg lsb-release
   sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

   # Install ROS 2 packages
   sudo apt update
   sudo apt install ros-humble-desktop
   sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential

   # Initialize rosdep
   sudo rosdep init
   rosdep update

   # Source ROS 2 environment
   echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
   source ~/.bashrc
   ```

4. **Install Isaac ROS packages**
   ```bash
   # Create a ROS 2 workspace
   mkdir -p ~/isaac_ros_ws/src
   cd ~/isaac_ros_ws

   # Source ROS 2 environment
   source /opt/ros/humble/setup.bash

   # Install Isaac ROS dependencies
   sudo apt update
   rosdep install --from-paths src --ignore-src -r -y

   # Build the workspace
   colcon build
   ```

## Repository Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to the book directory and install dependencies**
   ```bash
   cd book
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```
   This will start the Docusaurus development server at http://localhost:3000

## Isaac Sim Environment Setup

### Basic Scene Creation
1. Launch Isaac Sim from Omniverse Launcher
2. Create a new scene: File → New Scene
3. Add a humanoid robot: Create → Robot → Select humanoid model
4. Add sensors: Create → Sensors → Camera, LiDAR, IMU
5. Save the scene to your project directory

### Isaac ROS Bridge Configuration
1. In Isaac Sim, navigate to Isaac Examples → ROS2 → ROS2-Simple-World
2. Run the example to verify Isaac Sim to ROS 2 communication
3. In a new terminal, source ROS 2:
   ```bash
   source /opt/ros/humble/setup.bash
   ```
4. Verify ROS 2 topics are being published:
   ```bash
   ros2 topic list
   ros2 topic echo /camera/camera_info
   ```

## Content Creation Workflow

1. **Create a new lesson**
   ```bash
   # Create the lesson file in the appropriate module directory
   touch docs/isaac-ai-brain/lesson-x-title.md
   ```

2. **Add lesson metadata**
   ```markdown
   ---
   id: lesson-x-title
   title: Lesson Title
   sidebar_position: X
   description: Brief description of the lesson
   ---

   # Lesson Title

   Content here...
   ```

3. **Update sidebar configuration**
   Edit `book/sidebars.js` to include the new lesson in the navigation.

4. **Create Isaac Sim examples**
   ```bash
   # Create example in the examples/isaac directory
   mkdir -p examples/isaac/new-example
   touch examples/isaac/new-example/example_script.py
   ```

## Interactive Tutorial Framework

1. **Set up validation scripts**
   ```bash
   # Create validation script for an exercise
   touch examples/isaac/interactive-tutorials/validation_scripts/validate_exercise_x.py
   ```

2. **Run validation**
   ```bash
   # Example of running a validation script
   cd examples/isaac/interactive-tutorials/validation_scripts
   python3 validate_isaac_sim.py
   ```

## Custom Bipedal Nav2 Plugin Setup

1. **Create custom plugin workspace**
   ```bash
   mkdir -p ~/nav2_bipedal_ws/src
   cd ~/nav2_bipedal_ws/src
   ```

2. **Create the custom controller plugin**
   ```bash
   # Create plugin package
   ros2 pkg create --build-type ament_cmake nav2_bipedal_controller
   ```

3. **Build the custom plugin**
   ```bash
   cd ~/nav2_bipedal_ws
   colcon build --packages-select nav2_bipedal_controller
   source install/setup.bash
   ```

## Quality Checks

1. **Validate Isaac Sim examples**
   ```bash
   cd examples/isaac
   # Run validation scripts for each example
   python3 interactive-tutorials/validation_scripts/validate_isaac_sim.py
   python3 interactive-tutorials/validation_scripts/validate_ros_integration.py
   python3 interactive-tutorials/validation_scripts/validate_nav2_setup.py
   ```

2. **Check RAG chunk sizes**
   ```bash
   # Verify content chunks are 500-1200 characters
   # This is done automatically during the build process
   ```

3. **Run all quality checks**
   ```bash
   # Execute comprehensive validation
   cd book
   npm run build
   ```

## Building for Production

```bash
cd book
npm run build
```

This creates a `book/build/` directory with the static site ready for deployment.

## Deployment

The site is configured for GitHub Pages deployment. After pushing changes to the main branch, GitHub Actions will automatically build and deploy the site.

## Troubleshooting

1. **Isaac Sim not launching**
   - Verify NVIDIA drivers are properly installed
   - Check GPU compatibility
   - Ensure Omniverse Launcher is signed in

2. **ROS 2 communication issues**
   - Verify ROS 2 Humble is properly sourced
   - Check network configuration
   - Confirm Isaac ROS packages are installed

3. **Performance issues**
   - Ensure GPU meets minimum requirements (RTX 4090 or equivalent)
   - Close unnecessary applications
   - Verify sufficient RAM (32GB+ recommended)