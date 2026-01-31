---
id: 0002
title: Hide Hero Image on Mobile
stage: general
date: 2026-01-31
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: 017-auth-flow-better-auth
user: hak
command: implement plan
labels: ["frontend", "mobile", "css", "responsive"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/pages/index.module.css
tests:
  - manual verification (resize browser to <996px)
---

## Prompt

Implement the following plan:

# Plan: Hide Hero Image on Mobile

## Problem
The hero banner image (robot/banner image) takes up significant scroll space on mobile devices without adding proportional value, since the text content is the primary focus.

## Solution
Hide the `.heroVisual` container on mobile screens (≤996px) using CSS `display: none`.

## File to Modify
- `frontend/src/pages/index.module.css`

## Implementation

Add `display: none` to the `.heroVisual` class inside the existing mobile media query:

```css
@media screen and (max-width: 996px) {
  /* ... existing styles ... */

  .heroVisual {
    display: none;
  }

  /* ... rest of existing styles ... */
}
```

The current mobile styles at lines 119-121 set `order: 2` on `.heroVisual`, which becomes unnecessary when hidden. Replace with `display: none`.

## Verification
1. Run `cd frontend && npm run start`
2. Open browser DevTools and toggle mobile view (or resize to <996px width)
3. Verify the hero image is hidden on mobile
4. Verify the hero text and buttons display correctly and are centered
5. Test on actual mobile device if available

## Response snapshot

Read the CSS file at `frontend/src/pages/index.module.css` and identified the mobile media query containing `.heroVisual { order: 2; }` at lines 119-121. Applied the edit to change `order: 2` to `display: none`, hiding the hero image on mobile screens.

## Outcome

- Impact: Hero image now hidden on mobile (≤996px), reducing scroll and focusing on text content
- Tests: Manual verification required
- Files: 1 file modified (index.module.css)
- Next prompts: Verify on actual mobile device, consider similar optimizations for other sections
- Reflection: Simple CSS change, plan was clear and implementation was straightforward

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (manual verification)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
