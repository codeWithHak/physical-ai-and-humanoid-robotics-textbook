# ADR-0002: Package Manager Standardization

> **Scope**: Development Environment and Tooling

- **Status:** Accepted
- **Date:** 2025-12-04
- **Feature:** 001-platform-foundation-setup
- **Context:** A consistent development environment is crucial for a reproducible build pipeline and developer onboarding. We need to select a package manager for the Node.js/TypeScript ecosystem that balances performance with ease of use.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? Yes (dev workflows).
     2) Alternatives: Multiple viable options considered with tradeoffs? Yes.
     3) Scope: Cross-cutting concern (not an isolated detail)? Yes.
-->

## Decision

We will use **npm** (Node Package Manager) as the standard package manager.

- **Tool**: npm (latest stable version included with Node.js LTS)
- **Lockfile**: `package-lock.json`

## Consequences

### Positive

- **Standardization**: Comes pre-installed with Node.js; no additional global installation steps required for contributors.
- **Compatibility**: Broadest compatibility with CI/CD tools and other ecosystem libraries.
- **Simplicity**: Lower barrier to entry for users who may be new to the JS ecosystem (given this is a Robotics textbook).

### Negative

- **Performance**: Installation speed is generally slower than pnpm.
- **Disk Space**: Uses more disk space (hoisted `node_modules`) compared to pnpm's content-addressable store.

## Alternatives Considered

### pnpm
- **Pros**: Significantly faster installs, efficient disk usage, strict dependency handling (avoids phantom dependencies).
- **Cons**: Requires extra installation step. Strictness can sometimes break widely-used tools that rely on hoisting.
- **Rationale**: Rejected to prioritize simplicity and lower barrier to entry for a diverse audience (robotics engineers, students).

### Yarn (v1 or Berry)
- **Pros**: Popular, historically faster than npm.
- **Cons**: Yarn v1 is legacy; Yarn Berry (PnP) has a learning curve and compatibility quirks.
- **Rationale**: npm has largely caught up in performance and reliability, making the extra tool unnecessary.

## References

- Feature Spec: specs/001-platform-foundation-setup/spec.md
- Implementation Plan: specs/001-platform-foundation-setup/plan.md