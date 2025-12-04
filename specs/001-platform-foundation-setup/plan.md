# Implementation Plan: Platform Foundation Setup

**Branch**: `001-platform-foundation-setup` | **Date**: 2025-12-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-platform-foundation-setup/spec.md`

## Summary

Initialize the project as a Docusaurus v3+ website with TypeScript, hosted on GitHub Pages via GitHub Actions. The project will be structured with the Docusaurus app in a `frontend/` directory. The default template will be cleaned up, `lucide-react` installed, and metadata configured for the "Physical AI & Humanoid Robotics Textbook".

## Technical Context

**Language/Version**: TypeScript 5.x / Node.js 20+ (LTS)
**Primary Dependencies**: Docusaurus v3+, React 18+, lucide-react
**Storage**: N/A (Static Site)
**Testing**: Jest (if needed for custom logic), GitHub Actions (CI)
**Target Platform**: GitHub Pages (Static Web Hosting)
**Project Type**: Web Application (Docusaurus Static Site Generator)
**Performance Goals**: Static load < 1s, Lighthouse Performance Score > 90
**Constraints**: Must use `frontend/` directory for Docusaurus root.
**Scale/Scope**: 3 Chapters (initially placeholders), extensible architecture.

## Critical Configuration

*   **Analytics (FR-007)**: `docusaurus.config.ts` MUST include the `google-gtag` plugin. We will use the **provided ID** (`trackingID: 'G-BZ53J6GGHN'`) for initialization. No API key is required at this stage.
*   **CI/CD Permissions**: The `.github/workflows/deploy.yml` file MUST explicitly define the following permissions to ensure successful deployment to GitHub Pages:
    ```yaml
    permissions:
      contents: read
      pages: write
      id-token: write
    ```

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **The Triad Architecture**: Not applicable to platform setup (infrastructure), but site structure supports it.
- [x] **Software-to-Hardware Causality**: Not applicable to platform setup.
- [x] **Tech Stack Isolation**:
    - ROS 2: N/A (Platform)
    - Gazebo/Unity: N/A (Platform)
    - NVIDIA Isaac: N/A (Platform)
    - *Exception*: Docusaurus is the mandated documentation framework per Constitution Global Constraints.
- [x] **Compute-Aware Deployment**: Not applicable to static site hosting.
- [x] **Global Constraints**:
    - Framework: Docusaurus (Correct)
    - Deployment: GitHub Pages (Correct)
    - Tech Stack: Verified Docusaurus v3+ (Correct)

## Project Structure

### Documentation (this feature)

```text
specs/001-platform-foundation-setup/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command) - N/A for infrastructure
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command) - N/A for infrastructure
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/                # Docusaurus Root
├── blog/                # (To be removed/cleaned)
├── docs/                # Content Root
│   ├── intro.md         # (Placeholder)
│   └── ...
├── src/
│   ├── components/      # Custom React Components
│   ├── css/             # Custom Styles
│   └── pages/           # Landing Page (index.tsx)
├── static/              # Static Assets (Images)
├── docusaurus.config.ts # Main Config
├── package.json
├── sidebars.ts
└── tsconfig.json

.github/
└── workflows/
    └── deploy.yml       # CI/CD Workflow
```

**Structure Decision**: Docusaurus project initialized in `frontend/` to keep root clean for future Python/ROS components, aligning with the Constitution's separation of concerns (though typically applying to logic, here applying to repo structure).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| `frontend/` subdirectory | Future Python/ROS backend separation | Root-level Docusaurus would clutter the repo when backend code is added later. |