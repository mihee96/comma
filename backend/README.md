# Comma API (FastAPI)

## 개발 환경

- **Python 3.12** (`.python-version` 참고). 3.11+ 면 동작.
- venv 는 **시스템에 설치된 Python** 으로 만드세요. 다른 가상환경이 활성화된 상태에서
  `python -m venv` 를 하면 격리가 깨질 수 있습니다 (`where python` / `which python` 확인).

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
copy .env.example .env            # cp .env.example .env
uvicorn app.main:app --port 8000
```

- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

로컬은 SQLite(`dev.db`) 로 설정 없이 실행됩니다. 앱 시작 시 테이블이 자동 생성됩니다.

> 자동 재시작을 쓰려면 `pip install watchfiles` 후 `uvicorn app.main:app --reload --port 8000`.

## 의존성 버전 관리

`requirements*.txt` 는 정확한 버전(`==`)으로 고정되어 있습니다. 두 사람 모두 동일한
버전을 받습니다. **패키지를 추가/변경하면** `requirements.txt` 를 직접 편집하고
`pip install -r requirements.txt` 후 커밋 → PR 로 공유하세요.

- `requirements.txt` — 코어 (로컬 개발)
- `requirements-dev.txt` — + pytest, httpx
- `requirements-prod.txt` — + MySQL 인증(cryptography), gunicorn, uvicorn[standard]

## DB

| 환경 | DB | URL |
| --- | --- | --- |
| 로컬 | SQLite | `sqlite:///./dev.db` (기본값) |
| 운영 | AWS RDS **MySQL 8** | `mysql+pymysql://user:pw@host:3306/comma?charset=utf8mb4` |

로컬에서도 MySQL 로 맞추고 싶으면 로컬에 MySQL 을 설치하거나 Docker 로 띄운 뒤
`.env` 의 `DATABASE_URL` 을 바꾸면 됩니다. 모델은 MySQL 호환(`VARCHAR` 길이 지정,
문자열 Enum)으로 작성되어 있습니다.

## 테스트

```bash
pip install -r requirements-dev.txt
pytest
```

## 마이그레이션 (Alembic)

운영에서는 `app/main.py` 의 `Base.metadata.create_all` 을 제거하고 사용:

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## 구조

```
app/
├── main.py                 # 앱 생성, CORS, 라우터 등록, (개발용) create_all
├── core/config.py          # 환경설정 (pydantic-settings)
├── core/security.py        # 비밀번호 해시 + JWT
├── api/deps.py             # get_db, get_current_user
├── db/                     # Base, 엔진/세션
├── models/                 # User, Village, Reservation, Review, Subscription
├── schemas/                # Pydantic 스키마
└── api/v1/
    ├── api.py              # 라우터 취합
    └── endpoints/          # health, auth, villages, reservations, reviews
```

## AWS 배포 메모

- **DB**: RDS MySQL 8. `.env` 의 `DATABASE_URL` 교체. 파라미터 그룹에서 `utf8mb4` 확인.
- **실행**: `gunicorn -k uvicorn.workers.UvicornWorker app.main:app`
- **시크릿**: `SECRET_KEY`, `DATABASE_URL` 은 SSM Parameter Store / Secrets Manager 로 주입.
- **CORS**: `BACKEND_CORS_ORIGINS` 를 앱 도메인만 허용으로 좁히기.
