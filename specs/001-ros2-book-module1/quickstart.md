# Quickstart Guide: Physical AI Book — Module 1: ROS 2

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- ROS 2 development environment (Humble Hawksbill or later recommended)
- Python 3.8+ with rclpy
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
   touch docs/module-1-ros2/lesson-x-title.md
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

## Quality Checks

1. **Validate content coherence**
   ```bash
   node tools/content-validator.js
   ```

2. **Check RAG chunk sizes**
   ```bash
   node tools/chunk-optimizer.js
   ```

3. **Run all quality checks**
   ```bash
   node tools/quality-checker.js
   ```

## Building for Production

```bash
npm run build
```

This creates a `build/` directory with the static site ready for deployment.

## Deployment

The site is configured for GitHub Pages deployment. After pushing changes to the main branch, GitHub Actions will automatically build and deploy the site.