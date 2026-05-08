# 데이터 모델

목적: VisaAtGlance에서 사용하는 핵심 데이터 구조를 사람이 읽기 쉬운 형태로 정리한다.

비목적: 제품 방향, UI 설계, 리팩터링 순서, Git workflow는 각각 `developer-notes.md`, `refactoring-notes.md`, `git-workflow.md`에서 관리한다.

## 한눈에 보기

VisaAtGlance는 미국 비자/이민 데이터를 다음 객체로 나누어 관리한다.

| 모델 | 한 줄 설명 | 주요 연결 |
|---|---|---|
| `VisaProgram` | 비자 category, pathway, status type | `Requirement`, `SourceRecord`, `TimelineRecord` |
| `Requirement` | 조건, 문서, fee, deadline, eligibility rule | `VisaProgram`, `SourceRecord`, `ChecklistItem` |
| `CountryProfile` | 국가 또는 jurisdiction context | `VisaProgram` |
| `UserCase` | 사용자의 저장된 scenario와 관심 조건 | `TimelineRecord`, `ChecklistItem`, `CohortSummary` |
| `TimelineRecord` | 공개/익명 case timeline의 정규화 record | `VisaProgram`, `UserCase`, `SourceRecord` |
| `CohortSummary` | 유사 case 집단의 집계 통계 | `TimelineRecord`, `PrivacyRule` |
| `SourceRecord` | source URL, checked date, confidence metadata | `VisaProgram`, `Requirement`, `TimelineRecord` |
| `ChecklistItem` | requirement에서 파생된 사용자 action | `Requirement`, `UserCase` |
| `PrivacyRule` | small cohort suppression, row masking 기준 | `TimelineRecord`, `CohortSummary` |

## 모델 책임

| 질문 | 담당 모델 |
|---|---|
| 어떤 비자 category 또는 pathway인가? | `VisaProgram` |
| 사용자가 만족하거나 제출해야 하는 것은 무엇인가? | `Requirement` |
| 어느 국가나 jurisdiction의 데이터인가? | `CountryProfile` |
| 이 사용자의 저장된 관심 조건은 무엇인가? | `UserCase` |
| 이 case timeline은 어떤 단계와 날짜를 갖는가? | `TimelineRecord` |
| 유사 case 집단의 평균, percentile, sample size는 무엇인가? | `CohortSummary` |
| 이 정보는 어디에서 왔고 언제 확인했는가? | `SourceRecord` |
| 사용자가 다음에 해야 할 일은 무엇인가? | `ChecklistItem` |
| 이 데이터는 공개해도 안전한가? | `PrivacyRule` |

## 핵심 관계

```text
CountryProfile
  └─ VisaProgram.countryCode

VisaProgram
  ├─ Requirement.visaProgramId
  ├─ TimelineRecord.visaProgramId
  └─ SourceRecord.subjectId

TimelineRecord
  ├─ CohortSummary.timelineRecordIds
  └─ SourceRecord.subjectId

UserCase
  ├─ TimelineRecord.userCaseId
  └─ ChecklistItem.userCaseId

Requirement
  ├─ ChecklistItem.requirementId
  └─ SourceRecord.subjectId
```

## 저장 요약

저장 방식은 backend scaffold 이후에도 아직 최종 확정하지 않았다. 현재 키는 local/prototype 또는 future DB table 이름의 기준으로 둔다.

| 데이터 | 저장 키 또는 table 후보 |
|---|---|
| `VisaProgram[]` | `visaatglance.visaPrograms.v1` |
| `Requirement[]` | `visaatglance.requirements.v1` |
| `CountryProfile[]` | `visaatglance.countryProfiles.v1` |
| `UserCase[]` | `visaatglance.userCases.v1` |
| `TimelineRecord[]` | `visaatglance.timelineRecords.v1` |
| `CohortSummary[]` | `visaatglance.cohortSummaries.v1` |
| `SourceRecord[]` | `visaatglance.sourceRecords.v1` |
| `ChecklistItem[]` | `visaatglance.checklistItems.v1` |
| `PrivacyRule[]` | `visaatglance.privacyRules.v1` |

## 기본 원칙

- 공개/공식 source와 사용자 입력 timeline을 조용히 섞지 않는다.
- row-level 원본 데이터 공개는 제한하고, 기본 표현은 aggregate-first로 둔다.
- `receiptNumber`, 여권 사본, SSN, full case document는 수집하거나 공개하지 않는다.
- cohort 통계는 sample size와 기준 필드를 함께 보여준다.
- small cohort는 percentile이나 상세 비교를 숨기거나 경고한다.
- source, checked date, limitation은 chart 주변에서 확인 가능해야 한다.

## VisaProgram

`VisaProgram`은 비자 유형, pathway, status category를 나타낸다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 고유 ID | `us-eb2` |
| `countryCode` | `string` | 대상 국가 또는 jurisdiction | `US` |
| `name` | `string` | 사용자에게 보이는 이름 | `EB-2` |
| `category` | `employment \| family \| study \| visitor \| humanitarian \| other` | 큰 분류 | `employment` |
| `summary` | `string` | 짧은 설명 | `Employment-based second preference` |
| `status` | `draft \| active \| archived` | record lifecycle | `draft` |
| `lastReviewedAt` | `string?` | 마지막 검토 시각 ISO string | `2026-05-07T18:00:00.000Z` |

## Requirement

