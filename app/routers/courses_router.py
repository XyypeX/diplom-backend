from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, Course, CourseElement, CourseConnection
from app.schemas.schemas import (
    CourseCreate, CourseOut, BoardOut,
    ElementCreate, ElementUpdate, ElementOut,
    ConnectionCreate, ConnectionOut,
    CourseUpdate, ProgressUpdate,
)
from app.auth import get_current_user

router = APIRouter(prefix="/api/courses", tags=["courses"])


# --- Курсы ---

@router.get("", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()


@router.post("", response_model=CourseOut)
def create_course(data: CourseCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    course = Course(title=data.title, description=data.description, tutor_id=user.id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    return course


@router.patch("/{course_id}", response_model=CourseOut)
def update_course(course_id: int, data: CourseUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    if course.tutor_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")
    if data.title is not None:
        course.title = data.title
    if data.description is not None:
        course.description = data.description
    if data.is_public is not None:
        course.is_public = data.is_public
    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    if course.tutor_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")
    db.delete(course)
    db.commit()
    return {"ok": True}


# --- Доска ---

@router.get("/{course_id}/board", response_model=BoardOut)
def get_board(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")

    elements = db.query(CourseElement).filter(
        CourseElement.course_id == course_id,
        CourseElement.is_hidden == False,
    ).all()

    connections = db.query(CourseConnection).filter(CourseConnection.course_id == course_id).all()

    return BoardOut(
        course=CourseOut.model_validate(course),
        elements=[ElementOut.model_validate(e) for e in elements],
        connections=[ConnectionOut.model_validate(c) for c in connections],
    )


# --- Элементы ---

@router.post("/{course_id}/elements", response_model=ElementOut)
def create_element(course_id: int, data: ElementCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    if course.tutor_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    element = CourseElement(
        course_id=course_id,
        title=data.title,
        content_url=data.content_url,
        file_url=data.file_url,
        tutor_comment=data.tutor_comment,
        x=data.x,
        y=data.y,
        width=data.width,
        height=data.height,
        background_color=data.background_color,
        border_color=data.border_color,
        custom_data=data.custom_data,
    )
    db.add(element)
    db.commit()
    db.refresh(element)
    return element


@router.patch("/{course_id}/elements/{element_id}", response_model=ElementOut)
def update_element(course_id: int, element_id: int, data: ElementUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    element = db.query(CourseElement).filter(CourseElement.id == element_id, CourseElement.course_id == course_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    if element.course.tutor_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    if data.title is not None:
        element.title = data.title
    if data.content_url is not None:
        element.content_url = data.content_url
    if data.file_url is not None:
        element.file_url = data.file_url
    if data.tutor_comment is not None:
        element.tutor_comment = data.tutor_comment
    if data.x is not None:
        element.x = data.x
    if data.y is not None:
        element.y = data.y
    if data.width is not None:
        element.width = data.width
    if data.height is not None:
        element.height = data.height
    if data.background_color is not None:
        element.background_color = data.background_color
    if data.border_color is not None:
        element.border_color = data.border_color
    if data.custom_data is not None:
        element.custom_data = data.custom_data

    db.commit()
    db.refresh(element)
    return element


@router.delete("/{course_id}/elements/{element_id}")
def delete_element(course_id: int, element_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    element = db.query(CourseElement).filter(CourseElement.id == element_id, CourseElement.course_id == course_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    if element.course.tutor_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    element.is_hidden = True
    db.commit()
    return {"ok": True}


# --- Связи ---

@router.post("/{course_id}/connections", response_model=ConnectionOut)
def create_connection(course_id: int, data: ConnectionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    if course.tutor_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    conn = CourseConnection(course_id=course_id, from_element_id=data.from_element_id, to_element_id=data.to_element_id)
    db.add(conn)
    db.commit()
    db.refresh(conn)
    return conn


@router.delete("/{course_id}/connections")
def delete_all_connections(course_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    if course.tutor_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")
    db.query(CourseConnection).filter(CourseConnection.course_id == course_id).delete()
    db.commit()
    return {"ok": True}


@router.delete("/{course_id}/connections/{connection_id}")
def delete_connection(course_id: int, connection_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    conn = db.query(CourseConnection).filter(CourseConnection.id == connection_id, CourseConnection.course_id == course_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Связь не найдена")
    if conn.course.tutor_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    db.delete(conn)
    db.commit()
    return {"ok": True}


# --- Прогресс ---

@router.put("/{course_id}/progress")
def update_progress(course_id: int, data: ProgressUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    element = db.query(CourseElement).filter(CourseElement.id == data.element_id, CourseElement.course_id == course_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    return {"ok": True}