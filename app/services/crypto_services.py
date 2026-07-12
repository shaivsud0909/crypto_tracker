from app.crypto.custom_pipeline.evaluate import evaluate_trades
from app.crypto.custom_pipeline.pipeline_24 import pipeline_last_24_hours
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

def custom_pipeline(request: TradeRequest):

    result=pipeline_last_24_hours(request.symbol)

    return result

def evaluate_pipeline():


    result=evaluate_trades()
    
    if result is None:

        return {
            "message": "No Trade Opportunity"
        }
    
    return {

        "message": "Trade Generated",

        "trade": result
    }







    






