```python
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
import psutil
import subprocess
from database import get_db
from models import ActivityLog, Employee
from sqlalchemy import func

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_active_window_info():
    try:
        # Using xdotool to get window information on Linux
        active_window_id = subprocess.check_output(['xdotool', 'getactivewindow']).decode().strip()
        window_title = subprocess.check_output(['xdotool', 'getwindowname', active_window_id]).decode().strip()
        
        # Get process info using psutil
        pid = int(subprocess.check_output(['xdotool', 'getwindowpid', active_window_id]).decode().strip())
        process = psutil.Process(pid)
        app_name = process.name()
        
        return {
            "app": app_name,
            "title": window_title,
            "pid": pid
        }
    except Exception as e:
        return {
            "app": "Unknown",
            "title": "Unknown",
            "pid": None,
            "error": str(e)
        }

@app.get("/current-activity")
async def get_current_activity(db: Session = Depends(get_db)):
    activity = get_active_window_info()
    
    if activity["app"] != "Unknown":
        log = ActivityLog(
            employee_id=1,  # Временно хардкодим ID сотрудника
            window_title=activity["title"],
            app_name=activity["app"],
            start_time=datetime.utcnow()
        )
        db.add(log)
        db.commit()
    
    return activity

@app.post("/stop")
async def stop_day(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    try:
        start_time = datetime.fromisoformat(data["start_time"])
        end_time = datetime.fromisoformat(data["end_time"])
        
        # Закрываем последнюю активность
        last_activity = db.query(ActivityLog)\
            .filter(ActivityLog.employee_id == 1)\
            .filter(ActivityLog.end_time.is_(None))\
            .first()
            
        if last_activity:
            last_activity.end_time = end_time
            db.commit()
            
    except Exception as e:
        return {"error": f"Неверный формат времени: {e}"}

    duration = (end_time - start_time).total_seconds()
    return {
        "message": "Рабочий день завершен",
        "start": start_time.isoformat(),
        "end": end_time.isoformat(),
        "duration_seconds": duration,
        "duration_human": f"{int(duration // 3600)} ч {int((duration % 3600) // 60)} мин"
    }

@app.get("/report")
async def generate_report(
    start_date: str,
    end_date: str,
    department: Optional[str] = None,
    employee_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    
    # Базовый запрос
    query = db.query(
        ActivityLog,
        Employee
    ).join(
        Employee,
        ActivityLog.employee_id == Employee.id
    ).filter(
        ActivityLog.start_time >= start,
        ActivityLog.start_time <= end
    )
    
    # Применяем фильтры
    if department:
        query = query.filter(Employee.department == department)
    if employee_id:
        query = query.filter(Employee.id == employee_id)
    
    activities = query.all()
    
    # Обработка результатов
    report_data = {}
    for activity, employee in activities:
        if employee.id not in report_data:
            report_data[employee.id] = {
                "employeeId": employee.id,
                "employeeName": employee.name,
                "department": employee.department,
                "totalTime": 0,
                "activeTime": 0,
                "apps": {}
            }
        
        # Расчет времени
        duration = (activity.end_time - activity.start_time).total_seconds() / 60
        report_data[employee.id]["totalTime"] += duration
        
        # Учет времени по приложениям
        if activity.app_name not in report_data[employee.id]["apps"]:
            report_data[employee.id]["apps"][activity.app_name] = 0
        report_data[employee.id]["apps"][activity.app_name] += duration
    
    # Формируем итоговый отчет
    items = list(report_data.values())
    total_time = sum(item["totalTime"] for item in items)
    
    return {
        "items": items,
        "totalDepartmentTime": total_time,
        "averageEmployeeTime": total_time / len(items) if items else 0
    }

@app.get("/employees")
async def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return [{"id": emp.id, "name": emp.name, "department": emp.department} for emp in employees]
```