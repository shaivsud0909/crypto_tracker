import json
import pandas as pd

from app.crypto.fetch_data import get_latest_crypto_data


def evaluate_trades(json_file="signals.json"):

    with open(json_file, "r") as f:
        trades = json.load(f)

    results = []

    for trade in trades:

        symbol = trade["symbol"]

        df = get_latest_crypto_data(symbol)

        # convert time for comparison
        df["utc_time"] = pd.to_datetime(df["utc_time"])
        signal_time = pd.to_datetime(trade["utc_time"])

        # candles AFTER signal
        future = df[df["utc_time"] > signal_time]

        status = "OPEN"

        for _, candle in future.iterrows():

            high = candle["high"]
            low = candle["low"]

            if trade["signal"] == "LONG":

                if low <= trade["sl"]:
                    status = "LOSS"
                    break

                if high >= trade["target"]:
                    status = "WIN"
                    break

            else:  # SHORT

                if high >= trade["sl"]:
                    status = "LOSS"
                    break

                if low <= trade["target"]:
                    status = "WIN"
                    break

        trade["status"] = status
        results.append(trade)

    with open("trade_results.json", "w") as f:
        json.dump(results, f, indent=4)

    wins = sum(t["status"] == "WIN" for t in results)
    losses = sum(t["status"] == "LOSS" for t in results)
    open_trades = sum(t["status"] == "OPEN" for t in results)

    print(f"Wins   : {wins}")
    print(f"Losses : {losses}")
    print(f"Open   : {open_trades}")

    return {
        "summary": {
            "wins": wins,
            "losses": losses,
            "open": open_trades,
            "total": len(results)
        },
        "trades": results
    }