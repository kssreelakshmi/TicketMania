from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app.schemas import BookingCreate, BookingResponse
from app.models import Booking, Event
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


# -------------------------
# Create Booking
# -------------------------
@router.post("/", response_model=BookingResponse, status_code=201)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a booking with row-level locking to prevent overbooking.
    """

    try:
        # Lock the event row
        event = (
            db.query(Event)
            .filter(Event.id == booking_data.event_id)
            .with_for_update()
            .first()
        )

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        if booking_data.seats_booked > event.available_seats:
            raise HTTPException(
                status_code=400,
                detail="Not enough seats available"
            )

        # Deduct seats
        event.available_seats -= booking_data.seats_booked

        # Create booking
        booking = Booking(
            user_id=current_user.id,
            event_id=event.id,
            seats_booked=booking_data.seats_booked,
            status="confirmed"
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking

    except:
        db.rollback()
        raise


# -------------------------
# Get My Bookings
# -------------------------
@router.get("/my", response_model=List[BookingResponse])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get bookings for the logged-in user.
    """

    bookings = (
        db.query(Booking)
        .filter(Booking.user_id == current_user.id)
        .order_by(Booking.created_at.desc())
        .all()
    )

    return bookings
