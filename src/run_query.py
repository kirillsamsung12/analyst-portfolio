import sqlite3
import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


def run_query(query_or_file):
    db_path = os.path.join("data", "fintech_sandbox.db")
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    sql = query_or_file
    if os.path.exists(query_or_file):
        with open(query_or_file, "r", encoding="utf-8") as f:
            sql = f.read()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
        
        if cols:
            # Format as simple table
            col_widths = [max(len(str(c)), max((len(str(r[i])) for r in rows), default=0)) for i, c in enumerate(cols)]
            header = " | ".join(f"{c:<{col_widths[i]}}" for i, c in enumerate(cols))
            sep = "-+-".join("-" * col_widths[i] for i in range(len(cols)))
            print(header)
            print(sep)
            for r in rows[:50]:
                print(" | ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(r)))
            if len(rows) > 50:
                print(f"... and {len(rows) - 50} more rows (total: {len(rows)})")
            else:
                print(f"\nTotal rows: {len(rows)}")
        else:
            print("Query executed successfully (no returning rows).")
    except Exception as e:
        print(f"SQL Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_query(sys.argv[1])
    else:
        print("Usage: python src/run_query.py <sql_query_or_file_path>")
