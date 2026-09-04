from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.base import Base  # 모든 모델 등록
from app.db.session import engine


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 개발 편의: 시작 시 테이블 자동 생성.
    # 운영에서는 이 줄을 지우고 Alembic 마이그레이션을 사용하세요.
    Base.metadata.create_all(bind=engine)

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.get("/", tags=["root"])
    def root() -> dict:
        return {"service": settings.PROJECT_NAME, "docs": "/docs"}

    return app


app = create_app()
