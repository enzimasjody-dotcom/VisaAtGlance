# Docs Map

VisaAtGlance docs separate product decisions, data structure, refactoring plans, and Git workflow so the repository stays easy to maintain.

## Document Roles

| Doc | Role | Update When |
|---|---|---|
| [Developer Notes](developer-notes.md) | Current product and implementation standards | Product behavior, screen purpose, or implementation principles change |
| [Data Model](data-model.md) | Core data structures and field descriptions | Models, fields, storage keys, or relationships change |
| [Refactoring Notes](refactoring-notes.md) | Code structure improvement plan | Folder structure, extraction order, or structural debt changes |
| [Git Workflow](git-workflow.md) | Planning, commit, push, and QA rules | Development procedure or checklist changes |
| [Product Spec v0.1](product-spec-v0.1.md) | Initial idea archive | Usually not edited after the current standards docs exist |

## Writing Rules

| Rule | Description |
|---|---|
| Record final decisions | Do not copy the whole brainstorming process into docs |
| Pick the doc owner first | Decide which document owns the change before editing |
| Remove conflicts | When an old decision changes, update the old text instead of adding a contradictory note |
| Keep it short | Prefer tables, checklists, and examples over long prose |
| Avoid extra docs | Add a section to an existing doc unless a new doc has a clear long-term role |
| Review docs before push | Before pushing, scan `docs/` for stale or conflicting information |

## New Decision Recording Process

1. Confirm the direction in conversation first.
2. Choose the document that owns the decision.
3. Record only the final decision and short reasoning.
4. If QA changes, update [Git Workflow](git-workflow.md).
5. If structure changes, update [Refactoring Notes](refactoring-notes.md).
6. Before pushing, scan all docs for consistency.

## New Document Criteria

Create a new doc only when all of these are true:

- The topic will be updated repeatedly.
- The topic is clearly different from existing document roles.
- Adding it to an existing doc would make that doc harder to read.

Otherwise, add a section to the closest existing document.
