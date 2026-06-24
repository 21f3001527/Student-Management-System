from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# Admin table
class Admin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str

# Student table
class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
    cgpa: float = 0.0

    # Relationships
    enrollments: List["Enrollment"] = Relationship(back_populates="student")
    grades: List["Grade"] = Relationship(back_populates="student")

# Course table
class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    code: str  # jaise "CS101"
    credits: int

    # Relationships
    enrollments: List["Enrollment"] = Relationship(back_populates="course")
    grades: List["Grade"] = Relationship(back_populates="course")

# Enrollment table
class Enrollment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    course_id: int = Field(foreign_key="course.id")

    # Relationships
    student: Optional[Student] = Relationship(back_populates="enrollments")
    course: Optional[Course] = Relationship(back_populates="enrollments")  # ← yahan fix karo

# Grade table
class Grade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    course_id: int = Field(foreign_key="course.id")
    grade: str  # A, B, C, D, F
    marks: float  # 0-100

    # Relationships
    student: Optional[Student] = Relationship(back_populates="grades")
    course: Optional[Course] = Relationship(back_populates="grades")