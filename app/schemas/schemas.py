from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# --- Авторизация ---

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


# --- Курсы ---

class CourseCreate(BaseModel):
    title: str
    description: str = ""


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None


class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    is_public: bool
    tutor_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Элементы доски ---

class ElementCreate(BaseModel):
    title: str
    content_url: str = ""
    file_url: str = ""
    tutor_comment: str = ""
    x: float = 0
    y: float = 0
    width: float = 200
    height: float = 120
    background_color: str = "#ffffff"
    border_color: str = "#333333"
    custom_data: Optional[dict] = None


class ElementUpdate(BaseModel):
    title: Optional[str] = None
    content_url: Optional[str] = None
    file_url: Optional[str] = None
    tutor_comment: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    background_color: Optional[str] = None
    border_color: Optional[str] = None
    custom_data: Optional[dict] = None


class ElementOut(BaseModel):
    id: int
    course_id: int
    title: str
    content_url: str
    file_url: str
    tutor_comment: str
    x: float
    y: float
    width: float
    height: float
    background_color: str
    border_color: str
    custom_data: Optional[dict] = None
    is_hidden: bool
    created_at: datetime

    class Config:
        from_attributes = True


# --- Связи ---

class ConnectionCreate(BaseModel):
    from_element_id: int
    to_element_id: int


class ConnectionOut(BaseModel):
    id: int
    course_id: int
    from_element_id: int
    to_element_id: int

    class Config:
        from_attributes = True


# --- Доска ---

class BoardOut(BaseModel):
    course: CourseOut
    elements: list[ElementOut]
    connections: list[ConnectionOut]


# --- Прогресс ---

class ProgressUpdate(BaseModel):
    element_id: int
    viewed: bool