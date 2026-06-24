# Student Management System

A REST API built with FastAPI for managing students, courses, enrollments, and grades with JWT based authentication.

## Tech Stack

- FastAPI - High performance Python web framework (ASGI based, faster than Flask)
- SQLModel - Database ORM combining Pydantic and SQLAlchemy
- JWT Authentication - Secure token based authentication using python-jose
- passlib - Password hashing with bcrypt
- SQLite - Lightweight database for development
- Uvicorn - ASGI server to run the application

## Features

- Admin registration and login with JWT tokens
- Full CRUD for Students, Courses, Enrollments and Grades
- Student enrollment management in courses
- Grade assignment and updates per student per course
- Duplicate checks for emails, course codes and enrollments
- Marks validation between 0 and 100
- All routes are protected and require a valid JWT token
- Auto generated interactive API documentation at /docs

## Live Demo

API is live and accessible at:
https://web-production-617bc.up.railway.app/docs

## Project Structure
student-management/

├── main.py                  # App entry point, routers registered here

├── database.py              # Database connection and session dependency

├── models.py                # SQLModel table definitions

├── schemas.py               # Pydantic request and response schemas

├── auth.py                  # JWT token creation, verification and current user dependency

├── requirements.txt         # All project dependencies

├── Procfile                 # Deployment config for Railway

├── .gitignore               # Files ignored by git

├── README.md                # Project documentation

└── routers/

├── init.py          # Makes routers a Python package

├── admin.py             # Admin register and login routes

├── students.py          # Student CRUD routes

├── courses.py           # Course CRUD routes

├── enrollments.py       # Enrollment management routes

└── grades.py            # Grade assignment and management routes

## Installation and Setup

```bash
# Clone the repository
git clone https://github.com/21f3001527/student-management.git
cd student-management

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

Once the server is running, open http://127.0.0.1:8000/docs in your browser to access the interactive Swagger UI.

## Screenshots

### API Routes
![API Routes](screenshots/swagger_routes.png)

### Admin Authentication
![Authentication](screenshots/swagger_login.png)

### Grades and Enrollments
![Grades and Enrollments](screenshots/swagger_grades.png)
## API Endpoints

### Admin
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /admin/register | Register a new admin account | No |
| POST | /admin/login | Login and receive JWT token | No |

### Students
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /students/ | Add a new student | Yes |
| GET | /students/ | Get all students | Yes |
| GET | /students/{id} | Get a student by ID | Yes |
| PATCH | /students/{id} | Update student details | Yes |
| DELETE | /students/{id} | Delete a student | Yes |

### Courses
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /courses/ | Add a new course | Yes |
| GET | /courses/ | Get all courses | Yes |
| GET | /courses/{id} | Get a course by ID | Yes |
| PATCH | /courses/{id} | Update course details | Yes |
| DELETE | /courses/{id} | Delete a course | Yes |

### Enrollments
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /enrollments/ | Enroll a student in a course | Yes |
| GET | /enrollments/ | Get all enrollments | Yes |
| GET | /enrollments/student/{id} | Get all enrollments of a student | Yes |
| DELETE | /enrollments/{id} | Remove an enrollment | Yes |

### Grades
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /grades/ | Assign a grade to a student | Yes |
| GET | /grades/ | Get all grades | Yes |
| GET | /grades/student/{id} | Get all grades of a student | Yes |
| PATCH | /grades/{id} | Update a grade | Yes |
| DELETE | /grades/{id} | Delete a grade | Yes |

## How Authentication Works

1. Register an admin account using POST /admin/register
2. Login using POST /admin/login and copy the access token from the response
3. Open Swagger UI at /docs and click the Authorize button at the top right
4. Paste the token and click Authorize
5. All protected routes are now accessible from the Swagger UI

## Why FastAPI over Flask

- FastAPI is ASGI based which means it handles async requests natively, making it significantly faster than Flask which is WSGI based
- Swagger UI is auto generated from type hints, no extra configuration needed
- Pydantic validation is built in, no need to manually validate request data
- Type hints make the code cleaner and easier to maintain
- Automatic 422 error responses for invalid input data


## Contact

Rajeev Kumar
- LinkedIn: https://www.linkedin.com/in/rajeev245/
- GitHub: https://github.com/21f3001527
- Email: rajeev90767@gmail.com