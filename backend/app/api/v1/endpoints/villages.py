from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User, UserRole
from app.models.village import Village
from app.schemas.village import VillageCreate, VillageRead

router = APIRouter(prefix="/villages", tags=["villages"])


@router.get("", response_model=List[VillageRead])
def list_villages(
    db: Session = Depends(get_db),
    region: Optional[str] = Query(default=None),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
) -> List[Village]:
    stmt = select(Village)
    if region:
        stmt = stmt.where(Village.region == region)
    stmt = stmt.order_by(Village.created_at.desc()).limit(limit).offset(offset)
    return list(db.scalars(stmt).all())


@router.get("/{village_id}", response_model=VillageRead)
def get_village(village_id: int, db: Session = Depends(get_db)) -> Village:
    village = db.get(Village, village_id)
    if village is None:
        raise HTTPException(status_code=404, detail="마을을 찾을 수 없습니다.")
    return village


@router.post("", response_model=VillageRead, status_code=201)
def create_village(
    payload: VillageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Village:
    if current_user.role != UserRole.village:
        raise HTTPException(status_code=403, detail="마을 계정만 등록할 수 있습니다.")
    village = Village(
        owner_id=current_user.id,
        name=payload.name,
        region=payload.region,
        description=payload.description,
    )
    db.add(village)
    db.commit()
    db.refresh(village)
    return village
