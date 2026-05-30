from fastapi import FastAPI
from app.routers.bot_api import bot_router
from app.services.sheduler import scheduler

app = FastAPI()

@app.on_event("startup")

def startup():
    scheduler.start()

app.include_router(bot_router,tags=["bot"])