# Quickstart Guide: Module 3: The AI-Robot Brain (NVIDIA Isaac™)

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- NVIDIA Isaac Sim installed
- ROS 2 (Humble Hawksbill or later) installed
- Git for version control
- NVIDIA GPU with CUDA support (for optimal Isaac Sim performance)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to the book directory**
   ```bash
   cd book
   ```

3. **Install dependencies**
   ```bash
   npm install
   ```

4. **Start the development server**
   ```bash
   npm start
   ```
   This will start the Docusaurus development server at http://localhost:3000

## Content Creation Workflow

1. **Create a new lesson**
   ```bash
   # Create the lesson file in the appropriate module directory
   touch docs/module-3-ai-robot-brain/lesson-x-title.md
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
   Edit `sidebars.js` to include the new lesson in the navigation.

## Isaac Sim Environment Setup

### Isaac Sim Installation
1. Install NVIDIA Isaac Sim following official installation guide
2. Verify installation: Check Isaac Sim GUI launches without errors
3. Test with basic example: Run Isaac Sim sample scenes

### Isaac ROS Integration
1. Install Isaac ROS packages for your ROS 2 distribution
2. Verify ROS bridge: Test Isaac Sim to ROS 2 communication
3. Test perception pipelines: Validate camera and sensor data flow

## Quality Checks

1. **Validate content coherence**
   ```bash
   # Run content validation tools
   ```

2. **Check RAG chunk sizes**
   ```bash
   # Verify content chunks are 500-1200 characters
   ```

3. **Run all quality checks**
   ```bash
   # Execute comprehensive validation
   ```

## Building for Production

```bash
npm run build
```

This creates a `build/` directory with the static site ready for deployment.

## Deployment

The site is configured for GitHub Pages deployment. After pushing changes to the main branch, GitHub Actions will automatically build and deploy the site.