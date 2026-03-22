# Job Platform

A mini job board API with a server-rendered frontend. Built with FastAPI, SQLAlchemy, SQLite, JWT authentication, and Pydantic validation.

---

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy ORM, SQLite
- **Auth**: JWT (python-jose), bcrypt password hashing (passlib)
- **Validation**: Pydantic v2
- **Frontend**: Jinja2 templates, Tailwind CSS (CDN), vanilla JS
- **Python**: 3.9.6

---

## Project Structure

```
job_platform/
├── app/
│   ├── main.py               # App entry point, router registration, DB init
│   ├── dependencies.py       # get_current_user dependency
│   ├── core/
│   │   ├── config.py         # Settings (SECRET_KEY, DB URL, token expiry)
│   │   └── security.py       # Password hashing, JWT creation/decoding
│   ├── db/
│   │   └── session.py        # Engine, SessionLocal, Base, get_db
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── company.py
│   │   ├── job.py
│   │   └── application.py
│   ├── schemas/              # Pydantic request/response schemas
│   │   ├── token.py
│   │   ├── user.py
│   │   ├── company.py
│   │   ├── job.py
│   │   └── application.py
│   ├── routers/              # Route handlers
│   │   ├── auth.py
│   │   ├── companies.py
│   │   ├── jobs.py
│   │   ├── applications.py
│   │   ├── admin.py
│   │   └── frontend.py
│   └── front/
│       ├── templates/        # Jinja2 HTML pages
│       └── static/           # CSS and JS
├── requirements.txt
└── env/                      # Python virtual environment
```

---

## Setup

```bash
# Activate the virtual environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the App

```bash
uvicorn app.main:app --reload
```

The app will be available at `http://localhost:8000`.
Interactive API docs (Swagger UI) are at `http://localhost:8000/docs`.

The SQLite database file (`job_platform.db`) is created automatically on first run.

---

## Test User

A user account is pre-created for testing:

| Field    | Value                |
|----------|----------------------|
| Name     | John Doe             |
| Email    | johndoe@gmail.com    |
| Password | securepassword1234   |

---

## API Endpoints

### Auth
| Method | Path             | Access    | Description              |
|--------|------------------|-----------|--------------------------|
| POST   | /auth/register   | Public    | Register a new user      |
| POST   | /auth/login      | Public    | Login, returns JWT token |
| GET    | /auth/me         | Auth      | Get current user info    |

### Companies
| Method | Path                  | Access        | Description              |
|--------|-----------------------|---------------|--------------------------|
| GET    | /companies/           | Public        | List all companies       |
| POST   | /companies/           | Auth          | Create a company         |
| GET    | /companies/{id}       | Public        | Get a single company     |
| PUT    | /companies/{id}       | Owner only    | Update company name      |
| DELETE | /companies/{id}       | Owner only    | Delete a company         |

### Jobs
| Method | Path            | Access     | Description                              |
|--------|-----------------|------------|------------------------------------------|
| GET    | /jobs/          | Public     | List all jobs (filter by ?company_id=)   |
| POST   | /jobs/          | Auth       | Post a job (must own the company)        |
| GET    | /jobs/{id}      | Public     | Get a single job                         |
| PUT    | /jobs/{id}      | Owner only | Update a job                             |
| DELETE | /jobs/{id}      | Owner only | Delete a job                             |

### Applications
| Method | Path                   | Access | Description                        |
|--------|------------------------|--------|------------------------------------|
| POST   | /jobs/{id}/apply       | Auth   | Apply for a job with a cover letter |
| GET    | /my-applications       | Auth   | List your own applications         |

### Admin
| Method | Path                  | Access | Description                                       |
|--------|-----------------------|--------|---------------------------------------------------|
| GET    | /admin/applications   | Auth   | See all applicants for your companies' vacancies  |

---

## Frontend Pages

| Path               | Description                                         |
|--------------------|-----------------------------------------------------|
| /                  | Landing page — job listings with live search        |
| /login             | Login form                                          |
| /register          | Registration form                                   |
| /companies/new     | Create a company (auth required)                    |
| /jobs/new          | Post a job vacancy (auth + company required)        |
| /my-applications   | View jobs you've applied to (auth required)         |
| /dashboard         | Manage your companies, jobs, and view applicants    |

---

## Data Models

**User** — name, phone, email, password
**Company** — name, owner (user)
**Job** — title, position, salary (USD), company
**Application** — applicant (user), job, message (cover letter)

---

## Authentication

Login returns a Bearer token. Include it in the `Authorization` header for protected endpoints:

```
Authorization: Bearer <token>
```

Tokens expire after 30 minutes by default. The `SECRET_KEY` in `app/core/config.py` should be changed before deploying to production.
