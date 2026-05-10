# 로드맵

VisaAtGlance 로드맵은 단계별 구현 현황, 다음 계획, 장기 비전을 한곳에서 추적한다.

이 문서는 실행 계획의 현재 위치를 보여주는 문서다. 제품 원칙과 법적/운영적 범위는 [제품 스펙 v0.1](product-spec-v0.1.md)을 기준으로 하고, 데이터 모델 세부사항은 [데이터 모델](data-model.md)을 기준으로 한다.

## 구현 현황

| 단계 | 내용 | 상태 |
|---|---|---|
| 0 | GitHub 저장소 연결, `main` 초기 커밋, 원격 푸쉬 | 완료 |
| 0.1 | `classpilot` 문서 workflow 형식 참고 후 기본 docs 세트 생성 | 완료 |
| 0.2 | 모든 문서 업데이트를 한국어로 작성하는 규칙 추가 | 완료 |
| 0.3 | 프로젝트별 GitHub SSH alias(`github-enzimas`) workflow 문서화 | 완료 |
| 0.4 | 제품 방향 정리: 법률 자문/AI 추천이 아닌 정보·데이터 시각화 플랫폼 | 완료 |
| 0.5 | 공개 사용자/로그인 사용자 접근 범위 초안 정의 | 완료 |
| 0.6 | timeline 입력 → 즉시 visualization → 저장 시 로그인 → alerts UX 흐름 정의 | 완료 |
| 0.7 | 개인정보 최소화 원칙: anonymous username, optional email, no receipt number 공개, no full case documents | 완료 |
| 1 | 앱 스택 선택: Next.js frontend + FastAPI backend monorepo | 완료 |
| 1.1 | frontend/backend 초기 scaffold | 완료 |
| 2 | backend domain model과 privacy guard foundation | 완료 |
| 2.1 | template checkpoint 생성 | 완료 |
| 3 | i485tracker-like mock timeline ingestion prototype | 완료 |
| 4 | public dashboard MVP + anonymous timeline contribution | 다음 |
| 5 | AdSense 필수 페이지 | 예정 |
| 6 | sign up/auth + saved timeline 최소 기능 | 예정 |
| 7 | timeline 입력 기반 즉시 visualization 확장 | 예정 |
| 8 | premium 후보 기능 검증 | 장기 |

## 검증된 현재 기준

현재까지 검증된 것은 코드 동작이 아니라 프로젝트 운영 기준이다.

```text
문서 workflow 생성
  → 제품 스펙 정리
  → Git workflow 정리
  → GitHub main 푸쉬
  → roadmap 추가 준비
```

현재 기준:

- 브랜드명은 `VisaAtGlance`로 통일한다.
- 법률 자문, 비자 추천, 승인 가능성 평가는 하지 않는다.
- 공개 데이터와 익명 timeline 데이터를 집계·정제해 시각화한다.
- 공개 사용자는 기본 통계와 public chart를 볼 수 있다.
- 로그인 사용자는 advanced filtering, saved timelines, alerts, custom dashboard를 사용할 수 있다.
- 개인정보 수집은 최소화하고, receipt number 원문이나 full case documents는 공개하지 않는다. receipt number가 중복 방지에 필요해지면 원문 저장 없이 hash 처리한다.

## 우선순위 기준

로드맵 순서는 고정된 일정이 아니라 기술적 복잡성, 확장성, 장기계획을 함께 고려해 재정렬한다.

현재 재정렬 이유:

