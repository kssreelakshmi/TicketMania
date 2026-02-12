from fastapi import APIRouter

from app.routers.auth import router as auth_router
from app.routers.events import router as events_router
# from app.routers.bookings import router as bookings_router

api_router = APIRouter()

# Register all routers here
api_router.include_router(auth_router)
api_router.include_router(events_router)
# api_router.include_router(bookings_router)
