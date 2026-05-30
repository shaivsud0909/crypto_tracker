from apscheduler.schedulers.background import BackgroundScheduler

from app.services.crypto_services import (
    check_trade_opportunity,
    trade_executed_result
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

        request = TradeRequest(
            symbol=symbol
        )

        check_trade_opportunity(
            request
        )


# Daily trade result tracking
scheduler.add_job(
    trade_executed_result,
    trigger="cron",
    hour=0,
    minute=5,
    id="trade_tracker"
)

# Every hour after candle close
scheduler.add_job(
    run_opportunity,
    trigger="cron",
    minute=1,
    id="opportunity_scanner"
)