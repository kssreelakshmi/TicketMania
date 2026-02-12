# TicketMania
Event Ticket Booking System

TicketMania is a backend application where users can view events and book tickets, while admins can create and manage events.
The system is built to handle real-world problems like overbooking, authentication, and performance.

TicketMania/
├── app/
│   ├── main.py          # App entry point
│   ├── database.py      # Database connection
│   ├── models.py        # Database tables
│   ├── schemas.py       # Request/response models
│   ├── deps.py          # Auth & DB dependencies
│   ├── routers/
│   │   ├── auth.py      # Login & signup
│   │   ├── events.py   # Event APIs
│   │   └── bookings.py # Booking APIs
│   └── utils/
│       ├── security.py # JWT & password hashing
│       └── cache.py    # Redis cache logic
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