`Requirement`는 사용자가 만족, 제출, 지불, 예약, 이해해야 하는 조건이다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 고유 ID | `req-medical-exam` |
| `visaProgramId` | `string` | 연결된 visa program | `us-eb2` |
| `kind` | `eligibility \| document \| fee \| appointment \| timeline \| restriction \| note` | requirement 종류 | `document` |
| `title` | `string` | 짧은 제목 | `Medical examination` |
| `description` | `string` | 설명 | `Complete required medical examination` |
| `required` | `boolean` | 필수 여부 | `true` |
| `status` | `draft \| verified \| stale \| needs-review` | confidence 상태 | `needs-review` |
| `sourceRecordId` | `string?` | 주요 source | `source-123` |

## TimelineRecord

`TimelineRecord`는 공개/익명 case timeline을 정규화한 record다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 고유 ID | `timeline-123` |
| `visaProgramId` | `string` | 관련 visa category | `us-eb2` |
| `userCaseId` | `string?` | 로그인 사용자의 저장 case일 때 연결 | `case-default` |
| `sourceRecordId` | `string?` | 원본 source 또는 import batch | `source-sheet-001` |
| `filingDate` | `string?` | 접수일 | `2025-01-10` |
| `approvalDate` | `string?` | 승인일 | `2025-09-21` |
| `serviceCenter` | `string?` | service center 또는 processing office | `Nebraska` |
| `caseStatus` | `pending \| approved \| denied \| transferred \| unknown` | 상태 | `approved` |
| `visibility` | `private \| aggregate-only \| public-preview` | 공개 범위 | `aggregate-only` |
| `createdAt` | `string` | 생성 시각 ISO string | `2026-05-07T18:00:00.000Z` |

금지:

- `receiptNumber`를 공개 필드로 두지 않는다.
- 여권 사본, SSN, full case document를 연결하지 않는다.

## CohortSummary

`CohortSummary`는 유사 case 집단의 집계 통계다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 고유 ID | `cohort-eb2-nebraska-2025-q1` |
| `visaProgramId` | `string` | 관련 visa program | `us-eb2` |
| `filters` | `Record<string, string>` | cohort 기준 | `{ "serviceCenter": "Nebraska" }` |
| `sampleSize` | `number` | 표본 수 | `128` |
| `averageWaitDays` | `number?` | 평균 대기일 | `116` |
| `medianWaitDays` | `number?` | 중앙값 대기일 | `109` |
| `percentiles` | `Record<string, number>?` | percentile 집계 | `{ "p75": 142 }` |
| `suppressed` | `boolean` | small cohort 등으로 숨김 여부 | `false` |
| `computedAt` | `string` | 계산 시각 ISO string | `2026-05-07T18:00:00.000Z` |

## SourceRecord

`SourceRecord`는 정보 출처와 freshness를 기록한다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 고유 ID | `source-123` |
| `subjectType` | `visa-program \| requirement \| timeline-record \| country-profile` | 연결 record 종류 | `timeline-record` |
| `subjectId` | `string` | 연결 record ID | `timeline-123` |
| `url` | `string?` | source URL | `https://example.com/sheet` |
| `title` | `string?` | source 제목 | `Public timeline sheet` |
| `sourceKind` | `official \| public-dataset \| crowd-sourced \| user-note` | source 종류 | `crowd-sourced` |
| `checkedAt` | `string` | 확인 시각 ISO string | `2026-05-07T18:00:00.000Z` |
| `confidence` | `high \| medium \| low` | confidence level | `medium` |

## UserCase

`UserCase`는 사용자가 저장한 scenario와 관심 조건을 저장한다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 고유 ID | `case-default` |
| `anonymousUsername` | `string?` | 익명 사용자명 | `casewatcher-17` |
| `email` | `string?` | optional email | `user@example.com` |
| `savedVisaProgramIds` | `string[]` | 저장한 visa category | `["us-eb2"]` |
| `savedCohortIds` | `string[]` | 저장한 cohort | `["cohort-eb2-nebraska-2025-q1"]` |
| `alertOptIn` | `boolean` | alert 수신 여부 | `false` |

## ChecklistItem

`ChecklistItem`은 requirement에서 파생되거나 사용자가 직접 만든 action이다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 고유 ID | `check-123` |
| `userCaseId` | `string` | 연결 user case | `case-default` |
| `requirementId` | `string?` | source requirement | `req-medical-exam` |
| `title` | `string` | action 제목 | `Check medical exam status` |
| `dueAt` | `string?` | 선택 due date | `2026-06-01T17:00:00.000Z` |
| `status` | `open \| completed \| hidden` | 진행 상태 | `open` |

## PrivacyRule

`PrivacyRule`은 데이터 공개와 cohort 계산의 안전장치다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 고유 ID | `privacy-small-cohort` |
| `name` | `string` | 규칙 이름 | `Small cohort suppression` |
| `minimumSampleSize` | `number` | 통계 표시 최소 표본 수 | `20` |
| `hidePercentilesBelowMinimum` | `boolean` | 작은 표본에서 percentile 숨김 | `true` |
| `maskRowLevelData` | `boolean` | row-level data masking | `true` |

## 아직 확정되지 않은 부분

| 주제 | 현재 상태 |
|---|---|
| DB 선택 | 아직 확정하지 않음 |
| Google Sheet import schema | 다음 단계에서 샘플 기반 검토 |
| USCIS/Visa Bulletin ingestion 방식 | 다음 단계에서 결정 |
| small cohort 기준값 | 초기 후보 필요 |
| user deletion flow | 로그인 기능 전 설계 필요 |
