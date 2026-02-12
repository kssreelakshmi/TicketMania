from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.utils.cache import get_cache, set_cache, delete_cache
from app.schemas import (EventCreate, EventUpdate, EventResponse)
from app.models import Event
from app.deps import get_db, get_current_admin, get_current_user

router = APIRouter(prefix="/events", tags=["Events"])



# Create Event (Admin Only)
@router.post("/", response_model=EventResponse, status_code=201)
def create_event(event_data: EventCreate, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):

    new_event = Event(
        title = event_data.title,
        description = event_data.description,
        location = event_data.location,
        event_date = event_data.event_date,
        total_seats = event_data.total_seats,
        available_seats = event_data.total_seats,  # auto-set
        created_at = datetime.utcnow()
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


@router.get("/", response_model=List[EventResponse])
def get_events(db: Session = Depends(get_db)):
    cache_key = "events_list"

    cached_events = get_cache(cache_key)
    if cached_events:
        return cached_events

    events = db.query(Event).order_by(Event.event_date.asc()).all()

    # Convert ORM → dict
    events_data = [
        {
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "location": e.location,
            "event_date": e.event_date.isoformat(),
            "total_seats": e.total_seats,
            "available_seats": e.available_seats,
            "created_at": e.created_at.isoformat(),
        }
        for e in events
    ]

    set_cache(cache_key, events_data)
    return events_data



# Update Event (Admin Only)
@router.patch("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, update_data: EventUpdate, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):

    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    # Patch update (only provided fields)
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(event, key, value)

    # If total_seats changed, adjust available_seats carefully
    if update_data.total_seats is not None:
        if update_data.total_seats < event.total_seats - event.available_seats:
            raise HTTPException(
                status_code=400,
                detail="Cannot reduce total seats below seats already booked"
            )

        # adjust available seats proportionally
        seats_used = event.total_seats - event.available_seats
        event.available_seats = update_data.total_seats - seats_used

    db.commit()
    db.refresh(event)

    return event



# Delete Event (Admin Only)

@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()

    return {"detail": "Event deleted successfully"}
