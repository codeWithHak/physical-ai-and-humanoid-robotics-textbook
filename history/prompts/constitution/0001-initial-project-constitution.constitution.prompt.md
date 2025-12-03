---
id: 0001
title: Initial Project Constitution
stage: constitution
date: 2025-12-04
surface: agent
model: gemini-2.0-flash
feature: none
branch: main
user: codeWithHak
command: /sp.constitution
labels: ["governance", "setup"]
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
3. Curriculum Fidelity: Content must align strictly with the "Physical AI" curriculum (ROS 2, Gazebo, NVIDIA Isaac Sim)[cite: 53, 58, 63].
4. Hardware Reality: Content must assume the "Digital Twin" workstation (RTX GPU) and "Edge Kit" (Jetson Orin) architecture[cite: 122, 137].

Global Constraints (Tech Stack & Requirements):
- Framework: Docusaurus (deployed to GitHub Pages)[cite: 15].
- Chatbot Backend: FastAPI with OpenAI Agents/ChatKit SDKs[cite: 18].
- Database: Neon (Serverless Postgres) and Qdrant Cloud (Vector DB)[cite: 18].
- Auth: Better-Auth with mandatory background survey at signup[cite: 21].
- Scope: The project deliverables are limited to THREE (3) complete, high-quality chapters.

Workflow Policies:
- Documentation Strategy: DO NOT rely on internal training data for libraries (Better-Auth, OpenAI SDKs, Docusaurus). ALWAYS uses the "Context 7" MCP Server to fetch up-to-date documentation.
- Citation Style: IEEE format for all technical claims and references.

Quality Standards:
- Documentation: Markdown files must use Docusaurus-specific features (admonitions, tabs).
- Code Style: Python must be type-hinted and follow PEP8.
- Tone: Technical, empowering (aimed at future founders), and academic[cite: 10].
- Accessibility: Support for Urdu translation toggle and personalization[cite: 23, 24].

Success Criteria:
- A fully deployed Docusaurus site containing 3 complete, interactive chapters.
- A functional RAG chatbot that answers questions based on these chapters[cite: 18].
- User authentication flow that captures software/hardware background[cite: 21].

## Response snapshot

Updated project constitution to v1.0.0 with 4 core principles (AI-Native Education, Embodied Intelligence, Curriculum Fidelity, Hardware Reality), defined global constraints, workflow policies, and success criteria.

## Outcome

- ✅ Impact: Constitution established
- 🧪 Tests: N/A
- 📁 Files: 1 file updated
- 🔁 Next prompts: Plan or Spec creation
- 🧠 Reflection: Initial constitution created successfully.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None