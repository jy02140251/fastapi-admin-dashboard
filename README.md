# FastAPI Admin Dashboard

A modern, full-featured admin dashboard built with **FastAPI** (backend) and **Vue 3** (frontend), featuring JWT authentication, role-based access control, and a responsive UI.

## Features

- **JWT Authentication** with access & refresh tokens
- **Role-Based Access Control** (Admin, Manager, Viewer)
- **RESTful API** with auto-generated OpenAPI docs
- **Async Database** operations with SQLAlchemy 2.0
- **Docker Compose** deployment with Nginx reverse proxy
- **Comprehensive Testing** with pytest

## Tech Stack

| Layer     | Technology                    |
|-----------|-------------------------------|
| Backend   | FastAPI, SQLAlchemy 2.0, Alembic |
| Frontend  | Vue 3, TypeScript, Pinia     |
| Database  | PostgreSQL 15                 |
| Cache     | Redis 7                       |
| Auth      | JWT (python-jose)             |
| Deploy    | Docker, Docker Compose, Nginx |

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Node.js 18+ (for frontend development)

### Installation

```bash
git clone https://github.com/jy02140251/fastapi-admin-dashboard.git
cd fastapi-admin-dashboard
cp .env.example .env
docker-compose up -d
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT License