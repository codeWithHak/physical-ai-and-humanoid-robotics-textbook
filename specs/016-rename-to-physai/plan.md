# Project Rename Plan: physical-ai-and-humanoid-robotics-textbook → PhysAI

## Overview

**Current State:**
- GitHub: `codeWithHak/physical-ai-and-humanoid-robotics-textbook`
- Frontend: `physical-ai-and-humanoid-robotics-h.vercel.app`
- Backend: `hak-16-physical-ai-backend.hf.space`
- HF Repo: `HAK-16/physical-ai-backend`

**Target State:**
- GitHub: `codeWithHak/physai`
- Frontend: `physai.vercel.app`
- Backend: `hak-16-physai-backend.hf.space`
- HF Repo: `HAK-16/physai-backend`

---

## Critical Understanding

### What CAN Be Renamed
| Service | Renameable? | Method |
|---------|-------------|--------|
| GitHub Repo | ✅ Yes | Settings → Rename |
| Vercel Project | ✅ Yes | Settings → Rename |
| Vercel Domain | ✅ Yes | Auto-updates with project name |
| HF Space | ❌ No | Must create NEW space, delete old |
| Local Folder | ✅ Yes | `mv` command |

### What CANNOT Be Renamed
- HF Space URL (immutable once created)
- Git commit history (stays intact)
- Existing links to old URLs (will break)

---

## Execution Order (CRITICAL)

The order matters. Wrong order = broken app.

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: PREPARE (No breaking changes)                     │
│  - Create new HF Space                                      │
│  - Deploy backend to new space                              │
│  - Verify new backend works                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: SWITCH (Brief downtime possible)                  │
│  - Update frontend to use new backend URL                   │
│  - Rename GitHub repo                                       │
│  - Update local git remote                                  │
│  - Push changes                                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: VERIFY                                            │
│  - Test frontend → backend connection                       │
│  - Verify all endpoints working                             │
│  - Check CORS is correct                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 4: CLEANUP                                           │
│  - Rename Vercel project                                    │
│  - Update internal references                               │
│  - Delete old HF Space                                      │
│  - Update documentation                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Detailed Steps

### PHASE 1: PREPARE (No Breaking Changes)

#### Step 1.1: Create New HF Space
**Action:** Create `HAK-16/physai-backend` on Hugging Face
**URL:** https://huggingface.co/new-space

Settings:
- Name: `physai-backend`
- SDK: Docker
- Hardware: CPU basic (free)

**Verification:** Space created and shows empty state

#### Step 1.2: Clone New HF Space
```bash
cd ~/projects
git clone https://huggingface.co/spaces/HAK-16/physai-backend hf-physai-backend
```

#### Step 1.3: Copy Backend Files to New Space
```bash
cp -r ~/projects/hf-backend-deploy/* ~/projects/hf-physai-backend/
cp ~/projects/hf-backend-deploy/.gitignore ~/projects/hf-physai-backend/
cp ~/projects/hf-backend-deploy/.dockerignore ~/projects/hf-physai-backend/
```

#### Step 1.4: Update CORS in New Backend
Edit `~/projects/hf-physai-backend/src/main.py`:
```python
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://physai.vercel.app",                              # NEW
    "https://physical-ai-and-humanoid-robotics-h.vercel.app", # Keep for transition
]
```

#### Step 1.5: Push to New HF Space
```bash
cd ~/projects/hf-physai-backend
git add -A
git commit -m "Initial deployment of PhysAI backend"
git push origin main
```

#### Step 1.6: Add Secrets to New HF Space
Go to: https://huggingface.co/spaces/HAK-16/physai-backend/settings

Add secrets:
- `OPENAI_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`

#### Step 1.7: Verify New Backend
```bash
curl https://hak-16-physai-backend.hf.space/health
# Expected: {"status": "healthy", ...}
```

**CHECKPOINT:** New backend is running. Old backend still works. No breaking changes yet.

---

### PHASE 2: SWITCH

#### Step 2.1: Update Frontend Backend URL
Edit `frontend/src/context/ChatContext.tsx`:
```typescript
// OLD
const API_URL = 'https://hak-16-physical-ai-backend.hf.space/api/chat';

// NEW
const API_URL = 'https://hak-16-physai-backend.hf.space/api/chat';
```

