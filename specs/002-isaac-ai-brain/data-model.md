# Data Model: Module 3: The AI-Robot Brain (NVIDIA Isaac™)

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

**Relationships**:
- belongs to one Lesson
- optionally belongs to one Section

## Module Entity

**Fields**:
- id: string (unique identifier, e.g., "module-3-ai-robot-brain")
- title: string (module title)
- description: string (overview of the module)
- lesson_count: integer (number of lessons)
- estimated_duration: string (e.g., "6-8 hours")
- learning_outcomes: array of strings
- simulation_environments: array of strings (e.g., ["isaac-sim", "isaac-ros", "nav2"])

**Relationships**:
- contains many Lessons
- contains many Sections (through Lessons)
- contains many Isaac Sim Examples (through Lessons)