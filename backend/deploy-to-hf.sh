#!/bin/bash
# Deploy backend to Hugging Face Spaces
# Usage: ./deploy-to-hf.sh "commit message"

set -e

HF_DEPLOY_DIR="/home/hak/projects/hf-backend-deploy"
BACKEND_DIR="$(dirname "$0")"
COMMIT_MSG="${1:-Update backend}"

echo "📦 Syncing backend to HF Spaces..."

# Clean destination (keep .git)
find "$HF_DEPLOY_DIR" -mindepth 1 -maxdepth 1 ! -name '.git' ! -name '.gitattributes' -exec rm -rf {} +

# Copy backend files
cp -r "$BACKEND_DIR/src" "$HF_DEPLOY_DIR/"
cp -r "$BACKEND_DIR/api" "$HF_DEPLOY_DIR/"
cp "$BACKEND_DIR/Dockerfile" "$HF_DEPLOY_DIR/"
cp "$BACKEND_DIR/requirements.txt" "$HF_DEPLOY_DIR/"
cp "$BACKEND_DIR/README.md" "$HF_DEPLOY_DIR/"
cp "$BACKEND_DIR/.dockerignore" "$HF_DEPLOY_DIR/" 2>/dev/null || true
cp "$BACKEND_DIR/ingest.py" "$HF_DEPLOY_DIR/" 2>/dev/null || true

# Clean pycache
find "$HF_DEPLOY_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$HF_DEPLOY_DIR" -name "*.pyc" -delete 2>/dev/null || true

# Commit and push
cd "$HF_DEPLOY_DIR"
git add -A
git commit -m "$COMMIT_MSG" || echo "No changes to commit"
git push origin main

echo "✅ Deployed to HF Spaces!"
echo "🔗 https://huggingface.co/spaces/HAK-16/physical-ai-backend"
