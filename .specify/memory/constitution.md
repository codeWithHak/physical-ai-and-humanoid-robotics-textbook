<!--
Sync Impact Report:
- Version change: 1.1.0 -> 2.0.0
- List of modified principles:
  - Renamed/Redefined: AI-Native Education -> The Triad Architecture
  - Renamed/Redefined: Embodied Intelligence -> Software-to-Hardware Causality
  - Renamed/Redefined: Curriculum Fidelity -> Tech Stack Isolation
  - Renamed/Redefined: Hardware Reality -> Compute-Aware Deployment
- Modified sections:
  - Core Principles (completely redefined as Engineering Directives)
- Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ (Generic references ok)
  - .specify/templates/spec-template.md: ✅ (Generic references ok)
  - .specify/templates/tasks-template.md: ✅ (Generic references ok)
- Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles (Engineering Directives)

### The Triad Architecture
Content must structure every solution as: Human Intent (Voice/Prompt) -> AI Planner (LLM/VLA) -> Robotic Execution (ROS 2/Actuators).

### Software-to-Hardware Causality
All code examples must explicitly explain the physical outcome on the robot hardware (e.g., "This node triggers the gripper").

### Tech Stack Isolation
Strictly limit tooling to the defined stack: ROS 2 (Humble/Iron), Gazebo/Unity (Simulation), and NVIDIA Isaac (Perception).

### Compute-Aware Deployment
Explicitly segregate code into "Workstation Logic" (High VRAM/Sim) and "Edge Logic" (Low RAM/Jetson deployment).

## Global Constraints & Tech Stack

- **Framework**: Docusaurus (deployed to Vercel).
- **Chatbot Backend**: FastAPI with OpenAI Agents/ChatKit SDKs.
- **Database**: Neon (Serverless Postgres) and Qdrant Cloud (Vector DB).
- **Auth**: Better-Auth.
- **Scope**: Content generation is limited to THREE (3) complete chapters. However, the TECHNICAL PLATFORM must be fully functional.

## Workflow & Quality Standards

- **Documentation Strategy**: DO NOT rely on internal training data for libraries (Better-Auth, OpenAI SDKs, Docusaurus). ALWAYS use the "Context 7" MCP Server to fetch up-to-date documentation.
- **Citation Style**: IEEE format for all technical claims and references.
- **Documentation Quality**: Markdown files must use Docusaurus-specific features (admonitions, tabs).
- **Code Style**: Python must be type-hinted and follow PEP8.
- **Tone**: Technical, empowering (aimed at future founders), and academic.

## Success Criteria

- **Content**: 3 complete, high-quality chapters deployed on Docusaurus.
- **RAG Agent**: A chatbot that answers questions about the book AND specifically allows users to highlight text and ask questions about the selection.
- **Auth Flow**: Sign-up/Sign-in implemented via Better-Auth, including a mandatory survey on the user's software/hardware background.
- **Personalization**: A functional button at the start of each chapter that adapts content based on the logged-in user's background.
- **Localization**: A functional button at the start of each chapter that translates the content into Urdu.

## Governance

This Constitution supersedes all other practices. Amendments require documentation, approval, and a clear migration plan. All PRs and reviews must verify compliance with these principles.

**Version**: 2.0.0 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-04