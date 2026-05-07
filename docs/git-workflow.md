# Git 워크플로우

VisaAtGlance 작업은 계획, 구현, 검토, 푸쉬를 분리해서 진행한다.

## 작업 전 필수 절차

코드 구현 전에는 먼저 구체적인 제안을 사용자에게 보여주고 확인받는다.

| 항목 | 포함할 내용 |
|---|---|
| 목표 | 어떤 문제를 해결하는지 |
| 접근 방식 | 어떤 모델, UI, 저장소, 로직을 바꾸는지 |
| 영향 범위 | 어떤 화면, 데이터, 테스트, 기존 흐름이 영향을 받을 수 있는지 |
| 대안 | 가능한 다른 접근과 선택하지 않는 이유 |
| MR 크기 | 하나의 작은 브랜치로 충분한지, 나눠야 하는지 |

사용자가 방향을 확인한 뒤에 구현을 시작한다.

예외:

- 명확한 오타 수정
- 깨진 import 수정
- 실패한 테스트의 직접 수정
- 사용자가 명시적으로 요청한 문서-only 수정
- 앱이 깨져 있는 긴급 수정

예외 상황에서도 커밋이나 푸쉬 전에는 영향 범위를 설명한다.

## 브랜치 전략

| 브랜치 | 역할 |
|---|---|
| `main` | 안정 버전. 직접 기능 작업을 피한다 |
| `codex/<name>` | Codex 작업 브랜치 |

규칙:

- 한 브랜치는 하나의 의미 있는 변경만 담는다.
- 모델, 저장소, UI를 함께 건드리는 변경은 작게 나눈다.
- `main`에 머지하기 전에는 관련 체크를 통과해야 한다.

## 커밋 규칙

- 관련 변경만 함께 커밋한다.
- 사용자가 만든 unrelated 변경은 stage/revert하지 않는다.
- docs-only 변경은 코드 변경과 분리할 수 있다.
- Git에 남는 로그는 한국어로 작성한다. 커밋 메시지, PR 제목, PR 본문, merge 관련 설명은 기본적으로 한국어를 사용한다.
- 커밋 메시지는 가능하면 다음 형식을 따른다.

```text
<type>: <한국어 요약>
```

예시:

```text
docs: 페이지 모델 문서화
chore: 프론트엔드 백엔드 스캐폴드 추가
```

권장 type:

| type | 용도 |
|---|---|
| `feat` | 기능 추가 |
| `fix` | 버그 수정 |
| `refactor` | 동작 유지 구조 변경 |
| `docs` | 문서 변경 |
| `test` | 테스트 추가/수정 |
| `chore` | 기타 관리 작업 |

## 프로젝트별 GitHub SSH 키

여러 GitHub 계정을 함께 사용할 때는 전역 GitHub 계정을 바꾸지 않는다. 대신 프로젝트별 SSH host alias를 만들고, 해당 프로젝트의 `origin`만 그 alias를 쓰게 한다.

VisaAtGlance는 권한 있는 GitHub 계정의 SSH alias인 `github-enzimas`를 사용한다.

현재 기준 원격 URL:

```bash
git remote set-url origin git@github-enzimas:enzimasjody-dotcom/VisaAtGlance.git
```

확인 명령:

```bash
git remote -v
ssh -T git@github-enzimas
```

정상 인증 예시:

```text
Hi enzimasjody-dotcom! You've successfully authenticated, but GitHub does not provide shell access.
```

`~/.ssh/config` 예시:

```sshconfig
Host github-enzimas
  HostName github.com
  User git
  IdentityFile ~/.ssh/<project-specific-private-key>
  IdentitiesOnly yes
```

규칙:

- 다른 프로젝트의 GitHub 인증에 영향을 주지 않기 위해 전역 SSH 기본값을 바꾸지 않는다.
- 이 프로젝트의 `origin`은 `github.com`이 아니라 `github-enzimas` alias를 사용한다.
- 푸쉬가 권한 문제로 실패하면 먼저 `git remote -v`와 `ssh -T git@github-enzimas`를 확인한다.
- 새 Mac이나 새 환경에서는 private key, public key 등록, `~/.ssh/config`, `origin` URL 네 가지를 모두 확인한다.
- 문서에는 private key 내용, passphrase, access token을 기록하지 않는다.

