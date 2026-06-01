from app.crypto.ema import calculate_ema
from app.crypto.fetch_data import get_latest_crypto_data
from app.crypto.genrate_signal import generate_signal

def pipeline_fun(symbol):
        
    try:    

        df = get_latest_crypto_data(symbol)

        df = calculate_ema(df)

        print(df)

        previous = df.iloc[-2]
        current = df.iloc[-1]

        avg_vol = df['volume'].tail(20).mean()

        good_volume = current['volume'] > avg_vol

        signal = None

        entry = current['close']

        trade_setup = generate_signal(previous,current,good_volume)

        print(trade_setup)

        if trade_setup is None:
            return None
        
        signal = trade_setup["signal"]

        sl = trade_setup["sl"]

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