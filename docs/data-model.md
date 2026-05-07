# Data Model

Purpose: describe the core VisaAtGlance data structures in a human-readable way.

Non-purpose: product direction, UI design, refactoring order, and Git workflow are managed in `developer-notes.md`, `refactoring-notes.md`, and `git-workflow.md`.

## At a Glance

VisaAtGlance starts with these conceptual models.

| Model | One-Line Description | Main Links |
|---|---|---|
| `VisaProgram` | A visa type, pathway, or status category | `Requirement`, `CountryProfile`, `SourceRecord` |
| `Requirement` | A condition, document, fee, deadline, or eligibility rule | `VisaProgram`, `SourceRecord`, `ChecklistItem` |
| `CountryProfile` | Country or jurisdiction context | `VisaProgram` |
| `UserCase` | User-specific situation and saved preferences | `VisaProgram`, `ChecklistItem` |
| `SourceRecord` | Source URL, date checked, and confidence metadata | `VisaProgram`, `Requirement` |
| `ChecklistItem` | User-facing action derived from a requirement | `Requirement`, `UserCase` |

## Model Responsibilities

| Question | Model |
|---|---|
| What visa option is this? | `VisaProgram` |
| What must the user satisfy or submit? | `Requirement` |
| Which country or jurisdiction does this belong to? | `CountryProfile` |
| What is true about this user scenario? | `UserCase` |
| Where did this information come from? | `SourceRecord` |
| What should the user do next? | `ChecklistItem` |

## Core Relationships

```text
CountryProfile
  └─ VisaProgram.countryCode

VisaProgram
  ├─ Requirement.visaProgramId
  └─ SourceRecord.subjectId

Requirement
  ├─ ChecklistItem.requirementId
  └─ SourceRecord.subjectId

UserCase
  └─ ChecklistItem.userCaseId
```

## Storage Summary

Storage keys are placeholders until the app stack and persistence layer are chosen.

| Data | Storage Key |
|---|---|
| `VisaProgram[]` | `visaatglance.visaPrograms.v1` |
| `Requirement[]` | `visaatglance.requirements.v1` |
| `CountryProfile[]` | `visaatglance.countryProfiles.v1` |
| `UserCase[]` | `visaatglance.userCases.v1` |
| `SourceRecord[]` | `visaatglance.sourceRecords.v1` |
| `ChecklistItem[]` | `visaatglance.checklistItems.v1` |

## Base Principles

- Store each visa program once.
- Store each requirement once and connect it to a visa program.
- Keep source metadata separate from user notes.
- Preserve stale or uncertain information as reviewable instead of deleting it silently.
- Treat screens as views of shared records, not separate copies.

## VisaProgram

`VisaProgram` represents a visa type, pathway, or status category.

| Field | Type | Purpose | Example |
|---|---|---|---|
| `id` | `string` | Unique ID | `us-f1-student` |
| `countryCode` | `string` | Destination country or jurisdiction | `US` |
| `name` | `string` | User-facing name | `F-1 Student Visa` |
| `category` | `tourism \| study \| work \| family \| transit \| other` | Broad grouping | `study` |
| `summary` | `string` | Short explanation | `For academic study in the United States` |
| `status` | `draft \| active \| archived` | Record lifecycle | `draft` |
| `lastReviewedAt` | `string?` | ISO date/time when reviewed | `2026-05-07T18:00:00.000Z` |

## Requirement

`Requirement` describes something the user must satisfy, submit, pay, schedule, or understand.

| Field | Type | Purpose | Example |
|---|---|---|---|
| `id` | `string` | Unique ID | `req-passport-validity` |
| `visaProgramId` | `string` | Related visa program | `us-f1-student` |
| `kind` | `eligibility \| document \| fee \| appointment \| timeline \| restriction \| note` | Requirement type | `document` |
| `title` | `string` | Short label | `Valid passport` |
| `description` | `string` | Requirement detail | `Passport must be valid for the required period` |
| `required` | `boolean` | Whether it is mandatory | `true` |
| `status` | `draft \| verified \| stale \| needs-review` | Confidence state | `needs-review` |
| `sourceRecordId` | `string?` | Primary source record | `source-123` |

## CountryProfile

`CountryProfile` describes a country or jurisdiction used by visa programs.

| Field | Type | Purpose | Example |
|---|---|---|---|
| `code` | `string` | ISO-like country code | `US` |
| `name` | `string` | Display name | `United States` |
| `officialVisaSiteUrl` | `string?` | Main official visa source | `https://travel.state.gov/` |
| `notes` | `string?` | Internal notes | `Use official source first` |

## UserCase

`UserCase` stores the user's scenario for filtering and checklist generation.

| Field | Type | Purpose | Example |
|---|---|---|---|
| `id` | `string` | Unique ID | `case-default` |
| `name` | `string` | Display name | `My study plan` |
| `citizenshipCountryCode` | `string?` | User citizenship | `KR` |
| `destinationCountryCode` | `string?` | Destination | `US` |
| `purpose` | `string?` | Travel or immigration purpose | `study` |
| `targetStartDate` | `string?` | Relevant date | `2026-08-15` |
| `savedVisaProgramIds` | `string[]` | Saved options | `["us-f1-student"]` |

## SourceRecord

`SourceRecord` records where information came from and how fresh it is.

| Field | Type | Purpose | Example |
|---|---|---|---|
| `id` | `string` | Unique ID | `source-123` |
| `subjectType` | `visa-program \| requirement \| country-profile` | Linked record type | `requirement` |
| `subjectId` | `string` | Linked record ID | `req-passport-validity` |
| `url` | `string` | Source URL | `https://example.gov/visa` |
| `title` | `string?` | Source title | `Student visa requirements` |
| `sourceKind` | `official \| unofficial \| user-note` | Source category | `official` |
| `checkedAt` | `string` | ISO date/time checked | `2026-05-07T18:00:00.000Z` |
| `confidence` | `high \| medium \| low` | Confidence level | `medium` |

## ChecklistItem

`ChecklistItem` is a user-facing action derived from a requirement or created manually.

| Field | Type | Purpose | Example |
|---|---|---|---|
| `id` | `string` | Unique ID | `check-123` |
| `userCaseId` | `string` | Related user case | `case-default` |
| `requirementId` | `string?` | Source requirement | `req-passport-validity` |
| `title` | `string` | Action label | `Check passport expiration date` |
| `dueAt` | `string?` | Optional due date/time | `2026-06-01T17:00:00.000Z` |
| `status` | `open \| completed \| hidden` | User progress | `open` |

## Undecided Areas

| Topic | Status |
|---|---|
| Exact enum values | Draft |
| Backend schema | Not selected |
| Data import format | Not selected |
| Source freshness policy | Needs decision |
| Legal disclaimer model | Needs decision |
