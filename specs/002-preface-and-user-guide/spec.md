# Feature Specification: Preface and User Guide

**Feature Branch**: `002-preface-and-user-guide`  
**Created**: 2025-12-04  
**Status**: Draft  
**Input**: User description: "Feature: Preface and User Guide Intent: Create a "How to Use This Book" (Preface) page that acts as the entry point for the course. It must guide the learner on hardware prerequisites, time commitment, and how to utilize the interactive AI features (Chatbot, Personalization). Feature Scope: 1. Section 1: "Who This Is For." Target audience: Future founders and engineers entering the "Partnership of People + AI + Robots" era[cite: 2]. 2. Section 2: "The Hardware Reality Check." A critical warning section detailing the need for: - "Digital Twin" Workstation (RTX 4070 Ti+, 64GB RAM, Ubuntu 22.04) [cite: 122-131]. - "Physical AI" Edge Kit (Jetson Orin Nano, RealSense Camera) [cite: 137-140]. - The "Cloud Alternative" (AWS g5.2xlarge) for those without hardware. 3. Section 3: "Learning Path & Time." Explain the 13-week structure, estimating ~10 hours/week of effort. 4. Section 4: "Interactive Features." Briefly explain how to use the "Urdu Translation" toggle and the "Ask the Book" RAG chatbot to clear doubts. Success Criteria (SMART): - Format: Docusaurus Markdown (`00-preface.md`) positioned at the very top of the sidebar. - Visuals: Uses Docusaurus `<Admonition type="danger">` for the Hardware Requirements to ensure they are not missed. - Clarity: Includes a simple "Checklist" for students to verify they are ready to start. - Navigation: Links clearly to "Chapter 1" at the bottom. - Accuracy: Hardware specs match the source document exactly (e.g., "RTX 4070 Ti or higher")[cite: 125]. Non-Goals: - NOT writing Chapter 1 content. - NOT implementing the actual logic for the buttons yet. User Stories: - "As a student, I want to know immediately if my laptop is powerful enough for this course so I don't waste time." - "As a learner, I want to know how many hours a week I need to set aside to finish the course.""

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Hardware Assessment (Priority: P1)

As a student, I want to know immediately if my current hardware is powerful enough for this course or if I need to upgrade/use the cloud, so I don't waste time starting a course I cannot technically complete.

**Why this priority**: This is a blocking constraint. Users without the right hardware cannot complete the technical exercises.

**Independent Test**: Verify that the "Hardware Reality Check" section is prominently displayed with a danger admonition and clearly lists the three options (Workstation, Edge, Cloud).

**Acceptance Scenarios**:

1. **Given** I am on the Preface page, **When** I scroll to the hardware section, **Then** I see a red "Danger" or "Critical Warning" box.
2. **Given** the hardware section, **When** I read the Workstation requirements, **Then** I see "RTX 4070 Ti+" and "64GB RAM" explicitly listed.
3. **Given** I do not own the hardware, **When** I look for alternatives, **Then** I see the "Cloud Alternative" (AWS g5.2xlarge) listed.

---

### User Story 2 - Course Commitment Understanding (Priority: P2)

As a learner, I want to know the course duration and weekly time commitment so I can plan my schedule effectively.

**Why this priority**: Essential for expectation setting and reducing drop-off rates.

**Independent Test**: Verify the "Learning Path & Time" section explicitly mentions "13 weeks" and "~10 hours/week".

**Acceptance Scenarios**:

1. **Given** the Preface page, **When** I find the Learning Path section, **Then** I see the estimated effort of ~10 hours/week.
2. **Given** the Learning Path section, **When** I look for the total duration, **Then** I see the 13-week structure mentioned.

---

### User Story 3 - Feature Onboarding (Priority: P3)

As a user, I want to understand how to use the "Urdu Translation" and "Ask the Book" features so I can utilize them during my learning.

**Why this priority**: Ensures users are aware of the platform's unique value propositions (AI & Localization) from the start.

**Independent Test**: Verify the "Interactive Features" section describes the existence and purpose of the Translation and RAG features.

**Acceptance Scenarios**:

1. **Given** the "Interactive Features" section, **When** I read about the chatbot, **Then** it explains that I can "Ask the Book" to clear doubts.
2. **Given** the "Interactive Features" section, **When** I read about localization, **Then** it explains the "Urdu Translation" toggle.

### Edge Cases

- **Mobile View**: The hardware requirements table or admonition must remain readable on small screens.
- **Missing Cloud Info**: If the cloud alternative details are vague, users might feel blocked. (Spec ensures AWS instance type is listed).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a "Preface" page accessible from the top of the sidebar (order 0).
- **FR-002**: The Preface page MUST contain a "Who This Is For" section targeting founders and engineers.
- **FR-003**: The Preface page MUST contain a "Hardware Reality Check" section wrapped in a `<Admonition type="danger">` (or similar visual warning).
- **FR-004**: The Hardware section MUST list specific specs: RTX 4070 Ti+, 64GB RAM, Ubuntu 22.04 (Workstation); Jetson Orin Nano, RealSense Camera (Edge); AWS g5.2xlarge (Cloud).
- **FR-005**: The Preface page MUST contain a "Learning Path & Time" section stating 13 weeks duration and ~10 hours/week effort.
- **FR-006**: The Preface page MUST contain an "Interactive Features" section explaining the Urdu Translation and RAG Chatbot.
- **FR-007**: The Preface page MUST include a "Readiness Checklist" at the end.
- **FR-008**: The page MUST include a navigation link to "Chapter 1" at the bottom.

### Key Entities *(include if feature involves data)*

*None (Static Content)*

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **Visibility**: The "Hardware Reality Check" uses a visually distinct warning style (red/danger) that differentiates it from normal text.
- **SC-002**: **Accuracy**: 100% of the hardware specifications (GPU model, RAM amount, AWS instance) match the source text provided in the prompt.
- **SC-003**: **Navigation**: Clicking the "Chapter 1" link at the bottom successfully navigates to the Chapter 1 placeholder (or 404 if not created yet, but the link exists).
- **SC-004**: **Sidebar Position**: The Preface appears as the very first item in the documentation sidebar.