# Tasks: Landing Page Complete Redesign

**Input**: Design documents from `/specs/014-landing-page-redesign/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: No automated tests requested. Manual visual testing and Lighthouse accessibility audit specified.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/src/` (Docusaurus structure)
- Components: `frontend/src/components/Landing/`
- Pages: `frontend/src/pages/`
- Config: `frontend/docusaurus.config.ts`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create component directory structure and data files

- [x] T001 Create Landing component directory at frontend/src/components/Landing/
- [x] T002 Create data subdirectory at frontend/src/components/Landing/data/
- [x] T003 [P] Create ChapterCard interface and CHAPTERS data in frontend/src/components/Landing/data/chapters.ts
- [x] T004 [P] Create HardwareTier interface and HARDWARE_TIERS data in frontend/src/components/Landing/data/tiers.ts
- [x] T005 [P] Create barrel export file at frontend/src/components/Landing/index.ts

**Checkpoint**: Directory structure and data files ready for component development

---

## Phase 2: Foundational (Shared Components)

**Purpose**: Create section CSS base patterns that will be reused across components

**⚠️ CRITICAL**: This phase establishes shared styling patterns; complete before story-specific components

- [x] T006 Add shared section CSS variables to frontend/src/css/custom.css (section padding, container max-width, headline styles)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - First-Time Visitor Discovery (Priority: P1) 🎯 MVP

**Goal**: Visitors see a compelling narrative with hero, journey, and value proposition sections

**Independent Test**: Visit landing page, scroll through all sections, verify content hierarchy renders correctly

### Implementation for User Story 1

- [x] T007 [P] [US1] Create JourneySection component in frontend/src/components/Landing/JourneySection.tsx
- [x] T008 [P] [US1] Create JourneySection styles in frontend/src/components/Landing/JourneySection.module.css
- [x] T009 [P] [US1] Create WhySection component in frontend/src/components/Landing/WhySection.tsx
- [x] T010 [P] [US1] Create WhySection styles in frontend/src/components/Landing/WhySection.module.css
- [x] T011 [US1] Import and render JourneySection in frontend/src/pages/index.tsx
- [x] T012 [US1] Import and render WhySection in frontend/src/pages/index.tsx
- [x] T013 [US1] Add responsive styles for mobile breakpoint (996px) in JourneySection.module.css
- [x] T014 [US1] Add responsive styles for mobile breakpoint (996px) in WhySection.module.css
- [x] T015 [US1] Visual verification: Scroll through hero, journey, why sections on desktop and mobile

**Checkpoint**: User Story 1 complete - visitors can see hero + Your Journey + Why This Matters sections

---

## Phase 4: User Story 2 - Hardware Decision Path (Priority: P2)

**Goal**: Visitors see 3 hardware tier options with clear requirements and costs

**Independent Test**: View Hardware Tiers section, verify all 3 tiers display with correct information

### Implementation for User Story 2

- [x] T016 [P] [US2] Create HardwareTiers component in frontend/src/components/Landing/HardwareTiers.tsx
- [x] T017 [P] [US2] Create HardwareTiers styles in frontend/src/components/Landing/HardwareTiers.module.css
- [x] T018 [US2] Add "Recommended" badge styling for Cloud + Edge tier in HardwareTiers.module.css
- [x] T019 [US2] Import and render HardwareTiers in frontend/src/pages/index.tsx
- [x] T020 [US2] Add responsive grid layout for tier cards (3-col desktop, 1-col mobile) in HardwareTiers.module.css
- [x] T021 [US2] Visual verification: Verify all 3 tiers display with costs, requirements, and recommendation badge

**Checkpoint**: User Story 2 complete - visitors can compare hardware options

---

## Phase 5: User Story 3 - Call-to-Action Conversion (Priority: P2)

**Goal**: Visitors have a clear path to start learning via CTA button and footer links

**Independent Test**: Click "Get Started Free" button, verify navigation to /docs/preface; verify footer links work

### Implementation for User Story 3

- [x] T022 [P] [US3] Create CtaSection component in frontend/src/components/Landing/CtaSection.tsx
- [x] T023 [P] [US3] Create CtaSection styles in frontend/src/components/Landing/CtaSection.module.css
- [x] T024 [US3] Import and render CtaSection in frontend/src/pages/index.tsx
- [x] T025 [US3] Add "Get Started Free" button with href="/docs/preface" in CtaSection.tsx
- [x] T026 [US3] Update footer configuration in frontend/docusaurus.config.ts with Learn, Community, Contact links
- [x] T027 [US3] Add responsive styles for CTA section (mobile) in CtaSection.module.css
- [x] T028 [US3] Visual verification: Click CTA button, verify navigation; check footer links

