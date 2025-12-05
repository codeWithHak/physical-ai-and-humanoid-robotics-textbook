import React from 'react';
import styles from './styles.module.css';

const GLOSSARY: Record<string, string> = {
  "SLAM": "Simultaneous Localization and Mapping: A technique for a robot to build a map of an unknown environment while keeping track of its location within it.",
  "URDF": "Unified Robot Description Format: An XML format used in ROS to describe the physical structure (links and joints) of a robot.",
  "VLA": "Vision-Language-Action Model: A type of AI model that takes images and text as input and outputs direct robot actions (e.g., joint angles).",
  "ROS 2": "Robot Operating System 2: The industry-standard middleware for building robot applications, handling communication between nodes.",
  "Sim2Real": "Simulation to Reality: The process of training a robot policy in a physics simulator (like Isaac Sim) and transferring it to physical hardware.",
  "Zero-Shot": "The ability of a model to perform a task it wasn't explicitly trained on.",
  "Inverse Kinematics": "Calculating the joint angles required to place a robot's end-effector at a specific position and orientation."
};

interface Props {
  term: string;
  children: React.ReactNode;
}

export default function TermTooltip({ term, children }: Props) {
  const definition = GLOSSARY[term] || "Definition not found.";

  return (
    <span className={styles.tooltipContainer}>
      {children}
      <span className={styles.tooltipText}>{definition}</span>
    </span>
  );
}