#### Step 2.2: Commit Frontend Changes
```bash
git add frontend/src/context/ChatContext.tsx
git commit -m "feat: Switch to new PhysAI backend URL"
```

#### Step 2.3: Rename GitHub Repository
1. Go to: https://github.com/codeWithHak/physical-ai-and-humanoid-robotics-textbook/settings
2. Scroll to "Repository name"
3. Change to: `physai`
4. Click "Rename"

**WARNING:** This changes your remote URL immediately!

#### Step 2.4: Update Local Git Remote
```bash
git remote set-url origin git@github.com:codeWithHak/physai.git
# Or HTTPS:
git remote set-url origin https://github.com/codeWithHak/physai.git
```

#### Step 2.5: Verify Remote
```bash
git remote -v
# Should show: origin git@github.com:codeWithHak/physai.git
```

#### Step 2.6: Push Changes
```bash
git push origin 016-rename-to-physai
```

**CHECKPOINT:** GitHub repo renamed. Frontend points to new backend.

---

### PHASE 3: VERIFY

#### Step 3.1: Check Vercel Deployment
Vercel should auto-detect the repo rename and continue deploying.
Check: https://vercel.com/dashboard

If Vercel lost connection:
1. Go to Project Settings
2. Reconnect to `codeWithHak/physai`

#### Step 3.2: Test Frontend → Backend Connection
1. Visit your Vercel preview URL for the branch
2. Open browser DevTools → Network tab
3. Use the chat feature
4. Verify requests go to `hak-16-physai-backend.hf.space`
5. Verify responses return successfully (no CORS errors)

#### Step 3.3: Test Health Endpoints
```bash
# Backend health
curl https://hak-16-physai-backend.hf.space/api/health

# Chat endpoint
curl -X POST https://hak-16-physai-backend.hf.space/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is physical AI?"}'
```

**CHECKPOINT:** Everything works with new URLs.

---

### PHASE 4: CLEANUP

#### Step 4.1: Rename Vercel Project
1. Go to Vercel Dashboard → Your Project → Settings
2. Change project name to `physai`
3. Domain will auto-update to `physai.vercel.app`

#### Step 4.2: Update Deploy Script
Edit `backend/deploy-to-hf.sh`:
```bash
HF_DEPLOY_DIR="$HOME/projects/hf-physai-backend"
# ... update echo URL at the end
```

#### Step 4.3: Update Documentation
Files to update:
- `README.md` (root)
- `docs/DEPLOYMENT_GUIDE.md`
- `CLAUDE.md`
- Any hardcoded URLs in specs/

#### Step 4.4: Rename Local Folder (Optional)
```bash
cd ~/projects
mv physical-ai-and-humanoid-robotics-textbook physai
```

#### Step 4.5: Update HF Backend Deploy Directory
```bash
mv ~/projects/hf-backend-deploy ~/projects/hf-physai-backend-old
# Keep as backup until verified
```

#### Step 4.6: Delete Old HF Space (LAST STEP)
Only after everything is verified working for at least 24 hours:
1. Go to: https://huggingface.co/spaces/HAK-16/physical-ai-backend/settings
2. Scroll to bottom → "Delete this space"

---

## Vulnerabilities & Risks

### HIGH RISK

| Risk | Impact | Mitigation |
|------|--------|------------|
| CORS errors after URL change | App broken, API calls fail | Update CORS BEFORE switching frontend |
| Vercel loses GitHub connection | Deploys stop working | Reconnect in Vercel settings |
| Secrets not added to new HF Space | Backend crashes with 403 | Add secrets immediately after creating space |
| Deleting old HF Space too early | No rollback if issues found | Wait 24-48 hours before deleting |

### MEDIUM RISK

| Risk | Impact | Mitigation |
|------|--------|------------|
| DNS propagation delay | Old URLs cached | Wait, or hard refresh |
| Local git remote outdated | Push fails | Update remote URL immediately after rename |
| Cached frontend in browser | Users see old version | Clear cache, or wait |
| SEO impact | Old links return 404 | GitHub auto-redirects repo URLs |

### LOW RISK

| Risk | Impact | Mitigation |
|------|--------|------------|
| Typo in new URLs | Broken links | Double-check all URLs |
| Forgetting a hardcoded URL | Partial breakage | Search codebase for old URLs |
| HF Space build fails | Backend down | Test locally first |

---

## Things to NOT Do

