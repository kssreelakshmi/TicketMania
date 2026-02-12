from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    event_date: datetime
    total_seats: int


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    event_date: Optional[datetime] = None
    total_seats: Optional[int] = None


class EventResponse(EventBase):
    id: int
    available_seats: int
    created_at: datetime

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    event_id: int
    seats_booked: int = Field(gt=0)


class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    seats_booked: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
