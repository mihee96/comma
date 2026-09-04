# Comma (촌스테이)

농촌 마을 체험·예약 플랫폼. 일반 사용자는 관심사 기반으로 마을을 추천받아 예약하고,
방문 후 마을을 구독해 관계를 이어갑니다. 마을 주민(이장)은 마을을 등록하고 예약을
승인/거절하며 리뷰·커뮤니티로 소통합니다. (`mockup_v2.pdf` 참고)

두 플로우의 연결점:

- **예약**: 사용자가 신청 → 마을 대시보드에 실시간 표시 → 마을 승인 시 사용자에게 확정 알림
- **관계**: 방문 후 사용자는 마을을 구독, 마을은 리뷰 게시판으로 소통 → 양쪽에 관계가 남음

## 스택

| 영역       | 기술                                             |
| ---------- | ------------------------------------------------ |
| 모바일     | React Native + Expo (Expo Go), TypeScript        |
| 상태/데이터 | Zustand, TanStack Query, Axios                   |
| 백엔드     | FastAPI, SQLAlchemy 2.0, Pydantic v2             |
| DB         | 로컬: SQLite · 운영: AWS RDS **MySQL 8**          |
| 인증       | JWT (PyJWT), 비밀번호 해시(passlib pbkdf2_sha256) |

## 폴더 구조

```
comma/
├── package.json     # 루트: 백엔드+모바일 동시 실행 스크립트 (concurrently)
├── scripts/         # run-backend.mjs (venv 파이썬으로 uvicorn 실행)
├── mobile/          # Expo 앱   (.nvmrc → Node 20)
│   └── src/{api,components,screens,navigation,store,hooks,constants,types,utils}
├── backend/         # FastAPI 서버   (.python-version → 3.12)
│   └── app/{api,core,db,models,schemas}
└── CONTRIBUTING.md  # 협업 흐름 (브랜치/PR, 의존성, 시크릿)
```

## 사전 준비

- **Node.js 20 LTS** + npm — https://nodejs.org (nvm 사용 시 `nvm install 20`)
- **Python 3.12** (3.11+ 가능) — 다른 venv 가 활성화되지 않은 상태에서 사용
- Expo Go 앱 (iOS/Android 스토어)

버전 재현성: 라이브러리는 `requirements*.txt` / `package-lock.json` 으로 고정,
런타임 버전은 `.python-version` / `.nvmrc` 로 고정합니다. 자세한 협업 규칙은
[CONTRIBUTING.md](CONTRIBUTING.md).

## 빠른 시작

### 0) 최초 1회 셋업

```bash
# 백엔드 가상환경 (sparta_web 등 다른 venv 가 활성화 안 된 상태에서!)
cd backend
py -3.12 -m venv .venv                     # macOS/Linux: python3.12 -m venv .venv
.venv\Scripts\Activate.ps1                 # macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
cd ..

# 루트 + 모바일 의존성 (postinstall 이 mobile 까지 설치)
npm install
cp mobile/.env.example mobile/.env         # EXPO_PUBLIC_API_URL 을 PC 의 LAN IP 로 수정
```

### 1) 실행 — 터미널 2개 (권장)

Expo는 QR 코드/대화형 메뉴(`a`, `i`, `r` …)를 띄우려면 **진짜 터미널(TTY)** 이 필요합니다.
`concurrently`로 합쳐서 실행하면 파이프로 인식돼 QR이 아예 안 뜨니, 실제로 앱을 열 땐
터미널을 나눠서 쓰세요.

```bash
# 터미널 1
npm run dev:api      # FastAPI  http://localhost:8000/docs · /api/v1/health (--reload)

# 터미널 2
npm run dev:app      # Expo 개발 서버 → 여기 뜨는 QR 을 Expo Go 로 스캔
```

로컬 DB 는 SQLite 로 설정 없이 실행됩니다 (운영은 RDS MySQL).

> 실기기/안드로이드 에뮬레이터에서는 `localhost` 가 PC 를 가리키지 않습니다.
> `mobile/.env` 의 `EXPO_PUBLIC_API_URL` 을 `http://<PC-LAN-IP>:8000/api/v1` 로 바꾸세요.

### 1-b) 한 터미널에서 같이 로그만 보고 싶을 때

```bash
npm run dev
```

백엔드+모바일을 한 번에 띄우지만 **QR 이 출력되지 않습니다** (TTY 아님). 두 서버가
잘 뜨는지 로그만 확인할 때 쓰고, Expo Go로 실제로 열어볼 땐 위 1) 방식을 쓰세요.

자세한 내용: [backend/README.md](backend/README.md) · [mobile/README.md](mobile/README.md)
