# def monitor_open_trades():

#     try:
#         open_trades = get_open_trades()

#         if not open_trades:

#             print("No Open Trades")

#             return {
#                 "success": True,
#                 "message": "No Open Trades"
#             }
        
#         for trade in open_trades:

#             try:
#                 symbol=trade['symbol']

#                 latest_df = get_latest_crypto_data(symbol)

#                 if latest_df is None:

#                     print(
#                         f"Data Fetch Failed : {symbol}"
#                     )

#                     continue

#                 future_candles = latest_df[
#                     latest_df['utc_time'] > trade['entry_time']
#                 ]



