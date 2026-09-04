from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.reservation import Reservation, ReservationStatus
from app.models.user import User, UserRole
from app.models.village import Village
from app.schemas.reservation import (
    ReservationCreate,
    ReservationRead,
    ReservationStatusUpdate,
)

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.get("", response_model=List[ReservationRead])
def list_my_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Reservation]:
    """사용자면 자신의 예약, 마을 계정이면 자기 마을로 들어온 예약(대시보드 V4)."""
    if current_user.role == UserRole.village:
        stmt = (
            select(Reservation)
            .join(Village, Village.id == Reservation.village_id)
            .where(Village.owner_id == current_user.id)
        )
    else:
        stmt = select(Reservation).where(Reservation.user_id == current_user.id)
    stmt = stmt.order_by(Reservation.created_at.desc())
    return list(db.scalars(stmt).all())


@router.post("", response_model=ReservationRead, status_code=201)
def create_reservation(
    payload: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Reservation:
    if db.get(Village, payload.village_id) is None:
        raise HTTPException(status_code=404, detail="마을을 찾을 수 없습니다.")
    reservation = Reservation(
        user_id=current_user.id,
        village_id=payload.village_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        party_size=payload.party_size,
        note=payload.note,
        status=ReservationStatus.pending,
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    # TODO: 마을 대시보드로 실시간 알림(웹소켓/푸시) 발행
    return reservation


@router.patch("/{reservation_id}/status", response_model=ReservationRead)
def update_reservation_status(
    reservation_id: int,
    payload: ReservationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Reservation:
    reservation = db.get(Reservation, reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="예약을 찾을 수 없습니다.")
    village = db.get(Village, reservation.village_id)
    if village is None or village.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="해당 마을의 예약만 처리할 수 있습니다.")
    reservation.status = payload.status
    db.commit()
    db.refresh(reservation)
    # TODO: status 가 approved 면 사용자에게 확정 알림 발송
    return reservation
