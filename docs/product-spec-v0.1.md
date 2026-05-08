# VisaAtGlance 제품 스펙 v0.1

목적: VisaAtGlance의 초기 제품 방향, 법적/운영 원칙, 단계별 제품 구조를 보관한다.

비목적: 세부 구현 기준, 데이터 모델, Git workflow, 리팩터링 계획의 기준 문서가 아니다.

현재 기준 문서:

| 주제 | 문서 |
|---|---|
| 현재 제품/구현 기준 | [개발자 노트](developer-notes.md) |
| 현재 데이터 모델 | [데이터 모델](data-model.md) |
| 리팩터링 계획 | [리팩터링 노트](refactoring-notes.md) |
| 작업 절차 | [Git 워크플로우](git-workflow.md) |
| 단계별 계획 | [로드맵](roadmap.md) |

## 1. 프로젝트 목표

VisaAtGlance는 미국 비자 및 이민 관련 공개 데이터와 익명 crowd-sourced timeline 데이터를 직관적으로 시각화하여, 사용자가 미국 이민 프로세스를 한눈에 이해할 수 있도록 돕는 정보 플랫폼이다.

핵심 방향:

| 방향 | 상태 |
|---|---|
| 법률 자문 서비스 | 하지 않음 |
| AI 기반 비자 추천 서비스 | 하지 않음 |
| 정보/데이터 시각화 플랫폼 | 핵심 방향 |
| USCIS 및 공개 데이터 기반 대시보드 | 핵심 방향 |
| 익명 timeline 기반 aggregate insight | 핵심 방향 |

## 2. 프로젝트 포지셔닝

브랜드 포지션:

```text
US visa information, at a glance.
```

서비스 성격:

- US Visa Data Dashboard
- Visa Trend Analytics
- Immigration Data Visualization
- USCIS Processing Dashboard
- Immigration Data Platform

주의: `Immigration Intelligence Platform` 같은 표현은 분석/전략 제공처럼 보일 수 있으므로, 외부 문구에서는 데이터 플랫폼 중심 표현을 우선한다.

## 3. 법적/운영적 원칙

### 3.1 하지 않는 것

VisaAtGlance는 법률 자문을 제공하지 않는다.

제공하지 않는 기능:

- 비자 추천
- 승인 가능성 평가
- 개인 맞춤 이민 전략
- 법률 의견 제공
- "이 비자가 유리하다" 같은 판단
- "승인 가능성이 높다/낮다" 같은 개인별 예측
- "best visa", "recommended immigration strategy" 같은 표현

### 3.2 제공하는 범위

허용 범위:

- USCIS processing times
- Visa bulletin tracker
- 공개 통계 시각화
- 정책 업데이트 요약
- 공식 사이트 링크
- 공개 데이터 기반 trend 분석
- 익명 timeline 데이터의 aggregate trend
- 유사 cohort의 통계적 비교

중요한 구분:

- percentile, histogram, average wait 같은 정보는 통계 비교로만 제공한다.
- 개인의 승인 가능성, 법적 전략, 신청 판단으로 표현하지 않는다.
- "similar cases"는 법적 동일성이 아니라 사용자가 선택한 category, filing date, service center 등 데이터 필드 기준의 cohort를 뜻한다.

### 3.3 필수 디스클레이머

사이트 내 명시 문구:

```text
VisaAtGlance is an informational platform and does not provide legal advice.
```

추가 문구:

```text
Always consult official USCIS resources or licensed immigration attorneys for legal guidance.
```

디스클레이머는 About, Terms, footer, 데이터 해석 페이지에서 반복 노출한다.

## 4. 개인정보 및 규정 준수

기본 원칙:

- 초기 제품은 로그인 없이도 주요 공개 정보에 접근할 수 있게 한다.
- 개인정보 수집은 최소화한다.
- 민감한 법률 문서나 식별자는 수집하지 않는다.
- 익명 데이터라도 재식별 가능성을 고려한다.

초기 수집 가능 데이터:

- anonymous username
- optional email
- visa category
- filing date / approval date 같은 case timeline data
- service center 또는 processing office
- 사용자가 직접 입력한 비식별 timeline field

