---
description: >
  Break down the plan into small, testable tasks for implementation.
  Each task must be an atomic step (setup -> config -> implementation -> verify).
---

# Checklist: Visual Identity & Landing Page Overhaul

## Phase 1: Setup & Typography Engine
- [x] T001 Configure Google Fonts (Space Grotesk)
  - **Description**: Import Space Grotesk from Google Fonts in `custom.css`.
  - **Context**: Prerequisites for FR-003.
  - **Steps**:
    - Edit `frontend/src/css/custom.css`.
    - Add `@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');`.
  - **Test**: `grep "Space Grotesk" frontend/src/css/custom.css` returns match.

- [x] T002 [US1] Implement Typography Engine in `custom.css`
  - **Description**: Configure global font variables and scaling.
  - **Context**: FR-003, FR-004.
  - **Steps**:
    - Edit `frontend/src/css/custom.css`.
    - Override `--ifm-font-family-base` and `--ifm-heading-font-family` to 'Space Grotesk', sans-serif.
    - Set H1 (900), H2 (700) weights.
    - Implement scaling rule: `h2 { font-size: 2rem; }` (relative to base).
  - **Test**: `grep "Space Grotesk" frontend/src/css/custom.css` returns match.

## Phase 2: User Story 1 - Visual Identity Experience (P1)
**Goal**: Enforce the "RoboLearn" dark aesthetic (Colors + Dark Mode).

- [x] T003 [US1] Enforce Dark Mode in `docusaurus.config.ts`
  - **Description**: Set default color mode to dark and disable switch (optional, but enforce default).
  - **Context**: FR-001.
  - **Steps**:
    - Edit `frontend/docusaurus.config.ts`.
    - Set `colorMode: { defaultMode: 'dark', disableSwitch: false, respectPrefersColorScheme: false }`.
  - **Test**: grep `defaultMode: 'dark'` in config.

- [x] T004 [US1] Implement Global Color Palette in `custom.css`
  - **Description**: Override Infima CSS variables for the new palette.
  - **Context**: FR-002.
  - **Steps**:
    - Override `--ifm-color-primary` variants to `#BFE600` shades.
    - Set `--ifm-background-color` to `#000000`.
    - Set `--ifm-font-color-base` to `#FFFFFF`.
  - **Test**: grep `#BFE600` and `#000000` in `custom.css`.

- [x] T005 [US1] Style Navbar (Transparent/Black)
  - **Description**: CSS overrides for Navbar transparency and hover states.
  - **Context**: FR-007.
  - **Steps**:
    - Target `.navbar` in `custom.css`.
    - Set background to `transparent` or `rgba(0,0,0,0.8)`.
    - Style `.navbar__link:hover` with color `#BFE600`.
  - **Test**: grep `.navbar` in `custom.css`.

## Phase 3: User Story 2 - Responsive Landing Page Structure (P1)
**Goal**: Rebuild the homepage layout to match the reference design.

- [x] T006 [US2] Restructure `src/pages/index.tsx` Layout
  - **Description**: Update the React component structure.
  - **Context**: FR-005, SC-004.
  - **Steps**:
    - Create a two-column layout container (Grid/Flex).
    - Left Column: Heading, Subtext, CTA Buttons.
    - Right Column: Visual/Diagram placeholder.
  - **Test**: Check `index.tsx` for the new grid structure.

- [x] T007 [US2] Implement Hero Styling in `index.module.css`
  - **Description**: Apply specific styles for the Hero section (Left-align, Spacing).
  - **Context**: FR-006 (Buttons), FR-008 (Glow).
  - **Steps**:
    - Add `.heroContainer`, `.heroText`, `.heroVisual` classes.
    - Implement `#BFE600` Glow effect for the visual container.
    - Style primary button (Solid #BFE600) and secondary button (Outline).
  - **Test**: grep `box-shadow` or `filter: drop-shadow` in `index.module.css`.

- [x] T008 [US2] Ensure Mobile Responsiveness
  - **Description**: Add Media Queries for stacking order.
  - **Context**: SC-003.
  - **Steps**:
    - In `index.module.css`, add `@media (max-width: 996px)`.
    - Change flex-direction to column (or column-reverse if needed).
  - **Test**: grep `@media` in `index.module.css`.

## Phase 4: Polish & Verification
- [x] T009 Verify Visual Success Criteria
  - **Description**: Final check of fonts, colors, and layout.
  - **Steps**:
    - Check SC-001 (Color Accuracy).
    - Check SC-002 (Font Verification).
    - Check SC-003 (Responsiveness).

## Phase 5: Fixes (Added)
- [x] T010 Fix `window.gtag` Runtime Error
  - **Description**: Analytics plugin is firing before window load or in dev mode where it might not be initialized.
  - **Step**: Add defensive check or disable gtag in dev if possible, or ensure it loads. Actually, this usually happens if the plugin is configured but ad-blocker blocks it or env is weird. We will wrap it.
  - **Test**: Click button without error.

- [x] T011 Fix Broken Link `/docs/00-preface`
  - **Description**: The file `00-preface.md` exists but Docusaurus routing might be different (e.g., slug is `/` or it's effectively the index of docs).
  - **Step**: Check `frontend/docs/00-preface.md` frontmatter. It has `slug: /`. This conflicts with the homepage `/`.
  - **Fix**: Change `00-preface.md` slug to `/preface` or remove slug to let it use filename.
  - **Test**: Link works.

- [x] T012 Style Footer
  - **Description**: Match footer to dark theme.
  - **Step**: Override footer CSS variables or style `custom.css`.
  - **Test**: Footer is black with correct link colors.

- [x] T013 Fix Layout & Gtag (Final Polish)
  - **Description**: Reduce hero top padding and shim window.gtag.
  - **Step**: Update `index.module.css` (4rem padding) and add `clientModule.js` shim.
  - **Test**: Visual check + no console errors.