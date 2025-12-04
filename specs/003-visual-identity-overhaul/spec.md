# Feature Specification: Visual Identity & Landing Page Overhaul

**Feature Branch**: `003-visual-identity-overhaul`  
**Created**: 2025-12-04  
**Status**: Draft  
**Input**: User description: "Feature: Visual Identity & Landing Page Overhaul Intent: Completely re-theme the Docusaurus application to match the "RoboLearn" dark aesthetic. REFERENCE IMAGE: See `specs/references/landing-ref.png` (or the uploaded `image_4b87dc.jpg`) for the exact layout structure. The implementation MUST mimic this visual hierarchy. Feature Scope (Design System): 1. Typography Engine: - Font Family: "Space Grotesk" (primary for Headings and Body). - H1 Weight: Black (900). - H2 Weight: Bold (700). - Button Weight: Semi-Bold (600). - Scaling Rule: Implement the "Divide by 2" method (H2 size = 50% of H1 size). - Letter Spacing: Tight tracking (-25/30 em units equivalent). - Settings: Headlines must be "Title Case". 2. Color Palette (Global CSS Overrides): - Primary/Glow/CTA: #BFE600 (Lime Green). - Background/Base: #000000 (Pure Black). - Text: #FFFFFF (White). - Dark Mode: Enforce Dark Mode by default. 3. Landing Page Architecture (`src/pages/index.tsx`): - Layout Reference: Strict adherence to @frontend/landing-page.png (Text Left, Diagram Right). - Hero Section: Left-aligned H1 and Subtext. - CTA: "Get Started" button (Solid #BFE600) and Secondary Button (Outline). - Visuals: Right-aligned Schematic Diagram with CSS glow effects. - Navbar: Transparent/black with #BFE600 hover states. Success Criteria (SMART): - Visual Fidelity: The rendered homepage visually matches @/frontend/landing-page.png structure. - Typography: CSS verifies font-family is set to 'Lufga' (or closest available match). - Color: Primary buttons use exactly #BFE600. - Responsiveness: Layout stacks vertically on mobile (Diagram moves below Text). Non-Goals: - NOT writing new chapter content. - NOT changing the structure of the docs sidebar. User Stories: - "As a visitor, I see a landing page that looks exactly like the 'RoboLearn' design mockup.""

## Clarifications

### Session 2025-12-04
- Q: How should the custom "Space Grotesk" font be integrated? → A: Configure fonts in `custom.css` (Google Fonts import) and `docusaurus.config.ts`.
- Q: How should the global color palette be implemented? → A: Override Infima CSS variables in `custom.css` :root.
- Q: How should the Navbar styling be implemented? → A: Pure CSS overrides in `custom.css`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visual Identity Experience (Priority: P1)

As a visitor, I want the website to match the "RoboLearn" dark aesthetic (Pure Black background, Lime Green accents, Lufga typography) so that I feel immersed in a modern, high-tech learning environment.

**Why this priority**: Establish the product brand and emotional connection immediately upon arrival.

**Independent Test**: Visual inspection of the homepage against the reference design specs. Verify background is #000000, primary color is #BFE600, and font family is 'Lufga'.

**Acceptance Scenarios**:

1. **Given** I land on the homepage, **When** I inspect the background color, **Then** it is #000000 (Pure Black) and Dark Mode is active by default.
2. **Given** I see a Heading 1, **When** I check the font properties, **Then** the font-family is "Space Grotesk" and weight is 900 (Black).
3. **Given** I see a Primary Button (CTA), **When** I verify the color, **Then** the background color is #BFE600 (Lime Green).

---

### User Story 2 - Responsive Landing Page Structure (Priority: P1)

As a user on any device, I want the landing page content to be readable and logically ordered, with the layout adapting from a side-by-side view on desktop to a vertical stack on mobile.

**Why this priority**: Ensures accessibility and usability across all device types.

**Independent Test**: Resize the browser window from desktop width to mobile width and observe the Hero section layout change.

**Acceptance Scenarios**:

1. **Given** I am on a desktop browser (>1024px), **When** I view the Hero section, **Then** the text is on the left and the diagram/visual is on the right.
2. **Given** I am on a mobile browser (<768px), **When** I view the Hero section, **Then** the text is stacked above the diagram/visual.
3. **Given** the Navbar, **When** I scroll or hover, **Then** the background is transparent/black and interaction states use the #BFE600 accent color.

### Edge Cases

- **Font Fallback**: If "Lufga" fails to load, the system should gracefully fallback to a modern sans-serif font (e.g., Inter, system-ui) without breaking layout.
- **Light Mode Toggle**: Since Dark Mode is "Enforced by default", ensuring the manual toggle (if present) doesn't break the specific "RoboLearn" aesthetic or color contrast (specifically white text on black background).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST enforce Dark Mode as the default and primary theme state.
- **FR-002**: Global CSS MUST be updated to use the defined Color Palette: Primary (#BFE600), Background (#000000), Text (#FFFFFF) by overriding Infima variables (e.g., `--ifm-color-primary`, `--ifm-background-color`) in `custom.css` `:root`.
- **FR-003**: The Typography Engine MUST be configured to use "Space Grotesk" as the primary font family for Headings and Body by importing it in `custom.css` (Google Fonts) and referencing it in `docusaurus.config.ts` (or CSS variables).
- **FR-004**: Heading levels MUST follow the specific weight and scaling rules: H1 (Black/900), H2 (Bold/700, 50% size of H1).
- **FR-005**: The Landing Page (`src/pages/index.tsx`) MUST be restructured to match the "Text Left, Diagram Right" layout on desktop.
- **FR-006**: The Hero Section MUST include a Primary CTA button ("Get Started", Solid #BFE600) and a Secondary Outline button.
- **FR-007**: The Navbar MUST be styled with a transparent/black background and #BFE600 hover effects using pure CSS overrides in `custom.css` (targeting `.navbar` classes).
- **FR-008**: CSS Glow effects MUST be implemented for the right-aligned visual/diagram element.

### Key Entities *(include if feature involves data)*

*None (Style and Layout only)*

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **Color Accuracy**: Computed style for primary buttons returns `rgb(191, 230, 0)` (equivalent to #BFE600).
- **SC-002**: **Font Verification**: Computed style for `h1` elements shows `font-family` containing 'Space Grotesk'.
- **SC-003**: **Responsiveness**: At viewport width 375px (mobile), the Hero Text element appears visually above the Hero Image element.
- **SC-004**: **Visual Fidelity**: The implemented layout matches the provided visual reference structure (Left-aligned text, Right-aligned image) on desktop viewports.