- backend domain model과 privacy guard를 먼저 두어 ingestion, dashboard, saved timeline이 같은 공개 제한 기준을 공유하게 한다.
- Phase 2 완료 시점에 template checkpoint를 만들어 Next.js/FastAPI scaffold 이상의 재사용 가능한 app foundation을 보존한다.
- i485tracker-like local mock data를 먼저 사용해 외부 API 의존 없이 visualization을 빠르게 검증하고, Google Sheet raw data 변환은 후속 작업으로 분리한다.
- public dashboard는 ingestion prototype과 privacy 기준이 있어야 신뢰 가능한 형태로 확장된다.
- Phase 4부터 사용자 입력은 1회 제출 row가 아니라 `CaseRecord + CaseEvent` 업데이트 구조로 관리한다.
- 익명 사용자는 private edit link로 같은 case를 계속 업데이트하고, 로그인 후 optional claim으로 계정에 연결할 수 있게 한다.
- 개별 사용자 입력 row와 edit link는 public으로 공개하지 않고, privacy guard를 통과한 aggregate-only output에만 반영한다.
- AdSense 필수 페이지는 dashboard MVP 뒤에 두어 단순 페이지 껍데기가 아니라 original dashboard와 함께 검토 가능한 사이트가 되게 한다.
- sign up/auth는 anonymous case creation과 private edit link가 먼저 안정된 뒤 optional claim, saved timeline, alerts를 위해 도입한다.

## 다음 단계

### Phase 1 — 프로젝트 scaffold

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| 스택 확정 | Next.js frontend + FastAPI backend monorepo로 확정. chart는 Recharts부터 시작 | 완료 |
| 기본 scaffold 생성 | `frontend/` Next.js와 `backend/` FastAPI 생성. frontend 첫 화면, backend `/health` 포함 | 완료 |
| 디자인 기준 | Tableau 같은 analytics platform landing 구조를 참고하되 복제하지 않음. dashboard preview-first, legal-safe language 유지 | 첫 화면에서 public dashboard와 정보 플랫폼 성격이 명확함 |
| 기본 QA | `make visa-check`, `make visa-frontend-check`, `make visa-backend-check` 명령 정리와 backend CI 연결 | README, Git workflow, GitHub Actions에 반영 |

### Phase 2 — backend domain model과 privacy guard

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| domain model foundation | 초기에는 `Apr '26` 탭 검토에서 시작했고, 현재는 i485tracker-like normalized `TimelineRecord`, `CohortSummary`, `SourceRecord`, `PrivacyRule` 기준으로 정렬 | 완료: backend domain test 통과 |
| privacy guard foundation | small cohort suppression, row-level 공개 제한 기준 구현 | 완료: 작은 sample에서 percentile/recent trend 숨김 테스트 통과 |
| cohort summary helper | average, median, percentile 후보 계산을 privacy guard 뒤에 둠 | 완료: 충분한 sample에서만 percentile 표시 |
| template checkpoint | Phase 2 완료 상태를 재사용 가능한 app foundation으로 기록 | 완료: `template-domain-foundation-v0.1` tag 생성 |

### Phase 3 — i485tracker-like mock timeline ingestion prototype

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| local mock fixture | i485tracker-like JSON sample을 repo 안에 작게 보관 | 외부 API 호출 없이 local dev/test 가능 |
| mock data adapter | local JSON fixture를 `TimelineRecord`로 변환 | mock records가 domain model로 변환됨 |
| source metadata | mock source의 limitation과 checked date 표시 구조 | production source가 아님을 명확히 기록 |
| local full-data cache | i485tracker 공개 API는 개발자가 명시적으로 실행하는 fetch script로만 호출하고, full data는 `backend/.data/`에 ignored cache로 저장 | 데이터가 적을 때와 많을 때의 visualization, quality, performance 비교 가능 |
| quality report | local full-data cache와 mock fixture의 missing field, invalid date, cohort 규모를 점검 | 완료: validation gate report 생성 및 backend test 통과 |
| data validation gate | full-data cache 품질 리포트, invalid row sample, raw-to-normalized mapping, small cohort suppression 기준을 리뷰 | 완료: 480 records, 8 invalid rows, publishable cohorts 8개, blocker 없음 |
| import validation | 필수 field, ISO date format, 비현실적 year 처리 기준 | 완료: invalid row를 errors로 분리하고 테스트로 검증 |
| aggregate-first output | row-level 원본 대신 public dashboard용 집계 구조 생성 | 완료: `PublicDashboardSummary` domain builder와 aggregate-only 테스트 추가 |
| Google Sheet adapter | `Apr '26` raw CSV 변환 | 후속 작업으로 분리 |

