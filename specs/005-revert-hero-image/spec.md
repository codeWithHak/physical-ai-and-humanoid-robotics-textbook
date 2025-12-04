# Feature Specification: Revert Hero Image

**Feature Branch**: `005-revert-hero-image`  
**Created**: 2025-12-04  
**Status**: Draft  
**Input**: User description: "can we rewert back and use the image in hero section as we wer usig before"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Restoration of Static Hero Image (Priority: P1)

As a stakeholder, I want to revert the Landing Page hero visual from the `RobotBody` component back to the previous static SVG image (`undraw_docusaurus_mountain.svg`), so that the landing page matches the original simpler design.

**Why this priority**: Immediate visual regression requested by the user.

**Independent Test**: Verify that the `src/pages/index.tsx` file imports and uses the SVG image instead of the `RobotBody` component.

**Acceptance Scenarios**:

1. **Given** I load the homepage, **When** the Hero section renders, **Then** I see the `undraw_docusaurus_mountain.svg` image on the right side.
2. **Given** I inspect the DOM, **When** I check the visual container, **Then** the `<RobotBody />` component is NOT present.
3. **Given** the visual container, **When** I check its styling, **Then** the "glow" effects associated with the RobotBody are removed or adjusted to fit the SVG.

---

### User Story 2 - Code Cleanup (Priority: P2)

As a developer, I want the unused `RobotBody` component code to be preserved (optional) or cleanly removed from the active rendering path so the codebase remains maintainable.

**Why this priority**: Preventing dead code execution and bundle bloat.

**Independent Test**: Verify `RobotBody` is not imported in `index.tsx`.

**Acceptance Scenarios**:

1. **Given** `src/pages/index.tsx`, **When** I search for imports, **Then** `import RobotBody` is removed.

### Edge Cases

- **Styling Conflicts**: Ensure the `glowContainer` or other specific styles added for `RobotBody` do not break the rendering of the SVG image. The SVG might need the `diagramImage` class re-applied or adjusted.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST render the static image `img/undraw_docusaurus_mountain.svg` in the Hero section of the landing page.
- **FR-002**: The system MUST NOT render the `RobotBody` component on the landing page.
- **FR-003**: The visual layout (Text Left, Image Right) MUST be preserved.
- **FR-004**: The "Glow" effect container should be retained if it enhances the SVG, or removed if it was specific to the wireframe look (Assumption: Retain container for layout, replace content).

### Key Entities *(include if feature involves data)*

*None*

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **Visual Verification**: The homepage displays the "mountain" SVG instead of the wireframe robot.
- **SC-002**: **Build Success**: The application builds without errors after removing the component usage.