**Checkpoint**: User Story 3 complete - visitors can navigate to content via CTA and footer

---

## Phase 6: User Story 4 - Responsive Experience (Priority: P3)

**Goal**: All sections display correctly on mobile and tablet viewports

**Independent Test**: View page at 375px, 768px, and 1200px widths; verify no horizontal scroll, content readable

### Implementation for User Story 4

- [x] T029 [US4] Review and refine JourneySection mobile layout at 375px width
- [x] T030 [US4] Review and refine HardwareTiers mobile layout at 375px width
- [x] T031 [US4] Review and refine CtaSection mobile layout at 375px width
- [x] T032 [US4] Test tablet layout (768px) for all sections
- [x] T033 [US4] Verify no horizontal scrollbar at any viewport width
- [x] T034 [US4] Run Lighthouse accessibility audit and fix any critical issues

**Checkpoint**: User Story 4 complete - responsive design verified across devices

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup and validation

- [x] T035 [P] Update barrel export in frontend/src/components/Landing/index.ts with all components
- [x] T036 [P] Add aria-labels to interactive elements (chapter cards, tier cards, CTA button)
- [x] T037 Verify all chapter links in JourneySection navigate to correct docs pages
- [x] T038 Run full page load timing test (target: < 3 seconds)
- [x] T039 Final visual review on Chrome, Firefox, Safari
- [x] T040 Run quickstart.md checklist validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 can start immediately after Phase 2
  - US2, US3, US4 can start in parallel after Phase 2 (or sequentially)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - Independent of US1
- **User Story 3 (P2)**: Can start after Foundational - Independent of US1, US2
- **User Story 4 (P3)**: Should wait until US1-US3 components exist to test responsiveness

### Within Each User Story

- Component TSX and CSS files can be created in parallel [P]
- Import into index.tsx after component files are ready
- Responsive styles after initial component works
- Visual verification after all story tasks complete

### Parallel Opportunities

**Phase 1 (Setup)**:
```bash
# Run in parallel:
Task: T003 - chapters.ts
Task: T004 - tiers.ts
Task: T005 - index.ts
```

**Phase 3 (US1)**:
```bash
# Run in parallel:
Task: T007 - JourneySection.tsx
Task: T008 - JourneySection.module.css
Task: T009 - WhySection.tsx
Task: T010 - WhySection.module.css
```

**Phase 4 (US2)**:
```bash
# Run in parallel:
Task: T016 - HardwareTiers.tsx
Task: T017 - HardwareTiers.module.css
```

**Phase 5 (US3)**:
```bash
# Run in parallel:
Task: T022 - CtaSection.tsx
Task: T023 - CtaSection.module.css
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006)
3. Complete Phase 3: User Story 1 (T007-T015)
4. **STOP and VALIDATE**: Test landing page with hero, journey, why sections
5. Deploy preview if ready

### Incremental Delivery

1. Setup + Foundational → Base ready
2. Add US1 (Journey + Why) → Test → Preview
3. Add US2 (Hardware Tiers) → Test → Preview
4. Add US3 (CTA + Footer) → Test → Preview
5. Add US4 (Responsive polish) → Test → Deploy

### Sequential Full Implementation

```
T001 → T002 → T003/T004/T005 (parallel) → T006 →
T007/T008/T009/T010 (parallel) → T011 → T012 → T013 → T014 → T015 →
T016/T017 (parallel) → T018 → T019 → T020 → T021 →
T022/T023 (parallel) → T024 → T025 → T026 → T027 → T028 →
T029 → T030 → T031 → T032 → T033 → T034 →
T035/T036 (parallel) → T037 → T038 → T039 → T040
```

---

## Summary

| Phase | Story | Tasks | Parallel |
|-------|-------|-------|----------|
| Setup | - | 5 | 3 |
| Foundational | - | 1 | 0 |
| US1 (P1) | First-Time Visitor | 9 | 4 |
| US2 (P2) | Hardware Decision | 6 | 2 |
| US3 (P2) | CTA Conversion | 7 | 2 |
| US4 (P3) | Responsive | 6 | 0 |
| Polish | - | 6 | 2 |
| **Total** | | **40** | **13** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No automated tests - manual visual verification at checkpoints
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