### Phase 4 — public dashboard MVP + anonymous case record foundation

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| public overview | 기존 첫 화면 구조를 유지하면서 public dashboard 준비 상태와 privacy-safe 방향 표시 | 진행 중: mock 기반 핵심 KPI는 노출하지 않고 pending-aware 분석 모델과 production data 준비 상태만 표시 |
| case/event domain model | `CaseRecord`, `CaseEvent`, `CaseEditToken`, `CaseClaim`, `DuplicateCandidate` 기준 구현 | 사용자 입력을 일회성 row가 아니라 업데이트 가능한 case + event 구조로 저장 가능 |
| anonymous case creation | 로그인 없이 case를 만들고 private edit link를 발급 | 사용자가 edit link로 같은 case를 다시 열 수 있음 |
| case event updates | biometrics, RFE, transfer, approval 등 진행 이벤트를 추가/수정 | 같은 case에 이벤트가 누적되고 `updatedAt`이 갱신됨 |
| duplicate candidate detection | receipt 원문 없이 form/category/country/service center/date 조합으로 유사 case 후보 탐지 | 자동 병합 없이 기존 case 업데이트 제안을 표시할 수 있음 |
| aggregate-only contribution | 사용자가 동의한 case/event를 privacy guard 뒤 aggregate stats에 반영 | 개별 row, receipt number, notes, edit link 없이 aggregate 계산에만 사용 |
| timeline dashboard | i485tracker-like normalized timeline aggregate statistics와 chart | filing-month cohort movement, pending-aware timeline analysis, cohort context를 MVP 핵심 축으로 검토 |
| cohort context | 사용자가 입력한 timeline을 비슷한 filing-month/category/field office cohort 흐름 안에서 설명 | approval prediction이나 legal advice 없이 historical community-data position만 표시 |
| recent approvals | aggregate 또는 제한된 row preview | 재식별 위험 없이 최근 흐름 확인 가능 |
| source/limitation 표시 | source, checked date, sample size, limitation 표시 | chart 주변에서 데이터 한계 확인 가능 |
| SEO analysis pages 초안 | H1B processing time, Visa Bulletin, I-485 delay 등 | 검색 유입용 공개 페이지 초안 |

#### Phase 4 구현 우선순위

기술적 복잡성, 확장성, 데이터 안정성을 기준으로 Phase 4 구현 순서는 다음과 같이 둔다.

1. `CaseRecord + CaseEvent` backend domain model과 테스트
2. anonymous case creation API와 private edit token 발급/검증
3. edit link 기반 case event update API
4. duplicate candidate detection의 보수적 후보 탐지
5. aggregate-only contribution pipeline과 privacy guard 연결
6. filing-month cohort movement chart/API 후보 검토
7. pending-aware timeline analysis 후보 검토
8. user-entered timeline cohort context UI/API

이 순서의 이유:

- case/event 모델이 먼저 안정되어야 중복 방지, edit link, optional claim, aggregate contribution이 같은 저장 단위를 공유한다.
- private edit token은 로그인 없는 업데이트 경험의 핵심이므로 auth보다 먼저 검증한다.
- duplicate detection은 자동 병합이 아니라 후보 제안으로 시작해 데이터 손상 위험을 낮춘다.
- pending-aware 분석과 cohort context는 통계 방식 검증이 필요하므로 저장 모델 이후에 붙인다.

#### Phase 4 analytics 기준

