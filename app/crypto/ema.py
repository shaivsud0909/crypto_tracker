def calculate_ema(df):

    try:
        df['ema9'] = (
            df['close']
            .ewm(span=9, adjust=False)
            .mean()
        )

        df['ema21'] = (
            df['close']
            .ewm(span=21, adjust=False)
            .mean()
        )

        return df
    
    except Exception as e:
        return e