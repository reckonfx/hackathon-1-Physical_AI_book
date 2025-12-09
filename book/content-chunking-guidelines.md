# Content Chunking Guidelines for RAG Optimization

## Purpose
This document outlines the guidelines for chunking content to optimize for Retrieval-Augmented Generation (RAG) systems. All content in the Physical AI Book must follow these guidelines to ensure effective retrieval and response generation.

## Chunk Size Requirements
- **Target range**: 500-1200 characters per chunk
- **Minimum**: 400 characters (to ensure semantic completeness)
- **Maximum**: 1300 characters (to avoid exceeding token limits)
- **Preferred**: 600-1000 characters for optimal balance

## Chunking Principles

### 1. Semantic Boundaries
Chunks should respect semantic boundaries:
- Complete paragraphs (when under 1200 characters)
- Complete sections or subsections
- Complete thought units
- Complete code examples with explanations

### 2. Context Preservation
Each chunk should be as self-contained as possible:
- Include necessary context within the chunk
- Avoid splitting related concepts across chunks
- Maintain topic coherence within each chunk

### 3. Retrieval Optimization
Structure chunks for effective retrieval:
- Start chunks with clear topic indicators
- Include relevant keywords naturally
- Maintain readability when retrieved independently

## Chunking Examples

### Good Chunking
```
# ROS 2 Action Servers

Action servers in ROS 2 provide a way to handle long-running tasks with feedback. Unlike services, which are synchronous and provide a single response, actions can run for extended periods and provide continuous feedback to the client. An action server implements the execution of action goals and provides feedback and result messages to the client.
```

### Poor Chunking
```
Action servers in ROS 2 provide a way to handle long-running tasks with feedback. Unlike services, which are synchronous and provide a single response, actions can run for extended periods
```

## Content Organization for Chunks
- Headings should be included with their associated content
- Code blocks should be complete with surrounding context
- Lists should be kept together when possible
- Tables should not be split across chunks

## Validation
Use the following command to validate chunk sizes:
```
# Example validation command
```

## Compliance
All content creators must verify that their content adheres to these guidelines before submission. Automated validation tools will check for compliance during the build process.