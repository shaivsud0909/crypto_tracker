from app.db.db import get_connection


def save_trade(trade):

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO trades (

            symbol,
            signal,
            entry,
            sl,
            target,
            status,
            hit,
            volume,
            entry_time,
            indian_time

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            trade['symbol'],
            trade['signal'],
            trade['entry'],
            trade['sl'],
            trade['target'],
            "OPEN",
            None,
            trade['volume'],
            trade['utc_time'],
            trade['indian_time']

        ))

        conn.commit()

        conn.close()

        return {

            "success": True,

            "message": "Trade Saved"

        }

    except Exception as e:

        return {

            "success": False,

            "message": str(e)

        }