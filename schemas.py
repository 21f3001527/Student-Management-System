from sqlmodel import SQLModel
from typing import Optional

# ── Admin Schemas ─────────────────────────
class AdminRegister(SQLModel):
    username: str
    password: str

class AdminLogin(SQLModel):
    username: str
    password: str

# ── Student Schemas ───────────────────────
class StudentCreate(SQLModel):
    name: str
    email: str
    phone: str
    cgpa: float = 0.0

class StudentUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    cgpa: Optional[float] = None

class StudentResponse(SQLModel):
    id: int
    name: str
    email: str
    phone: str
    cgpa: float

# ── Course Schemas ────────────────────────
class CourseCreate(SQLModel):
    name: str
    code: str
    credits: int

class CourseUpdate(SQLModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None

class CourseResponse(SQLModel):
    id: int
    name: str
    code: str
    credits: int

# ── Enrollment Schemas ────────────────────
class EnrollmentCreate(SQLModel):
    student_id: int
    course_id: int

class EnrollmentResponse(SQLModel):
    id: int
    student_id: int
    course_id: int

# ── Grade Schemas ─────────────────────────
class GradeCreate(SQLModel):
    student_id: int
    course_id: int
    grade: str
    marks: float

class GradeUpdate(SQLModel):
    grade: Optional[str] = None
    marks: Optional[float] = None

class GradeResponse(SQLModel):
    id: int
    student_id: int
    course_id: int
    grade: str
    marks: float

# ── Token Schema ──────────────────────────
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"