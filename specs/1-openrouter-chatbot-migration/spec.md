# Feature Specification: OpenRouter Chatbot Migration

**Feature Branch**: `1-openrouter-chatbot-migration`
**Created**: 2025-12-27
**Status**: Draft
**Input**: User description: "# sp.specify — Restore Chatbot Using OpenRouter (Minimal Change Policy)

## Context
The project contains an existing chatbot (RAG-based) that is currently failing with a generic error message (\"I encountered an error\").
The failure is due to an unpaid OpenAI API key.
The goal is to restore full chatbot functionality using **OpenRouter** instead of OpenAI, with **minimal or no changes to existing code** unless absolutely required.

The chatbot must:
- Answer user queries correctly
- Respond politely to greetings
- Stay focused on the book/domain
- Persist all chat-related data correctly in the database
- Avoid UI or widget regressions

---    ## Core Constraints (Must Follow)
1. **Do NOT refactor existing logic**
2. **Do NOT change file structure**
3. **Do NOT modify frontend code unless the backend cannot function otherwise**
4. **Reuse OpenAI-compatible SDKs if present**
5. **Only change configuration or initialization code if required**
6. **All existing database writes must continue to function**
7. **No mock responses or hardcoded fallbacks unless explicitly necessary for error handling**
8. **System must fail gracefully and log errors instead of returning generic UI messages**

---

## Required Outcome
- Chatbot works end-to-end using OpenRouter
- No breaking changes
- Existing RAG pipeline remains intact
- Database integrity is verified
- Errors are visible in logs, not hidden from developers

---   ## Step-by-Step Specification

### 1. LLM Provider Migration (Minimal Change)
- Replace OpenAI usage with **OpenRouter** by:
  - Keeping the same OpenAI-compatible client (if used)
  - Overriding ONLY:
    - `baseURL` → `https://openrouter.ai/api/v1`
    - `apiKey` → `process.env.OPENROUTER_API_KEY`
- Do NOT change function signatures or downstream calls.

Example (conceptual, not mandatory refactor):
- Same client
- Same method calls
- Same response handling

---

### 2. Model Selection
- Default model:
  - `meta-llama/llama-3-8b-instruct`
- Model must be configurable via environment variable:
  - `OPENROUTER_MODEL`
- No hardcoding unless config is missing.

---     ### 3. Environment Validation
- On backend startup:
  - Validate presence of `OPENROUTER_API_KEY`
  - Validate model name
- If missing:
  - Log a clear error
  - Do NOT crash the server
  - Return a developer-readable error message in API response

---

### 4. Error Handling Upgrade (No UI Change)
- Wrap chatbot execution in structured `try/catch`
- Log:
  - LLM provider errors
  - RAG retrieval errors
  - Database write failures
- Replace generic `\"I encountered an error\"` with:
  - A safe user-facing message
  - Full error logged server-side

---   ### 5. RAG Pipeline Preservation
- Keep:
  - Existing vector store
  - Existing embeddings
  - Existing retrieval logic
- Only ensure:
  - Retrieved context is passed to OpenRouter model
  - Prompt formatting remains unchanged unless required for compatibility

---

### 6. Database Verification (Mandatory)
- Verify the following data is being saved correctly:
  - User messages
  - Assistant responses
  - Timestamps
  - Conversation/session IDs
- Add verification steps:
  - Log successful DB writes
  - Log failed DB writes with reason
- Do NOT change schema unless corruption is detected.

---    ### 7. Polite & Focused Behavior Enforcement
System behavior must ensure:
- Greetings → polite response
- Off-topic questions → gentle redirection to book/domain
- No hallucinated system errors
- No API/provider mentions in user-facing responses

---

### 8. Verification Checklist (Must Be Executed)
Confirm:
- Backend starts without crashing
- Chat API returns HTTP 200
- OpenRouter request succeeds
- Model returns valid text
- RAG context is injected
- Data is written to database
- Chat widget receives responses correctly
- No frontend changes were required (unless justified)

---   ## Final Deliverable
Produce:
1. Minimal configuration/code changes (if any)
2. Confirmation that OpenRouter is active
3. Confirmation that database writes are successful
4. Summary of what was changed and why
5. List of files touched (should be minimal)

---

## Success Definition
The chatbot works exactly as before from a user perspective,
but now uses OpenRouter instead of OpenAI,
with verified persistence and proper error visibility."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Chat with Domain-Specific Content (Priority: P1)

User interacts with the chatbot to ask questions about the book/domain content and receives accurate, context-aware responses through the existing RAG system.

**Why this priority**: This is the core functionality that needs to be restored since the current chatbot is failing due to the OpenAI API key issue.

**Independent Test**: Can be fully tested by sending queries to the chatbot API endpoint and verifying that responses are generated using OpenRouter instead of OpenAI, while maintaining the same quality and context awareness as before.

**Acceptance Scenarios**:

1. **Given** user submits a query about book content, **When** chatbot processes the request, **Then** OpenRouter LLM generates a response based on retrieved RAG context
2. **Given** user sends a greeting message, **When** chatbot receives the message, **Then** chatbot responds politely and remains focused on book/domain content

---

### User Story 2 - Maintain Chat Session Persistence (Priority: P1)

User's conversation history with the chatbot is properly saved to the database and can be retrieved for continuity.

**Why this priority**: Database persistence is critical for maintaining conversation context and user experience as specified in requirements.

**Independent Test**: Can be tested by sending multiple messages in a conversation, verifying they are saved to the database, and checking that responses include proper timestamps and session IDs.

**Acceptance Scenarios**:

1. **Given** user sends a message to the chatbot, **When** response is generated, **Then** both user message and assistant response are saved to database with correct metadata
2. **Given** database write operation occurs, **When** write succeeds/fails, **Then** appropriate success/failure is logged for developer visibility

---

### User Story 3 - Graceful Error Handling (Priority: P2)

When errors occur in the system (LLM provider, RAG retrieval, database), they are properly logged while users receive appropriate messages.

**Why this priority**: Error handling is essential for system reliability and developer debugging as specified in the requirements.

**Independent Test**: Can be tested by simulating various failure scenarios (missing API keys, database errors) and verifying that errors are logged server-side while users receive safe, generic messages.

**Acceptance Scenarios**:

1. **Given** OpenRouter API call fails, **When** error occurs, **Then** error is logged server-side and user receives safe fallback message
2. **Given** RAG retrieval fails, **When** error occurs, **Then** error is logged and appropriate response is generated

---

### Edge Cases

- What happens when OPENROUTER_API_KEY is missing from environment?
- How does system handle OpenRouter rate limiting or service unavailability?
- What occurs when RAG context retrieval returns no relevant results?
- How does system behave when database write operations fail?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST connect to OpenRouter API at https://openrouter.ai/api/v1 using the OPENROUTER_API_KEY environment variable
- **FR-002**: System MUST use the meta-llama/llama-3-8b-instruct model as default or configurable model from OPENROUTER_MODEL environment variable
- **FR-003**: System MUST preserve existing RAG pipeline functionality and pass retrieved context to OpenRouter model
- **FR-004**: System MUST continue to save user messages, assistant responses, timestamps, and conversation IDs to the database
- **FR-005**: System MUST log all LLM provider errors, RAG retrieval errors, and database write failures for developer visibility
- **FR-006**: System MUST replace generic "I encountered an error" messages with safe user-facing messages while logging full errors server-side
- **FR-007**: System MUST validate presence of required environment variables on startup without crashing the server
- **FR-008**: System MUST maintain existing API endpoints and response formats to avoid breaking frontend functionality
- **FR-009**: System MUST continue to respond politely to greetings and redirect off-topic questions to book/domain content

### Key Entities *(include if feature involves data)*

- **User Message**: Text input from user with metadata including timestamp and conversation ID
- **Assistant Response**: Generated response from LLM with metadata including timestamp and associated user message ID
- **Conversation Session**: Collection of related user messages and assistant responses identified by session ID
- **RAG Context**: Retrieved book/domain-specific content used to inform the LLM response

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chatbot successfully processes user queries using OpenRouter instead of OpenAI with 95% response success rate
- **SC-002**: All user messages and assistant responses are persisted in the database with 100% success rate
- **SC-003**: System startup completes successfully when proper environment variables are configured, with clear error logging when variables are missing
- **SC-004**: Error scenarios are logged server-side with full context while users receive appropriate safe messages instead of generic errors
- **SC-005**: Existing frontend chat widget continues to function without modifications, receiving responses from the OpenRouter-powered backend