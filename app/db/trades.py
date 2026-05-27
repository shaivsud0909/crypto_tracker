from app.db.db import get_connection

#crete table
def create_trades_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS trades (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,

        signal TEXT,

        entry REAL,

        sl REAL,

        target REAL,

        status TEXT,

        volume REAL,

        entry_time TEXT,

        indian_time TEXT,

        exit_price REAL,

        exit_time TEXT,

        pnl REAL,
                   
        hit TEXT

    )

    """)

    conn.commit()

    conn.close()

    return "Trades Table Created"



def get_open_trades():

    try:

        conn = get_connection()

        cursor = conn.cursor()

        # =========================
        # FETCH OPEN TRADES
        # =========================

        cursor.execute("""

        SELECT *

        FROM trades

        WHERE status = 'OPEN'

        """)

        trades = cursor.fetchall()

        conn.close()

        return trades

    except Exception as e:

        print(f"Get Open Trades Error: {e}")

        return []
