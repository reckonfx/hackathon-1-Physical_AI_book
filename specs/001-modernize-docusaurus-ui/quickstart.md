# Quickstart: Modernize Docusaurus UI

## Development Setup

1. **Verify Dependencies**:
   ```bash
   cd book
   npm install
   ```

2. **Start Local Preview**:
   ```bash
   npm run start
   ```
   *Note: Ensure backend is running if testing ChatWidget AI responses, otherwise UI-only testing is sufficient.*

3. **Key Files to Monitor**:
   - `book/src/css/custom.css`: Global visual changes.
   - `book/src/pages/index.tsx`: Homepage layout changes.
   - `book/src/components/ChatWidget/ChatWidget.module.css`: Chat modernization.

## UI Verification Checklist

- [ ] Check Sidebar hover and active states.
- [ ] Verify homepage card animation on hover.
- [ ] Test dark mode transitions (all UI elements should adapt).
- [ ] Confirm mobile layout (sidebar collapsible, cards re-stack).
