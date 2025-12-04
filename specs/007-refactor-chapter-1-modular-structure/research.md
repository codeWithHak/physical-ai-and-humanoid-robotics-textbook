# Research Findings: Refactor Chapter 1

**Phase**: 0 (Research)
**Status**: Complete
**Date**: 2025-12-04

## Summary

This is a structural refactor supported natively by Docusaurus. No unknowns.

- **Sidebar Ordering**: `sidebar_position` frontmatter is the correct mechanism.
- **Imports**: Relative imports like `import HardwareCheck from '@site/src/components/HardwareCheck';` work regardless of depth, as long as `@site` alias is used (standard). If relative paths (`../../`) were used, they would need updating, but absolute `@site` imports are safer.

**Decision**: Proceed directly to implementation.
