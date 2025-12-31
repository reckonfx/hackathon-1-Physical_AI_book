# Research: Modernize Docusaurus UI

## Decisions & Rationale

### 1. Sidebar Modernization
- **Decision**: Use Infima CSS variables and global CSS overrides in `custom.css` to enhance the sidebar.
- **Rationale**: Docusaurus sidebar is built on Infima. Overriding `--ifm-menu-color-active` and adding transition effects to `.menu__link` is the cleanest way to modernize without a full swizzle.
- **Alternatives**: Swizzling the `DocSidebar` component.
- **Rejected Because**: Unnecessarily complex and harder to maintain across Docusaurus updates.

### 2. Homepage Section Cards
- **Decision**: Enhance `index.tsx` by wrapping module links in a consistent `.module-card` class and adding hover animations.
- **Rationale**: The current homepage uses simple columns. CSS-based cards with `box-shadow` and `transform: translateY` transitions provide a modern "lift" effect.
- **Alternatives**: Using a third-party UI library like Material UI.
- **Rejected Because**: Increases bundle size and contradicts the goal of using the native Docusaurus/Infima framework.

### 3. Typography Adjustments
- **Decision**: Update `--ifm-font-family-base` and heading weight/size variables in `:root`.
- **Rationale**: Clean typography is the baseline for modern UI. Adjusting `--ifm-line-height-base` to 1.6 improves readability for long-form content.

### 4. Chat Widget restyling
- **Decision**: Update `ChatWidget.module.css` with a more defined color palette and rounded corners.
- **Rationale**: The current chat widget is functional but slightly generic. Improving the shadow depth and adding subtle transitions to the toggle button aligns it with the modern theme.

## Docusaurus Best Practices
- **Prefer CSS Variables**: Always use Infima variables (`--ifm-*`) to ensure dark mode compatibility.
- **Component Localization**: Keep component-specific styles in `.module.css` files.
- **Minimal Swizzling**: Only swizzle components if CSS-only overrides are insufficient.
