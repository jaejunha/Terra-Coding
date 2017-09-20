import sqlite3

conn = sqlite3.connect("terra.db")

cur = conn.cursor()

cur.execute("select * from test")

rows = cur.fetchall()
for row in rows:
    print(row)

conn.close()
