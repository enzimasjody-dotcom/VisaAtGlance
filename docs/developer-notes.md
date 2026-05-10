# 개발자 노트

목적: VisaAtGlance의 현재 제품/구현 기준을 관리한다.

비목적: 필드별 데이터 설명, 리팩터링 순서, Git workflow, 초기 아이디어 보관은 각각 `data-model.md`, `refactoring-notes.md`, `git-workflow.md`, `product-spec-v0.1.md`에서 관리한다.

최종 업데이트: 2026-05-07

## 제품 방향

VisaAtGlance는 미국 비자 및 이민 관련 공개 데이터와 익명 timeline 데이터를 바탕으로 대기 시간, 흐름, 분포를 한눈에 이해하도록 돕는 정보/데이터 시각화 플랫폼이다.

| 원칙 | 설명 |
|---|---|
| At-a-glance clarity | 사용자가 processing time, trend, cohort 위치를 빠르게 이해해야 한다 |
| Source-aware information | 데이터는 source, checked date, sample size, limitation을 함께 가져야 한다 |
| No legal advice | 비자 추천, 승인 가능성 평가, 개인 맞춤 이민 전략을 제공하지 않는다 |
| Aggregate-first | 익명 timeline 데이터라도 재식별 위험을 고려해 집계/정제 중심으로 보여준다 |
| Backend-owned data logic | ingestion, normalization, cohort 계산, privacy guard는 backend/domain 쪽이 소유한다 |
| Shared data base | 공개 dashboard, timeline 입력, saved dashboard는 같은 데이터 기준을 공유한다 |

## 확정된 앱 스택

| 영역 | 선택 | 기준 |
|---|---|---|
| Repo 구조 | `frontend/`, `backend/`, `docs/` monorepo | frontend와 data/backend 로직을 분리하되 한 저장소에서 함께 관리 |
| Frontend | Next.js + React + TypeScript | SEO 공개 페이지와 interactive dashboard를 함께 지원 |
| Backend | FastAPI + Python | i485tracker-like timeline ingestion, 후속 Google Sheet/USCIS/Visa Bulletin ingestion 후보, cohort 계산, privacy guard를 backend에서 관리 |
| Styling | Tailwind CSS | 빠른 dashboard layout과 일관된 spacing/color 관리 |
| Visualization 시작점 | Recharts | MVP 차트 구현 속도와 React 통합성 우선 |
| Visualization 확장 | ECharts, D3.js | 복잡한 interactive chart나 custom visualization 필요 시 검토 |
| Frontend hosting | Vercel | Next.js 배포 기본 경로 |
| Backend hosting | 초기 로컬, 배포는 추후 결정 | Render/Fly.io/Railway/AWS 등은 운영 요구가 선명해진 뒤 선택 |
| Frontend package manager | npm | 초기 설정 단순화 |
| Backend package manager | `uv` | Python dependency와 실행 환경 재현성 확보 |

backend를 scaffold 단계부터 포함한다. VisaAtGlance는 곧바로 데이터 ingestion, 정규화, cohort 계산, small cohort suppression, alerts 준비가 필요하므로 frontend-only 구조로 시작하지 않는다.

## 핵심 데이터

자세한 필드 설명은 [데이터 모델](data-model.md)을 기준으로 한다.

| 모델 | 역할 |
|---|---|
| `VisaProgram` | 비자 유형, pathway, status category |
| `Requirement` | 조건, 문서, fee, deadline, eligibility rule |
| `CountryProfile` | 국가 또는 jurisdiction context |
| `UserCase` | 사용자의 저장된 scenario와 관심 조건 |
| `SourceRecord` | source URL, checked date, confidence metadata |
| `ChecklistItem` | requirement에서 파생된 사용자 action |

## Source / Confidence 정책

| 규칙 | 설명 |
|---|---|
| source metadata 유지 | dashboard 수치와 requirement는 출처를 추적할 수 있어야 한다 |
| freshness 표시 | 중요한 데이터는 `checkedAt` 또는 `lastReviewedAt` 기준을 가진다 |
| facts와 notes 분리 | 공식/공개 데이터와 사용자 메모를 조용히 섞지 않는다 |
| uncertainty 표시 | stale, unofficial, low sample size는 UI에서 드러낸다 |
| legal advice framing 회피 | 데이터 정리와 통계 비교를 법률 판단처럼 표현하지 않는다 |

## Planned Screen Areas

초기 화면 가정:

```text
Overview
Processing Dashboard
Visa Bulletin
Timeline Input
Saved Dashboard
Sources
Settings
```

