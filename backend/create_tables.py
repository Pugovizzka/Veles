"""
Скрипт для создания таблиц и начальных данных
"""
from sqlalchemy import create_engine
from models import Base, User, Employee, UserRole
from database import SessionLocal
from passlib.context import CryptContext
import os

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_tables():
    """Создание всех таблиц"""
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")
    engine = create_engine(DATABASE_URL)
    
    print("Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы успешно!")

def create_initial_data():
    """Создание начальных данных"""
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже пользователи
        existing_user = db.query(User).first()
        if existing_user:
            print("Пользователи уже существуют, пропускаем создание начальных данных")
            return
        
        # Создаем администратора
        admin_user = User(
            email="admin@company.com",
            name="Администратор",
            role=UserRole.ADMIN,
            department="IT",
            password_hash=hash_password("admin123")
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        # Создаем запись сотрудника для администратора
        admin_employee = Employee(
            user_id=admin_user.id,
            name="Администратор",
            department="IT"
        )
        db.add(admin_employee)
        
        # Создаем тестового менеджера
        manager_user = User(
            email="manager@company.com",
            name="Менеджер Тестов",
            role=UserRole.MANAGER,
            department="Управление",
            password_hash=hash_password("manager123")
        )
        db.add(manager_user)
        db.commit()
        db.refresh(manager_user)
        
        manager_employee = Employee(
            user_id=manager_user.id,
            name="Менеджер Тестов",
            department="Управление"
        )
        db.add(manager_employee)
        
        # Создаем тестового сотрудника
        employee_user = User(
            email="employee@company.com",
            name="Сотрудник Тестов",
            role=UserRole.EMPLOYEE,
            department="Разработка",
            password_hash=hash_password("employee123")
        )
        db.add(employee_user)
        db.commit()
        db.refresh(employee_user)
        
        employee_employee = Employee(
            user_id=employee_user.id,
            name="Сотрудник Тестов",
            department="Разработка"
        )
        db.add(employee_employee)
        
        db.commit()
        
        print("Начальные данные созданы успешно!")
        print("\nТестовые учетные записи:")
        print("Администратор: admin@company.com / admin123")
        print("Менеджер: manager@company.com / manager123")
        print("Сотрудник: employee@company.com / employee123")
        
    except Exception as e:
        print(f"Ошибка при создании начальных данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    create_initial_data()