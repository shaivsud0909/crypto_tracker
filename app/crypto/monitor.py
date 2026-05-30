from app.crypto.fetch_data import get_latest_crypto_data
from app.db.trades import update_trade_status


def monitor_open_trades(open_trades):

    results = []

    for trade in open_trades:

        try:

            latest_df = get_latest_crypto_data(
                trade["symbol"]
            )

            if latest_df is None:
                continue

            # Only candles after entry candle
            future_candles = latest_df[
                latest_df["utc_time"] >
                trade["entry_time"]
            ]

            if future_candles.empty:

                results.append({

                    "trade_id": trade["id"],

                    "status": "OPEN",

                    "message": "No candle formed yet"

                })

                continue

            for _, candle in future_candles.iterrows():

                high = candle["high"]

                low = candle["low"]

                exit_time = candle["utc_time"]

                # =====================
                # LONG
                # =====================

                if trade["signal"] == "LONG":

                    if low <= trade["sl"]:

                        pnl = (
                            trade["sl"]
                            - trade["entry"]
                        )

                        update_trade_status(

                            trade["id"],

                            "CLOSED",

                            "SL",

                            trade["sl"],

                            exit_time,

                            pnl

                        )

                        results.append({

                            "trade_id": trade["id"],

                            "status": "CLOSED",

                            "hit": "SL"

                        })

                        break

                    elif high >= trade["target"]:

                        pnl = (

                            trade["target"]
                            - trade["entry"]

                        )

                        update_trade_status(

                            trade["id"],

                            "CLOSED",

                            "TP",

                            trade["target"],

                            exit_time,

                            pnl

                        )

                        results.append({

                            "trade_id": trade["id"],

                            "status": "CLOSED",

                            "hit": "TP"

                        })

                        break

                # =====================
                # SHORT
                # =====================

                elif trade["signal"] == "SHORT":

                    if high >= trade["sl"]:

                        pnl = (
                            trade["entry"]
                            - trade["sl"]
                        )

                        update_trade_status(

                            trade["id"],

                            "CLOSED",

                            "SL",

                            trade["sl"],

                            exit_time,

                            pnl

                        )

                        results.append({

                            "trade_id": trade["id"],

                            "status": "CLOSED",

                            "hit": "SL"

                        })

                        break

                    elif low <= trade["target"]:

                        pnl = (
                            trade["entry"]
                            - trade["target"]
                        )

                        update_trade_status(

                            trade["id"],

                            "CLOSED",

                            "TP",

                            trade["target"],

                            exit_time,

                            pnl

                        )

                        results.append({

                            "trade_id": trade["id"],

                            "status": "CLOSED",

                            "hit": "TP"

                        })

                        break

            else:

                results.append({

                    "trade_id": trade["id"],

                    "status": "OPEN",

                    "message": "Target not hit yet"

                })

        except Exception as e:

            results.append({

                "trade_id": trade["id"],

                "status": "ERROR",

                "message": str(e)

            })

    return results