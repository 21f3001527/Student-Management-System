from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Grade, Student, Course, Enrollment, Admin
from schemas import GradeCreate, GradeUpdate, GradeResponse
from auth import get_current_admin

router = APIRouter(prefix="/grades", tags=["Grades"])

# ── Assign Grade ──────────────────────────
@router.post("/", response_model=GradeResponse)
def assign_grade(
    grade: GradeCreate,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    # Student exist karta hai?
    student = session.get(Student, grade.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Course exist karta hai?
    course = session.get(Course, grade.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Student enrolled hai is course mein?
    enrollment = session.exec(
        select(Enrollment).where(
            Enrollment.student_id == grade.student_id,
            Enrollment.course_id == grade.course_id
        )
    ).first()
    if not enrollment:
        raise HTTPException(status_code=400, detail="Student not enrolled in this course")

    # Grade already assigned?
    existing = session.exec(
        select(Grade).where(
            Grade.student_id == grade.student_id,
            Grade.course_id == grade.course_id
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Grade already assigned")

    # Marks valid hai?
    if grade.marks < 0 or grade.marks > 100:
        raise HTTPException(status_code=400, detail="Marks 0-100 ke beech hone chahiye")

    new_grade = Grade(**grade.dict())
    session.add(new_grade)
    session.commit()
    session.refresh(new_grade)
    return new_grade

# ── Get All Grades ────────────────────────
@router.get("/", response_model=list[GradeResponse])
def get_grades(
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    grades = session.exec(select(Grade)).all()
    return grades

# ── Get Student Grades ────────────────────
@router.get("/student/{student_id}", response_model=list[GradeResponse])
def get_student_grades(
    student_id: int,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    grades = session.exec(
        select(Grade).where(Grade.student_id == student_id)
    ).all()
    return grades

# ── Update Grade ──────────────────────────
@router.patch("/{grade_id}", response_model=GradeResponse)
def update_grade(
    grade_id: int,
    updated: GradeUpdate,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    # Marks valid hai?
    if updated.marks and (updated.marks < 0 or updated.marks > 100):
        raise HTTPException(status_code=400, detail="Marks 0-100 ke beech hone chahiye")

    data = updated.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(grade, key, value)

    session.commit()
    session.refresh(grade)
    return grade

# ── Delete Grade ──────────────────────────
@router.delete("/{grade_id}")
def delete_grade(
    grade_id: int,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    session.delete(grade)
    session.commit()
    return {"message": f"Grade {grade_id} deleted"}