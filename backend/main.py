from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional

app = FastAPI()

# Разрешим CORS для всех источников (для разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно ограничить конкретными доменами в продакшене
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
