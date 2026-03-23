# Claw95 OSS Intake Policy

## Purpose
Claw95 is open-sourcing the core under the MIT License.

This document defines how ideas, patterns, and code from other repositories may be evaluated and incorporated without creating licensing confusion or accidental contamination.

---

## Core Policy
### 1. Prefer learning over copying
The safest default is:
- study architecture
- study behavior
- study UX patterns
- reimplement cleanly in Claw95

### 2. Permissive-license repos
If a dependency or reference repo is licensed under a permissive license such as:
- MIT
- BSD
- Apache-2.0

Then code reuse may be considered, but only when:
- the origin is documented
- license obligations are respected
- copied code is small, justified, and understandable

### 3. Copyleft or restrictive repos
If a repo is licensed under:
- GPL
- AGPL
- LGPL (depending on integration details)
- custom restrictive terms
- unknown / missing license

Then Claw95 core should treat it as:
- **idea/reference only**
- no direct code copying into MIT core
- clean-room reimplementation preferred

---

## Intake Checklist
Before incorporating anything substantial from another repo, record:
1. project/repo name
2. URL
3. license type
4. what we want from it
5. whether we are copying code or only learning from the idea
6. what attribution or notices are required

---

## Current Default Rule for Claw95
Unless explicitly reviewed and documented otherwise:

> Extract ideas, patterns, and behaviors first. Do not casually copy third-party code into the Claw95 core.

---

## Recommended Future Expansion
If Claw95 begins systematically reviewing other repos, maintain a structured matrix covering:
- repo
- license
- reusable ideas
- code reuse allowed? (yes/no)
- attribution required? (yes/no)
- notes
