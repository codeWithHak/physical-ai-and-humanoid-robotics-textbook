# Quickstart: Refactor Verification

**Goal**: Verify the new modular structure works as expected.

## Prerequisites
- [ ] Local development environment running (`npm start` in `frontend/`).

## Verification Steps

### 1. Navigation Check
- [ ] Open the sidebar.
- [ ] Is there a folder "Chapter 1: Embodied Intelligence"?
- [ ] Expand it. Are there 4 sub-items?
- [ ] Are they ordered 1-4 correctly?

### 2. Content Check
- [ ] Click "The Hardware Nervous System" (Item 3).
- [ ] **Critical**: Does the `<HardwareCheck />` component render and work?
- [ ] Click "The Triad Architecture" (Item 2).
- [ ] **Critical**: Does the Mermaid diagram render?

### 3. Dead Link Check
- [ ] Navigate to the *old* URL (`/docs/chapter-1`). Does it 404 (Correct) or redirect? (If 404, good, file is gone).
