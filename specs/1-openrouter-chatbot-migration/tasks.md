---
description: "Task list for OpenRouter chatbot migration feature implementation"
---

# Tasks: OpenRouter Chatbot Migration

**Input**: Design documents from `/specs/1-openrouter-chatbot-migration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Paths shown below assume web application structure**

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Update environment configuration to use OpenRouter settings in backend/.env
- [X] T002 [P] Update config.py to support OpenRouter environment variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Configure OpenAI client to use OpenRouter endpoint in backend/services/ai_agent_rag_service.py
- [X] T004 [P] Update ChatOpenAI initialization to use OpenRouter configuration
- [X] T005 [P] Update OpenAIEmbeddings initialization to work with OpenRouter-compatible endpoint
- [X] T006 Update model configuration to use meta-llama/llama-3-8b-instruct as default
- [X] T007 Add environment validation for OpenRouter API key on startup
- [X] T008 Configure error handling for OpenRouter API calls

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Chat with Domain-Specific Content (Priority: P1) 🎯 MVP

**Goal**: User interacts with the chatbot to ask questions about the book/domain content and receives accurate, context-aware responses through the existing RAG system using OpenRouter

**Independent Test**: Can be fully tested by sending queries to the chatbot API endpoint and verifying that responses are generated using OpenRouter instead of OpenAI, while maintaining the same quality and context awareness as before.

### Implementation for User Story 1

- [X] T009 [P] [US1] Update AIAgentRAGService to initialize with OpenRouter-compatible ChatOpenAI in backend/services/ai_agent_rag_service.py
- [X] T010 [P] [US1] Update AIAgentRAGService to use OpenRouter-compatible embeddings in backend/services/ai_agent_rag_service.py
- [X] T011 [US1] Test RAG functionality with OpenRouter model to ensure context is passed correctly in backend/services/ai_agent_rag_service.py
- [X] T012 [US1] Verify greeting responses work properly with OpenRouter model
- [X] T013 [US1] Test domain-specific queries to ensure RAG context is properly injected with OpenRouter

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Maintain Chat Session Persistence (Priority: P1)

**Goal**: User's conversation history with the chatbot is properly handled (noting that the system uses FAISS for RAG but doesn't have traditional database persistence for chat history)

**Independent Test**: Can be tested by verifying the system maintains conversation context through the RAG process and that responses are generated appropriately.

### Implementation for User Story 2

- [X] T014 [P] [US2] Verify FAISS vector store functionality remains intact with OpenRouter in backend/services/ai_agent_rag_service.py
- [X] T015 [US2] Test document loading and retrieval remains functional with OpenRouter integration
- [X] T016 [US2] Confirm similarity search functionality works with OpenRouter configuration
- [X] T017 [US2] Validate that retrieved context is properly formatted for OpenRouter model consumption

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Graceful Error Handling (Priority: P2)

**Goal**: When errors occur in the system (LLM provider, RAG retrieval), they are properly logged while users receive appropriate messages

**Independent Test**: Can be tested by simulating various failure scenarios (missing API keys, invalid requests) and verifying that errors are logged server-side while users receive safe, generic messages.

### Implementation for User Story 3

- [X] T018 [P] [US3] Update error handling in chat endpoint to log OpenRouter-specific errors in backend/api/v1/chat_router.py
- [X] T019 [P] [US3] Update error handling in AIAgentRAGService for OpenRouter API failures in backend/services/ai_agent_rag_service.py
- [X] T020 [US3] Replace generic "I encountered an error" messages with proper error handling
- [X] T021 [US3] Add specific logging for OpenRouter API errors vs other system errors
- [X] T022 [US3] Test error scenarios with invalid OpenRouter API key configuration

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T023 [P] Update API configuration to reflect OpenRouter usage in backend/config.py
- [X] T024 Update documentation to reflect OpenRouter implementation
- [X] T025 Test complete end-to-end flow with OpenRouter
- [X] T026 [P] Verify frontend chat widget compatibility with OpenRouter responses
- [X] T027 Run quickstart validation to confirm all functionality works
- [X] T028 Update model selection to be configurable via OPENROUTER_MODEL environment variable

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

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Update AIAgentRAGService to initialize with OpenRouter-compatible ChatOpenAI in backend/services/ai_agent_rag_service.py"
Task: "Update AIAgentRAGService to use OpenRouter-compatible embeddings in backend/services/ai_agent_rag_service.py"
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
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence