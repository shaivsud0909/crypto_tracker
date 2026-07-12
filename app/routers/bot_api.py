from fastapi import APIRouter
from app.services.crypto_services import check_trade_opportunity,trade_executed_result,custom_pipeline,evaluate_pipeline

bot_router=APIRouter()

bot_router.post("/opportunity")(check_trade_opportunity)
bot_router.post("/strategy-accuracy")(trade_executed_result)

bot_router.post("/last-24-hours-pipeline")(custom_pipeline)
bot_router.get("/evaluate")(evaluate_pipeline)

