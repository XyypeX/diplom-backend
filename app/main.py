from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.models.models import User, Course, CourseElement, CourseConnection
from app.auth import hash_password
from app.routers import auth_router, courses_router

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# Автоинициализация базы
db = SessionLocal()
if not db.query(User).filter(User.email == "tutor@nexus.ru").first():
    tutor = User(email="tutor@nexus.ru", hashed_password=hash_password("Test1234"), is_tutor=True)
    student = User(email="student@nexus.ru", hashed_password=hash_password("Test1234"), is_tutor=False)
    db.add_all([tutor, student])
    db.commit()
db.close()

app = FastAPI(title="Course Board API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(courses_router.router)


@app.get("/")
def root():
    return {"message": "Course Board API работает"}