수집하지 않는 것:

- 여권 사본
- SSN
- receipt number 공개 표시
- 민감한 법률 문서 전체
- full case documents

운영 원칙:

- receipt number는 공개하지 않는다.
- row-level 원본 데이터 공개는 신중히 제한한다.
- 소규모 cohort는 재식별 위험이 있으므로 percentile이나 상세 비교를 숨기거나 경고한다.
- 사용자가 저장한 timeline은 삭제할 수 있어야 한다.

필수 페이지:

- Privacy Policy
- Contact
- About
- Terms of Service
- Disclaimer 또는 Terms 내 명확한 disclaimer 섹션

연락처 예시:

```text
support@usvisaatglance.com
```

개인 전화번호나 개인 주소 공개는 필수로 두지 않는다.

## 5. 제품 구조

### Phase 1 — 공개 정보/시각화 플랫폼

목표:

- SEO 확보
- 초기 사용자 유입
- 데이터 구조 구축
- USCIS 및 공개 데이터 기반 대시보드 구축
- 익명 crowd-sourced timeline 데이터의 aggregate visualization 제공

공개 사용자가 볼 수 있는 것:

- 전체 표 일부 또는 제한된 preview table
- 기본 statistics
- public charts
- visa bulletin trends
- recent approvals
- aggregate trends
- average processing time
- EB2 trend
- H1B approval histogram

핵심 기능:

| 기능 | 공개 범위 |
|---|---|
| USCIS Processing Dashboard | 공개 기본 차트와 요약 제공 |
| Visa Bulletin Tracker | 공개 trend와 월별 변화 제공 |
| Recent Approvals | aggregate 또는 제한된 row preview 제공 |
| Spreadsheet 기반 데이터 시각화 | 공개 preview + 로그인 후 상세 제공 |
| 공식 사이트 링크 | 공개 제공 |
| 데이터 출처와 한계 설명 | 공개 제공 |

### Phase 1.5 — timeline 입력 기반 즉시 visualization

UX 흐름:

```text
Step 1: 사용자 timeline 입력
  ↓
Step 2: 즉시 visualization 제공
  ↓
Step 3: save하려면 로그인
  ↓
Step 4: alerts 제공
```

즉시 제공 가능한 visualization:

- average wait
- percentile
- similar cases
- cohort distribution
- processing histogram

표현 예시:

```text
You are faster than 72% of similar cases.
```

주의:

- 위 문구는 승인 가능성 예측이 아니라 입력된 timeline과 유사 cohort의 통계적 위치를 보여주는 표현이다.
- cohort 기준과 sample size를 함께 보여준다.
- sample size가 너무 작으면 percentile을 제공하지 않는다.

### Phase 2 — 로그인 사용자 기능

로그인 사용자가 추가로 받는 가치:

- advanced filtering
- compare with my case
- percentile ranking
- saved timelines
- alerts
- cohort analysis
- custom dashboard

로그인 기능의 목표:

- retention 증가
- recurring visits 유도
- crowd-sourced timeline 품질 개선
- 개인 관심 category와 cohort 저장

Alerts 예시:

- visa bulletin update
- service center delay
- similar case approvals
- saved cohort movement

### Phase 3 — premium 기능 후보

Premium 후보:

- 실시간 visa bulletin alerts
- advanced tracking
- advanced cohort comparison
- custom dashboard 확장
- export 기능
- 더 긴 historical range 분석

## 6. 수익 구조

초기 단계:

| 수익원 | 목표 |
|---|---|
| Google AdSense | 초기 트래픽 수익화 |
| SEO 기반 트래픽 | 공개 dashboard와 analysis page 기반 유입 |

핵심 SEO 키워드 후보:

- H1B processing time
- Visa bulletin
- I-485 delay
- Green card backlog
- EB2 trend
- USCIS processing time

중기 단계:

| 수익원 | 예시 |
|---|---|
| Premium Alerts | visa bulletin alerts, saved cohort alerts |
| Advanced Analytics | 고급 필터, 비교, export |
| Custom Dashboard | 저장된 timeline과 관심 cohort 기반 dashboard |

