from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_tutor = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    courses = relationship("Course", back_populates="tutor")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    is_public = Column(Boolean, default=True)
    tutor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tutor = relationship("User", back_populates="courses")
    elements = relationship("CourseElement", back_populates="course", cascade="all, delete-orphan")
    connections = relationship("CourseConnection", back_populates="course", cascade="all, delete-orphan")


class CourseElement(Base):
    __tablename__ = "course_elements"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    content_url = Column(String, default="")
    file_url = Column(String, default="")
    tutor_comment = Column(String, default="")
    background_color = Column(String, default="#ffffff")
    border_color = Column(String, default="#333333")
    x = Column(Float, default=0)
    y = Column(Float, default=0)
    width = Column(Float, default=200)
    height = Column(Float, default=120)
    is_hidden = Column(Boolean, default=False)
    custom_data = Column(JSON, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course = relationship("Course", back_populates="elements")


class CourseConnection(Base):
    __tablename__ = "course_connections"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    from_element_id = Column(Integer, ForeignKey("course_elements.id"), nullable=False)
    to_element_id = Column(Integer, ForeignKey("course_elements.id"), nullable=False)

    course = relationship("Course", back_populates="connections")