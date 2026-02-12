from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import api_router
from app.database import Base, engine


def create_tables():
    """
    automatically create tables.
    """
    Base.metadata.create_all(bind=engine)


app = FastAPI(title="TicketMania Booking System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def health_check():
    return {"status": "ok"}

create_tables()