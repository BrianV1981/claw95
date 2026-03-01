# Release Process

## Branching
- All active development lands on `devbranch`.
- `main` receives tested, reviewed merges only.

## Pre-release checklist
- [ ] `make check` passes locally
- [ ] CI green on `devbranch`
- [ ] CHANGELOG updated
- [ ] docs updated for behavior changes
- [ ] threat/audit impacts reviewed

## Cut release
1. Merge `devbranch` -> `main`
2. Create tag: `vX.Y.Z`
3. Publish GitHub release notes from CHANGELOG
4. Announce quickstart + migration notes (if any)
