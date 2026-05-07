# 리팩터링 노트

목적: VisaAtGlance의 코드 구조 개선 계획과 구조적 부채를 관리한다.

비목적: 제품 동작, 데이터 모델, Git workflow는 각각 `developer-notes.md`, `data-model.md`, `git-workflow.md`에서 관리한다.

## 왜 필요한가

VisaAtGlance는 문서 주도 프로젝트로 시작한다. 구현이 시작되면 ingestion, cohort 계산, privacy guard, source tracking, UI state, visualization, 저장 로직이 빠르게 얽힐 수 있다.

이 문서는 frontend와 backend 경계를 작게 유지하고, 경계가 보일 때만 코드를 이동하기 위한 기준이다.

## 현재 상태

| 영역 | 상태 |
|---|---|
| App stack | Next.js frontend + FastAPI backend monorepo로 확정 |
| Frontend code | 아직 생성하지 않음 |
| Backend code | 아직 생성하지 않음 |
| Domain logic | backend 우선 계획 |
| Storage | 계획됨 |
| Tests | 계획됨 |
| Docs workflow | 생성 완료 |

## 초기 구조 방향

Next.js App Router와 FastAPI backend를 함께 두는 monorepo 구조다. 다음 scaffold 단계에서 실제 생성 구조에 맞춰 조정한다.

```txt
VisaAtGlance/
  README.md
  docs/

  frontend/
    app/
      layout.tsx
      page.tsx
      processing/
        page.tsx
      visa-bulletin/
        page.tsx
      timeline/
        page.tsx
      sources/
        page.tsx
      settings/
        page.tsx

    src/
      components/
        common/
        dashboard/
        charts/
        timeline/
        sources/
        settings/
      lib/
        api.ts
      theme/
        colors.ts
        spacing.ts
        typography.ts

  backend/
    app/
      main.py
      api/
        health.py
        processing.py
        visa_bulletin.py
        timelines.py
      domain/
        models.py
        cohorts.py
        privacy.py
        sources.py
      ingestion/
        google_sheets.py
        uscis.py
        visa_bulletin.py
      storage/
        repository.py
      tests/
        test_health.py
        test_cohorts.py
        test_privacy.py
```

이 구조는 방향이지, 한 번에 모든 파일을 완성하라는 뜻은 아니다.

## 리팩터링 원칙

| 원칙 | 설명 |
|---|---|
| 동작 유지 | 리팩터링 변경은 명시적 제품 변경이 아니면 동작을 바꾸지 않는다 |
| 작은 변경 | 큰 구조 재작성은 작은 PR로 나눈다 |
| frontend/backend 경계 유지 | ingestion, cohort, privacy guard는 backend가 소유하고 frontend는 presentation에 집중한다 |
| domain은 framework-independent | backend domain logic은 FastAPI route와 분리해 테스트 가능하게 둔다 |
| storage는 좁은 API 뒤에 둔다 | 저장 방식 변경이 route와 UI 전체에 퍼지지 않게 한다 |
| UI는 dashboard-first | 공개 정보와 chart를 빠르게 이해하는 밀도 있는 화면을 우선한다 |

## 기능 전 gate

큰 기능 전에 필요한 foundation:

| Gate | 목적 |
|---|---|
| monorepo scaffold | `frontend/`, `backend/` 실행 구조 확보 |
| Backend `/health` | frontend/backend 연결과 배포 확인의 최소 기준 |
| Domain types/models | visa, timeline, source, cohort record를 일관되게 유지 |
| Privacy guard | small cohort suppression과 row-level 공개 제한을 공통 처리 |
| Source freshness helper | stale/official/sample size 표시 로직 중복 방지 |
| Chart primitives | Recharts 기반 기본 card/chart wrapper 정리 |
| Basic tests | backend cohort 계산과 privacy guard 보호 |

## 아직 하지 말 것

| 항목 | 이유 |
|---|---|
| global frontend state library 도입 | 초기 규모에서는 React state/context로 충분한지 먼저 확인 |
| backend hosting 고정 | 운영 요구가 더 명확해진 뒤 결정 |
| DB 선도입 | ingestion 형태와 저장 요구를 확인한 뒤 선택 |
| D3.js 선도입 | MVP chart는 Recharts로 충분한지 먼저 검증 |
| 복잡한 recommendation engine | 통계 비교와 dashboard 가시성이 먼저다 |
| 자동 scraping 가정 | 비자 데이터는 source, freshness, limitation 정책이 먼저 필요하다 |

## Refactor MR 체크리스트

- [ ] 동작이 유지되는가?
- [ ] unrelated product change가 섞이지 않았는가?
- [ ] frontend/backend 경계가 명확한가?
- [ ] backend domain logic이 route 밖에서도 테스트 가능한가?
- [ ] storage 변경이 있으면 호환성 메모가 있는가?
- [ ] 변경 위험에 맞는 테스트 또는 수동 확인을 했는가?
- [ ] 구조 결정이 바뀌었다면 docs를 업데이트했는가?
