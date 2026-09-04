# 협업 가이드 (2인)

## 0. 최초 1회 셋업

```bash
git clone <repo-url> comma
cd comma
```

- 백엔드: [backend/README.md](backend/README.md) — Python 3.12 + venv + `pip install -r requirements-dev.txt`
- 모바일: [mobile/README.md](mobile/README.md) — Node 20 + `npm ci`
- 루트: `npm install` (concurrently 및 mobile 의존성 설치)

버전은 `backend/.python-version`, `.nvmrc` 에 고정되어 있습니다.
pyenv / nvm 을 쓰면 폴더 진입 시 자동으로 맞춰집니다.

### 실행

Expo는 QR/대화형 메뉴를 띄우려면 실제 터미널(TTY)이 필요해서, **터미널 2개로 나눠서**
실행하는 게 기본입니다.

| 명령 (루트) | 동작 |
| --- | --- |
| `npm run dev:api` | 백엔드만 (터미널 1) |
| `npm run dev:app` | 모바일만, QR/메뉴 정상 표시 (터미널 2) |
| `npm run dev` | 백엔드+모바일 한 터미널에 로그만 같이 — **QR 안 뜸**, 헬스체크 용도 |

`npm run dev:api` 는 `backend/.venv` 의 파이썬을 직접 호출하므로 venv 활성화가
필요 없습니다. 단, `backend/.venv` 는 최초 1회 직접 만들어야 합니다.

## 1. 브랜치 전략

- `main` — 항상 실행 가능한 상태. 직접 push 금지 (GitHub 에서 branch protection 설정).
- 작업은 브랜치에서: `feat/village-matching`, `fix/reservation-status`, `chore/ci` …

```bash
git switch -c feat/onboarding
# ... 작업 ...
git add -A && git commit -m "feat(mobile): 온보딩 관심사 선택 화면"
git push -u origin feat/onboarding
# GitHub 에서 Pull Request 생성 → 상대방 리뷰 → Squash merge
```

2인이라 리뷰가 부담되면 최소 규칙만: **서로의 PR에 대충이라도 한 번 훑고 Approve**,
본인 코드 self-merge 는 작은 변경만.

## 2. 커밋 메시지 (권장, 강제 아님)

`<type>(<scope>): <요약>` — type: feat / fix / chore / docs / refactor / test
scope: mobile / backend / db …

## 3. 의존성 추가

락파일이 핵심입니다. 추가 후 **반드시 락파일까지 커밋**하고, 상대방은 pull 후 재설치.

| | 추가 | 상대방 |
| --- | --- | --- |
| 백엔드 | `requirements.txt` 편집 + `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| 모바일 | `npx expo install <pkg>` | `npm ci` |

## 4. DB 스키마 변경

모델(`backend/app/models/`) 을 바꾸면:

- 로컬(SQLite)은 `dev.db` 삭제하면 재생성됨 (개발 초기 단계)
- 운영 전환 후에는 Alembic 마이그레이션 파일을 만들어 커밋
  (`alembic revision --autogenerate -m "..."`)

## 5. 시크릿 / 환경변수

- `.env` 는 **커밋하지 않습니다** (`.gitignore` 처리됨).
- 키가 추가되면 `.env.example` 을 업데이트해서 커밋하고, 실제 값은 1Password / 메신저 등
  코드 밖 경로로 공유.
- AWS 키는 절대 커밋 금지. 노출되면 즉시 로테이션.

## 6. 충돌이 잦은 파일

- `package-lock.json` 충돌: 한쪽 버전 채택 후 `npm install` 로 재생성하는 게 빠름.
- `dev.db`, `.expo/`, `__pycache__/` 등은 커밋 대상이 아님 (`.gitignore` 확인).
