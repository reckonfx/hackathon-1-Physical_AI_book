---
id: 1
title: Update-project-constitution-for-Physical-AI-Robotics
stage: constitution
date: 2025-12-08
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: AKE
command: /sp.constitution
labels: [constitution, project-setup, spec-driven-development]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Project:
 Physical AI & Humanoid Robotics — Spec-Driven Book + Embedded RAG Chatbot
 Built using Spec-Kit Plus, Claude Code, Docusaurus, GitHub Pages, FastAPI, OpenAI Agents/ChatKit, Neon Postgres, and Qdrant Cloud.

Core Principles
Strict adherence to Spec-Kit Plus specifications.


Zero hallucination: all technical content grounded in official docs.


Clear, structured writing optimized for RAG retrieval.


Executable, verified code examples.


Robotics content tied to embodied intelligence and real-world behavior.



Key Standards
Book:


Docusaurus v3


Structure: 4 Modules → Lessons → Sections


Full GitHub Pages deployment required


RAG Chatbot:


Stack: FastAPI + OpenAI Agents/ChatKit + Neon + Qdrant


Must answer ONLY from book content


Must support "selected-text-only" answering


Must return source section for each answer


Technical Coverage (Mandatory):


ROS 2 (nodes, topics, services, rclpy, URDF)


Gazebo & Unity (physics, sensors, digital twins)


NVIDIA Isaac (Isaac Sim, Isaac ROS, VSLAM, Nav2)


VLA (Whisper, LLM planning, cognitive robotics, final project)


Content Requirements:


4–7 lessons per module


Clean code blocks (Python, ROS 2, etc.)


Diagrams or architecture explanations


Tasks and hands-on exercises



Constraints
Book length: ~30,000 words


Chunk size for RAG: 500–1200 chars


Only open-source or AI-generated images


Must build with npm run build


Auto-deploy via GitHub Pages workflow


FastAPI endpoints must pass basic functional tests



Success Criteria
Book fully covers the Physical AI roadmap (ROS2 → Gazebo → Isaac → VLA).


All examples run in real environments (ROS 2, Gazebo, Isaac Sim).


RAG chatbot retrieves accurate, citation-linked content.


Answers are grounded strictly in book text.


GitHub Pages site live and functional.


Entire workflow reproducible via project README.


All outputs follow Spec-Kit Plus rules and Claude Code operations.

## Response snapshot

Created a comprehensive constitution for the Physical AI & Humanoid Robotics project that incorporates all specified principles and requirements. The constitution includes:

- Core principles: Spec-Kit Plus adherence, zero hallucination, clear structured writing, embodied intelligence focus, technical completeness, and reproducible workflows
- Key Standards and Constraints section with all specified requirements
- Development Workflow and Success Criteria section
- Governance section with compliance rules
- Sync Impact Report tracking the changes made

## Outcome

- ✅ Impact: Project constitution fully updated with all specified principles and requirements
- 🧪 Tests: No tests required for constitution update
- 📁 Files: Updated .specify/memory/constitution.md with comprehensive project constitution
- 🔁 Next prompts: User can proceed with feature specification using /sp.specify
- 🧠 Reflection: Constitution properly reflects all project requirements and can guide future development

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All principles properly incorporated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on constitution