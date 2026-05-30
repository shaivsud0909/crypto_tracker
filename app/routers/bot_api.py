from fastapi import APIRouter
from app.services.crypto_services import check_trade_opportunity,trade_executed_result

bot_router=APIRouter()

bot_router.post("/opportunity")(check_trade_opportunity)
bot_router.post("/strategy-accuracy")(trade_executed_result)

