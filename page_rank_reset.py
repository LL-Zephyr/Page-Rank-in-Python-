import sqlite3

conn = sqlite3.connect("Page_Rank.db")
cur = conn.cursor()

with conn:
	cur.execute("""UPDATE visited_sites SET old_page_rank=NULL, new_page_rank=1.0""")

print("Successful Reset")
