import sys
import csv
import sqlite3
from pathlib import Path

DB_PATH = "data/hsi.db"  

def ensure_table_exists(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS hsi_data (
            index_name  TEXT,
            date        TEXT,
            open        REAL,
            high        REAL,
            low         REAL,
            close       REAL,
            adj_close   REAL,
            volume      INTEGER,
            close_usd   REAL
        );
    """)
    conn.commit()

def process_and_insert(csv_file, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    ensure_table_exists(conn)
    cur = conn.cursor()

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row['Index'], row['Date'], float(row['Open']), float(row['High']),
                float(row['Low']), float(row['Close']), float(row['Adj Close']),
                int(row['Volume']), float(row['CloseUSD'])
            )
            for row in reader
        ]

    cur.executemany("""
        INSERT INTO hsi_data (index_name, date, open, high, low, close, adj_close, volume, close_usd)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, rows)

    conn.commit()
    conn.close()
    print(f"Inserted {len(rows)} rows from {csv_file} into {db_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_chunk_sqlite.py <chunk_file>")
        sys.exit(1)
    
    process_and_insert(sys.argv[1])
