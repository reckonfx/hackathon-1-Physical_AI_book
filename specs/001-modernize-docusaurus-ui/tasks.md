# Tasks: Modernize Docusaurus UI

**Input**: Design documents from `/specs/001-modernize-docusaurus-ui/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Manual visual verification is requested. Automated tests are not explicitly requested.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create modernization directory structure in book/src
- [x] T002 Verify local development environment with `npm install` in book/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Initialize global CSS variables for typography and spacing in book/src/css/custom.css
- [x] T004 [P] Setup dark mode variable overrides in book/src/css/custom.css
- [x] T005 [P] Implement global transition variables in book/src/css/custom.css

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 3 - Reading Content with Improved Typography (Priority: P1) 🎯 MVP

**Goal**: Update global typography and spacing for better readability.

**Independent Test**: Verify font sizes, line-heights, and heading hierarchy on documentation pages.

### Implementation for User Story 3

- [x] T006 [US3] Update `--ifm-font-family-base` and `--ifm-line-height-base` in book/src/css/custom.css
- [x] T007 [US3] Define clear visual hierarchy for H1-H6 headings in book/src/css/custom.css
- [x] T008 [US3] Optimize paragraph spacing and content container width in book/src/css/custom.css

**Checkpoint**: At this point, User Story 3 should be fully functional and testable independently.

---

## Phase 4: User Story 1 - Navigating Content with Modern Sidebar (Priority: P1)

**Goal**: Modernize the sidebar with better active states and hover effects.

**Independent Test**: Interact with the sidebar and verify smooth transitions and clear active page highlighting.

### Implementation for User Story 1

- [x] T009 [US1] Implement modern hover effects for `.menu__link` in book/src/css/custom.css
- [x] T010 [US1] Enhance active sidebar item highlighting using `--ifm-menu-color-active` in book/src/css/custom.css
- [x] T011 [US1] Adjust sidebar typography and nesting indentation in book/src/css/custom.css
- [x] T012 [US1] Verify mobile sidebar collapsible behavior and styling in book/src/css/custom.css

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 5: User Story 2 - Engaging with the Homepage via Modern Cards (Priority: P2)

**Goal**: Implement modern cards with hover animations on the homepage.

**Independent Test**: Navigate to the homepage and verify card layouts and "lift" animations on hover.

### Implementation for User Story 2

- [x] T013 [US2] Implement `.module-card` CSS class with shadows and transitions in book/src/css/custom.css
- [x] T014 [US2] Define card-specific module colors and gradients in book/src/css/custom.css
- [x] T015 [US2] Refactor homepage section layout to use cards in book/src/pages/index.tsx
- [x] T016 [US2] Add hover animation logic (transform/shadow) for cards in book/src/css/custom.css

**Checkpoint**: At this point, User Story 2 should be fully functional and testable independently.

---

## Phase 6: User Story 4 - Interacting with the Modernized Chat Widget (Priority: P3)

**Goal**: Modernize the chat widget UI components and animations.

**Independent Test**: Open the chat widget and verify updated colors, buttons, and smooth typing animations.

### Implementation for User Story 4

- [x] T017 [US4] Update chat container shadows and border-radius in book/src/components/ChatWidget/ChatWidget.module.css
- [x] T018 [US4] Modernize message bubble colors and typography in book/src/components/ChatWidget/ChatWidget.module.css
- [x] T019 [US4] Update chat trigger button and header styling in book/src/components/ChatWidget/ChatWidget.module.css
- [x] T020 [US4] Enhance typing indicator and message entry animations in book/src/components/ChatWidget/ChatWidget.module.css

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T021 Code cleanup and Infima variable consolidation in book/src/css/custom.css
- [x] T022 Final cross-browser and mobile responsiveness verification
- [x] T023 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - US3 and US1 (both P1) can proceed in parallel.
  - US2 and US4 follow afterward.

### Within Each User Story

- CSS variables before application to components.
- Global overrides before specific component modifications.

### Parallel Opportunities

- All Tasks marked [P] can run in parallel within their phase.
- User Story 3 and User Story 1 implementation tasks can run in parallel.
- Chat Widget modernization (different file) can run in parallel with Sidebar/Homepage work.

---

## Implementation Strategy

### MVP First (Typography & Sidebar)

1. Complete Phase 1 & 2 (Setup & Foundational).
2. Complete Phase 3 (US3 - Typography).
3. Complete Phase 4 (US1 - Sidebar).
4. **STOP and VALIDATE**: Test navigation and readability independently.

### Incremental Delivery

1. Add Phase 5 (US2 - Homepage Cards).
2. Add Phase 6 (US4 - Chat Widget).
3. Final Polish.
