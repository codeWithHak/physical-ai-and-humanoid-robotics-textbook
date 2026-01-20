# Implementation Plan: Landing Page Complete Redesign

**Branch**: `014-landing-page-redesign` | **Date**: 2026-01-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/014-landing-page-redesign/spec.md`

## Summary

Implement 4 new landing page sections below the existing hero: "Your Journey" (chapter cards), "Why This Matters" (value proposition), "Hardware Tiers" (3 setup options), and "CTA with Footer". The implementation uses React components within Docusaurus, leveraging the existing design system (dark mode, lime green accent, Space Grotesk typography).

## Technical Context

**Language/Version**: TypeScript 5.6 / React 19.0
**Primary Dependencies**: Docusaurus 3.9.2, Infima CSS, lucide-react (icons), clsx
**Storage**: N/A (static content, chapter data from docs/ structure)
**Testing**: Manual visual testing, accessibility audit (Lighthouse/axe)
**Target Platform**: Web (modern browsers), deployed to Vercel
**Project Type**: Web application (Docusaurus static site)
**Performance Goals**: Page load < 3 seconds, LCP < 2.5s
**Constraints**: Must maintain existing design system, no JavaScript required for core content visibility
**Scale/Scope**: Single landing page, 4 new sections, ~5 new CSS module files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| The Triad Architecture | N/A | Landing page is informational UI, not robotics code |
| Software-to-Hardware Causality | N/A | No robot code involved |
| Tech Stack Isolation | PASS | Using approved stack: Docusaurus (framework per constitution) |
| Compute-Aware Deployment | N/A | Static frontend, no edge/workstation segregation needed |
| Framework Constraint | PASS | Docusaurus deployed to Vercel (matches constitution) |
| Documentation Quality | PASS | Will use Docusaurus features, maintain consistent styling |

**Gate Result**: PASS - No violations. Feature is purely frontend/informational.

## Project Structure

### Documentation (this feature)

```text
specs/014-landing-page-redesign/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (component props/data)
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── pages/
│   │   ├── index.tsx              # Landing page (MODIFY)
│   │   └── index.module.css       # Hero styles (MODIFY - add section styles)
│   ├── components/
│   │   └── Landing/               # NEW: Landing page sections
│   │       ├── JourneySection.tsx
│   │       ├── JourneySection.module.css
│   │       ├── WhySection.tsx
│   │       ├── WhySection.module.css
│   │       ├── HardwareTiers.tsx
│   │       ├── HardwareTiers.module.css
│   │       ├── CtaSection.tsx
│   │       ├── CtaSection.module.css
│   │       ├── Footer.tsx
│   │       └── Footer.module.css
│   └── css/
│       └── custom.css             # Global theme (MINOR updates if needed)
└── docs/
    ├── chapter-1/                 # Source for chapter data
    ├── chapter-2/
    └── chapter-3/
```

**Structure Decision**: Extend existing Docusaurus frontend structure. New landing page sections created as modular components in `src/components/Landing/` directory for reusability and maintainability.

## Complexity Tracking

No violations requiring justification. Implementation follows existing patterns.

## Design Decisions

### Component Architecture

Each landing page section is a standalone React component:
1. **JourneySection** - Displays 3 chapter cards with dynamic data from docs
2. **WhySection** - Static value proposition content
3. **HardwareTiers** - 3 tier cards with recommendation badge
4. **CtaSection** - Final CTA with button
5. **Footer** - Site-wide footer with links

### Styling Approach

- CSS Modules for component-scoped styles (`.module.css`)
- Extend existing design tokens from `custom.css`
- Grid-based layouts consistent with hero section
- Responsive breakpoint at 996px (Docusaurus default)

### Data Flow

- Chapter data: Import from sidebar configuration or hardcode initial 3 chapters
- Hardware tier data: Static JSON object within component
- Footer links: Props or static configuration

### Accessibility

- Semantic HTML (section, article, nav, footer)
- ARIA labels for interactive elements
- Keyboard navigable
- Color contrast compliant (existing palette passes WCAG AA)

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Chapter data structure changes | Low | Medium | Use abstraction layer for chapter retrieval |
| Style conflicts with Docusaurus updates | Low | Low | CSS Modules provide isolation |
| Mobile layout issues | Medium | Medium | Test on multiple viewport sizes early |

## Next Steps

1. **Phase 0**: Research existing component patterns, chapter data structure
2. **Phase 1**: Create data-model.md (component props), quickstart.md
3. **Phase 2**: Generate tasks.md with implementation steps (`/sp.tasks`)
