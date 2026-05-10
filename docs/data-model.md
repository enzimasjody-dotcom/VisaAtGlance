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
| `UserCase` | 로그인 사용자의 저장된 관심 조건과 claim한 case 목록 | `CaseRecord`, `ChecklistItem`, `CohortSummary` |
| `CaseRecord` | 사용자가 생성하거나 claim한 I-485 case의 안정적인 기본 record | `CaseEvent`, `CaseEditToken`, `CaseClaim`, `TimelineRecord` |
| `CaseEvent` | case 진행 중 계속 업데이트되는 timeline event | `CaseRecord`, `SourceRecord` |
| `CaseEditToken` | 로그인 없이 case를 수정할 수 있는 private edit link 권한 | `CaseRecord` |
| `CaseClaim` | 익명 case를 로그인 계정에 연결한 기록 | `CaseRecord`, `UserCase` |
| `DuplicateCandidate` | 비슷한 case가 이미 있는지 판단하는 내부 후보 | `CaseRecord` |
| `TimelineRecord` | 외부 source 또는 import 데이터를 정규화한 aggregate 입력 record | `VisaProgram`, `CaseRecord`, `SourceRecord` |
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
| 이 사용자의 저장된 관심 조건과 claim한 case는 무엇인가? | `UserCase` |
| 이 case의 안정적인 기본 정보는 무엇인가? | `CaseRecord` |
| 이 case timeline은 어떤 단계와 날짜를 갖는가? | `CaseEvent` |
| 로그인 없이 이 case를 다시 수정할 수 있는가? | `CaseEditToken` |
| 익명 case가 로그인 계정에 연결되었는가? | `CaseClaim` |
| 비슷한 case가 이미 있는가? | `DuplicateCandidate` |
| 유사 case 집단의 평균, percentile, sample size는 무엇인가? | `CohortSummary` |
| 이 정보는 어디에서 왔고 언제 확인했는가? | `SourceRecord` |
| 사용자가 다음에 해야 할 일은 무엇인가? | `ChecklistItem` |
| 이 데이터는 공개해도 안전한가? | `PrivacyRule` |

## 핵심 관계

