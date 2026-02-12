# TicketMania
Event Ticket Booking System

TicketMania is a backend application where users can view events and book tickets, while admins can create and manage events.  
The system is built to handle real-world problems like overbooking, authentication, and performance.

---

## Features

- User registration and login using JWT authentication
- Role-based access (Admin / User)
- Admin can create, update, and delete events
- Users can view events and book tickets
- Prevents overbooking using database transactions
- Redis caching for faster event listing
- Dockerized setup for easy execution

---

## Tech Stack

- Backend: FastAPI (Python)
- Database: Neon PostgreSQL
- ORM: SQLAlchemy
- Authentication: JWT
- Caching: Redis
- Containerization: Docker & Docker Compose

---

## Project Structure

TicketMania/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── deps.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── events.py
│   │   └── bookings.py
│   └── utils/
│       ├── security.py
│       └── cache.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md

---

## Environment Variables

Create a `.env` file in the project root (do not commit this file):

DATABASE_URL=postgresql://<username>:<password>@<neon-host>/<database>?sslmode=require  
SECRET_KEY=your_secret_key  
REDIS_URL=redis://redis:6379/0  

---

## Running the Application

Make sure Docker is installed and running.

Build and start the services:

docker compose up --build

Access the application:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

---

## Authentication

Signup:
POST /auth/signup

Login:
POST /auth/login

Use the access token in request headers:
Authorization: Bearer <token>

---

## Events API

- POST /events – Create event (Admin only)
- GET /events – Get all events (cached)
- PATCH /events/{id} – Update event (Admin only)
- DELETE /events/{id} – Delete event (Admin only)

---

## Bookings API

- POST /bookings – Book tickets for an event
- GET /bookings/my – View logged-in user bookings

---

## Important Implementation Details

- Row-level locking is used while booking tickets to prevent overbooking
- Redis is used to cache event listings and improve performance
- JWT authentication secures all protected routes
- Docker Compose ensures consistent local setup

---

## Future Improvements

- Email notifications
- Alembic database migrations
- Pagination and filtering
- Rate limiting

---



Sreelakshmi KS  
Python Backend / Full Stack Developer
