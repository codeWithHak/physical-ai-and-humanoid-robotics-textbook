---
sidebar_position: 0
slug: /preface
title: Preface
---

# Preface: How to Use This Book

## Who This Is For

This course is designed for **future founders, engineers, and researchers** who are ready to enter the emerging era of **"Partnership of People + AI + Robots"**.

It bridges the gap between high-level AI theory and low-level robotic control, focusing on the practical skills needed to build embodied intelligence.

:::danger Hardware Reality Check

To successfully complete the technical exercises in this course, you **must** meet specific hardware requirements. "Physical AI" is computationally expensive.

### 1. Digital Twin Workstation
This is your primary development machine for simulation (Isaac Sim/Gazebo) and training.
- **GPU**: NVIDIA RTX 4070 Ti or higher (12GB+ VRAM is critical).
- **RAM**: 64GB DDR5 recommended (32GB minimum).
- **OS**: Ubuntu 22.04 LTS.

### 2. Physical AI Edge Kit
This is the hardware for the real-world robot.
- **Compute**: NVIDIA Jetson Orin Nano (or Orin AGX).
- **Sensors**: Intel RealSense Camera (Depth + RGB).

### 3. Cloud Alternative
If you do not have the workstation hardware, you can rent a cloud instance.
- **Instance Type**: AWS **g5.2xlarge** (or equivalent with A10G GPU).

:::

## Learning Path & Time

This is a rigorous technical course structured over **13 weeks**.

- **Time Commitment**: You should expect to set aside **~10 hours per week**.
- **Structure**: Each week builds upon the previous one, moving from simulation to reality.

## Interactive Features

We have built this textbook with interactive AI features to accelerate your learning.

### Urdu Translation
Use the **"Urdu Translation"** toggle at the top of the page to instantly translate the technical content into Urdu, making it accessible to a broader audience.

### Ask the Book (RAG Chatbot)
Stuck on a concept? Use the **"Ask the Book"** chatbot in the bottom corner. It is trained specifically on this textbook's content and can help clarify doubts or debug code snippets.

## Readiness Checklist

Before you begin Chapter 1, please verify:

- [ ] I have a machine running Ubuntu 22.04 (or a cloud instance ready).
- [ ] I have verified my GPU meets the VRAM requirements.
- [ ] I am ready to commit ~10 hours/week for the next 13 weeks.

[Start Chapter 1](./intro.md)
