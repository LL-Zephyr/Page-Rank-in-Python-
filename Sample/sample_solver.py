import sqlite3

conn = sqlite3.connect("sample.db")
cur = conn.cursor()

#Database functions
def get_new_page_rank(url):
	cur.execute("""SELECT new_page_rank FROM visited_sites WHERE urls=?""", (url,))
	new_rank = cur.fetchone()[0]
	return new_rank

def new_to_old(url, new_rank):
	with conn:
		cur.execute("""UPDATE visited_sites SET old_page_rank=?, new_page_rank=? WHERE urls=?""", (new_rank, None, url))
	
def get_outbound(url_id):
	cur.execute("""SELECT outbound FROM outbound_links WHERE url_id=?""", (url_id,))
	ls_outbound = cur.fetchall()
	return ls_outbound

def url_previous_rank(url):
	cur.execute("""SELECT old_page_rank FROM visited_sites WHERE urls=?""", (url,))
	old_page_rank = cur.fetchone()[0]
	return old_page_rank

def count_outbound_links(url):
	cur.execute("""SELECT id FROM visited_sites WHERE urls=?""",(url,))
	url_id = cur.fetchone()[0]
	cur.execute("""SELECT COUNT(*) FROM outbound_links WHERE url_id=?""", (url_id,))
	count = cur.fetchone()[0]
	return count

def get_all_urls():
	cur.execute("""SELECT urls FROM visited_sites""")
	all_urls = cur.fetchall()
	return all_urls

def new_page_rank(url):
	cur.execute("""SELECT id FROM visited_sites WHERE urls=?""", (url,))
	url_id = cur.fetchone()[0]
	cur.execute("""SELECT url_id FROM outbound_links WHERE outbound=?""", (url_id,))
	ls_inbound_links = cur.fetchall()

	ls_result = []
	for link in ls_inbound_links:
		mod_link = link[0]
		cur.execute("""SELECT urls FROM visited_sites WHERE id=?""", (mod_link,))
		inbound_url = cur.fetchone()[0]
		previous_rank = url_previous_rank(inbound_url)
		outbound_of_inbound = count_outbound_links(inbound_url)
		page_rank_inbound = previous_rank/outbound_of_inbound
		ls_result.append(page_rank_inbound)
	new_rank = sum(ls_result)
	return new_rank


def update_new_rank(url, new_rank):
	with conn:
		cur.execute("""UPDATE visited_sites SET new_page_rank=? WHERE urls=?""", (new_rank, url))


all_urls = get_all_urls()

print("Updating Database...\n")
for link in all_urls:
	mod_link = link[0]
	new_rank = get_new_page_rank(mod_link)
	new_to_old(mod_link, new_rank)

for url in all_urls:
	mod_url = url[0]
	n_rank = get_new_page_rank(mod_url)
	new_rank = new_page_rank(mod_url)
	update_new_rank(mod_url, new_rank)

print("Successful Update")