```text
CountryProfile
  └─ VisaProgram.countryCode

UserCase
  ├─ CaseClaim.userCaseId
  ├─ CaseRecord.ownerUserCaseId
  └─ ChecklistItem.userCaseId

CaseRecord
  ├─ CaseEvent.caseRecordId
  ├─ CaseEditToken.caseRecordId
  ├─ CaseClaim.caseRecordId
  ├─ DuplicateCandidate.caseRecordId
  └─ TimelineRecord.caseRecordId

VisaProgram
  ├─ Requirement.visaProgramId
  ├─ CaseRecord.visaProgramId
  ├─ TimelineRecord.visaProgramId
  └─ SourceRecord.subjectId

TimelineRecord
  ├─ CohortSummary.timelineRecordIds
  └─ SourceRecord.subjectId

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
| `CaseRecord[]` | `visaatglance.caseRecords.v1` |
| `CaseEvent[]` | `visaatglance.caseEvents.v1` |
| `CaseEditToken[]` | `visaatglance.caseEditTokens.v1` |
| `CaseClaim[]` | `visaatglance.caseClaims.v1` |
| `DuplicateCandidate[]` | `visaatglance.duplicateCandidates.v1` |
| `TimelineRecord[]` | `visaatglance.timelineRecords.v1` |
| `CohortSummary[]` | `visaatglance.cohortSummaries.v1` |
| `SourceRecord[]` | `visaatglance.sourceRecords.v1` |
| `ChecklistItem[]` | `visaatglance.checklistItems.v1` |
| `PrivacyRule[]` | `visaatglance.privacyRules.v1` |

## 기본 원칙

- 공개/공식 source와 사용자 입력 timeline을 조용히 섞지 않는다.
- 사용자 입력은 1회 제출 row가 아니라 `CaseRecord + CaseEvent` 업데이트 구조로 관리한다.
- 익명 사용자는 private edit link로 같은 case를 계속 업데이트할 수 있고, 로그인 후 optional claim으로 계정에 연결할 수 있다.
- row-level 원본 데이터 공개는 제한하고, 기본 표현은 aggregate-first로 둔다.
- `receiptNumber`, 여권 사본, SSN, full case document는 공개하지 않는다. receipt number가 중복 방지를 위해 필요해지면 원문을 저장하지 않고 hash 처리하며 삭제 가능해야 한다.
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

`TimelineRecord`는 i485tracker 형식에 가까운 normalized I-485 source snapshot이다. Spreadsheet, public dataset, imported user contribution은 ingestion 단계에서 이 형식으로 변환되어 aggregate 계산에 들어간다.

사용자가 직접 입력하고 계속 업데이트하는 제품 내부 모델은 `CaseRecord + CaseEvent`가 기준이다. `TimelineRecord`는 외부 source shape를 보존한 normalized layer이며, 필요할 때 `caseRecordId`로 내부 case와 연결할 수 있다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 고유 ID | `source-i485tracker-dev:case-1` |
| `caseRecordId` | `string?` | 내부 case와 연결된 경우의 ID | `case-abc123` |
| `pd` | `string?` | priority date | `2023-07-07` |
| `cat` | `string` | visa category | `EB2 NIW` |
| `filed` | `string?` | I-485 filed/received date | `2026-04-01` |
| `receipt` | `string?` | receipt notice date | `2026-04-06` |
| `receiptBlock` | `string?` | partial receipt block only | `IOE09362` |
| `bio` | `string?` | biometric date | `2026-04-14` |
| `ead` | `string?` | EAD approval date | `2026-05-01` |
| `ap` | `string?` | Advance Parole approval date | `2026-05-01` |
| `fieldOffice` | `string?` | field office 또는 processing office | `NBC` |
| `foTransferDate` | `string?` | field office transfer date | `2026-04-21` |
| `silent` | `string[]` | silent update dates | `["2026-04-15"]` |
| `gcApproved` | `string?` | green card approval date | `2026-05-02` |
| `gcReceived` | `string?` | green card received date | `2026-05-08` |
| `interview` | `string?` | interview date, if structured | `2026-04-15` |
| `coc` | `string?` | country of concern marker | `75 COC` |
| `rfe` | `string?` | RFE status | `None` |
| `region` | `ROW \| NROW?` | ROW grouping | `ROW` |
| `applicantGroup` | `string?` | single/spouse/kids grouping | `Spouse` |
| `notes` | `string?` | free-text notes | `Interview waived` |
| `lastUpdated` | `string?` | last updated date | `2026-05-07` |
| `hasPassword` | `boolean` | dev/user-contributed row lock hint | `false` |
| `source_id` | `string?` | source record ID | `source-apr-26` |
| `visibility` | `private \| aggregate-only \| public-preview` | 공개 범위 | `aggregate-only` |
| `createdAt` | `string` | 생성 시각 ISO string | `2026-05-07T18:00:00.000Z` |

금지:

- full `receiptNumber`를 저장하거나 공개하지 않는다. 개발용 adapter도 `receipt_num`은 partial `receiptBlock`으로 제한한다.
- 여권 사본, SSN, full case document를 연결하지 않는다.
- `notes`, `coc`, `receiptBlock`은 public dashboard row에 직접 노출하지 않고 aggregate/privacy guard 뒤에 둔다.

## CaseRecord

`CaseRecord`는 사용자가 생성하거나 나중에 claim할 수 있는 I-485 case의 안정적인 기본 record다. 한 번 만든 뒤 같은 case에 `CaseEvent`가 계속 추가되거나 수정된다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 내부 case ID. edit token과 분리 | `case-abc123` |
| `publicCaseKey` | `string` | URL 또는 UI에서 쓰는 비밀이 아닌 case key | `c_9f12ab` |
| `ownerUserCaseId` | `string?` | 로그인 후 claim된 사용자 case ID | `case-default` |
| `visaProgramId` | `string?` | 연결된 visa program | `us-eb2` |
| `formType` | `string` | 신청 form | `I-485` |
| `category` | `string` | visa category | `EB2 NIW` |
| `country` | `string?` | country 또는 ROW/NROW 후보 | `ROW` |
| `serviceCenter` | `string?` | service center 또는 processing office | `NBC` |
| `fieldOffice` | `string?` | field office | `Chicago, IL` |
| `priorityDate` | `string?` | priority date | `2023-08-17` |
| `filedDate` | `string?` | filed date | `2024-12-20` |
| `receiptDate` | `string?` | receipt notice date | `2026-03-27` |
| `receiptHash` | `string?` | 중복 방지용 hash. 원문 저장 금지 | `sha256:...` |
| `receiptBlock` | `string?` | 공개하지 않는 partial block 후보 | `IOE09361` |
| `sourceKind` | `user-submitted \| imported-public \| claimed-import` | 생성 경로 | `user-submitted` |
| `visibility` | `private \| aggregate-only` | 공개 범위 | `aggregate-only` |
| `status` | `active \| archived \| deleted` | case lifecycle | `active` |
| `createdAt` | `string` | 생성 시각 ISO string | `2026-05-09T18:00:00.000Z` |
| `updatedAt` | `string` | 마지막 업데이트 시각 ISO string | `2026-05-10T18:00:00.000Z` |

기준:

- `publicCaseKey`는 case 식별용이며 수정 권한을 주지 않는다.
- 수정 권한은 `CaseEditToken`이 담당한다.
- receipt number를 받는 경우에도 원문은 저장하지 않고 `receiptHash`만 저장한다.
- `receiptBlock`, `country`, `fieldOffice`, `serviceCenter` 조합이 rare detail이 될 수 있으므로 public row에는 직접 노출하지 않는다.

## CaseEvent

`CaseEvent`는 case timeline에서 계속 업데이트되는 개별 사건이다. i485tracker raw field의 `bio`, `ead`, `ap`, `fo_transfer_date`, `silent`, `gc_approved`, `gc_received`, `interview`, `rfe` 같은 날짜/상태는 내부 모델에서 event로 분리한다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | event ID | `event-123` |
| `caseRecordId` | `string` | 연결 case | `case-abc123` |
| `eventType` | `filed \| receipt \| biometrics \| ead_approved \| ap_approved \| field_office_transfer \| silent_update \| interview \| rfe \| rfe_response \| approved \| card_received \| other` | timeline event 종류 | `biometrics` |
| `eventDate` | `string?` | event 날짜 | `2026-04-30` |
| `eventStatus` | `active \| corrected \| deleted` | 수정 이력 상태 | `active` |
| `metadata` | `Record<string, string>?` | 구조화 가능한 추가 정보 | `{ "rfe": "medical" }` |
| `note` | `string?` | private note. public 직접 노출 금지 | `2 FTA0s after Biometrics.` |
| `sourceRecordId` | `string?` | source 연결 | `source-i485tracker-full-cache` |
| `createdAt` | `string` | 생성 시각 ISO string | `2026-05-09T18:00:00.000Z` |
| `updatedAt` | `string` | 수정 시각 ISO string | `2026-05-10T18:00:00.000Z` |

기준:

- 같은 case에 여러 event를 누적해 업데이트한다.
- 사용자가 날짜를 고치면 기존 event를 덮어쓰기보다 `corrected` 상태 또는 audit 가능한 update로 관리하는 방향을 우선 검토한다.
- public dashboard는 `CaseEvent` row를 직접 노출하지 않고 aggregate 계산 결과만 표시한다.

## CaseEditToken

`CaseEditToken`은 로그인 없이 case를 다시 수정할 수 있게 하는 private edit link 권한이다. URL에 포함되는 원문 token은 사용자에게 한 번 보여주되, 저장소에는 hash만 둔다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | token record ID | `edit-token-123` |
| `caseRecordId` | `string` | 수정 가능한 case | `case-abc123` |
| `tokenHash` | `string` | edit token hash. 원문 저장 금지 | `sha256:...` |
| `scope` | `edit-case \| claim-case` | 권한 범위 | `edit-case` |
| `createdAt` | `string` | 생성 시각 ISO string | `2026-05-09T18:00:00.000Z` |
| `lastUsedAt` | `string?` | 마지막 사용 시각 | `2026-05-10T18:00:00.000Z` |
| `expiresAt` | `string?` | 만료 시각. 초기에는 optional | `2026-08-09T18:00:00.000Z` |
| `revokedAt` | `string?` | 폐기 시각 | `2026-05-11T18:00:00.000Z` |

보안 기준:

- edit link는 사실상 비밀번호처럼 취급한다.
- analytics, log, referrer, public page에 edit token이 남지 않게 한다.
- public case key와 edit token은 분리한다.
- 사용자가 로그인 후 claim하면 기존 edit token을 유지할지 폐기할지 별도 정책으로 정한다.

## CaseClaim

`CaseClaim`은 익명 case를 나중에 로그인 계정에 연결한 기록이다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | claim ID | `claim-123` |
| `caseRecordId` | `string` | claim 대상 case | `case-abc123` |
| `userCaseId` | `string` | 연결되는 로그인 사용자 case/profile | `case-default` |
| `claimMethod` | `edit-token \| receipt-hash-review \| admin-review` | claim 방식 | `edit-token` |
| `claimedAt` | `string` | claim 시각 ISO string | `2026-05-10T18:00:00.000Z` |
| `revokedAt` | `string?` | claim 해제 시각 | `null` |

기준:

- 초기 입력은 로그인 없이 가능해야 한다.
- 로그인 후 `Claim this case` 흐름으로 saved timeline, alerts, custom dashboard와 연결한다.
- claim은 공개 output을 바꾸지 않고 private ownership만 바꾼다.

## DuplicateCandidate

`DuplicateCandidate`는 새 입력이 기존 case와 너무 비슷할 때 사용자에게 기존 case 업데이트를 제안하기 위한 내부 판단 결과다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 후보 ID | `dup-123` |
| `caseRecordId` | `string` | 기존 case | `case-abc123` |
| `candidateInputHash` | `string` | 새 입력 조합의 hash | `sha256:...` |
| `matchedFields` | `string[]` | 비슷하다고 판단한 필드 | `["formType", "category", "filedDate"]` |
| `score` | `number` | 유사도 점수 | `0.86` |
| `createdAt` | `string` | 생성 시각 ISO string | `2026-05-10T18:00:00.000Z` |

초기 중복 후보 필드:

- `formType`
- `category`
- `country`
- `serviceCenter`
- `fieldOffice`
- `filedDate`
- `receiptDate`
- `priorityDate`
- `biometricsDate`

기준:

- 중복 후보는 자동 병합하지 않는다.
- 사용자에게 “비슷한 케이스가 이미 있습니다. 기존 케이스를 업데이트하시겠습니까?” 수준으로 제안한다.
- receipt number를 쓰는 경우에도 원문 비교가 아니라 hash 또는 파생값 비교만 허용한다.

## CohortSummary

`CohortSummary`는 유사 case 집단의 집계 통계다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 고유 ID | `cohort-eb2-nebraska-2025-q1` |
| `visaProgramId` | `string` | 관련 visa program | `us-eb2` |
| `filters` | `Record<string, string>` | cohort 기준 | `{ "serviceCenter": "Nebraska" }` |
| `sample_size` | `number` | 표본 수 | `128` |
| `averageWaitDays` | `number?` | 평균 대기일 | `116` |
| `medianWaitDays` | `number?` | 중앙값 대기일 | `109` |
| `percentiles` | `Record<string, number>?` | percentile 집계 | `{ "p75": 142 }` |
| `suppressed` | `boolean` | small cohort 등으로 숨김 여부 | `false` |
| `computedAt` | `string` | 계산 시각 ISO string | `2026-05-07T18:00:00.000Z` |

## PublicDashboardSummary

`PublicDashboardSummary`는 public dashboard가 읽는 aggregate-only 응답이다. `TimelineRecord` row를 직접 노출하지 않고, `PrivacyRule`을 통과한 집계와 source transparency metadata만 담는다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `total_records` | `number` | 전체 normalized record 수 | `480` |
| `approved_records` | `number` | approval date가 있어 처리기간 계산 가능한 후보 | `53` |
| `pending_records` | `number` | 아직 승인일이 없는 record 수 | `427` |
| `category_counts` | `DashboardBucket[]` | category별 aggregate count | `[{ "label": "EB2 NIW", "count": 120 }]` |
| `field_office_counts` | `DashboardBucket[]` | field office별 aggregate count | `[{ "label": "NBC", "count": 103 }]` |
| `status_counts` | `DashboardBucket[]` | normalized status 분포 | `[{ "label": "approved", "count": 53 }]` |
| `processing_days` | `ProcessingDaysSummary` | approved record의 처리기간 요약 | `{ "sampleSize": 53, "medianDays": 245 }` |
| `cohorts` | `PublicDashboardCohort[]` | `cat + fieldOffice` 기준 공개 가능한 cohort summary | `[{ "sampleSize": 20 }]` |
| `sources` | `DashboardSourceSummary[]` | source, checked date, limitation, sample size | `[{ "sourceId": "source-i485tracker-mock-v0" }]` |
| `suppressed_small_cohort_count` | `number` | small cohort로 개별 label을 숨긴 cohort 수 | `166` |
| `warnings` | `string[]` | dashboard 주변에 표시할 data limitation 후보 | `["small cohort bucket은 ..."]` |

공개 제한:

- `id`, `notes`, `receiptBlock`, full raw row는 포함하지 않는다.
- small cohort bucket은 개별 label을 숨기고 `suppressed_small_cohort` aggregate bucket으로 합친다.
- percentile이나 recent trend 성격의 값은 `PrivacyRule`을 통과하는 cohort에서만 표시한다.
- `GET /dashboard/public` API route는 local mock fixture를 읽어 이 aggregate-only response contract를 반환한다. full-data cache, DB, 외부 API runtime 연결은 후속 작업으로 둔다.

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

`UserCase`는 로그인 사용자의 저장한 scenario, 관심 조건, claim한 case 목록을 저장한다. 로그인 전 익명 case 자체는 `CaseRecord`와 `CaseEditToken`으로 관리하고, 로그인 후 claim되면 `CaseClaim`으로 연결한다.

| 필드 | 타입 | 목적 | 예시 |
|---|---|---|---|
| `id` | `string` | 고유 ID | `case-default` |
| `anonymousUsername` | `string?` | 익명 사용자명 | `casewatcher-17` |
| `email` | `string?` | optional email | `user@example.com` |
| `savedVisaProgramIds` | `string[]` | 저장한 visa category | `["us-eb2"]` |
| `savedCohortIds` | `string[]` | 저장한 cohort | `["cohort-eb2-nebraska-2025-q1"]` |
| `claimedCaseRecordIds` | `string[]` | claim한 case records | `["case-abc123"]` |
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


## Normalized ingestion 기준

Phase 3 ingestion은 `raw source -> normalized TimelineRecord -> privacy/aggregate layer` 순서로 처리한다.

사용자 입력은 Phase 4부터 `anonymous case creation -> CaseRecord -> CaseEvent updates -> optional CaseClaim -> aggregate-only public output` 순서로 처리한다. 외부 source snapshot과 사용자가 계속 수정하는 case record를 같은 row 모델로 섞지 않는다.

### i485tracker-like local mock adapter

`i485tracker`의 공개 shape는 schema reference로 사용한다. 개발은 repo 안의 작은 local mock fixture와 ignored full-data cache를 함께 참고하되, full raw data는 커밋하지 않는다.

2026-05-09 기준 `backend/.data/i485tracker_cases.full.json`에서 확인한 raw field는 다음과 같다.

```text
id, pd, cat, filed, receipt, receipt_num, bio, ead, ap,
field_office, fo_transfer_date, silent, gc_approved, gc_received,
interview, coc, rfe, region, notes, last_updated, created_at,
has_password
```

이 raw shape는 한 row 안에 여러 timeline event가 들어 있는 source snapshot이다. 제품 내부 사용자 입력 모델에서는 이 날짜/상태들을 `CaseEvent`로 분리한다.

| i485tracker 필드 | Backend 필드 | 기준 |
|---|---|---|
| `pd` | `pd` | ISO date |
| `cat` | `cat` | 필수 category |
| `filed` | `filed` | processing start |
| `receipt` | `receipt` | receipt event |
| `receipt_num` | `receiptBlock` 또는 `receiptHash` | public row 노출 금지. 중복 방지에 쓰면 원문 저장 없이 hash |
| `bio` | `bio` | biometric event |
| `ead` | `ead` | EAD event |
| `ap` | `ap` | Advance Parole event |
| `field_office` | `fieldOffice` | cohort filter 후보 |
| `fo_transfer_date` | `foTransferDate` | timeline event |
| `silent` | `silent` | ISO date array |
| `gc_approved` | `gcApproved` | processing days 계산 |
| `gc_received` | `gcReceived` | timeline event |
| `interview` | `interview` | timeline event |
| `coc` | `coc` | 민감하게 취급 |
| `rfe` | `rfe` | filter 후보 |
| `region` | `region` | cohort filter 후보 |
| `notes` | `notes` | public row 직접 노출 금지 |
| `last_updated` | `lastUpdated` | freshness 후보 |
| `has_password` | `hasPassword` | private edit link UX 참고 |

주의:

- 데이터 검증은 Phase 3 안에서 먼저 수행한다. public dashboard MVP는 full-data cache 품질 리포트, invalid row sample, raw-to-normalized mapping, small cohort suppression 기준을 확인한 뒤 시작한다.
- 외부 API를 반복 호출하지 않고 local fixture를 사용한다.
- production source로 장기 사용하려면 permission/license/운영 리스크를 별도 확인한다.
- full raw data를 repo에 커밋하지 않는다. 테스트와 개발은 작은 fixture만 사용한다.
- 모든 경로는 repo root(`/Users/kimdoyeong/Documents/VisaAtGlance`) 기준으로 기록한다. 규모별 visualization, data quality, performance 비교가 필요할 때만 `cd backend && PYTHONPATH=. uv run python scripts/fetch_i485tracker_full.py`를 실행한다. full-data cache는 `backend/.data/i485tracker_cases.full.json`과 `backend/.data/i485tracker_quality_report.json`에 생성되며 git에 커밋하지 않는다.
- `receipt_num`, `notes`, `coc`, edit 권한 힌트는 private/internal data로 취급하고 public aggregate response에는 직접 포함하지 않는다.


### Phase 3 validation gate 결과

2026-05-09 기준 local full-data cache를 validation gate로 재생성한 결과는 다음과 같다. 이 raw file과 report file은 `backend/.data/` 아래에만 두고 git에는 커밋하지 않는다.

| 항목 | 결과 | 의미 |
|---|---:|---|
| normalized records | 480 | public aggregate dashboard 개발에 사용할 수 있는 변환 성공 record |
| invalid raw rows | 8 | invalid sample 검토 필요. 현재 blocker는 아니지만 source quality warning으로 표시 |
| invalid ratio | 1.64% | warning threshold 5% 이하 |
| approved records | 53 | processing days 계산 가능 record |
| pending records | 427 | 현재 pending 중심 데이터셋 |
| field office missing | 0 | `cat + field_office` cohort 구성 가능 |
| total cohorts | 174 | `cat + field_office` 기준 cohort 수 |
| publishable cohorts | 8 | 기본 minimum cohort size를 통과해 aggregate 공개 가능 |
| percentile-ready cohorts | 4 | percentile 공개 기준을 통과하는 cohort |
| small cohorts | 166 | percentile/recent trend 숨김 또는 warning 필요 |
| largest cohort size | 103 | 큰 cohort visualization 성능 확인 가능 |

판단:

- `public_dashboard_ready`는 `true`다. blocker는 없다.
- 단, invalid raw row가 있으므로 invalid sample review를 dashboard 착수 전/중에 계속 유지한다.
- small cohort가 많으므로 public dashboard는 aggregate-first로 시작하고, percentile과 recent trend는 `PrivacyRule`을 통과하는 cohort에서만 표시한다.
- full-data cache는 개발 검증용이며 production source로 장기 사용하려면 permission/license/운영 리스크를 별도 확인한다.

### Apr '26 spreadsheet adapter 후보

Google Sheet `Apr '26` 탭 변환은 후속 작업 후보로 둔다. 현재 Phase 3의 primary 개발 데이터는 i485tracker-like local mock fixture다.