## 구현 후 검토 체크리스트

커밋이나 푸쉬 전 다음 내용을 사용자에게 정리해 보여준다.

- [ ] 변경된 파일과 이유
- [ ] 영향을 받을 수 있는 화면/기능
- [ ] 저장소, sync, migration, 데이터 호환성 영향
- [ ] 추가된 테스트 또는 수정된 테스트
- [ ] 실행한 QA 명령과 결과
- [ ] 수동 확인한 시나리오
- [ ] docs 전체를 훑고 오래된 내용이나 새 변경과 충돌하는 내용이 없는지 확인
- [ ] 필요한 docs 업데이트를 같은 MR 또는 별도 docs MR로 반영
- [ ] 확인하지 못한 항목과 이유

## Docs 최신화 규칙

푸쉬 전에는 `docs/`의 모든 문서를 빠르게 검토한다. 코드나 제품 결정이 바뀌었는데 문서가 오래된 상태로 남으면, 해당 변경은 푸쉬 전에 업데이트하거나 별도 docs MR로 분리한다.

| 문서 | 확인할 내용 |
|---|---|
| `docs/README.md` | 문서 역할, 작성 규칙, 새 결정 기록 절차가 최신인지 |
| `docs/developer-notes.md` | 제품 동작, 화면 목적, 구현 원칙이 최신인지 |
| `docs/data-model.md` | 모델, 필드, 상태값, 저장 키, 관계가 최신인지 |
| `docs/refactoring-notes.md` | 완료된 리팩터링, 다음 순서, 폴더 구조 계획이 최신인지 |
| `docs/git-workflow.md` | 작업 전 승인, QA, SSH alias, 푸쉬 규칙이 최신인지 |
| `docs/product-spec-v0.1.md` | 초기 스펙 보관 문서로 유지되는지, 현재 기준 문서와 충돌을 만들지 않는지 |

## 문서 변경 diff 승인 절차

문서를 수정할 때는 파일별 diff를 보여주고 사용자 승인을 받은 뒤 다음 단계로 넘어간다.

규칙:

- 문서 변경 후 `git diff --check`를 실행한다.
- 변경된 문서 파일을 하나씩 나누어 diff를 보여준다.
- 새 파일은 전체 내용을 보여주기보다 구조와 핵심 섹션 diff를 우선 보여준다.
- diff가 길면 바뀐 섹션 중심으로 잘라 보여주되, 생략 사실을 명시한다.
- 사용자가 승인하기 전에는 커밋, 푸쉬, 다음 대규모 문서 수정으로 넘어가지 않는다.
- 사용자가 수정 요청을 하면 해당 파일을 고친 뒤 다시 그 파일의 diff를 보여준다.

## 푸쉬 전 체크리스트

푸쉬 전에는 impact checklist를 다시 작성한다.

```md
## Pre-Push Impact Checklist

Changed files:
- ...

Potentially affected implementation:
- ...

Checks run:
- ...

Manual checks:
- ...

Docs checked:
- Ready / Updated / Not needed

Not checked:
- ...

Push decision:
- Ready / Not ready
```

Push decision이 `Ready`일 때만 푸쉬한다.

## 기본 QA

| 변경 종류 | 기본 확인 |
|---|---|
| docs-only 변경 | `git diff --check` |
| TypeScript 코드 변경 | `npx tsc --noEmit` |
| unit-tested logic | 프로젝트 테스트 명령 |
| UI wiring 변경 | 가능한 경우 수동 smoke check 또는 browser check |
| storage/data model 변경 | load/save, migration, 기존 데이터 호환성 |

## 현재 QA 한계

| 항목 | 상태 |
|---|---|
| App stack | 아직 선택하지 않음 |
| 자동 테스트 | 아직 설정하지 않음 |
| 수동 UI 확인 | 실행 가능한 첫 앱이 생긴 뒤 시작 |
