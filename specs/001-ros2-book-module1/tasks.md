---
description: "Task list for Physical AI Book — Module 1: ROS 2"
---

# Tasks: Physical AI Book — Module 1: ROS 2

**Input**: Design documents from `/specs/001-ros2-book-module1/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/` or `book/` for this project
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create book directory structure per implementation plan
- [ ] T002 [P] Initialize Docusaurus v3 project with npm in book/ directory
- [ ] T003 [P] Configure package.json with project dependencies and scripts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Configure docusaurus.config.js with site metadata and basic settings
- [ ] T005 [P] Set up sidebars.js structure for module-1-ros2 with empty lessons
- [ ] T006 [P] Create module-1-ros2 directory in book/docs/
- [ ] T007 Set up static/img directory for diagrams and images
- [ ] T008 Create tools directory with content-validator.js, chunk-optimizer.js, and quality-checker.js
- [ ] T009 Configure GitHub Actions workflow for GitHub Pages deployment

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - ROS 2 Core Concepts Introduction (Priority: P1) 🎯 MVP

**Goal**: Students can read explanations of Nodes, Topics, and Services and explain these concepts in their own words with clear understanding of how they interact in a ROS 2 system

**Independent Test**: Students can read the Nodes, Topics, and Services lesson and explain these concepts with real-world examples

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T010 [P] [US1] Create content coherence test for lesson-1-nodes.md
- [ ] T011 [P] [US1] Create RAG chunk size validation test for lesson-1-nodes.md

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create lesson-1-nodes.md with ROS 2 Node concepts and explanations
- [ ] T013 [P] [US1] Create lesson-2-topics.md with ROS 2 Topic concepts and explanations
- [ ] T014 [P] [US1] Create lesson-3-services.md with ROS 2 Service concepts and explanations
- [ ] T015 [US1] Add official ROS 2 documentation citations to each lesson (FR-008)
- [ ] T016 [US1] Create simple diagrams for Nodes, Topics, and Services in static/img/ (FR-010)
- [ ] T017 [US1] Validate content chunks are 500-1200 characters for RAG optimization (FR-009)
- [ ] T018 [US1] Update sidebars.js to include the new lessons in correct order

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Code Implementation Examples (Priority: P2)

**Goal**: Students can run the provided code examples and observe the communication patterns between different ROS 2 components working correctly

**Independent Test**: Students can run the provided code examples and observe the communication patterns between different ROS 2 components working correctly

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T019 [P] [US2] Create runnable code validation test for publisher/subscriber examples
- [ ] T020 [P] [US2] Create code example integration test for client-service communication

### Implementation for User Story 2

- [ ] T021 [P] [US2] Create lesson-4-rclpy.md with Python (rclpy) publisher example code
- [ ] T022 [P] [US2] Create lesson-4-rclpy.md with Python (rclpy) subscriber example code
- [ ] T023 [P] [US2] Create lesson-4-rclpy.md with Python (rclpy) service example code
- [ ] T024 [US2] Add runnable Python code blocks with proper syntax highlighting to lesson-4-rclpy.md (FR-002)
- [ ] T025 [US2] Add explanations for each code example in lesson-4-rclpy.md
- [ ] T026 [US2] Create runnable code example files in book/static/code/ for students to download
- [ ] T027 [US2] Update lesson-4-rclpy.md to include instructions for running the examples
- [ ] T028 [US2] Add code example diagrams to static/img/ showing communication patterns

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Robot Controller Connection (Priority: P3)

**Goal**: Students can set up a basic connection between code and a simulated or real robot controller

**Independent Test**: Students can set up a basic connection between code and a simulated or real robot controller

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T029 [P] [US3] Create robot controller connection test for lesson-5-urdf.md
- [ ] T030 [P] [US3] Create humanoid robot description validation test

### Implementation for User Story 3

- [ ] T031 [P] [US3] Create lesson-5-urdf.md with robot description format structure and examples
- [ ] T032 [P] [US3] Create lesson-6-integration.md with software agent to robot controller connection examples
- [ ] T033 [US3] Add URDF code examples with proper structure to lesson-5-urdf.md (FR-004)
- [ ] T034 [US3] Add robot controller connection code examples to lesson-6-integration.md (FR-003)
- [ ] T035 [US3] Create diagrams for robot controller connection in static/img/
- [ ] T036 [US3] Add practical robot control examples that connect concepts from US1 and US2
- [ ] T037 [US3] Validate all content chunks are 500-1200 characters for RAG optimization (FR-009)
- [ ] T038 [US3] Update sidebars.js to include the new lessons in correct order

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T039 [P] Add consistent educational admonitions (tips, warnings, exercises) across all lessons
- [ ] T040 [P] Add accessibility alt text to all diagrams and images
- [ ] T041 Add cross-references between related concepts across lessons
- [ ] T042 [P] Run content coherence checks using tools/content-validator.js
- [ ] T043 [P] Run RAG chunk size optimization checks using tools/chunk-optimizer.js
- [ ] T044 Run all quality checks using tools/quality-checker.js
- [ ] T045 Update README.md with project overview and setup instructions
- [ ] T046 Validate complete build process with npm run build
- [ ] T047 Test deployment to GitHub Pages

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Content before examples
- Basic concepts before advanced integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Lessons within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all lessons for User Story 1 together:
Task: "Create lesson-1-nodes.md with ROS 2 Node concepts and explanations"
Task: "Create lesson-2-topics.md with ROS 2 Topic concepts and explanations"
Task: "Create lesson-3-services.md with ROS 2 Service concepts and explanations"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence