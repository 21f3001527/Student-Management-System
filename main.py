from fastapi import FastAPI
from database import create_tables
from routers import admin, students, courses, enrollments, grades

app = FastAPI(
    title="Student Management System",
    description="FastAPI + SQLModel + JWT Auth",
    version="1.0.0"
)

# Tables create karo on startup
@app.on_event("startup")
def on_startup():
    create_tables()

# Saare routers include karo
app.include_router(admin.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(grades.router)

# Health check
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "running", "app": "Student Management System"}