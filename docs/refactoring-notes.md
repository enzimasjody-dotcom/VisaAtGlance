# Refactoring Notes

Purpose: manage VisaAtGlance code structure plans and structural debt as the project grows.

Non-purpose: product behavior, data model, and Git workflow are managed in `developer-notes.md`, `data-model.md`, and `git-workflow.md`.

## Why This Exists

VisaAtGlance is starting documentation-first. Once implementation begins, visa matching, checklist generation, source tracking, UI state, and persistence can become tangled quickly.

This document keeps structure decisions explicit and small.

## Current State

| Area | Status |
|---|---|
| App code | Not created yet |
| Domain logic | Planned |
| Storage | Planned |
| Tests | Planned |
| Docs workflow | Created |

## Initial Structure Direction

The exact framework is not selected yet. This target shape should be adapted to the chosen stack.

```txt
VisaAtGlance/
  README.md
  docs/

  src/
    domain/
      types.ts
      visaPrograms.ts
      requirements.ts
      checklist.ts
      sources.ts

    storage/
      storageKeys.ts
      migrations.ts
      planStorage.ts

    components/
      common/
      overview/
      search/
      compare/
      checklist/
      sources/
      settings/

    state/
      useVisaData.ts
      useUserCase.ts

    theme/
      colors.ts
      spacing.ts
      typography.ts
```

This is a direction, not a command to create every folder immediately.

## Refactoring Principles

| Principle | Description |
|---|---|
| Preserve behavior | Refactoring changes should avoid product behavior changes unless explicit |
| Small changes | Avoid large structure rewrites in one MR |
| Move when boundaries are visible | Do not create abstractions before repeated shape is clear |
| Domain is UI-independent | Visa matching, requirement rules, and checklist logic should not depend on components |
| Storage has a narrow API | Persistence details should not leak across screens |
| UI stays task-focused | Product screens should remain clear, dense, and practical |

## Feature Gates

Before larger features, consider whether these foundations are needed:

| Gate | Purpose |
|---|---|
| Domain types | Keep visa, requirement, source, and checklist records consistent |
| Source freshness helper | Avoid duplicating stale/verified logic across screens |
| Checklist generator | Keep user-facing next actions consistent |
| Storage API | Make later backend or local storage changes easier |
| Basic tests | Protect matching and checklist logic |

## Not Yet

| Item | Reason |
|---|---|
| Global state library | Wait until app complexity justifies it |
| Full backend design | Product scope and data source strategy are not decided |
| Large UI redesign | First implementation should prove the workflow |
| Complex recommendation engine | Start with transparent checklist and comparison logic |
| Automated scraping assumptions | Visa information requires careful source and freshness policy |

## Refactor MR Checklist

- [ ] Behavior is preserved unless product change is explicit
- [ ] Unrelated product changes are not mixed in
- [ ] New modules have clear ownership
- [ ] Domain logic remains reusable outside the UI
- [ ] Storage changes include compatibility notes when needed
- [ ] Tests or manual checks match the risk of the change
- [ ] Docs are updated if structure decisions changed
