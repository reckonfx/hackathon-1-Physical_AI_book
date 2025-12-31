# Data Model: Modernize Docusaurus UI

## UI State Entities

### 1. Sidebar Item
- **Active State**: boolean (tracked by Docusaurus)
- **Hover State**: boolean (CSS `:hover`)
- **Visual Attributes**:
  - Background color (Active)
  - Text color (Active/Inactive)
  - Border left/radius
  - Transition speed (200ms)

### 2. Module Card
- **Content**: Title, Description, Link
- **Visual Attributes**:
  - Shadow (Idle)
  - Shadow (Hover - elevated)
  - Transform (Hover - translate up)
  - Padding (1.5rem)
  - Border-top color (Module-specific)

### 3. Chat Widget
- **Visibility**: Toggle state
- **Palette**:
  - Header background
  - Message bubble colors (User vs AI)
  - Send button state
- **Animations**:
  - Typing indicator
  - Fade-in/out for container
