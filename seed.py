from app.database import SessionLocal, engine, Base
from app.models.models import User, Course, CourseElement, CourseConnection
from app.auth import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Создаём тестовых пользователей
tutor = db.query(User).filter(User.email == "tutor@nexus.ru").first()
if not tutor:
    tutor = User(email="tutor@nexus.ru", hashed_password=hash_password("Test1234"), is_tutor=True)
    db.add(tutor)
    db.commit()
    db.refresh(tutor)

student = db.query(User).filter(User.email == "student@nexus.ru").first()
if not student:
    student = User(email="student@nexus.ru", hashed_password=hash_password("Test1234"), is_tutor=False)
    db.add(student)
    db.commit()
    db.refresh(student)

# Курс 1
course1 = Course(title="Основы Python", description="Введение в программирование на Python", is_public=True, tutor_id=tutor.id)
db.add(course1)
db.commit()
db.refresh(course1)

el1 = CourseElement(course_id=course1.id, title="Переменные и типы данных", x=100, y=100, width=240, height=140, background_color="#e3f2fd", border_color="#1e88e5", order_index=0)
el2 = CourseElement(course_id=course1.id, title="Условные операторы", x=400, y=100, width=240, height=140, background_color="#fff3e0", border_color="#fb8c00", order_index=1)
el3 = CourseElement(course_id=course1.id, title="Циклы for и while", x=700, y=100, width=240, height=140, background_color="#e8f5e9", border_color="#43a047", order_index=2)
db.add_all([el1, el2, el3])
db.commit()

conn1 = CourseConnection(course_id=course1.id, from_element_id=el1.id, to_element_id=el2.id)
conn2 = CourseConnection(course_id=course1.id, from_element_id=el2.id, to_element_id=el3.id)
db.add_all([conn1, conn2])
db.commit()

# Курс 2
course2 = Course(title="Веб-разработка", description="HTML, CSS, JavaScript", is_public=False, tutor_id=tutor.id)
db.add(course2)
db.commit()
db.refresh(course2)

el4 = CourseElement(course_id=course2.id, title="HTML основы", x=100, y=100, width=240, height=140, background_color="#fff8e1", border_color="#f9a825", order_index=0)
el5 = CourseElement(course_id=course2.id, title="CSS стилизация", x=400, y=100, width=240, height=140, background_color="#e8eaf6", border_color="#3949ab", order_index=1)
db.add_all([el4, el5])
db.commit()

conn3 = CourseConnection(course_id=course2.id, from_element_id=el4.id, to_element_id=el5.id)
db.add(conn3)
db.commit()

print("=" * 55)
print("  БАЗА ЗАПОЛНЕНА ТЕСТОВЫМИ ДАННЫМИ")
print("=" * 55)
print("  Тьютор:   tutor@nexus.ru / Test1234")
print("  Студент:  student@nexus.ru / Test1234")
print(f"  Курс 1:   «Основы Python» (id={course1.id}, публичный)")
print(f"  Курс 2:   «Веб-разработка» (id={course2.id}, приватный)")
print("=" * 55)

db.close()