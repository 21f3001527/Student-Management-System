from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Enrollment, Student, Course, Admin
from schemas import EnrollmentCreate, EnrollmentResponse
from auth import get_current_admin

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

# ── Enroll Student ────────────────────────
@router.post("/", response_model=EnrollmentResponse)
def enroll_student(
    enrollment: EnrollmentCreate,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    # Student exist karta hai?
    student = session.get(Student, enrollment.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Course exist karta hai?
    course = session.get(Course, enrollment.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Already enrolled?
    existing = session.exec(
        select(Enrollment).where(
            Enrollment.student_id == enrollment.student_id,
            Enrollment.course_id == enrollment.course_id
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course")

    new_enrollment = Enrollment(**enrollment.dict())
    session.add(new_enrollment)
    session.commit()
    session.refresh(new_enrollment)
    return new_enrollment

# ── Get All Enrollments ───────────────────
@router.get("/", response_model=list[EnrollmentResponse])
def get_enrollments(
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    enrollments = session.exec(select(Enrollment)).all()
    return enrollments

# ── Get Student Enrollments ───────────────
@router.get("/student/{student_id}", response_model=list[EnrollmentResponse])
def get_student_enrollments(
    student_id: int,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    # Student exist karta hai?
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    enrollments = session.exec(
        select(Enrollment).where(Enrollment.student_id == student_id)
    ).all()
    return enrollments

# ── Delete Enrollment ─────────────────────
@router.delete("/{enrollment_id}")
def delete_enrollment(
    enrollment_id: int,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    enrollment = session.get(Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    session.delete(enrollment)
    session.commit()
    return {"message": f"Enrollment {enrollment_id} deleted"}