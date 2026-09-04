from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Subscription(Base):
    """방문 후 사용자가 마을을 구독(U5). 양쪽에 남는 '관계'."""

    __tablename__ = "subscriptions"
    __table_args__ = (UniqueConstraint("user_id", "village_id", name="uq_subscription"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    village_id: Mapped[int] = mapped_column(ForeignKey("villages.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
