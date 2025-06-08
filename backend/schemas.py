from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional


class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


# Модель для создания пользователя (ввод от клиента)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    department: str
    role: UserRole


# Модель для чтения (выдачи) пользователя (ответ клиенту)
class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
