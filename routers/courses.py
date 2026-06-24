from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Course, Admin
from schemas import CourseCreate, CourseUpdate, CourseResponse
from auth import get_current_admin

router = APIRouter(prefix="/courses", tags=["Courses"])

# ── Create Course ─────────────────────────
@router.post("/", response_model=CourseResponse)
def create_course(
    course: CourseCreate,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    # Course code already exist karta hai?
    existing = session.exec(
        select(Course).where(Course.code == course.code)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course code already exists")

    new_course = Course(**course.dict())
    session.add(new_course)
    session.commit()
    session.refresh(new_course)
    return new_course

# ── Get All Courses ───────────────────────
@router.get("/", response_model=list[CourseResponse])
def get_courses(
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    courses = session.exec(select(Course)).all()
    return courses

# ── Get One Course ────────────────────────
@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# ── Update Course ─────────────────────────
@router.patch("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    updated: CourseUpdate,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    data = updated.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(course, key, value)

    session.commit()
    session.refresh(course)
    return course

# ── Delete Course ─────────────────────────
@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    session: Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    session.delete(course)
    session.commit()
    return {"message": f"Course {course_id} deleted"}