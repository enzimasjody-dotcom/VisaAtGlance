# VisaAtGlance Product Spec v0.1

Purpose: archive the first product idea for VisaAtGlance.

Non-purpose: this document is not the current source of truth for implementation, data model, Git workflow, or refactoring plans.

Current standards docs:

| Topic | Doc |
|---|---|
| Current product and implementation standards | [Developer Notes](developer-notes.md) |
| Current data model | [Data Model](data-model.md) |
| Refactoring plan | [Refactoring Notes](refactoring-notes.md) |
| Work process | [Git Workflow](git-workflow.md) |

The notes below are an initial product sketch and should be refined after the MVP user and stack are chosen.

## Product Thesis

VisaAtGlance helps users turn scattered visa information into a clear overview of options, requirements, timelines, and next actions.

Visa research often spans official government pages, school or employer instructions, personal documents, deadlines, and uncertain edge cases. Users need a way to see what applies to them, what is missing, and which facts need re-checking.

## Target User

Initial target user needs a decision.

Possible starting users:

- International students comparing study visa requirements
- Travelers checking visitor visa requirements
- Workers tracking employment visa steps
- Families organizing dependent visa paperwork

## Core Concept

VisaAtGlance separates information into four concepts:

1. Visa programs
2. Requirements
3. Source records
4. User checklists

This distinction matters because a visa option is not the same as a document requirement, and a requirement is not the same as the user's personal action item.

## Primary Screens

### Overview

Shows the user's saved visa paths, open checklist items, important dates, and source freshness warnings.

### Search

Lets users explore visa options by destination, citizenship, purpose, duration, and other filters.

### Compare

Shows visa programs side by side with requirements, fees, timelines, restrictions, and source status.

### Checklist

Turns requirements into trackable actions.

Actions may include:

- Mark complete
- Add due date
- Add note
- Link to source
- Hide if not applicable

### Sources

Shows where information came from, whether it is official, and when it was last checked.

## Data Source Strategy

The first implementation should avoid pretending that uncertain data is verified.

Default policy:

- Prefer official sources.
- Store source URL and checked date.
- Mark unofficial or stale data clearly.
- Let users keep personal notes separate from sourced facts.
- Avoid irreversible overwrites when requirements are updated.

## Current MVP Questions

| Question | Needed Decision |
|---|---|
| First user type | Student, traveler, worker, or another segment |
| First destination coverage | One country first or multi-country from the start |
| Data entry method | Manual entry, curated seed data, import, or admin tool |
| App stack | Next.js, React/Vite, mobile-first app, or another stack |
| Persistence | Local-only first or backend from the start |

## Product Principles

- Make complex visa information scannable.
- Preserve source and freshness metadata.
- Mark uncertainty instead of hiding it.
- Separate official requirements from user notes.
- Turn requirements into actionable checklists.
