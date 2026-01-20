# Data Model: Landing Page Complete Redesign

**Feature**: 014-landing-page-redesign
**Date**: 2026-01-20
**Status**: Complete

## Overview

This document defines the TypeScript interfaces and data structures for the landing page components. Since this is a static frontend feature, there are no database entities—only component props and configuration objects.

## Component Interfaces

### Chapter Data (JourneySection)

```typescript
/**
 * Represents a chapter card in the "Your Journey" section
 */
interface ChapterCard {
  /** Unique identifier (1, 2, 3) */
  id: number;
  /** Chapter number for display (e.g., "Chapter 1") */
  number: string;
  /** Chapter title */
  title: string;
  /** Brief description (1-2 sentences) */
  description: string;
  /** Navigation path to chapter */
  href: string;
  /** Optional icon name from lucide-react */
  icon?: string;
}

/**
 * Static chapter data for the landing page
 */
const CHAPTERS: ChapterCard[] = [
  {
    id: 1,
    number: "Chapter 1",
    title: "Embodied Intelligence",
    description: "The Great Transition from digital AI to physical machines that move, sense, and act.",
    href: "/docs/chapter-1/great-transition",
    icon: "Brain"
  },
  {
    id: 2,
    number: "Chapter 2",
    title: "Robotic Nervous System",
    description: "Master ROS 2 - the middleware that connects sensors, actuators, and AI planners.",
    href: "/docs/chapter-2/why-middleware",
    icon: "Network"
  },
  {
    id: 3,
    number: "Chapter 3",
    title: "Digital Twin",
    description: "Build virtual robots in simulation before deploying to the physical world.",
    href: "/docs/chapter-3/mirror-world",
    icon: "Layers"
  }
];
```

### Hardware Tier Data (HardwareTiers)

```typescript
/**
 * Represents a hardware configuration option
 */
interface HardwareTier {
  /** Unique identifier (1, 2, 3) */
  id: number;
  /** Tier name (e.g., "Workstation") */
  name: string;
  /** Approach label (e.g., "Full Local Setup") */
  label: string;
  /** Key benefit (e.g., "Best Experience") */
  benefit: string;
  /** Hardware requirements summary */
  requirements: string;
  /** Additional note (optional) */
  note?: string;
  /** Cost estimate */
  cost: string;
  /** Whether this tier is recommended */
  isRecommended: boolean;
}

/**
 * Static hardware tier data
 */
const HARDWARE_TIERS: HardwareTier[] = [
  {
    id: 1,
    name: "Workstation",
    label: "Full Local Setup",
    benefit: "Best Experience",
    requirements: "RTX 4070 Ti+, 64GB RAM, Ubuntu 22.04",
    note: "Run Isaac Sim locally with full performance",
    cost: "~$2,500+ hardware",
    isRecommended: false
  },
  {
    id: 2,
    name: "Cloud + Edge",
    label: "Hybrid Approach",
    benefit: "Flexible",
    requirements: "AWS/Azure GPU instances for simulation, Jetson kit for physical deployment",
    cost: "~$200/quarter cloud + $700 Jetson",
    isRecommended: true
  },
  {
    id: 3,
    name: "Simulation Only",
    label: "Learning Focus",
    benefit: "Lowest Cost",
    requirements: "Cloud-based simulation without physical hardware",
    note: "Complete the theory and simulation modules",
    cost: "Cloud compute only",
    isRecommended: false
  }
];
```

### Footer Configuration (Docusaurus Config)

```typescript
/**
 * Footer configuration for docusaurus.config.ts
 */
interface FooterConfig {
  style: 'dark';
  links: FooterLinkGroup[];
  copyright: string;
}

interface FooterLinkGroup {
  title: string;
  items: FooterLink[];
}

interface FooterLink {
  label: string;
  href?: string;
  to?: string;
}

/**
 * Footer configuration values
 */
const FOOTER_CONFIG: FooterConfig = {
  style: 'dark',
  links: [
    {
      title: 'Learn',
      items: [
        { label: 'Get Started', to: '/docs/preface' },
        { label: 'Chapter 1', to: '/docs/chapter-1' },
        { label: 'Chapter 2', to: '/docs/chapter-2' },
        { label: 'Chapter 3', to: '/docs/chapter-3' }
      ]
    },
    {
      title: 'Community',
      items: [
        { label: 'GitHub', href: 'https://github.com/[repo]' },
        { label: 'Twitter', href: 'https://twitter.com/[handle]' },
        { label: 'LinkedIn', href: 'https://linkedin.com/in/[profile]' }
      ]
    },
    {
      title: 'Contact',
      items: [
        { label: 'Email', href: 'mailto:contact@[domain]' }
      ]
    }
  ],
  copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook`
};
```

## Component Props

### JourneySection Props

```typescript
interface JourneySectionProps {
  /** Optional custom chapters (defaults to CHAPTERS constant) */
  chapters?: ChapterCard[];
}
```

### WhySection Props

```typescript
interface WhySectionProps {
  // No props - static content
}
```

### HardwareTiers Props

```typescript
interface HardwareTiersProps {
  /** Optional custom tiers (defaults to HARDWARE_TIERS constant) */
  tiers?: HardwareTier[];
}
```

### CtaSection Props

```typescript
interface CtaSectionProps {
  /** CTA button destination */
  href?: string; // defaults to "/docs/preface"
}
```

## Validation Rules

### ChapterCard
- `id`: Must be unique positive integer
- `number`: Non-empty string
- `title`: Non-empty string, max 50 characters
- `description`: Non-empty string, max 150 characters
- `href`: Valid internal path starting with `/`

### HardwareTier
- `id`: Must be unique positive integer (1-3)
- `name`: Non-empty string
- `cost`: Non-empty string
- `isRecommended`: Exactly one tier should have `true`

## State Management

No state management required. All data is static and passed as props or imported constants.

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      index.tsx (Landing Page)                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐                                        │
│  │  HomepageHeader │ ← Existing (no changes)                │
│  │    (Hero)       │                                        │
│  └─────────────────┘                                        │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────┐     ┌──────────────────┐              │
│  │ JourneySection  │ ◄───│ CHAPTERS const    │              │
│  └─────────────────┘     └──────────────────┘              │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────┐                                        │
│  │   WhySection    │ ← Static content                       │
│  └─────────────────┘                                        │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────┐     ┌──────────────────┐              │
│  │ HardwareTiers   │ ◄───│ HARDWARE_TIERS    │              │
│  └─────────────────┘     └──────────────────┘              │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────┐                                        │
│  │   CtaSection    │ ← href="/docs/preface"                 │
│  └─────────────────┘                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Docusaurus Footer (configured)                  │
│                 via docusaurus.config.ts                     │
└─────────────────────────────────────────────────────────────┘
```

## File Locations

| Data | Location | Format |
|------|----------|--------|
| CHAPTERS | `src/components/Landing/data/chapters.ts` | TypeScript |
| HARDWARE_TIERS | `src/components/Landing/data/tiers.ts` | TypeScript |
| Footer config | `docusaurus.config.ts` | TypeScript |
