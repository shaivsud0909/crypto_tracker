import ccxt
import pandas as pd

exchange = ccxt.binance()

def get_latest_crypto_data(symbol):

    try:
        bars = exchange.fetch_ohlcv(
            symbol,
            timeframe='1h',
            limit=100
        )

        df = pd.DataFrame(
            bars,
            columns=[
                'timestamp',
                'open',
                'high',
                'low',
                'close',
                'volume'
            ]
        )

        # UTC Time
        df['utc_time'] = pd.to_datetime(
            df['timestamp'],
            unit='ms',
            utc=True
        )

        # India Time
        df['india_time'] = df['utc_time'].dt.tz_convert(
            'Asia/Kolkata'
        )

        # Format
        df['utc_time'] = df['utc_time'].dt.strftime(
            '%Y-%m-%d %I:%M:%S %p'
        )

        df['india_time'] = df['india_time'].dt.strftime(
            '%Y-%m-%d %I:%M:%S %p'
        )

        return df
    
    except Exception as e:
        return e

