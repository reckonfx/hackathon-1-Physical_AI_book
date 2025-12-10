# Data Model: Module 3: The AI-Robot Brain (NVIDIA Isaac™)

## Module Entity

**Fields**:
- id: string (unique identifier, e.g., "module-3-ai-robot-brain")
- title: string (module title)
- description: string (overview of the module)
- lesson_count: integer (number of lessons)
- estimated_duration: string (e.g., "6-8 hours")
- learning_outcomes: array of strings
- simulation_environments: array of strings (e.g., ["isaac-sim", "isaac-ros", "nav2"])
- target_audience: string (e.g., "intermediate AI/robotics students")

**Relationships**:
- contains many Lessons
- contains many Sections (through Lessons)
- contains many Isaac Sim Examples (through Lessons)

## Lesson Entity

**Fields**:
- id: string (unique identifier, e.g., "lesson-1-isaac-sim-fundamentals")
- title: string (lesson title)
- module: string (parent module identifier)
- order: integer (sequence number within module)
- content: string (Markdown content)
- objectives: array of strings (learning objectives)
- prerequisites: array of strings (required knowledge)
- examples: array of simulation examples
- exercises: array of practice problems
- references: array of official documentation links
- interactive_exercises: array of interactive exercise configurations
- validation_scripts: array of file paths to validation scripts

**Relationships**:
- belongs to one Module
- contains many Sections

## Section Entity

**Fields**:
- id: string (unique identifier)
- title: string (section title)
- lesson: string (parent lesson identifier)
- order: integer (sequence number within lesson)
- content: string (Markdown content)
- chunk_size: integer (for RAG optimization, 500-1200 chars)
- content_type: string (e.g., "explanation", "code_example", "diagram", "exercise")

**Relationships**:
- belongs to one Lesson
- belongs to one Module (through Lesson)

## Isaac Sim Example Entity

**Fields**:
- id: string (unique identifier)
- title: string (description of the example)
- environment: string (e.g., "isaac-sim", "isaac-ros", "nav2")
- type: string (e.g., "scene-setup", "perception", "vslam", "navigation")
- description: string (what the example demonstrates)
- lesson: string (associated lesson)
- files: array of file paths (for the simulation files)
- requirements: array of string (system requirements for the example)
- validation_script: string (path to validation script)

**Relationships**:
- belongs to one Lesson
- optionally belongs to one Section

## Diagram Entity

**Fields**:
- id: string (unique identifier)
- title: string (description of the diagram)
- alt_text: string (accessibility description)
- filename: string (file path in static/img)
- lesson: string (associated lesson)
- section: string (associated section, optional)
- diagram_type: string (e.g., "architecture", "workflow", "pipeline")

**Relationships**:
- belongs to one Lesson
- optionally belongs to one Section

## Isaac Sim Environment Entity

**Fields**:
- id: string (unique identifier for the simulation environment)
- name: string (name of the simulation scene)
- description: string (brief description of the environment)
- scene_file_path: string (path to the Isaac Sim scene file)
- physics_engine: string (type of physics engine used)
- rendering_quality: string (quality level for rendering)
- gpu_requirements: string (GPU specifications required, e.g., "RTX 4090 or equivalent")
- created_at: datetime (timestamp when environment was created)

**Relationships**:
- belongs to one Isaac Sim Example
- connects to many Isaac ROS Pipelines

## Isaac ROS Pipeline Entity

