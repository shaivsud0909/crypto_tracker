import json
import os

from app.crypto.ema import calculate_ema
from app.crypto.fetch_data import get_latest_crypto_data
from app.crypto.genrate_signal import generate_signal


def pipeline_last_24_hours(symbol, output_file="signals.json"):
    try:
        df = get_latest_crypto_data(symbol)
        df = calculate_ema(df)

        # 24 candles = last 24 hours (1-hour timeframe)
        candles = 24

        # Need 20 previous candles for average volume
        if len(df) < candles + 20:
            print(f"Not enough candles. Found {len(df)}, need at least {candles + 20}.")
            return None

        signals = []

        start_index = len(df) - candles

        for i in range(start_index, len(df)):

            previous = df.iloc[i - 1]
            current = df.iloc[i]

            # Average volume of previous 20 candles
            avg_vol = df.iloc[i - 20:i]["volume"].mean()

            good_volume = current["volume"] > avg_vol

            trade_setup = generate_signal(previous, current, good_volume)

            if trade_setup is None:
                continue

            signal = trade_setup["signal"]
            entry = current["close"]
            sl = trade_setup["sl"]

            risk = abs(entry - sl)

            if signal == "LONG":
                target = entry + (risk * 2)
            else:
                target = entry - (risk * 2)

            signals.append({
                "symbol": symbol,
                "signal": signal,
                "entry": float(entry),
                "sl": float(sl),
                "target": float(target),
                "volume": float(current["volume"]),
                "utc_time": current["utc_time"],
                "indian_time": current["india_time"]
            })

        # ----------------------------
        # Append to JSON
        # ----------------------------
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = []
        else:
            existing = []

        existing.extend(signals)

        with open(output_file, "w") as f:
            json.dump(existing, f, indent=4)

        print(f"Stored {len(signals)} signals.")
        return signals

    except Exception as e:
        print(e)
        return None