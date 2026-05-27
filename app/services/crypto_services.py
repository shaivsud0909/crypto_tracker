from app.schema import TradeRequest
from app.crypto.pipeline import pipeline_fun
from app.db.save import save_trade




def check_trade_opportunity(request: TradeRequest):

    result = pipeline_fun(request.symbol)

    # No Signal
    if result is None:

        return {
            "message": "No Trade Opportunity"
        }
    
    # Trade Generated
    return {

        "message": "Trade Generated",

        "trade": result
    }


def trade_executed_result(request: TradeRequest):

    result = pipeline_fun(request.symbol)

    # No Signal
    if result is None:

        return 
            
    save_trade(result)

    






