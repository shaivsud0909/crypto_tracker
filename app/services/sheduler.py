from apscheduler.schedulers.background import BackgroundScheduler

from app.services.crypto_services import (
    check_trade_opportunity,
    trade_executed_result,
    custom_pipeline,
    evaluate_pipeline
)

from app.schema import TradeRequest

scheduler = BackgroundScheduler()


def run_opportunity():
    symbols = [
        "BTC/USDT",
        "ETH/USDT",
        "SOL/USDT"
    ]

    for symbol in symbols:
        request = TradeRequest(symbol=symbol)
        check_trade_opportunity(request)


def run_custom_pipeline():
    symbols = [
        "BTC/USDT",
        "ETH/USDT",
        "SOL/USDT"
    ]

    for symbol in symbols:
        request = TradeRequest(symbol=symbol)
        custom_pipeline(request)


def run_evaluation():
    evaluate_pipeline()


# ----------------------------
# Daily trade result tracking
# ----------------------------
scheduler.add_job(
    trade_executed_result,
    trigger="cron",
    hour=0,
    minute=5,
    id="trade_tracker"
)

# ----------------------------
# Scan every hour
# ----------------------------
scheduler.add_job(
    run_opportunity,
    trigger="cron",
    minute=1,
    id="opportunity_scanner"
)

# ----------------------------
# Run custom pipeline every hour
# ----------------------------
scheduler.add_job(
    run_custom_pipeline,
    trigger="cron",
    minute=10,
    id="custom_pipeline_scanner"
)

# ----------------------------
# Evaluate completed trades daily
# ----------------------------
scheduler.add_job(
    run_evaluation,
    trigger="cron",
    hour=0,
    minute=15,
    id="trade_evaluator"
)