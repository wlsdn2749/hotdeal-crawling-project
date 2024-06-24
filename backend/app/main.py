from typing import Union
from fastapi import FastAPI

from app.router.hotdeal import hotdeal
from fastapi.middleware.cors import CORSMiddleware

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.database import db
import asyncio

app = FastAPI()

# 주기적으로 실행할 함수
async def periodic_task():
    db.update()

# 스케줄러 설정
scheduler = AsyncIOScheduler()
scheduler.add_job(periodic_task, IntervalTrigger(minutes=20))  # n은 원하는 분 간격

@app.on_event("startup")
async def startup_event():
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(hotdeal)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}