광고 UX 원칙:

- 공격적인 광고 UX를 피한다.
- 데이터 해석과 핵심 차트 가독성을 광고보다 우선한다.
- 법률 자문처럼 보이는 광고 문구나 placement를 조심한다.

## 7. 데이터 소스 전략

주요 데이터:

- USCIS 공개 데이터
- Visa Bulletin 공개 정보
- 공개 통계 자료
- 익명 crowd-sourced timeline data
- 사용자가 자유롭게 로깅한 공개 timeline 데이터

원칙:

- 공개 데이터라도 VisaAtGlance에서는 집계/정제해서 보여준다.
- row-level 원본 데이터 전체 공개는 신중히 제한한다.
- 데이터 출처, 업데이트 시점, 한계를 표시한다.
- 독점적으로 정제한 데이터셋은 공개 insight와 로그인 기능을 분리해 보호한다.

독점 데이터셋에 가까운 경우:

- 원본 row-level 데이터는 공개하지 않는다.
- 공개 페이지는 집계/요약/preview 중심으로 구성한다.
- 전체 interactive visualization은 로그인 후 제공한다.
- export, alerts, advanced analytics는 premium 후보로 둔다.
- SEO를 위해 official/public data 설명 페이지와 요약 분석 페이지는 공개한다.

## 8. 기술 구조

현재 확정된 초기 스택:

| 영역 | 선택 |
|---|---|
| Frontend | Next.js, React, TypeScript |
| Visualization 기본 | Recharts |
| Backend | FastAPI, Python |
| Backend dependency/runtime | uv |
| Repository | frontend/backend monorepo |
| Frontend hosting 후보 | Vercel |
| Backend hosting | 미정 |

확장 검토 기준:

- 복잡한 interactive chart가 필요해지면 ECharts를 검토한다.
- D3.js는 커스텀 시각화가 명확히 필요할 때만 사용한다.
- DB와 backend hosting은 ingestion, privacy guard, saved timeline 요구가 명확해진 뒤 결정한다.

## 9. AdSense 승인 준비

필수 조건:

| 항목 | 내용 |
|---|---|
| 콘텐츠 | original dashboards, data visualization, analysis pages |
| 필수 페이지 | About, Contact, Privacy Policy, Terms, Disclaimer |
| 연락처 | support email |
| 품질 | 복제 콘텐츠가 아닌 자체 설명, 차트, 분석 제공 |

초기 공개 콘텐츠 후보:

- USCIS processing time by form/category/service center
- Visa bulletin monthly movement page
- Backlog trend explainer
- H1B processing time trend preview
- How to read USCIS processing data
- How to interpret crowd-sourced timeline data

## 10. 브랜딩 방향

브랜드 톤:

- Calm
- Reliable
- Data-driven
- Minimal
- Clear

피해야 할 표현:

- Guaranteed approval
- Best visa for you
- Recommended immigration strategy
- Approval chance
- Faster approval
- Success guarantee
- You should apply for...

## 11. 핵심 성공 요소

가장 중요한 가치:

```text
불확실성을 줄여주는 데이터 가시성
```

사용자가 원하는 가치:

- wait time visibility
- process transparency
- similar case comparison
- cohort-level trend
- recent movement visibility

주의:

- `approval certainty`는 사용자 욕구로는 존재하지만, 제품 가치 문구로 사용하지 않는다.
- 제품은 확실성을 보장하는 것이 아니라 공개/익명 데이터를 통해 흐름과 분포를 보여준다.

## 12. 핵심 원칙 요약

DO:

- 공개 데이터 기반
- 익명 timeline의 aggregate visualization
- 시각화 중심
- 정보 플랫폼 포지셔닝
- UX 차별화
- minimal/legal-safe language
- source, sample size, limitation 표시

DON'T:

- 법률 자문
- AI 비자 추천
- 승인 보장 표현
- 개인별 승인 가능성 평가
- 공격적 광고 UX
- 민감 개인정보 수집 초기 도입
- 개인별 법적 판단처럼 보이는 문구
- 공식 출처처럼 오인될 수 있는 표현
