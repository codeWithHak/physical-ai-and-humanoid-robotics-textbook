# Quickstart: Landing Page Complete Redesign

**Feature**: 014-landing-page-redesign
**Date**: 2026-01-20

## Prerequisites

- Node.js 18+ installed
- pnpm package manager
- Repository cloned and on branch `014-landing-page-redesign`

## Development Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pnpm install

# Start development server
pnpm start
```

The site will be available at `http://localhost:3000`.

## File Structure

After implementation, the following files will be created/modified:

```
frontend/
├── src/
│   ├── pages/
│   │   └── index.tsx                    # Modified: import and render new sections
│   └── components/
│       └── Landing/
│           ├── index.ts                 # Barrel export
│           ├── data/
│           │   ├── chapters.ts          # Chapter card data
│           │   └── tiers.ts             # Hardware tier data
│           ├── JourneySection.tsx       # "Your Journey" section
│           ├── JourneySection.module.css
│           ├── WhySection.tsx           # "Why This Matters" section
│           ├── WhySection.module.css
│           ├── HardwareTiers.tsx        # Hardware options section
│           ├── HardwareTiers.module.css
│           ├── CtaSection.tsx           # Call-to-action section
│           └── CtaSection.module.css
└── docusaurus.config.ts                 # Modified: footer configuration
```

## Implementation Steps

### Step 1: Create Component Directory

```bash
mkdir -p frontend/src/components/Landing/data
```

### Step 2: Create Data Files

Create `frontend/src/components/Landing/data/chapters.ts`:
```typescript
export interface ChapterCard {
  id: number;
  number: string;
  title: string;
  description: string;
  href: string;
  icon?: string;
}

export const CHAPTERS: ChapterCard[] = [
  {
    id: 1,
    number: "Chapter 1",
    title: "Embodied Intelligence",
    description: "The Great Transition from digital AI to physical machines.",
    href: "/docs/chapter-1/great-transition",
    icon: "Brain"
  },
  // ... (see data-model.md for full data)
];
```

### Step 3: Create Section Components

Each component follows this pattern:

```typescript
// JourneySection.tsx
import React from 'react';
import styles from './JourneySection.module.css';
import { CHAPTERS } from './data/chapters';

export function JourneySection() {
  return (
    <section className={styles.journey}>
      <div className={styles.container}>
        <h2>Your Journey</h2>
        <p className={styles.subtitle}>From Zero to Building Robots That Think</p>
        <div className={styles.cards}>
          {CHAPTERS.map((chapter) => (
            <article key={chapter.id} className={styles.card}>
              {/* Card content */}
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
```

### Step 4: Update Landing Page

Modify `frontend/src/pages/index.tsx`:

```typescript
import { JourneySection } from '../components/Landing/JourneySection';
import { WhySection } from '../components/Landing/WhySection';
import { HardwareTiers } from '../components/Landing/HardwareTiers';
import { CtaSection } from '../components/Landing/CtaSection';

export default function Home(): JSX.Element {
  return (
    <Layout>
      <HomepageHeader />
      <main>
        <JourneySection />
        <WhySection />
        <HardwareTiers />
        <CtaSection />
      </main>
    </Layout>
  );
}
```

### Step 5: Update Footer Configuration

Modify `frontend/docusaurus.config.ts` footer section:

```typescript
footer: {
  style: 'dark',
  links: [
    {
      title: 'Learn',
      items: [
        { label: 'Get Started', to: '/docs/preface' },
        { label: 'Chapter 1', to: '/docs/chapter-1' },
      ],
    },
    {
      title: 'Community',
      items: [
        { label: 'GitHub', href: 'https://github.com/...' },
        { label: 'Twitter', href: 'https://twitter.com/...' },
        { label: 'LinkedIn', href: 'https://linkedin.com/...' },
      ],
    },
    {
      title: 'Contact',
      items: [
        { label: 'Email', href: 'mailto:...' },
      ],
    },
  ],
  copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook`,
},
```

## Testing

### Visual Testing

1. Run `pnpm start` and navigate to `http://localhost:3000`
2. Verify all 5 sections are visible (Hero, Journey, Why, Hardware, CTA)
3. Test responsive layout at 996px breakpoint
4. Test on mobile viewport (375px width)

### Accessibility Testing

```bash
# Install Lighthouse CLI (if not installed)
npm install -g lighthouse

# Run accessibility audit
lighthouse http://localhost:3000 --only-categories=accessibility
```

### Build Testing

```bash
# Build production version
pnpm build

# Serve production build locally
pnpm serve
```

## Design Tokens Reference

Use these CSS variables from `custom.css`:

```css
--ifm-color-primary: #BFE600;          /* Lime green */
--ifm-background-color: #000000;       /* Black */
--ifm-color-content: #FFFFFF;          /* White text */
--ifm-font-family-base: 'Space Grotesk', sans-serif;
```

## Common Issues

### Styles not applying
- Ensure CSS module import matches: `import styles from './Component.module.css'`
- Check class name usage: `className={styles.myClass}`

### Components not rendering
- Verify import paths are correct
- Check for TypeScript errors in terminal

### Footer not updating
- Restart dev server after modifying `docusaurus.config.ts`

## Success Criteria Checklist

- [ ] All 5 sections visible on page
- [ ] Hardware tiers show correct information
- [ ] "Get Started Free" navigates to /docs/preface
- [ ] Page loads in < 3 seconds
- [ ] No horizontal scroll on mobile
- [ ] Lighthouse accessibility score > 90
