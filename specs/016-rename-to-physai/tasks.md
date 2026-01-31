# Tasks: Rename to PhysAI

**Feature Branch**: `016-rename-to-physai`
**Created**: 2026-01-25
**Status**: Complete
**Plan**: [specs/016-rename-to-physai/plan.md](plan.md)

## Summary

Rename entire project from `physical-ai-and-humanoid-robotics-textbook` to `PhysAI`.

---

## Phase 1: Prepare

- [x] T001 Create new HF Space `physai-backend`
- [x] T002 Clone new HF Space locally
- [x] T003 Copy backend files to new space
- [x] T004 Update CORS for new domain
- [x] T005 Push to new HF Space
- [x] T006 Add secrets to new HF Space
- [x] T007 Verify new backend health endpoint

## Phase 2: Switch

- [x] T008 Update frontend API URL in ChatContext.tsx
- [x] T009 Commit frontend changes
- [x] T010 Rename GitHub repo to `physai`
- [x] T011 Update local git remote
- [x] T012 Push to new remote

## Phase 3: Verify

- [x] T013 Verify Vercel still deploying
- [x] T014 Verify frontend loads
- [x] T015 Verify chat feature works
- [x] T016 Verify no CORS errors
- [x] T017 Verify backend health returns healthy

## Phase 4: Cleanup

- [x] T018 Rename Vercel project to `physai`
- [x] T019 Update deploy script
- [x] T020 Update documentation
- [x] T021 Rename local folder
- [x] T022 Delete old HF Space (after verification period)

---

## Success Criteria (All Met)

- ✅ `physai.vercel.app` loads the frontend
- ✅ Chat feature works end-to-end
- ✅ `hak-16-physai-backend.hf.space/api/health` returns healthy
- ✅ No console errors (especially CORS)
- ✅ Deploy script works for future updates
- ✅ All documentation updated

---

**Completed**: 2026-01-25
