---
id: 1
title: openrouter-chatbot-migration-spec
stage: spec
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: openrouter-chatbot-migration
branch: 1-openrouter-chatbot-migration
user: claude-code
command: /sp.specify
labels: ["spec", "chatbot", "openrouter", "migration"]
links:
  spec: "specs/1-openrouter-chatbot-migration/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/1-openrouter-chatbot-migration/spec.md"
  - "specs/1-openrouter-chatbot-migration/checklists/requirements.md"
tests: []
---

# Prompt History Record: openrouter-chatbot-migration-spec

## User Input

```
# sp.specify — Restore Chatbot Using OpenRouter (Minimal Change Policy)

## Context
The project contains an existing chatbot (RAG-based) that is currently failing with a generic error message ("I encountered an error").
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
- Replace generic `"I encountered an error"` with:
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
with verified persistence and proper error visibility.
```

## Response Summary

Created a comprehensive feature specification for migrating the chatbot from OpenAI to OpenRouter. The specification includes:

- User scenarios with prioritized stories for core functionality
- Functional requirements that detail the system behavior
- Key entities involved in the chatbot system
- Measurable success criteria to validate the implementation

The spec ensures minimal code changes while preserving existing RAG pipeline, database persistence, and error handling capabilities. All requirements align with the core constraints of not refactoring existing logic and maintaining backward compatibility.

## Outcome

Successfully created feature specification document at specs/1-openrouter-chatbot-migration/spec.md with accompanying quality checklist.