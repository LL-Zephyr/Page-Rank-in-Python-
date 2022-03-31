import sqlite3
from bs4 import BeautifulSoup
import urllib.request as ur, urllib.parse as up, urllib.error as ue
import requests
import sys

#Urllib
def get_outbound_links1(url):
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

#Requests
def get_outbound_links2(url):
	source = requests.get(url, verify=False).text
	soup = BeautifulSoup(source, "lxml")
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

#Connecting database
conn = sqlite3.connect("Page_Rank.db")
cur = conn.cursor()

#Database functions
def new_main_insert(main_url):
	with conn:
		cur.execute("""INSERT INTO visited_sites(urls, visited_check,
			old_page_rank, new_page_rank) VALUES(?,?,?,?)""",
			(main_url, 1, None, 1))
	return main_url

def get_random_main(): 
	cur.execute("""SELECT urls FROM visited_sites WHERE visited_check=0 ORDER BY RANDOM()
		LIMIT 1""")
	main_url = cur.fetchone()[0]
	return main_url

def update_random_main(main_url):
	with conn:
		cur.execute("""UPDATE visited_sites SET visited_check=1 WHERE urls=?""", (main_url,))

def insert_outbound_links_first_table(ls_url):
	for url in ls_url:
		cur.execute("""SELECT * FROM visited_sites WHERE urls=?""", (url,))
		db_check = cur.fetchall()

		#Check duplicate
		if len(db_check) < 1:
			with conn:
				cur.execute("""INSERT INTO visited_sites(urls, visited_check,
					old_page_rank, new_page_rank) VALUES(?,?,?,?)""",
					(url, 0, None, 1))
		else:
			continue

def insert_outbound_links_second_table(main_url, ls_url):
	cur.execute("""SELECT id FROM visited_sites WHERE urls=?""", (main_url,))
	main_id = cur.fetchone()[0]
	for url in ls_url:
		cur.execute("""SELECT id FROM visited_sites WHERE urls=?""", (url,))
		outbound_id = cur.fetchone()[0]
		with conn:
			cur.execute("""INSERT INTO outbound_links(url_id, outbound) VALUES(?,?)""", (main_id, outbound_id))

#Database Tables
cur.execute("""CREATE TABLE IF NOT EXISTS visited_sites(id INTEGER PRIMARY KEY AUTOINCREMENT, 
	urls TEXT UNIQUE, visited_check INTEGER, old_page_rank REAL, new_page_rank REAL)""")

cur.execute("""CREATE TABLE IF NOT EXISTS outbound_links(url_id INTEGER, outbound INTEGER)""")

#Main loop
running = True
while running is True:
	start = input("Start getting the main url?[y/n]: ")
	print()
	#Check if the table is empty and Initialize the main url
	cur.execute("""SELECT * FROM visited_sites""")
	empty_check = cur.fetchall()

	if start == "y":
		if len(empty_check) < 1:
			url = input("Enter the Main Url: ")
			if len(url) < 1:
				url = "http://www.dr-chuck.com/"

			main_url = new_main_insert(url)

		else:
			try:
				print("Database Found! Getting Random Url...")
				main_url = get_random_main()
				update_random_main(main_url)
			except:
				print("No url found in database")
				ask_put_new = input("Do you want to put new url![y/n]: ")
				if ask_put_new == "y":
					main_url = input("Enter new url: ")
					new_main_insert(main_url)
				else:
					sys.exit("Exitted Successfully")
	else:
		sys.exit("Exitted Successfully")

	print("Main Url:", main_url)
	print("\n")

	#Get all the links inside the main url and Put them in the database
	try:
		ls_outbound_links = get_outbound_links1(main_url)
	except:
		ls_outbound_links = get_outbound_links2(main_url)

	insert_outbound_links_first_table(ls_outbound_links)
	insert_outbound_links_second_table(main_url, ls_outbound_links)
	print(len(ls_outbound_links), "Links Found")
	print()
	
	

	



