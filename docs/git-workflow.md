# Git Workflow

VisaAtGlance work separates planning, implementation, review, and push.

## Required Pre-Work Step

Before implementing code, first show the user a concrete proposal and receive confirmation.

| Item | Include |
|---|---|
| Goal | What problem the change solves |
| Approach | Which models, UI, storage, or logic will change |
| Impact | Which screens, data, tests, or existing flows may be affected |
| Alternatives | Other reasonable approaches and why they are not selected |
| MR size | Whether the work fits in one small branch or should be split |

Start implementation after the user confirms the direction.

Exceptions:

- Clear typo fixes
- Broken import fixes
- Direct fixes for failing tests
- User-requested docs-only changes
- Urgent fixes when the app is broken

Even in exceptions, explain the impact before commit or push.

## Branch Strategy

| Branch | Role |
|---|---|
| `main` | Stable version. Avoid direct feature work |
| `codex/<name>` | Codex work branch |

Rules:

- One branch should contain one meaningful change.
- Cross-cutting model, storage, or UI changes should stay small.
- Relevant checks should pass before merging to `main`.

## Commit Rules

- Commit related changes together.
- Do not stage or revert unrelated user changes.
- Separate docs-only changes from code changes when useful.
- Prefer this commit message format:

```text
<type>: <summary>
```

Recommended types:

| Type | Use |
|---|---|
| `feat` | Feature addition |
| `fix` | Bug fix |
| `refactor` | Behavior-preserving structure change |
| `docs` | Documentation change |
| `test` | Test addition or update |
| `chore` | Project maintenance |

## Post-Implementation Review Checklist

Before commit or push, summarize:

- [ ] Changed files and why
- [ ] Potentially affected screens or features
- [ ] Storage, sync, migration, or data compatibility impact
- [ ] Added or updated tests
- [ ] QA commands run and results
- [ ] Manual scenarios checked
- [ ] Docs reviewed for stale or conflicting information
- [ ] Needed docs updates included or separated into a docs change
- [ ] Items not checked and why

## Docs Freshness Rule

Before pushing, quickly review all docs in `docs/`. If code or product decisions changed but docs are stale, update the relevant doc before push or split the docs update into a separate change.

| Doc | Check |
|---|---|
| `docs/README.md` | Document roles, writing rules, and decision process are current |
| `docs/developer-notes.md` | Product behavior, screen purpose, and implementation principles are current |
| `docs/data-model.md` | Models, fields, status values, storage keys, and relationships are current |
| `docs/refactoring-notes.md` | Completed structure work and next steps are current |
| `docs/git-workflow.md` | Planning, QA, and push rules are current |
| `docs/product-spec-v0.1.md` | Initial spec remains archive-only and does not conflict with current standards |

## Pre-Push Checklist

Before pushing, write an impact checklist:

```md
## Pre-Push Impact Checklist

Changed files:
- ...

Potentially affected implementation:
- ...

Checks run:
- ...

Manual checks:
- ...

Docs checked:
- Ready / Updated / Not needed

Not checked:
- ...

Push decision:
- Ready / Not ready
```

Push only when the decision is `Ready`.

## Basic QA

| Change Type | Basic Check |
|---|---|
| Docs-only change | `git diff --check` |
| TypeScript code change | `npx tsc --noEmit` |
| Unit-tested logic | Project test command |
| UI wiring change | Manual smoke check or browser check when available |
| Storage/data model change | Load/save, migration, and existing data compatibility |

## Current QA Limits

| Item | Status |
|---|---|
| App stack | Not selected yet |
| Automated tests | Not configured yet |
| Manual UI check | Starts after the first runnable app exists |