| Spreadsheet 컬럼 | Backend 필드 | 공개/집계 기준 |
|---|---|---|
| `Priority Date` | `pd` | cohort filter 후보 |
| `Category` | `cat` | 필수 category |
| `I-485 Mailed Date` / `I-485 Received Date` | `filed` | received date 우선, 없으면 mailed date |
| `I-485 Receipt (I-797) Date` | `receipt` | receipt event |
| `Block #` | `receiptBlock` | partial block만 보관 |
| `Biometric Date` | `bio` | timeline event |
| `Interview` | `interview` 또는 `notes` | 날짜가 있으면 event, 아니면 notes |
| `EAD (I-765) Approval Date if applied` | `ead` | 날짜가 있으면 event |
| `Advanced Parole (I-131) Approval if applied` | `ap` | 날짜가 있으면 event |
| `Field Office Name` / `Lockbox` | `fieldOffice` | field office 우선, 없으면 lockbox |
| `Field Office Transfer Date` | `foTransferDate` | timeline event |
| `Silent updates after biometrics` | `silent` | date array로 정규화 |
| `GC Approved Date` | `gcApproved` | processing days 계산 |
| `GC Received Date` | `gcReceived` | timeline event |
| `Are you from a country of concern` | `coc` | 민감하게 취급 |
| `Single/Spouse status` | `region`, `applicantGroup` | ROW/NROW와 group 분리 |
| `FTA0 updates`, `Comments` | `notes` | public dashboard에 직접 노출하지 않음 |

구현 기준:

- `TimelineRecord.status`는 `gcReceived -> gcApproved -> interview -> ead -> bio -> receipt -> filed` 순서로 계산한다.
- `TimelineRecord.processingDays`는 `gcApproved - filed`로 계산한다.
- `TimelineRecord.visibility` 기본값은 `aggregate_only`다.
- `CohortSummary.sampleSize`는 유사 case count로 사용한다.
- `CohortSummary.userPercentile`과 `recentApprovalCount`는 `PrivacyRule` 기준을 통과할 때만 표시한다.

## 아직 확정되지 않은 부분

| 주제 | 현재 상태 |
|---|---|
| DB 선택 | 아직 확정하지 않음 |
| Ingestion schema | i485tracker-like local mock fixture와 normalized `TimelineRecord` adapter 구현 |
| USCIS/Visa Bulletin ingestion 방식 | 다음 단계에서 결정 |
| small cohort 기준값 | 기본 후보: percentile 20건 미만 숨김, recent trend 10건 미만 숨김 |
| user deletion flow | 로그인 기능 전 설계 필요 |
