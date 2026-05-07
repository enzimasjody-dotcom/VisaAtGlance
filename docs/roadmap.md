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
| 1 | 앱 스택 선택 및 초기 scaffold | 예정 |
| 2 | 데이터 ingestion 및 정규화 pipeline | 예정 |
| 3 | 공개 dashboard MVP | 예정 |
| 4 | timeline 입력 기반 즉시 visualization | 예정 |
| 5 | 로그인, saved timeline, alerts | 예정 |
| 6 | premium 후보 기능 검증 | 장기 |

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
- 개인정보 수집은 최소화하고, receipt number나 full case documents는 공개하거나 수집하지 않는다.

## 다음 단계

### Phase 1 — 프로젝트 scaffold

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| 스택 확정 | Next.js + React + Vercel 우선 검토. chart는 Recharts부터 시작 | README와 docs에 실행 명령 기록 |
| 기본 앱 생성 | 첫 화면, 기본 layout, About/Contact/Privacy/Terms placeholder | 로컬 dev server 실행 가능 |
| 디자인 기준 | Calm, Reliable, Data-driven, Minimal 톤의 dashboard UI 방향 설정 | 첫 화면에서 정보 플랫폼 성격이 명확함 |
| 기본 QA | typecheck, lint, build 명령 정리 | `README.md`와 `git-workflow.md`에 반영 |

### Phase 2 — 데이터 모델과 ingestion

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| source schema | USCIS, Visa Bulletin, crowd-sourced timeline 출처 구조 정의 | `SourceRecord`와 ingestion 기준 문서화 |
| spreadsheet import | Google Sheet 기반 timeline 데이터를 읽고 정규화하는 경로 결정 | 샘플 데이터로 local transform 가능 |
| privacy guard | row-level 공개 제한, small cohort 숨김, sample size 기준 설계 | 개인정보 원칙이 코드/문서에 반영 |
| update metadata | 데이터 출처, checked date, limitation 표시 구조 | dashboard에서 source/freshness 표시 가능 |

### Phase 3 — 공개 dashboard MVP

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| public overview | 핵심 지표와 public chart 첫 화면 | 로그인 없이 주요 지표 확인 가능 |
| processing dashboard | average processing time, category/service center 비교 | 기본 필터와 chart 제공 |
| visa bulletin tracker | 월별 변화, category movement, trend 표시 | 공개 trend page 제공 |
| recent approvals | aggregate 또는 제한된 row preview | 재식별 위험 없이 최근 흐름 확인 가능 |
| SEO analysis pages | H1B processing time, Visa Bulletin, I-485 delay 등 | 검색 유입용 공개 페이지 초안 |

### Phase 4 — timeline 입력 기반 즉시 visualization

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| timeline input | visa category, filing date, service center 등 최소 입력 | 로그인 없이 입력 가능 |
| instant stats | average wait, percentile, similar cases, histogram | 입력 직후 visualization 표시 |
| cohort rule | similar cases의 기준과 sample size 표시 | 사용자가 비교 기준을 이해 가능 |
| small cohort safety | 표본이 작으면 percentile 숨김 또는 경고 | 재식별/오해 위험 완화 |
| save prompt | 결과 저장 시 로그인 유도 | 저장 전까지 개인정보 최소 유지 |

### Phase 5 — 로그인 사용자 기능

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| auth | optional email 기반 계정 또는 provider 선택 | saved timeline 사용 가능 |
| saved timelines | 사용자가 timeline과 관심 cohort 저장 | 재방문 시 dashboard 복원 |
| advanced filtering | category, service center, date range 등 고급 필터 | 로그인 사용자에게 추가 가치 제공 |
| compare with my case | 내 case와 cohort 비교 | 통계 비교로만 표현, 법적 판단 금지 |
| alerts | visa bulletin update, service center delay, similar case approvals | opt-in alert 동작 |

### Phase 6 — 수익화와 premium 후보

| 작업 | 내용 | 완료 기준 |
|---|---|---|
| AdSense 준비 | About, Contact, Privacy Policy, Terms, Disclaimer, original dashboards | 승인 준비 체크리스트 충족 |
| Premium Alerts | saved cohort movement, bulletin update, delay alerts | 무료/유료 경계 검증 |
| Advanced Analytics | cohort comparison, longer history, export | 유료 가치 검증 |
| Custom Dashboard | 관심 category와 timeline 기반 개인 dashboard | retention 지표 확인 |

## 설계 결정

- **제품 포지션**: VisaAtGlance는 법률 자문 서비스가 아니라 정보/데이터 시각화 플랫폼이다.
- **AI 추천 금지**: AI 기반 비자 추천, 승인 가능성 평가, 개인 맞춤 이민 전략은 제공하지 않는다.
- **통계 비교 표현**: percentile, histogram, average wait는 통계적 위치를 보여주는 정보일 뿐 승인 가능성 예측이 아니다.
- **공개/로그인 분리**: 공개 사용자는 기본 statistics, public charts, aggregate trends를 볼 수 있고, 로그인 사용자는 advanced filtering, saved timelines, alerts를 사용한다.
- **row-level 데이터 제한**: 익명 데이터라도 재식별 가능성이 있으므로 원본 row-level 전체 공개는 신중히 제한한다.
- **small cohort safety**: 표본 수가 작으면 percentile이나 상세 비교를 숨기거나 경고한다.
- **개인정보 최소화**: anonymous username, optional email, visa category, case timeline data만 초기 후보로 둔다. receipt number 공개, 여권 사본, SSN, full case documents는 다루지 않는다.
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
      ↓ 통계 비교
[instant visualization]
      ↓ 로그인
[saved timelines / custom dashboard]
      ↓ opt-in
[alerts / premium analytics]
```

장기적으로 VisaAtGlance가 제공해야 하는 가치는 다음과 같다.

- 복잡한 미국 비자 데이터를 한눈에 이해하게 한다.
- 사용자가 자신의 timeline을 유사 cohort와 통계적으로 비교하게 한다.
- 승인 가능성이나 법률 전략이 아니라 대기 시간, 흐름, 분포의 가시성을 제공한다.
- 공개 데이터와 익명 timeline 데이터를 안전하게 집계해 trend를 보여준다.
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
