# Merge Checklist (devbranch -> main)

Use this before merging PR #1.

## Quality Gates
- [ ] CI is green on latest `devbranch` commit
- [ ] `make check` passes locally
- [ ] No critical security findings in `docs/DEEP_REVIEW.md`

## Documentation Gates
- [ ] `README.md` reflects actual commands and current architecture
- [ ] `CHANGELOG.md` includes all user-visible changes
- [ ] `docs/API.md` matches emitted server events
- [ ] `docs/RELEASE_NOTES_v0.1.0-rc1.md` reviewed

## Product Gates
- [ ] New user can run first room in <10 minutes
- [ ] `/help`, `/who`, `/pause`, `/resume`, `/topic`, `/stats` verified manually
- [ ] moderation reasons visible in logs and replay tool output

## Git Gates
- [ ] Tag created on reviewed commit: `v0.1.0-rc1`
- [ ] PR title and description finalized
- [ ] Squash/merge policy selected

## Post-merge
- [ ] Create GitHub Release from tag notes
- [ ] Announce quickstart in project README and community channels
- [ ] Open tracking issues for v0.2.0 milestones (auth + richer replay)
