# Research: Platform Foundation Setup

**Status**: Completed
**Date**: 2025-12-04

## Package Manager Choice
- **Decision**: `npm`
- **Rationale**: Standard stability, no extra toolchain installation required for contributors, full compatibility with Docusaurus CLI.
- **Alternatives Considered**:
    - `yarn` (Standard for Docusaurus but adds extra setup step).
    - `pnpm` (Fast/disk-efficient, but sometimes requires config tweaks for hoisting).

## Deployment Strategy
- **Decision**: GitHub Actions (`deploy.yml`)
- **Rationale**: Automated, auditable deployments triggered by git push. Integrates natively with GitHub Pages.
- **Alternatives Considered**:
    - Manual `npm run deploy` (Prone to human error, "works on my machine").
    - Vercel/Netlify (Excellent, but Constitution mandates GitHub Pages).

## Docusaurus + Lucide-React Compatibility
- **Findings**: `lucide-react` works with React 18+ (Docusaurus v3 dependency).
- **Action**: Install as standard dependency. No special config required.

## Observability
- **Decision**: Google Analytics (GA4)
- **Rationale**: Native plugin support in Docusaurus (`@docusaurus/plugin-google-gtag`).
- **Action**: Configure tracking ID in `docusaurus.config.ts` (placeholder until ID provided).