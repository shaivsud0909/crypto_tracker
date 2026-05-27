import pandas as pd

from app.crypto import verify_trade
from app.crypto.ema import calculate_ema
from app.crypto.fetch_data import get_latest_crypto_data

def pipeline_fun(symbol):
        
    try:    

        df = get_latest_crypto_data(symbol)

        df = calculate_ema(df)

        previous = df.iloc[-2]
        current = df.iloc[-1]

        avg_vol = df['volume'].tail(20).mean()

        good_volume = current['volume'] > avg_vol

        signal = None

        entry = current['close']

        # =========================
        # LONG
        # =========================

        if ( previous['ema9'] < previous['ema21'] and current['ema9'] > current['ema21'] and good_volume ):

            signal = "LONG"

            sl = current['low']

        # =========================
        # SHORT
        # =========================

        elif ( previous['ema9'] > previous['ema21'] and current['ema9'] < current['ema21'] and good_volume ):

            signal = "SHORT"

            sl = current['high']

        # =========================
        # NO SIGNAL
        # =========================

        if signal is None:
            return None

        # =========================
        # TARGET
        # =========================

        risk = abs(entry - sl)

        if signal == "LONG":
            target = entry + (risk * 2)

        elif signal == "SHORT":
            target = entry - (risk * 2)

        return {
            "signal": signal,
            "entry": entry,
            "sl": sl,
            "target": target,
            "volume": current['volume'],
            "utc_time": current['utc_time'],
            "indian_time":current['india_time']
        }
    
    except Exception as e:
        return e