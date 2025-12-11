<!--
Sync Impact Report:
Version change: 1.1.0 → 1.2.0
Added sections: Agent definitions, Service configurations, Skill definitions
Modified principles: None
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics — Spec-Driven Book + Embedded RAG Chatbot Constitution

## GitHub Configuration

Repository: https://github.com/reckonfx/hackathon-1-Physical_AI_book.git
Branch: main
Auto-commit: true
Commit message prefix: [Specskit]

## Core Principles

### Strict adherence to Spec-Kit Plus specifications
All development follows Spec-Kit Plus methodologies and templates; Every feature starts with a specification before implementation; Requirements traceability maintained from spec to code to tests

### Zero hallucination in technical content
All technical content must be grounded in official documentation; No fabricated or assumed information allowed; Citations and references required for all claims; RAG chatbot must answer ONLY from book content

### Clear, structured writing for RAG retrieval
Content optimized for vector search and retrieval; Chunk size maintained at 500-1200 characters; Well-structured headings and organization; Executable, verified code examples provided

### Robotics content tied to embodied intelligence
All robotics concepts connected to real-world behavior and physical embodiment; Focus on practical applications in ROS 2, Gazebo, Isaac, and VLA; Hands-on exercises and real-world examples prioritized

### Technical completeness across required stacks
Full coverage of mandatory technical areas: ROS 2, Gazebo & Unity, NVIDIA Isaac, VLA; All examples tested in real environments; Comprehensive documentation for each technology stack

### Reproducible and deployable workflows
Entire workflow must be reproducible via project README; GitHub Pages deployment functional; FastAPI endpoints pass basic functional tests; Build process succeeds with npm run build

## Project Agents

### BookChatAgent
Description: RAG agent to answer questions strictly from the book
Skills: AnswerBookQuestions, RespondCalmlyToNonBookQuestions
Services: rag_service, embedding_service, context7_service

### TranslatorAgent
Description: Translates book text into any language selected by the user
Skills: TranslateText, DetectLanguage
Services: translation_service, context7_service

## Project Skills

### AnswerBookQuestions
Description: Use RAG to answer questions based on the book

### RespondCalmlyToNonBookQuestions
Description: Respond politely to unrelated questions

### TranslateText
Description: Translate text from one language to another

### DetectLanguage
Description: Detect input language for translation

## Project Services

### rag_service
Type: vector_search
Description: Retrieve relevant content from Qdrant using embeddings
Configuration: qdrant_api_key, qdrant_url, embedding_model, llm_api_key, openai_agents_sdk

### embedding_service
Type: embedding
Description: Convert book text into embeddings for RAG
Configuration: model, api_key

### context7_service
Type: context_provider
Description: Retrieve additional context for enhanced responses

## Key Standards and Constraints

Book: Docusaurus v3, Structure: 4 Modules → Lessons → Sections, Full GitHub Pages deployment required
RAG Chatbot: Stack: FastAPI + OpenAI Agents/ChatKit + Neon + Qdrant, Must answer ONLY from book content, Must support "selected-text-only" answering, Must return source section for each answer
Content Requirements: 4–7 lessons per module, Clean code blocks (Python, ROS 2, etc.), Diagrams or architecture explanations, Tasks and hands-on exercises
Constraints: Book length: ~30,000 words, Chunk size for RAG: 500–1200 chars, Only open-source or AI-generated images, Must build with npm run build, Auto-deploy via GitHub Pages workflow, FastAPI endpoints must pass basic functional tests

## Development Workflow and Success Criteria

Development follows Spec-Kit Plus phases: spec → plan → tasks → implementation
Book fully covers the Physical AI roadmap (ROS2 → Gazebo → Isaac → VLA)
All examples run in real environments (ROS 2, Gazebo, Isaac Sim)
RAG chatbot retrieves accurate, citation-linked content
Answers are grounded strictly in book text
GitHub Pages site live and functional
Entire workflow reproducible via project README
All outputs follow Spec-Kit Plus rules and Claude Code operations

## Governance

Constitution supersedes all other practices and must be followed strictly
All implementations must comply with technical coverage requirements
Code reviews verify compliance with all principles and constraints
Amendments require documentation and justification

**Version**: 1.2.0 | **Ratified**: 2025-12-08 | **Last Amended**: 2025-12-10