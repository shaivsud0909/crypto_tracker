from fastapi import FastAPI
from app.routers.bot_api import bot_router

app = FastAPI()

app.include_router()

app.innclude_router(bot_router,tags=["bot"])