**Fields**:
- id: string (unique identifier for the pipeline)
- name: string (name of the pipeline)
- description: string (description of the pipeline's purpose)
- ros_distribution: string (ROS 2 distribution, should be "Humble Hawksbill")
- sensor_nodes: array[string] (list of sensor nodes in the pipeline)
- control_nodes: array[string] (list of control nodes in the pipeline)
- perception_nodes: array[string] (list of perception nodes in the pipeline)
- connection_status: string (current status of the connection)
- created_at: datetime (timestamp when pipeline was created)

**Relationships**:
- connects to one Isaac Sim Environment
- connects to many VSLAM Systems

## VSLAM System Entity

**Fields**:
- id: string (unique identifier for the VSLAM system)
- name: string (name of the VSLAM system)
- description: string (description of the VSLAM implementation)
- algorithm_type: string (type of VSLAM algorithm used)
- camera_sensors: array[string] (list of camera sensors used for visual input)
- map_resolution: float (resolution of the generated map)
- localization_accuracy: float (accuracy of localization in meters)
- processing_rate: float (frames per second processed)
- map_file_path: string (path to the saved map file)
- created_at: datetime (timestamp when VSLAM system was created)

**Relationships**:
- belongs to one Isaac ROS Pipeline
- connects to one Perception Pipeline

## Nav2 Navigation Stack Entity

**Fields**:
- id: string (unique identifier for the navigation stack)
- name: string (name of the navigation stack configuration)
- description: string (description of the navigation setup)
- bipedal_plugin_enabled: boolean (whether custom bipedal plugin is active)
- costmap_params_path: string (path to costmap parameters file)
- planner_params_path: string (path to planner parameters file)
- controller_params_path: string (path to controller parameters file)
- current_goal: string (current navigation goal)
- navigation_status: string (current navigation status)
- path_execution_rate: float (rate of path execution in Hz)
- created_at: datetime (timestamp when navigation stack was created)

**Relationships**:
- connects to one Isaac ROS Pipeline
- connects to one Bipedal Path Planner

## Perception Pipeline Entity

**Fields**:
- id: string (unique identifier for the perception pipeline)
- name: string (name of the perception pipeline)
- description: string (description of the perception pipeline)
- sensor_inputs: array[string] (list of sensor inputs used)
- processing_modules: array[string] (list of processing modules in the pipeline)
- output_format: string (format of the perception output)
- processing_latency: float (latency in seconds)
- detection_accuracy: float (accuracy of object detection)
- created_at: datetime (timestamp when pipeline was created)

**Relationships**:
- connects to one Isaac ROS Pipeline
- connects to one Synthetic Data Generator

## Synthetic Data Generator Entity

**Fields**:
- id: string (unique identifier for the data generator)
- name: string (name of the data generation process)
- description: string (description of the data generation setup)
- source_environment: string (reference to Isaac Sim Environment)
- data_type: string (type of data being generated, e.g., "perception_training_data")
- output_directory: string (directory where generated data is stored)
- generation_rate: integer (samples per second)
- dataset_size: integer (total number of samples generated)
- data_format: string (format of the generated data)
- created_at: datetime (timestamp when generator was created)

**Relationships**:
- connects to one Perception Pipeline
- connects to one Interactive Tutorial Framework

## Bipedal Path Planner Entity

**Fields**:
- id: string (unique identifier for the path planner)
- name: string (name of the path planner)
- description: string (description of the path planning approach)
- footstep_planning_enabled: boolean (whether footstep planning is active)
- balance_constraints: object (constraints for maintaining balance)
- terrain_adaptation: boolean (whether terrain adaptation is enabled)
- planning_algorithm: string (algorithm used for path planning)
- max_step_width: float (maximum width of a step)
- max_step_height: float (maximum height of a step)
- created_at: datetime (timestamp when planner was created)

**Relationships**:
- connects to one Nav2 Navigation Stack

## Interactive Tutorial Framework Entity

**Fields**:
- id: string (unique identifier for the tutorial framework)
- name: string (name of the tutorial)
- description: string (description of the tutorial objectives)
- exercise_type: string (type of exercise, e.g., "scene_setup", "perception", "vslam", "navigation")
- validation_script_path: string (path to validation script)
- feedback_mechanism: string (type of feedback provided)
- student_progress: object (tracking student progress)
- completion_criteria: array[string] (criteria for completing the exercise)
- created_at: datetime (timestamp when tutorial was created)

**Relationships**:
- connects to one Synthetic Data Generator
- connects to many Isaac Sim Environments