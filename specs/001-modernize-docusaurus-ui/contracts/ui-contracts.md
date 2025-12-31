# Contracts: Modernize Docusaurus UI

## Component Props (Visual)

### Module Card (Homepage)
```typescript
interface ModuleCardProps {
  title: string;
  description: string;
  link: string;
  moduleType: 'ros2' | 'gazebo' | 'isaac' | 'vla';
}
```

### Chat Widget (Theming)
```typescript
interface ChatThemeProps {
  primaryColor: string; // --ifm-color-primary
  bubbleRadius: string; // Default: '12px'
  animationSpeed: string; // Default: '0.2s'
}
```

## CSS Variable Contract (custom.css)

| Variable | Default Value | Usage |
|----------|---------------|-------|
| `--sidebar-hover-bg` | `rgba(0,0,0,0.05)` | Sidebar link hover |
| `--card-lift-transform` | `translateY(-4px)` | Homepage card animation |
| `--card-shadow-active` | `0 8px 24px rgba(0,0,0,0.15)` | Primary card hover |
| `--heading-font-weight` | `700` | Consistent header weight |
