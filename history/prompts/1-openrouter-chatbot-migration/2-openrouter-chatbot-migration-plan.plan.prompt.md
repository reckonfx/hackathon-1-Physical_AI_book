---
id: 2
title: openrouter-chatbot-migration-plan
stage: plan
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: openrouter-chatbot-migration
branch: 1-openrouter-chatbot-migration
user: claude-code
command: /sp.plan
labels: ["plan", "chatbot", "openrouter", "migration"]
links:
  spec: "specs/1-openrouter-chatbot-migration/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/1-openrouter-chatbot-migration/plan.md"
  - "specs/1-openrouter-chatbot-migration/research.md"
  - "specs/1-openrouter-chatbot-migration/data-model.md"
  - "specs/1-openrouter-chatbot-migration/quickstart.md"
  - "specs/1-openrouter-chatbot-migration/contracts/chat-api.yaml"
tests: []
---

# Prompt History Record: openrouter-chatbot-migration-plan

## User Input

```
# SP.PLAN — Implement OpenRouter for Existing Chatbot

## Goal
Restore chatbot functionality using **OpenRouter** instead of OpenAI, without unnecessary code changes, while ensuring all data is saved in the database and the RAG pipeline continues to work.

---

## Step 1: Prepare Environment

- [ ] Add OpenRouter API key to `.env`:
```env
OPENROUTER_API_KEY=or-xxxxxxxxxxxxxxxx
OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct

 Restart backend to load environment variables:

CTRL + C
npm run dev  # or npm start
 Verify key is loaded:

console.log("OpenRouter key loaded:", !!process.env.OPENROUTER_API_KEY);

Step 2: Update Backend for OpenRouter

 Replace OpenAI client initialization with OpenRouter-compatible configuration:

Change baseURL to https://openrouter.ai/api/v1

Use OPENROUTER_API_KEY from .env

 Keep all function calls, method signatures, and response handling unchanged

 Ensure model is configurable via OPENROUTER_MODEL

 Wrap all chat API logic in try/catch to log errors and prevent generic UI failures

Step 3: Verify RAG Pipeline Integrity

 Confirm existing embeddings and vector database are intact

 Do not re-ingest documents unless absolutely necessary

/?? Ensure retrieved context is passed to OpenRouter exactly as before

Step 4: Database Verification

 Monitor database for:

User messages

Assistant responses

Session/conversation IDs

Timestamps

 Log successful and failed writes

 Do not alter database schema unless corruption detected

Step 5: Test Chatbot Behavior

 Send greetings → verify polite response

 Ask book-related questions → verify accurate RAG responses

 Ask off-topic questions → verify polite redirection

 Verify no hallucinations or system/API errors are exposed to the user

Step 6: Backend & Frontend Integration Check

 Verify chat API returns HTTP 200

 Confirm chat widget displays responses correctly

 Ensure no frontend code changes were required

 Log any unexpected errors for debugging

Step 7: Error Handling & Logging

 All LLM errors logged to server console

 Generic UI error "I encountered an error" replaced with:

Safe, polite message

Server logs the actual error

 Optional: create a temporary console.log to verify responses during testing

Step 8: Completion Criteria

 Chatbot works end-to-end using OpenRouter

 Database writes are verified and intact

 RAG context still functioning correctly

 Minimal code/configuration changes

 Backend logs errors properly; no hidden failures

 Frontend chat widget works without changes

Step 9: Documentation

 List all files touched (should be minimal)

 Document any configuration changes (.env, model selection)

 Provide instructions for future key replacement or model updates

---

This version uses:

- `#` and `##` for headings
- `---` for section dividers
- `- [ ]` checkboxes for task tracking
- Proper code blocks for `.env` and JS commands
```

## Response Summary

Created a comprehensive implementation plan for migrating the chatbot from OpenAI to OpenRouter. The plan includes:

- Technical context and architecture analysis
- Research findings on OpenRouter compatibility
- Data model documentation
- Quickstart guide for implementation
- API contract documentation

The plan focuses on minimal code changes while preserving the existing RAG pipeline and API compatibility. Key findings include that OpenRouter is already configured in the .env file and that the system can leverage LangChain's OpenAI-compatible interface to work with OpenRouter.

## Outcome

Successfully created implementation plan artifacts including plan.md, research.md, data-model.md, quickstart.md, and API contracts in the specs/1-openrouter-chatbot-migration directory.