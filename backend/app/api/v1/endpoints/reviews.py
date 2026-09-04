from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.review import Review
from app.models.subscription import Subscription
from app.models.user import User
from app.models.village import Village
from app.schemas.review import ReviewCreate, ReviewRead

router = APIRouter(tags=["reviews"])


@router.get("/villages/{village_id}/reviews", response_model=List[ReviewRead])
def list_village_reviews(village_id: int, db: Session = Depends(get_db)) -> List[Review]:
    stmt = (
        select(Review)
        .where(Review.village_id == village_id)
        .order_by(Review.created_at.desc())
    )
    return list(db.scalars(stmt).all())


@router.post("/reviews", response_model=ReviewRead, status_code=201)
def create_review(
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Review:
    if db.get(Village, payload.village_id) is None:
        raise HTTPException(status_code=404, detail="마을을 찾을 수 없습니다.")
    review = Review(
        village_id=payload.village_id,
        user_id=current_user.id,
        rating=payload.rating,
        content=payload.content,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.post("/villages/{village_id}/subscribe", status_code=201)
def subscribe_village(
    village_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """방문 후 마을 구독(U5) — 양쪽에 '관계'가 남습니다."""
    if db.get(Village, village_id) is None:
        raise HTTPException(status_code=404, detail="마을을 찾을 수 없습니다.")
    existing = db.scalar(
        select(Subscription).where(
            Subscription.user_id == current_user.id,
            Subscription.village_id == village_id,
        )
    )
    if existing is None:
        db.add(Subscription(user_id=current_user.id, village_id=village_id))
        db.commit()
    return {"subscribed": True, "village_id": village_id}
