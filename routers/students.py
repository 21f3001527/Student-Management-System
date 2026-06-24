from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Student, Admin
from schemas import StudentCreate, StudentUpdate, StudentResponse
from auth import get_current_admin

router = APIRouter(prefix="/students", tags=["Students"])

# ── Create Student ────────────────────────
@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    # Email already exist karta hai?
    existing = session.exec(
        select(Student).where(Student.email == student.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_student = Student(**student.dict())
    session.add(new_student)
    session.commit()
    session.refresh(new_student)
    return new_student

# ── Get All Students ──────────────────────
@router.get("/", response_model=list[StudentResponse])
def get_students(
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    students = session.exec(select(Student)).all()
    return students

# ── Get One Student ───────────────────────
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# ── Update Student ────────────────────────
@router.patch("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    updated: StudentUpdate,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Sirf jo fields bheje gaye woh update karo
    data = updated.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(student, key, value)

    session.commit()
    session.refresh(student)
    return student

# ── Delete Student ────────────────────────
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    session.delete(student)
    session.commit()
    return {"message": f"Student {student_id} deleted"}