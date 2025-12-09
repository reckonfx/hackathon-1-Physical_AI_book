# Quickstart Guide: Module 2: The Digital Twin (Gazebo & Unity)

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Gazebo (Fortress or Harmonic) installed
- Unity (2022.3 LTS or later) installed
- Git for version control

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
   touch docs/module-2-digital-twin/lesson-x-title.md
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

## Simulation Environment Setup

### Gazebo Setup
1. Install Gazebo Fortress or Harmonic following official installation guide
2. Verify installation: `gz --version` or `gazebo --version`
3. Test with basic example: `gz sim shapes.sdf`

### Unity Setup
1. Install Unity Hub and Unity 2022.3 LTS
2. Create a new 3D project for simulation examples
3. Import required packages for robotics simulation

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