def generate_signal(previous, current, good_volume):

    if (
        previous['ema9'] < previous['ema21']
        and current['ema9'] > current['ema21']
        and good_volume
    ):

        return {
            "signal": "LONG",
            "sl": current['low']
        }

    elif (
        previous['ema9'] > previous['ema21']
        and current['ema9'] < current['ema21']
        and good_volume
    ):

        return {
            "signal": "SHORT",
            "sl": current['high']
        }

    return None