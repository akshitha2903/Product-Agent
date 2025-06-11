import sqlite3

conn = sqlite3.connect("memory.db")
conn.execute("DELETE FROM runs WHERE id IN (1,6)")
conn.commit()
conn.close()

print("Deleted successfully!")
