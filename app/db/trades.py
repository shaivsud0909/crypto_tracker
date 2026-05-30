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


def update_trade_status(
    trade_id,
    status,
    hit,
    exit_price,
    exit_time,
    pnl
):

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        UPDATE trades

        SET

            status = ?,

            hit = ?,

            exit_price = ?,

            exit_time = ?,

            pnl = ?

        WHERE id = ?

        """, (

            status,
            hit,
            exit_price,
            exit_time,
            pnl,
            trade_id

        ))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return {

            "success": True,

            "rows_updated": rows_updated

        }

    except Exception as e:

        return {

            "success": False,

            "message": str(e)

        }