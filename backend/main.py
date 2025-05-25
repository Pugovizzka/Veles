from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional
import psutil
import win32gui
import win32process
import win32con

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
async def get_current_activity():
    activity = get_active_window_info()
    return activity

@app.post("/stop")
async def stop_day(request: Request):
    data = await request.json()

    try:
        start_time = datetime.fromisoformat(data["start_time"])
        end_time = datetime.fromisoformat(data["end_time"])
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