- approved-only 평균/중앙값은 pending case가 많은 이민 timeline 데이터에서 왜곡될 수 있으므로 public hero metric으로 사용하지 않는다.
- public dashboard MVP의 핵심 분석은 filing-month cohort movement, pending-aware timeline analysis, user-entered timeline의 cohort context이다.
- field office median, category boxplot, approved-only histogram은 보조 탐색용으로만 사용하고 chart 주변에 limitation을 함께 표시한다.
- Kaplan-Meier류 pending-aware 분석은 후보 접근으로 유지하되, 첨부 분석 script를 그대로 채택하기 전 통계적 정확성을 별도로 확인한다.
- `predict my case`, `approval probability`처럼 승인 가능성을 암시하는 표현은 사용하지 않는다. 대신 `cohort timeline context`, `historical community-data position`, `similar case timeline`처럼 정보 제공 범위의 표현을 사용한다.

### Phase 5 — AdSense 필수 페이지

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| About | 정보 플랫폼 포지셔닝과 legal-safe 설명 | 법률 자문이 아님을 명확히 표시 |
| Contact | support email 중심 연락 페이지 | 개인 전화번호/주소 없이 문의 경로 제공 |
| Privacy Policy | 최소 수집, 수집하지 않는 데이터, 삭제 원칙 | timeline/auth 도입 전 기준 문서화 |
| Terms of Service | 사용 범위, 금지 표현, 책임 제한 | legal-safe language 반영 |
| Disclaimer | informational platform, no legal advice 문구 | footer와 주요 페이지에서 연결 가능 |

### Phase 6 — sign up/auth + saved timeline 최소 기능

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| auth provider 선택 | optional email 또는 provider 기반 최소 auth 결정 | workflow에 선택 이유 기록 |
| sign up/login/logout | 기본 계정 흐름 | 사용자가 계정 생성과 로그아웃 가능 |
| claim existing case | private edit link로 만든 익명 case를 로그인 계정에 연결 | `Claim this case` 흐름으로 기존 case ownership 연결 |
| protected dashboard shell | 로그인 사용자 영역 | claim한 case와 saved filters가 보이는 자리 제공 |
| saved timelines 최소 모델 | Phase 4에서 만든 case 또는 saved filter 저장 | 재방문 시 claim한 case와 저장 조건 복원 |
| account privacy controls | 삭제/opt-in 기준 | 개인정보 최소화 원칙 유지 |

### Phase 7 — timeline 입력 기반 즉시 visualization 확장

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| timeline input refinement | visa category, filing date, service center 등 최소 입력을 case/event form으로 다듬음 | 로그인 없이 입력하고 edit link로 수정 가능 |
| instant stats | cohort movement, similar case timeline, sample size, histogram 후보 | 입력 직후 visualization 표시 |
| cohort rule | similar cases의 기준과 sample size 표시 | 사용자가 비교 기준을 이해 가능 |
| small cohort safety | 표본이 작으면 percentile 숨김 또는 경고 | 재식별/오해 위험 완화 |
| save prompt | 결과 저장 시 로그인 유도 | 저장 전까지 개인정보 최소 유지 |

### Phase 8 — 수익화와 premium 후보

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| Premium Alerts | saved cohort movement, bulletin update, delay alerts | 무료/유료 경계 검증 |
| Advanced Analytics | cohort comparison, longer history, export | 유료 가치 검증 |
| Custom Dashboard | 관심 category와 timeline 기반 개인 dashboard | retention 지표 확인 |

## 설계 결정