| 화면 | 목적 | 주요 내용 |
|---|---|---|
| Overview | 공개 첫 화면 | 핵심 지표, public charts, recent aggregate trends |
| Processing Dashboard | USCIS 처리 시간 이해 | category/service center별 비교, historical trend |
| Visa Bulletin | 월별 bulletin 변화 추적 | category movement, priority date trend |
| Timeline Input | 즉시 통계 비교 | average wait, percentile, similar cohort |
| Saved Dashboard | 로그인 사용자 retention | saved timeline, custom dashboard, alerts |
| Sources | 데이터 투명성 | source, checked date, sample size, limitation |
| Settings | 사용자 설정 | account, alert preference, saved cohort 관리 |

## Public Dashboard Chart Language

Phase 4A public dashboard는 다음 chart label과 안전 문구를 기준으로 한다. 각 문구는 개인 승인 가능성 예측이 아니라 community-data timeline context임을 분명히 해야 한다.

| Chart label | 기반 분석 output | 안전 문구 |
|---|---|---|
| `Filing-month cohort movement` | `filing_month_approval_rate.png` | Community-submitted data에서 관측된 filing month별 움직임이다. 최근 cohort는 아직 pending case가 많아 낮게 보일 수 있다. |
| `Community timeline progression` | `km_approval_curve.png` | Pending case를 still in progress로 포함한 community-data timeline view다. 개인 승인 예측이 아니다. |
| `Approved-case processing distribution` | `approval_time_histogram.png` | Recorded approval이 있는 case만 보여준다. Pending case가 빠져 있으므로 전체 대기시간 추정으로 읽지 않는다. |

금지 표현:

- `Predict my case`
- `Approval probability`
- `Chance of approval`
- `Expected approval date`
- 개인별 승인 가능성을 높다/낮다로 판단하는 표현

## 페이지 모델

VisaAtGlance는 Tableau 같은 analytics platform landing 구조를 참고할 수 있다. 단, 레이아웃, 문구, 브랜드 표현을 복제하지 않고 정보 구조와 UX 패턴만 참고한다.

초기 public page 구조:

```text
Header
  Dashboard / Processing Times / Visa Bulletin / Timeline / Sources / About / Sign in
Hero
  US visa information, at a glance.
  Public dashboard preview + primary CTA
Public Data Sections
  USCIS Processing Dashboard / Visa Bulletin Tracker / Recent Approvals / Aggregate Trends
User Value Section
  Enter timeline -> average wait / percentile / similar cohort -> save with login
Trust and Safety Section
  Informational platform / no legal advice / official sources linked / privacy-minimal data
Footer
  About / Contact / Privacy Policy / Terms / Disclaimer
```

원칙:

- 첫 화면은 마케팅 hero만 두지 않고 public dashboard preview를 강하게 보여준다.
- Tableau식 제품 섹션 구조는 참고하되 VisaAtGlance의 legal-safe language와 데이터 투명성을 우선한다.
- 제품명, 카피, 색상, 레이아웃을 Tableau와 혼동될 정도로 유사하게 만들지 않는다.
- CTA는 `Explore public dashboard`, `Compare my timeline`처럼 정보 탐색과 통계 비교 중심으로 둔다.

## 구현 기준

| 영역 | 방향 |
|---|---|
| Backend API | FastAPI에서 `/health`, ingestion, cohort, privacy guard API를 단계적으로 제공한다 |
| Domain logic | cohort 계산, privacy guard, source freshness를 frontend component 밖에 둔다 |
| Frontend UI | Next.js page는 API 결과를 읽어 dashboard와 chart를 보여주는 presentation layer로 유지한다 |
| Storage | 저장 방식은 backend의 좁은 API 뒤에 둔다. 초기에는 파일/샘플 데이터, 이후 DB를 검토한다 |
| Visualization | Recharts로 시작하고 복잡도가 실제로 필요해질 때 ECharts/D3를 추가한다 |
| Data updates | source와 limitation을 보존하며, 불확실한 업데이트는 검토 가능하게 둔다 |
| Tests | backend cohort/privacy/source freshness 테스트를 우선하고, frontend는 smoke/build부터 시작한다 |

## Open Decisions

| 주제 | 현재 상태 |
|---|---|
| MVP user segment | 아직 결정 필요 |
| 첫 데이터 ingestion 방식 | i485tracker-like local mock fixture와 ignored full-data cache 기반으로 진행. Google Sheet 변환은 후속 후보 |
| backend 배포 대상 | scaffold 이후 결정 |
| DB 선택 | 초기 ingestion 구조 확인 후 결정 |
| 인증 방식 | saved timeline 단계에서 결정 |
| jurisdiction coverage | 미국 중심으로 시작, 세부 category 범위 결정 필요 |
