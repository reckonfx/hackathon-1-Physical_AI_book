# Implementation Plan: Modernize Docusaurus UI

**Branch**: `001-modernize-docusaurus-ui` | **Date**: 2025-12-31 | **Spec**: [specs/001-modernize-docusaurus-ui/spec.md](spec.md)
**Input**: Feature specification for UI modernization of the Physical AI book.

## Summary

This plan outlines the modernization of the Docusaurus-based "Physical AI" book UI. The focus is on enhancing the sidebar, homepage layout, typography, and chat widget styling using Infima CSS variables and custom components, while strictly avoiding backend or content changes.

## Technical Context

**Language/Version**: React 18, Docusaurus 3.1.0
**Primary Dependencies**: @docusaurus/preset-classic, prism-react-renderer, clsx
**Storage**: N/A (Frontend only)
**Testing**: manual verification, npm run build
**Target Platform**: GitHub Pages (reckonfx.github.io)
**Project Type**: Docusaurus Book (Web Application)
**Performance Goals**: Minimal Layout Shift (CLS < 0.1), Smooth transitions (< 200ms)
**Constraints**: Must not touch backend APIs, Must build with `npm run build`
**Scale/Scope**: ~30k words, 4 main modules, multiple lessons.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Strict adherence to Spec-Kit Plus**: All changes defined in this plan reflect requirements in `spec.md`. ✅
2. **Zero hallucination in technical content**: UX improvements do not alter technical info. ✅
3. **Reproducible and deployable workflows**: Changes tested to ensure `npm run build` succeeds. ✅
4. **Technical completeness across required stacks**: UI reflects the 4 modules (ROS2, Gazebo, Isaac, VLA). ✅

## Project Structure

### Documentation (this feature)

```text
specs/001-modernize-docusaurus-ui/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (UI state/props)
└── tasks.md             # Phase 2 output (generated via /sp.tasks)
```

### Source Code (repository root)

```text
book/
├── docusaurus.config.js       # Production config (themeConfig updates)
├── src/
│   ├── css/
│   │   └── custom.css         # Global Infima overrides & animations
│   ├── components/
│   │   ├── ChatWidget/        # UI/CSS modernization
│   │   ├── HomepageFeatures/  # Modern Card components
│   │   └── LayoutWrapper/     # Integration logic
│   └── theme/
│       └── Layout.js          # Swizzled layout for integration
```

**Structure Decision**: Using the existing Docusaurus structure. Enhancements will be centralized in `custom.css` and local component `module.css` files.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       | N/A        | N/A                                 |