- **제품 포지션**: VisaAtGlance는 법률 자문 서비스가 아니라 정보/데이터 시각화 플랫폼이다.
- **AI 추천 금지**: AI 기반 비자 추천, 승인 가능성 평가, 개인 맞춤 이민 전략은 제공하지 않는다.
- **통계 비교 표현**: percentile, histogram, average wait는 통계적 위치를 보여주는 정보일 뿐 승인 가능성 예측이 아니다.
- **공개/로그인 분리**: 공개 사용자는 기본 statistics, public charts, aggregate trends와 익명 case creation/edit link 기반 timeline context를 사용할 수 있고, 로그인 사용자는 claim한 case, saved timelines, advanced filtering, alerts를 사용한다.
- **익명 case 업데이트**: Phase 4부터 사용자가 입력한 비식별 timeline data는 `CaseRecord + CaseEvent` 구조로 저장하고 private edit link로 계속 업데이트할 수 있게 한다.
- **동의 기반 aggregate 반영**: 사용자가 동의한 case/event만 privacy guard 뒤 aggregate stats에 반영한다.
- **row-level 데이터 제한**: 익명 데이터라도 재식별 가능성이 있으므로 원본 row-level 전체 공개는 신중히 제한한다.
- **edit link 보호**: edit link는 비밀번호에 준하는 secret token으로 다루며 public id와 분리하고 원문 token은 저장하지 않는다.
- **small cohort safety**: 표본 수가 작으면 percentile이나 상세 비교를 숨기거나 경고한다.
- **개인정보 최소화**: anonymous case key, optional email, visa category, case timeline data만 초기 후보로 둔다. receipt number 공개, 여권 사본, SSN, full case documents는 다루지 않는다.
- **source transparency**: source, checked date, sample size, limitation을 chart 주변에 표시한다.
- **브랜딩**: Calm, Reliable, Data-driven, Minimal, Clear 톤을 유지한다.
- **광고 UX**: 광고는 핵심 차트와 데이터 해석을 방해하지 않아야 한다.

## 장기 고려 — 설계 방향

| 항목 | 내용 |
|---|---|
| 데이터 파이프라인 | USCIS, Visa Bulletin, crowd-sourced timeline 데이터를 정기적으로 정규화하는 구조 |
| 신뢰도 표시 | source freshness, official/unofficial, sample size, limitation을 일관되게 표시 |
| cohort engine | category, filing date, service center 등 기준으로 유사 cohort를 구성 |
| privacy layer | small cohort suppression, row-level masking, user deletion flow |
| alert engine | bulletin update, saved cohort movement, delay signal 감지 |
| premium boundary | alerts, export, advanced comparison, longer history를 유료 후보로 검증 |
| content strategy | dashboard + explanatory analysis page 조합으로 SEO 확보 |
| compliance docs | Privacy, Terms, Disclaimer를 제품 출시 전 최신화 |

## 장기 비전

목표: 미국 비자·이민 프로세스를 데이터로 이해하는 public-facing immigration data platform.

```text
[공개/공식 데이터]
      ↓ 정규화
[USCIS / Visa Bulletin Dashboard]
      ↓
[공개 chart + SEO analysis pages]
      ↓
[사용자 timeline 입력]
      ↓ 즉시 비교
[instant visualization]
      ↓ 동의 기반 비식별 저장
[aggregate stats 개선]
      ↓ 로그인
[saved timelines / custom dashboard]
      ↓ opt-in
[alerts / premium analytics]
```

장기적으로 VisaAtGlance가 제공해야 하는 가치는 다음과 같다.

- 복잡한 미국 비자 데이터를 한눈에 이해하게 한다.
- 사용자가 자신의 timeline을 유사 cohort와 통계적으로 비교하게 한다.
- 승인 가능성이나 법률 전략이 아니라 대기 시간, 흐름, 분포의 가시성을 제공한다.
- 공개 데이터와 동의 기반 익명 timeline 데이터를 안전하게 집계해 trend를 보여준다.
- 사용자가 반복 방문할 이유를 saved timeline, alerts, custom dashboard로 만든다.

## 장기 non-goals

아래 항목은 장기적으로도 신중히 피한다.

- 비자 추천
- 개인별 승인 가능성 예측
- 법률 의견 제공
- “best visa”, “guaranteed approval”, “recommended strategy” 같은 표현
- 민감 법률 문서 수집
- receipt number 공개
- 공식 정부 사이트처럼 보이는 브랜딩
