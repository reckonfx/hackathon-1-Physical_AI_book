# Research: Physical AI Book — Module 1: ROS 2

## Decision: Docusaurus Structure and Versioning

**Rationale**: Docusaurus v3 was selected as the publishing framework based on the project constitution requirements and industry best practices for documentation sites. It provides excellent support for modular content organization, search functionality, and deployment to GitHub Pages.

**Alternatives considered**:
- GitBook: Less flexible for custom components and RAG optimization
- MkDocs: Good but lacks some advanced features of Docusaurus
- Custom static site generator: Would require more maintenance effort

## Decision: Sidebar Strategy

**Rationale**: Hierarchical sidebar structure (Module → Lessons → Sections) provides clear navigation and aligns with the educational progression from basic to advanced concepts. This structure also supports the 4-7 lessons requirement specified in the feature spec.

**Alternatives considered**:
- Flat sidebar: Would not provide clear learning progression
- Tab-based organization: Less suitable for educational content with sequential dependencies

## Decision: Markdown Conventions

**Rationale**: Standard Docusaurus Markdown with custom admonitions for educational content (tips, warnings, exercises) provides the best balance of readability and functionality. Code examples will use proper syntax highlighting with language identifiers.

**Alternatives considered**:
- RestructuredText: Not compatible with Docusaurus
- Asciidoc: Would require additional tooling

## Decision: Citation Style

**Rationale**: Inline citations with links to official ROS 2 documentation pages provide students with direct access to authoritative sources. Citations will be formatted as footnotes with numbered references in the text.

**Alternatives considered**:
- Bibliography section: Would require scrolling back and forth
- Parenthetical citations: Less discoverable for students

## Decision: Image/Diagram Handling

**Rationale**: All diagrams will be AI-generated or open-source to comply with the feature constraints. Diagrams will be stored in the static/img directory and referenced using standard Markdown syntax. Complex diagrams will include detailed alt text for accessibility.

**Alternatives considered**:
- Third-party diagrams: Would violate the open-source requirement
- Hand-drawn diagrams: Less professional appearance

## Decision: Publishing Workflow

**Rationale**: GitHub Pages deployment was chosen as it aligns with the project constitution requirements for reproducible workflows. The workflow will use GitHub Actions to automatically build and deploy the site when changes are pushed to the main branch.

**Alternatives considered**:
- Netlify/Vercel: Would add complexity to the workflow
- Manual deployment: Would not meet automation requirements