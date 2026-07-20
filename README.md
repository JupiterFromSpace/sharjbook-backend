ShargBook 
A backend system for managing building service charges, residents, and payments — built with Django REST Framework.
ShargBook helps building managers track residential units, calculate and issue monthly charge invoices, and manage residents, while giving residents visibility into their own payment history through a role-based API.

Features:
    JWT Authentication with role-based access control for residents and building managers.
    Building & unit management — register buildings, residential units, and assign residents.
    Automated monthly charge invoicing for residential units.
    Background task processing with Celery + Redis for scheduled payment reminders and notifications.
    Redis caching on dashboard statistics and heavy aggregation queries to reduce database load.
    Dockerized deployment with Nginx as a reverse proxy and Gunicorn as the application server.
    

Tech Stack:
    Layer	                Technology
    Backend	                Python, Django, Django REST Framework
    Database	            PostgreSQL
    Auth	                JWT (SimpleJWT)
    Background Tasks	    Celery, Redis
    Caching	                Redis
    Web Server	            Gunicorn, Nginx
    Containerization	    Docker, Docker Compose
    CI/CD	                GitHub Actions


Architecture:
    The project is organized into three independent Django apps, each owning its own models and API endpoints:



sharjbook-backend/
├── core/
│   ├── accounts/     # Authentication, users, roles
│   ├── buildings/    # Buildings, residential units, residents
│   └── finance/      # Charges, invoices, payments
├── docker-compose.yml
├── docker-compose-stage.yml
├── Dockerfile
├── default.conf         # Nginx config
└── requirements.txt

_________________________

Getting Started
  
  Prerequisites:
        Docker & Docker Compose
        Python 3.11+ (for local development outside Docker)

  Run with Docker Compose:
          git clone https://github.com/JupiterFromSpace/sharjbook-backend.git
          cd sharjbook-backend
          cp .env.example .env   # fill in your own values
          docker compose up --build

  The API will be available at http://localhost:8000/.

  Note: After changing .env, restart with docker compose up --build — a plain up -d will not re-read environment changes.


  Environment Variables:
        Create a .env file in the project root with (at minimum):
                    SECRET_KEY=your-django-secret-key
                    DEBUG=True
                    DATABASE_URL=postgres://user:password@db:5432/sharjbook
                    REDIS_URL=redis://redis:6379/0
                    ALLOWED_HOSTS=localhost,127.0.0.1
                    
  Running Migrations:
          docker-compose exec web python manage.py migrate
          docker-compose exec web python manage.py createsuperuser

        
  API Documentation:
          Interactive API docs are available via Swagger/OpenAPI once the server is running:
                    http://localhost:8000/swagger/


  Author:
          Sina Matari — github.com/JupiterFromSpace


  License:
          This project is licensed under the MIT License — see the LICENSE file for details.