### NEVER
1. ❌ Delete old HF Space before new one is verified working
2. ❌ Rename GitHub repo before updating local remote URL
3. ❌ Push to old remote after renaming (will fail)
4. ❌ Skip CORS update (will cause silent failures)
5. ❌ Commit secrets to git (use HF Spaces secrets UI)

### AVOID
1. ⚠️ Doing all steps in one session without testing between phases
2. ⚠️ Renaming during high-traffic periods
3. ⚠️ Forgetting to update the deploy script
4. ⚠️ Skipping the verification phase

---

## Rollback Plan

If something goes wrong:

### Frontend Broken
```bash
# Revert to old backend URL
git revert HEAD
git push
```

### Backend Broken
Old HF Space is still running at:
`https://hak-16-physical-ai-backend.hf.space`

Update frontend to point back to old URL.

### GitHub Rename Broke Vercel
1. Go to Vercel Dashboard
2. Project Settings → Git
3. Disconnect and reconnect to new repo name

### Complete Rollback
If everything fails:
1. Rename GitHub repo back to original name
2. Update local remote back
3. Revert frontend URL changes
4. Continue using old HF Space

---

## Checklist

### Pre-Flight
- [ ] Backup any local uncommitted changes
- [ ] Note down all current URLs
- [ ] Have HF token ready for git push
- [ ] Have API keys ready for new HF Space secrets

### Phase 1: Prepare
- [ ] Create new HF Space `physai-backend`
- [ ] Clone new HF Space locally
- [ ] Copy backend files
- [ ] Update CORS for new domain
- [ ] Push to new HF Space
- [ ] Add secrets to new HF Space
- [ ] Verify new backend health endpoint

### Phase 2: Switch
- [ ] Update frontend API URL
- [ ] Commit change
- [ ] Rename GitHub repo
- [ ] Update local git remote
- [ ] Push to new remote

### Phase 3: Verify
- [ ] Vercel still deploying
- [ ] Frontend loads
- [ ] Chat feature works
- [ ] No CORS errors in console
- [ ] Backend health returns healthy

### Phase 4: Cleanup
- [ ] Rename Vercel project to `physai`
- [ ] Update deploy script
- [ ] Update documentation
- [ ] (Optional) Rename local folder
- [ ] (After 24-48h) Delete old HF Space

### Post-Rename
- [ ] Test on mobile
- [ ] Test in incognito (no cache)
- [ ] Update portfolio/resume with new URL
- [ ] Update any external links (LinkedIn, etc.)

---

## Timeline Estimate

| Phase | Duration | Notes |
|-------|----------|-------|
| Phase 1: Prepare | 15-20 min | HF Space build takes ~5 min |
| Phase 2: Switch | 5-10 min | Quick if no issues |
| Phase 3: Verify | 10-15 min | Thorough testing |
| Phase 4: Cleanup | 10-15 min | Documentation updates |
| **Total** | **40-60 min** | Plus 24-48h before deleting old space |

---

## Files That Will Change

```
frontend/src/context/ChatContext.tsx    # Backend URL
backend/deploy-to-hf.sh                 # Deploy script path
backend/src/main.py                     # CORS origins (in new HF space)
README.md                               # Project name/URLs
docs/DEPLOYMENT_GUIDE.md                # Example URLs
CLAUDE.md                               # Project references
```

---

## Success Criteria

The rename is complete when:
1. ✅ `physai.vercel.app` loads the frontend
2. ✅ Chat feature works end-to-end
3. ✅ `hak-16-physai-backend.hf.space/api/health` returns healthy
4. ✅ No console errors (especially CORS)
5. ✅ Deploy script works for future updates
6. ✅ All documentation updated
7. ✅ Old HF Space deleted (after verification period)

---

## Commands Quick Reference

```bash
# Clone new HF Space
git clone https://huggingface.co/spaces/HAK-16/physai-backend ~/projects/hf-physai-backend

# Update git remote after GitHub rename
git remote set-url origin git@github.com:codeWithHak/physai.git

# Verify remote
git remote -v

# Test backend
curl https://hak-16-physai-backend.hf.space/api/health

# Search for old URLs in codebase
grep -r "physical-ai" --include="*.ts" --include="*.tsx" --include="*.py" --include="*.md"
```

---

*Plan created: January 2026*
*Branch: 016-rename-to-physai*
