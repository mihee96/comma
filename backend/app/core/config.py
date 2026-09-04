from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Comma API"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "local"

    # 로컬: SQLite (설정 없이 실행) / 운영: AWS RDS MySQL
    # 예) mysql+pymysql://comma:PASSWORD@comma-db.xxxx.ap-northeast-2.rds.amazonaws.com:3306/comma
    DATABASE_URL: str = "sqlite:///./dev.db"

    SECRET_KEY: str = "dev-secret-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # 콤마 구분 문자열. "*" 이면 전체 허용.
    BACKEND_CORS_ORIGINS: str = "*"

    @property
    def cors_origins(self) -> List[str]:
        raw = self.BACKEND_CORS_ORIGINS.strip()
        if raw == "*" or raw == "":
            return ["*"]
        return [origin.strip() for origin in raw.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
