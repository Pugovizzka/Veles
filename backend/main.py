from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
import psutil
import win32gui
import win32process
import win32con
from database import get_db
from models import ActivityLog, Employee

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
        window = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(window)
        app_name = psutil.Process(pid).name()
        window_title = win32gui.GetWindowText(window)
        
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
    
    # Сохраняем активность в базу данных
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