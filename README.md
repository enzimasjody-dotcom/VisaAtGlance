# VisaAtGlance

VisaAtGlance is a new project for organizing visa-related information into a clear, easy-to-scan product experience.

The exact product scope is still being defined. This repository starts with a documentation-first workflow so product decisions, data shape, refactoring plans, and Git process stay separated as the app grows.

---

## Quick Start

Project setup is not decided yet.

When the app stack is chosen, update this section with the install and run commands.

```bash
# TODO: add setup command
# TODO: add development command
```

---

## Core Direction

| Principle | Description |
|---|---|
| Clarity first | Visa information should be summarized in a way users can scan quickly |
| Source-aware | Visa rules, requirements, and dates should preserve where the information came from |
| User control | The app should avoid making irreversible decisions without user confirmation |
| Shared data base | Product screens should show the same underlying records in different ways |
| Documentation-led | Important product and implementation decisions should be captured in `docs/` |

---

## Docs

| Doc | Purpose |
|---|---|
| [Docs Map](docs/README.md) | Role of each document and writing rules |
| [Developer Notes](docs/developer-notes.md) | Current product and implementation standards |
| [Data Model](docs/data-model.md) | Core models, fields, relationships, and storage notes |
| [Refactoring Notes](docs/refactoring-notes.md) | Structure improvement plan as the codebase grows |
| [Git Workflow](docs/git-workflow.md) | Planning, commit, push, and QA rules |
| [Product Spec v0.1](docs/product-spec-v0.1.md) | Initial product idea archive |

---

## Current Development Focus

| Focus | Status |
|---|---|
| Product scope | Initial definition needed |
| App stack | Not selected |
| Data model | Drafted as a starting point |
| Documentation workflow | Created from the ClassPilot workflow format |
| First implementation | Pending stack and MVP decision |

---

## Basic QA

For docs-only changes:

```bash
git diff --check
```

When the app stack is added, update this section with typecheck, test, and build commands.
