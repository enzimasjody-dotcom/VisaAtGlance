# Developer Notes

Purpose: maintain the current product and implementation standards for VisaAtGlance.

Non-purpose: field-by-field data details, refactoring order, Git workflow, and initial idea archive are managed in `data-model.md`, `refactoring-notes.md`, `git-workflow.md`, and `product-spec-v0.1.md`.

Last updated: 2026-05-07

## Product Direction

VisaAtGlance helps users understand visa options, requirements, timelines, and next actions at a glance.

The exact MVP is still open. Until it is decided, the project should keep product logic source-aware, easy to revise, and safe around uncertain information.

| Principle | Description |
|---|---|
| At-a-glance clarity | Users should quickly understand the status, requirements, and next steps |
| Source-aware information | Visa details should preserve source, date checked, and confidence where possible |
| No silent certainty | Unverified or ambiguous information should be marked instead of presented as final |
| Shared data base | Search, comparison, checklist, and detail screens should use the same records |
| Portable logic | Domain logic should stay separate from UI and platform-specific code |

## Core Data

Field details live in [Data Model](data-model.md).

| Model | Role |
|---|---|
| `VisaProgram` | A visa type, pathway, or status category |
| `Requirement` | A condition, document, fee, deadline, or eligibility rule |
| `CountryProfile` | Country or jurisdiction context |
| `UserCase` | User-specific situation used to filter or track options |
| `SourceRecord` | Source URL, date checked, and confidence metadata |
| `ChecklistItem` | User-facing next action derived from requirements |

## Source and Confidence Policy

| Rule | Description |
|---|---|
| Keep source metadata | Requirements should link back to where they came from |
| Track freshness | Important records should store `lastCheckedAt` when possible |
| Separate facts from notes | Official requirements and user notes should not be mixed silently |
| Mark uncertainty | Unknown, stale, or unofficial data should be visible in the UI |
| Avoid legal advice framing | The app can organize information, but should not pretend to replace professional advice |

## Planned Screen Areas

These are starting assumptions, not finalized scope.

```text
Overview
Search
Compare
Checklist
Sources
Settings
```

| Area | Purpose | Possible Content |
|---|---|---|
| Overview | Quick summary | Saved visa options, deadlines, missing items, recent source checks |
| Search | Explore options | Country, nationality, purpose, duration, work/study filters |
| Compare | Evaluate paths | Side-by-side requirements, timelines, fees, constraints |
| Checklist | Track actions | Documents, forms, appointments, fees, reminders |
| Sources | Audit data | URLs, official/unofficial flag, last checked date |
| Settings | Preferences | Home country, destination country, status, saved cases |

## Implementation Standards

| Area | Direction |
|---|---|
| Domain logic | Keep visa matching, checklist generation, and source freshness rules outside UI components |
| Storage | Put persistence behind a narrow API once a stack is chosen |
| UI | Prioritize dense, readable, task-focused screens over marketing-style pages |
| Data updates | Prefer explicit review before replacing sourced requirements |
| Tests | Add focused tests around matching, requirements, and checklist generation once logic exists |

## Open Decisions

| Topic | Current Status |
|---|---|
| App stack | Not selected |
| MVP user | Needs decision |
| Data source strategy | Needs decision |
| Offline/local storage vs backend | Needs decision |
| Jurisdiction coverage | Needs decision |
