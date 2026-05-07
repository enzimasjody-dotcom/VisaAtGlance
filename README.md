# VisaAtGlance

VisaAtGlance는 미국 비자 및 이민 관련 공개 데이터와 익명 timeline 데이터를 직관적으로 시각화하여, 사용자가 미국 이민 프로세스를 한눈에 이해할 수 있도록 돕는 정보 플랫폼이다.

이 저장소는 문서 주도 workflow로 시작한다. 제품 결정, 데이터 구조, 리팩터링 계획, Git 절차를 `docs/`에서 분리해 관리한다.

---

## 빠른 시작

앱 스택은 frontend와 backend를 함께 두는 monorepo 기준으로 확정한다.

| 영역 | 선택 |
|---|---|
| Repo 구조 | `frontend/`, `backend/`, `docs/` monorepo |
| Frontend | Next.js + React + TypeScript |
| Backend | FastAPI + Python |
| Visualization 시작점 | Recharts |
| Visualization 확장 | ECharts, D3.js |
| Styling | Tailwind CSS |
| Frontend hosting | Vercel |
| Backend hosting | 초기 로컬, 배포는 추후 결정 |
| Frontend package manager | npm |
| Backend package manager | scaffold 시 `uv` 우선 검토 |

아직 앱 scaffold는 생성하지 않았다. 다음 단계에서 `frontend/`와 `backend/`를 만든 뒤 아래 명령을 실제 실행 명령으로 업데이트한다.

```bash
# TODO: frontend install/run
# TODO: backend install/run
```

---

## 핵심 방향

| 원칙 | 설명 |
|---|---|
| 한눈에 이해 | 비자/이민 데이터를 빠르게 훑을 수 있게 요약한다 |
| 데이터 출처 명시 | source, checked date, sample size, limitation을 함께 보여준다 |
| 법률 자문 금지 | 비자 추천, 승인 가능성 평가, 개인별 전략을 제공하지 않는다 |
| Backend-first data logic | ingestion, cohort, privacy guard는 backend/domain 쪽에 둔다 |
| 공개/로그인 분리 | 공개 chart와 로그인 사용자용 advanced 기능을 구분한다 |
| 문서 주도 | 중요한 제품/구현 결정은 `docs/`에 기록한다 |

---

## 문서

| 문서 | 내용 |
|---|---|
| [문서 지도](docs/README.md) | 각 문서의 역할과 작성 규칙 |
| [개발자 노트](docs/developer-notes.md) | 현재 제품/구현 기준 |
| [데이터 모델](docs/data-model.md) | 핵심 모델, 필드, 관계, 저장 키 |
| [로드맵](docs/roadmap.md) | 단계별 구현 현황, 다음 계획, 장기 비전 |
| [리팩터링 노트](docs/refactoring-notes.md) | 코드 구조 개선 계획 |
| [Git 워크플로우](docs/git-workflow.md) | 계획, 커밋, 푸쉬, QA 규칙 |
| [제품 스펙 v0.1](docs/product-spec-v0.1.md) | 초기 제품 아이디어 보관 |

---

## 현재 개발 초점

| 초점 | 상태 |
|---|---|
| 제품 방향 | 정보/데이터 시각화 플랫폼으로 정리 완료 |
| 앱 스택 | Next.js frontend + FastAPI backend monorepo로 확정 |
| 데이터 모델 | 초안 작성 완료 |
| 문서 workflow | ClassPilot 형식을 참고해 생성 완료 |
| 첫 구현 | `frontend/`, `backend/` scaffold 예정 |

---

## 기본 QA

문서-only 변경:

```bash
git diff --check
```

앱 scaffold 후 frontend/backend typecheck, lint, test, build 명령을 이 섹션에 추가한다.
