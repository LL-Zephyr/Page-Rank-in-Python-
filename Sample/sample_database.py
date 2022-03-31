import sqlite3

conn = sqlite3.connect("sample.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS visited_sites(id INTEGER PRIMARY KEY AUTOINCREMENT, 
	urls TEXT UNIQUE, visited_check INTEGER, old_page_rank REAL, new_page_rank REAL)""")

cur.execute("""CREATE TABLE IF NOT EXISTS outbound_links(url_id INTEGER, outbound INTEGER)""")


#Database functions
def insert_url(main_url):
	with conn:
		cur.execute("""INSERT INTO visited_sites(urls, visited_check,
			old_page_rank, new_page_rank) VALUES(?,?,?,?)""",
			(main_url, 1, None, 1))
	return main_url

def insert_outbound(url_id, outbound):
	with conn:
		cur.execute("""INSERT INTO outbound_links(url_id, outbound) VALUES(?,?)""", (url_id, outbound))


insert_url("http://page1.com")
insert_url("http://page2.com")
insert_url("http://page3.com")
insert_url("http://page4.com")

insert_outbound(1,2)
insert_outbound(1,3)
insert_outbound(2,4)
insert_outbound(3,1)
insert_outbound(3,2)
insert_outbound(3,4)
insert_outbound(4,3)

print("Database Created")



