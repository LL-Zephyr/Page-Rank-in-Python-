import sqlite3
from bs4 import BeautifulSoup
import urllib.request as ur, urllib.parse as up, urllib.error as ue
import sys

#BeautifulSoup to get all hrefs
def get_outbound_links(url):
	with ur.urlopen(url) as response:
		response_text = response.read()
		soup = BeautifulSoup(response_text, "lxml")
		ls_links = []
		try:
			for anchor in soup.find_all("a"):
				link = anchor["href"]
				if link.endswith(".png") or link.endswith(".jpg") or link.endswith(".gif"):
					continue
				if link.startswith("https") or link.startswith("http"):
					if link not in ls_links:
						ls_links.append(link)
		except(AttributeError, KeyError) as err:
			pass

	return ls_links

#Database connection
conn = sqlite3.connect("Page_Rank.db")
cur = conn.cursor()

#Database functions
def get_new_page_rank(url):
	cur.execute("""SELECT new_page_rank FROM visited_sites WHERE urls=?""", (url,))
	new_rank = cur.fetchone()[0]
	return new_rank

def url_previous_rank(url):
	cur.execute("""SELECT old_page_rank FROM visited_sites WHERE urls=?""", (url,))
	old_page_rank = cur.fetchone()[0]
	return old_page_rank

def count_outbound_links(url):
	ls_outbound_links = get_outbound_links(url)
	return len(ls_outbound_links)

def get_all_urls():
	cur.execute("""SELECT urls FROM visited_sites""")
	all_urls = cur.fetchall()
	return all_urls

def get_all_previous_ranks():
	cur.execute("""SELECT new_page_rank FROM visited_sites""")
	ls_previous_rank = cur.fetchall()
	return ls_previous_rank

def update_new_to_old(url, new_rank):
	with conn:
		cur.execute("""UPDATE visited_sites SET old_page_rank=?, new_page_rank=? WHERE urls=?""", (new_rank, None, url))
	
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

	new_page_rank = sum(ls_result)
	return new_page_rank

def update_new_page_rank(url, new_rank):
	cur.execute("""SELECT id FROM visited_sites WHERE urls=?""", (url,))
	url_id = cur.fetchone()[0]
	with conn:
		cur.execute("""UPDATE visited_sites SET new_page_rank=? WHERE id=? AND urls=?""", (new_rank, url_id, url))


#Main
print("Updating database...\n")

all_urls = get_all_urls()

for link in all_urls:
	mod_link = link[0]
	new_rank = get_new_page_rank(mod_link)
	update_new_to_old(mod_link, new_rank)

for url in all_urls:
	mod_url = url[0]
	new_rank = new_page_rank(mod_url)
	update_new_page_rank(mod_url, new_rank)

print("New page ranks were updated")









