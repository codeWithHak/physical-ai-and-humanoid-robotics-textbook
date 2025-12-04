# Feature Specification: RobotBody Animation Component

**Feature Branch**: `004-robotbody-animation-component`  
**Created**: 2025-12-04  
**Status**: Draft  
**Input**: User description: "Feature: RobotBody Animation Component Intent: Create a custom React component (`RobotBody.tsx`) to replace the default `undraw_docusaurus_mountain.svg` on the landing page. This component visualizes the "Robotic Nervous System" using a CSS Grid humanoid layout with animated "energy pulses" representing data flow between the central compute (Torso) and peripherals (Limbs). Feature Scope (Component Architecture): 1. Structure (`RobotBody.tsx`): - A parent container holding 8 child "Card" divs arranged in a humanoid schematic: Head, Torso, Hips, L-Arm, R-Arm, L-Leg, R-Leg. - Semantic Mapping: * Head = "AI Brain (Isaac)" * Torso = "Compute (ROS 2)" * Limbs = "Actuators" 2. Layout & Styling: - Layout: Use CSS Grid to position parts with significant gutters (creating a "floating parts" aesthetic). - Theme: Background #000000 (Black), Text #FFFFFF (White). - Accents: Borders and Glows use #BFE600 (Neon Lime) to match the "Space Grotesk" design system. - Card Style: Minimalist, thin borders, tech-schematic look. 3. Animation Engine (Pure CSS): - Overlay: An absolute-positioned `<svg>` (z-index: 0) sitting behind the grid. - Connections: `<path>` lines connecting the "Torso" (Central Node) to all other body parts. - Flow Logic: CSS Keyframes animating `stroke-dashoffset` to create "Energy Pulses" (color #BFE600) moving outward from the Torso. - Constraint: NO external libraries (GSAP/Framer). Use pure CSS for performance. Success Criteria (SMART): - SSR Safety: The component must handle Server-Side Rendering without hydration mismatches (Docusaurus requirement). - Performance: Animation uses GPU-accelerated properties; no layout thrashing. - Visuals: Exact color match (#BFE600) for pulses and borders. - Responsiveness: The Grid scales down or stacks gracefully on mobile screens (energy lines hide or adjust). - Integration: Successfully imported and rendered in `src/pages/index.tsx` replacing the old SVG. Non-Goals: - NOT making the cards clickable/interactive yet. - NOT using 3D WebGL (keep it 2D CSS Grid for speed). User Stories: - "As a visitor, I see a pulsing schematic of a robot that visually explains how the 'Brain' connects to the 'Body', reinforcing the course theme.""

## Clarifications

### Session 2025-12-04
- Q: How should SSR hydration mismatches be handled for this dynamic component? → A: Wrap component in `<BrowserOnly>` or check `ExecutionEnvironment.canUseDOM`.
- Q: What specific CSS technique should define the "Pulse" animation? → A: `stroke-dashoffset` animation loop on dashed SVG paths.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visualizing the Robotic Nervous System (Priority: P1)

As a visitor, I see a pulsing schematic of a robot that visually explains how the 'Brain' connects to the 'Body', so I immediately grasp the course's focus on Physical AI and embodied intelligence.

**Why this priority**: This is the central visual metaphor for the entire textbook ("Partnership of People + AI + Robots"). It replaces the generic placeholder and establishes the product identity.

**Independent Test**: Verify that the component renders a humanoid shape with identifiable "Head" (AI), "Torso" (Compute), and "Limbs" (Actuators) connected by visible lines.

**Acceptance Scenarios**:

1. **Given** I load the landing page, **When** the hero section renders, **Then** I see a humanoid grid layout instead of the old SVG.
2. **Given** the RobotBody component, **When** I observe it for 5 seconds, **Then** I see animated green (#BFE600) pulses travelling from the central Torso to the peripheral limbs.
3. **Given** the component, **When** I inspect the DOM, **Then** it is composed of a CSS Grid container and an SVG overlay for lines (no Canvas/WebGL).

---

### User Story 2 - Responsive & Performant Design (Priority: P2)

As a user on a mobile device, I want the robotic diagram to scale down or rearrange gracefully without breaking the page layout or causing scroll lag.

**Why this priority**: The landing page must remain performant (Lighthouse > 90) and usable on all devices. Heavy JS animations could hurt SEO and UX.

**Independent Test**: Resize browser window and observe the component's behavior. Run a Lighthouse performance check.

**Acceptance Scenarios**:

1. **Given** I am on a mobile screen (<768px), **When** I view the hero section, **Then** the RobotBody scales down to fit within the container (or simplifies its layout) without horizontal scrollbars.
2. **Given** the animation is running, **When** I measure performance, **Then** there is no layout thrashing (animations use transform/opacity/stroke-dashoffset only).
3. **Given** I refresh the page, **When** the initial HTML loads, **Then** the component structure matches the client-rendered version (No SSR hydration errors).

### Edge Cases

- **Reduced Motion**: Users with `prefers-reduced-motion: reduce` should see a static version of the diagram without pulsing animations.
- **SSR Mismatch**: Since the SVG paths might need client-side dimensions, the component must handle the "loading" state gracefully or use percentages to avoid hydration errors (e.g., "Text content does not match server-rendered HTML").

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST render a custom React component `RobotBody` in the Hero section of the landing page, wrapped in Docusaurus `<BrowserOnly>` to prevent SSR hydration issues.
- **FR-002**: The component MUST use CSS Grid to arrange 8 div elements ("Cards") in a recognizable humanoid pattern (Head, Torso, Hips, Shoulders, Arms, Legs).
- **FR-003**: The visual theme MUST adhere to the design system: Black background (#000000), White text (#FFFFFF), and Neon Lime borders (#BFE600).
- **FR-004**: The system MUST display SVG connection lines behind the grid items, connecting the Torso (Central Node) to all other nodes.
- **FR-005**: The system MUST animate "energy pulses" along these connection lines using pure CSS animations that cycle the `stroke-dashoffset` of dashed SVG paths to simulate data flow.
- **FR-006**: The animation MUST respect `prefers-reduced-motion` media queries by disabling the pulse effect.
- **FR-007**: The component MUST NOT use external animation libraries (GSAP, Framer Motion) to minimize bundle size.
- **FR-008**: The component MUST be responsive, scaling down the grid gap and cell size on smaller viewports.

### Key Entities *(include if feature involves data)*

*None (Visual Component)*

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **Performance**: Lighthouse Performance score for the landing page remains >90 after adding the component.
- **SC-002**: **Bundle Size**: The JavaScript bundle size increase is negligible (< 5KB gzipped) since no libraries are added.
- **SC-003**: **Visual Accuracy**: The "Pulse" color matches the design token #BFE600 exactly.
- **SC-004**: **Stability**: No "Hydration failed" errors appear in the browser console during page load.