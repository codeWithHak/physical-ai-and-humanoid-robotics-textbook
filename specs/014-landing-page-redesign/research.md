# Research: Landing Page Complete Redesign

**Feature**: 014-landing-page-redesign
**Date**: 2026-01-20
**Status**: Complete

## Research Questions

### 1. Existing Landing Page Structure

**Question**: How is the current landing page implemented?

**Findings**:
- **Location**: `frontend/src/pages/index.tsx`
- **Current Structure**: Single `HomepageHeader` component with hero section
- **Layout**: CSS Grid (2 columns on desktop, 1 on mobile)
- **Main content area**: Currently empty (`<main>` tag present but no content)

**Decision**: Add new sections inside `<main>` element below the hero
**Rationale**: Maintains separation of concerns; hero remains isolated

### 2. Design System Tokens

**Question**: What design tokens should be used for consistency?

**Findings** (from `frontend/src/css/custom.css`):
- **Primary Color**: `#BFE600` (lime green)
- **Background**: `#000000` (pure black)
- **Surface**: `#0a0a0a` (dark gray for cards)
- **Text**: `#FFFFFF` (white)
- **Muted Text**: `#a0a0a0`
- **Font Family**: Space Grotesk
- **Max Width**: `1200px` (container)
- **Responsive Breakpoint**: `996px`
- **Border Radius**: Cards use subtle rounding
- **Spacing**: `4rem` gap in hero grid

**Decision**: Reuse all existing tokens via CSS variables
**Rationale**: Visual consistency with existing hero section

### 3. Chapter Data Structure

**Question**: How to retrieve chapter titles and descriptions for "Your Journey" section?

**Findings**:
- Chapters located in `frontend/docs/chapter-{n}/`
- Each chapter has `_category_.json` with `label` and `position`
- Chapter sections have MDX frontmatter with `title` and `sidebar_position`
- Docusaurus sidebars.ts auto-generates from file structure

**Options Considered**:
1. Import sidebar config dynamically
2. Hardcode chapter data as static object
3. Use Docusaurus plugin API

**Decision**: Hardcode chapter data as static TypeScript object
**Rationale**:
- Simpler implementation
- Only 3 chapters needed (per constitution scope)
- Avoids runtime complexity
- Easy to update if chapters change

**Alternatives Rejected**:
- Dynamic import adds complexity for minimal benefit
- Plugin API overkill for static content

### 4. Component Organization

**Question**: How should new components be organized?

**Findings**:
- Existing components in `frontend/src/components/`
- Each component has `.tsx` + `.module.css` pair
- Some components grouped by feature (e.g., RagChat/)

**Decision**: Create `frontend/src/components/Landing/` directory with all section components
**Rationale**: Groups related components, follows existing pattern

### 5. Footer Implementation

**Question**: Should footer be part of landing page or site-wide?

**Findings**:
- Docusaurus has built-in footer in theme config
- Current config uses `footer: { style: 'dark', links: [], copyright: '...' }`
- Custom footer would require theme swizzling or component

**Options Considered**:
1. Use Docusaurus built-in footer (configure in docusaurus.config.ts)
2. Create custom Footer component for landing page only
3. Swizzle Docusaurus Footer theme component

**Decision**: Use Docusaurus built-in footer configuration
**Rationale**:
- Simpler implementation
- Automatic site-wide consistency
- Configuration in docusaurus.config.ts suffices for our needs
- Avoids maintaining custom footer component

**Implementation**: Update `docusaurus.config.ts` footer section with:
- Copyright notice
- GitHub link
- Social links (Twitter, LinkedIn)
- Contact email

### 6. Responsive Design Strategy

**Question**: How to handle mobile layouts?

**Findings**:
- Existing hero uses `@media screen and (max-width: 996px)`
- Grid switches from 2-column to 1-column
- Font sizes reduce on mobile
- Padding adjusts proportionally

**Decision**: Follow same breakpoint pattern for all new sections
**Rationale**: Consistency with existing responsive behavior

### 7. Icon Library

**Question**: What icons to use for visual elements?

**Findings**:
- `lucide-react` already installed (v0.555.0)
- Used in existing components (RagChat)

**Decision**: Use lucide-react icons
**Rationale**: Already in dependency tree, comprehensive icon set

### 8. Accessibility Requirements

**Question**: What accessibility patterns to follow?

**Findings**:
- SC-005 requires accessibility audit with no critical issues
- Existing site uses semantic HTML
- Color contrast meets WCAG AA (lime on black)

**Decision**: Implement with:
- Semantic HTML (`<section>`, `<article>`, `<nav>`, `<footer>`)
- ARIA labels on interactive elements
- Focus states for keyboard navigation
- Alt text for decorative elements (empty alt for decorative)

**Rationale**: Meets success criteria, follows web standards

## Research Summary

| Topic | Decision | Confidence |
|-------|----------|------------|
| Component location | `src/components/Landing/` | High |
| Styling approach | CSS Modules + existing tokens | High |
| Chapter data | Static TypeScript object | High |
| Footer | Docusaurus built-in config | High |
| Responsive breakpoint | 996px (existing) | High |
| Icons | lucide-react | High |
| Layout system | CSS Grid | High |

## Unknowns Resolved

All "NEEDS CLARIFICATION" items from Technical Context have been resolved:
- ~~Testing approach~~ → Manual visual + Lighthouse accessibility
- ~~Chapter data retrieval~~ → Static object
- ~~Footer implementation~~ → Docusaurus config

## Next Phase

Proceed to Phase 1: Generate data-model.md with component prop interfaces.
