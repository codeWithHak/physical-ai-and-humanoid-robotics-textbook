---
id: 0003
title: Constitution Update v2.0.0
stage: constitution
date: 2025-12-04
surface: agent
model: gemini-2.0-flash
feature: none
branch: main
user: codeWithHak
command: /sp.constitution
labels: ["governance", "update", "v2.0.0", "engineering-directives"]
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

Core Principles (Engineering Directives):
1. The Triad Architecture: Content must structure every solution as: Human Intent (Voice/Prompt) -> AI Planner (LLM/VLA) -> Robotic Execution (ROS 2/Actuators).
2. Software-to-Hardware Causality: All code examples must explicitly explain the physical outcome on the robot hardware (e.g., "This node triggers the gripper").
3. Tech Stack Isolation: Strictly limit tooling to the defined stack: ROS 2 (Humble/Iron), Gazebo/Unity (Simulation), and NVIDIA Isaac (Perception).
4. Compute-Aware Deployment: Explicitly segregate code into "Workstation Logic" (High VRAM/Sim) and "Edge Logic" (Low RAM/Jetson deployment).


Global Constraints (Technical Platform):
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

Updated constitution to v2.0.0. Replaced educational core principles with explicit Engineering Directives (Triad Architecture, Hardware Causality, Tech Stack Isolation, Compute-Aware Deployment).

## Outcome

- ✅ Impact: Constitution major update to v2.0.0
- 🧪 Tests: N/A
- 📁 Files: 1 file updated
- 🔁 Next prompts: Plan or Spec creation
- 🧠 Reflection: Shifted project focus to strict engineering directives.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None