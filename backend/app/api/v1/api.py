from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, reservations, reviews, villages

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(villages.router)
api_router.include_router(reservations.router)
api_router.include_router(reviews.router)
