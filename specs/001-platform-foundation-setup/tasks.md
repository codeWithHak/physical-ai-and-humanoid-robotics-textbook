---
description: >
  Break down the plan into small, testable tasks for implementation.
  Each task must be an atomic step (setup -> config -> implementation -> verify).
---

# Checklist: Platform Foundation Setup

## Phase 1: Project Initialization & Configuration (Setup)
- [x] T001 Initialize Docusaurus project in `frontend/`
  - **Description**: Create a new Docusaurus v3 TypeScript project.
  - **Context**: We need a clean slate. The `frontend/` folder must be the root for the web app.
  - **Steps**:
    - Run `npx create-docusaurus@latest frontend classic --typescript` from repo root.
    - Verify `frontend/package.json` exists and contains `"docusaurus"`.
    - Verify `frontend/tsconfig.json` exists.
  - **Test**: `ls frontend/package.json` returns exit code 0.

- [x] T002 Install dependencies in `frontend/`
  - **Description**: Install `lucide-react` and `docusaurus-plugin-google-gtag` in `frontend/`.
  - **Context**: Required for icons (FR-005) and Analytics (FR-007).
  - **Steps**:
    - Run `cd frontend && npm install lucide-react @docusaurus/plugin-google-gtag`.
  - **Test**: `npm list lucide-react` inside `frontend/` returns valid tree.

- [x] T003 Configure Docusaurus Metadata in `frontend/docusaurus.config.ts`
  - **Description**: Update `docusaurus.config.ts` with project-specific metadata.
  - **Context**: Must match FR-002 (Title, Tagline, URL).
  - **Steps**:
    - Set `title` to "Physical AI & Humanoid Robotics Textbook".
    - Set `tagline` to "Mastering the Partnership of People + AI + Robots".
    - Set `url` to "https://codewithhak.github.io".
    - Set `baseUrl` to "/physical-ai-and-humanoid-robotics-textbook/".
    - Configure `organizationName: 'codeWithHak'` and `projectName: 'physical-ai-and-humanoid-robotics-textbook'`.
  - **Test**: `grep "Physical AI & Humanoid Robotics Textbook" frontend/docusaurus.config.ts` returns match.

- [x] T004 Configure Google Analytics in `frontend/docusaurus.config.ts`
  - **Description**: Add the gtag plugin to `docusaurus.config.ts`.
  - **Context**: FR-007 Requirement.
  - **Steps**:
    - Add the `gtag` preset to `docusaurus.config.ts`.
    - Use tracking ID: `G-BZ53J6GGHN`.
    - Set `anonymizeIP: true`.
  - **Test**: `grep "G-BZ53J6GGHN" frontend/docusaurus.config.ts` returns match.

## Phase 2: User Story 1 - Developer Automated Deployment (P1)
**Goal**: Enable automated deployment to GitHub Pages via GitHub Actions.

- [x] T005 [US1] Create GitHub Actions Workflow in `.github/workflows/deploy.yml`
  - **Description**: Create the deployment workflow file.
  - **Context**: FR-004. Automate deployment to GitHub Pages.
  - **Steps**:
    - Create `deploy.yml` with `on: push: branches: [main]`.
    - Configure `permissions` (contents: read, pages: write, id-token: write).
    - Configure steps: Checkout -> Setup Node -> Install -> Build -> Upload Pages Artifact -> Deploy to Pages.
    - Ensure `working-directory` is set to `./frontend` for build steps.
  - **Test**: `test -f .github/workflows/deploy.yml` returns 0.

- [x] T006 [US1] Verify Local Build
  - **Description**: Ensure the site builds locally without errors.
  - **Context**: SC-001. Prerequisite for deployment.
  - **Steps**:
    - Run `cd frontend && npm run build`.
  - **Test**: Build command exits with code 0 and `frontend/build` directory exists.

- [x] T007 [US1] Push and Verify Deployment
  - **Description**: Commit changes and verify GitHub Actions run.
  - **Context**: SC-003. Final verification of US1.
  - **Steps**:
    - Git add, commit, and push.
    - Check GitHub Actions tab for success.
  - **Test**: Manual verification of live URL (HTTP 200).

## Phase 3: User Story 2 - Reader Landing Page Access (P1)
**Goal**: Ensure the landing page reflects the correct branding and clean content.

- [x] T008 [US2] Remove Default Boilerplate in `frontend/`
  - **Description**: Clean up the "Tutorials" and "Blog" links and files.
  - **Context**: FR-003. We want a professional textbook look.
  - **Steps**:
    - Delete `frontend/blog/`.
    - Remove "blog" items from `frontend/docusaurus.config.ts` (navbar, footer, presets).
    - Remove "Tutorial" items from `frontend/docusaurus.config.ts` navbar.
  - **Test**: `ls frontend/blog` returns error (file not found).

- [x] T009 [US2] Update Landing Page Content in `frontend/src/pages/index.tsx`
  - **Description**: Create the "Coming Soon" landing page.
  - **Context**: FR-006.
  - **Steps**:
    - Modify `frontend/src/pages/index.tsx`.
    - Replace hero text with Course Title.
    - Add "Coming Soon" text.
  - **Test**: Grep "Coming Soon" in `frontend/src/pages/index.tsx`.

## Phase 4: Polish & Cross-Cutting Concerns
- [x] T010 Verify All Success Criteria
  - **Description**: Final manual check of all SCs.
  - **Steps**:
    - SC-001: Local Build.
    - SC-002: Deployment Availability.
    - SC-003: CI Reliability.
    - SC-004: Clean Slate.
    - SC-005: Tech Stack Verification.
    - SC-006: Traffic Metrics (check source code for tag).

## Dependencies
- **US1 (Deployment)** depends on **Phase 1 (Setup)**.
- **US2 (Branding)** depends on **Phase 1 (Setup)** but can be parallel with **US1**.

## Implementation Strategy
1. **MVP**: Complete Phase 1 (Setup) + US1 (Deployment). This gets a live site up.
2. **Refine**: Complete US2 (Branding) to make the live site look correct.