---
id: 0002
title: Constitution Update v1.1.0
stage: constitution
date: 2025-12-04
surface: agent
model: gemini-2.0-flash
feature: none
branch: main
user: codeWithHak
command: /sp.constitution
labels: ["governance", "update", "v1.1.0"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

/sp.constitution 

Project: "Physical AI & Humanoid Robotics Textbook"

Core Principles:
1. AI-Native Education: Content must be written for the "Partnership of People + AI + Robots" era.
2. Embodied Intelligence: All concepts must bridge the gap between digital AI (Brain) and physical robotics (Body).
3. Curriculum Fidelity: Content must align strictly with the "Physical AI" curriculum (ROS 2, Gazebo, NVIDIA Isaac Sim).
4. Hardware Reality: Content must assume the "Digital Twin" workstation (RTX GPU) and "Edge Kit" (Jetson Orin) architecture.

Global Constraints (Tech Stack & Requirements):
- Framework: Docusaurus (deployed to GitHub Pages).
- Chatbot Backend: FastAPI with OpenAI Agents/ChatKit SDKs.
- Database: Neon (Serverless Postgres) and Qdrant Cloud (Vector DB).
- Auth: Better-Auth.
- Scope: Content generation is limited to THREE (3) complete chapters. However, the TECHNICAL PLATFORM must be fully functional.

Workflow Policies:
- Documentation Strategy: DO NOT rely on internal training data for libraries (Better-Auth, OpenAI SDKs, Docusaurus). ALWAYS uses the "Context 7" MCP Server to fetch up-to-date documentation before implementation.
- Citation Style: IEEE format for all technical claims and references.

Quality Standards:
- Documentation: Markdown files must use Docusaurus-specific features (admonitions, tabs).
- Code Style: Python must be type-hinted and follow PEP8.
- Tone: Technical, empowering (aimed at future founders), and academic.

Success Criteria (Deliverables):
1. Content: 3 complete, high-quality chapters deployed on Docusaurus.
2. RAG Agent: A chatbot that answers questions about the book AND specifically allows users to highlight text and ask questions about the selection.
3. Auth Flow: Sign-up/Sign-in implemented via Better-Auth, including a mandatory survey on the user's software/hardware background.
4. Personalization: A functional button at the start of each chapter that adapts content based on the logged-in user's background.
5. Localization: A functional button at the start of each chapter that translates the content into Urdu.

## Response snapshot

Updated constitution to v1.1.0. Refined scope to clarify technical platform completeness. Expanded success criteria to include "Highlight to Ask" RAG feature, Personalization button, and Urdu Localization.

## Outcome

- ✅ Impact: Constitution updated to v1.1.0
- 🧪 Tests: N/A
- 📁 Files: 1 file updated
- 🔁 Next prompts: Plan or Spec creation
- 🧠 Reflection: Clear functional requirements added to success criteria.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None