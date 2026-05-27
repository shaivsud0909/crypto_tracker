from fastapi import APIRouter

bot_router=APIRouter()

bot_router.post("/start")(start_tracking)
bot_router.post("/stop")(stop_tracking)

