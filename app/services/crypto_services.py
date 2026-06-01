from app.schema import TradeRequest
from app.crypto.pipeline import pipeline_fun
from app.db.save import save_trade
from app.db.trades import get_open_trades
from app.crypto.monitor import monitor_open_trades




def check_trade_opportunity(request: TradeRequest):

    result = pipeline_fun(request.symbol)

    if result is None:

        return {
            "message": "No Trade Opportunity"
        }
    

    save_trade(result)

    return {

        "message": "Trade Generated",

        "trade": result
    }


def trade_executed_result():

    open_trades=get_open_trades()

    results=monitor_open_trades(open_trades)

    return results







    






