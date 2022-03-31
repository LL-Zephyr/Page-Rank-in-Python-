# Page-Rank-in-Python-
Implementation of PageRank algorithm using python and database.

_________________PAGE RANK_________________

Introduction:

* The page rank is a way to solve rank pages based on the outbound links and as well as the inbound links.
The outboundlinks (in your website perspective) are links from other websites to yours, and the 
inbound links (in your website perspective) are links from your website to someone else's. The inbound links
and the outbound links can be used due to the fact that page rank formula depends on other pages' page.

* The page is superb if the page rank was higher among others, because the assumption in the page rank is 
that more important page are likely to receive more links from other pages.

* The Google use page rank and it is their main method to rank web pages and eventually display it on
the search engine results. In this page rank code, it was just a simple page rank application which can 
quantify the quality of a page based only on the formula, and disregarding the popularity of the page.

Needed:
1. python
2. sqlite3
3. BeautifulSoup
4. urllib
5. requests
6. sys

Target:
1. Make a simple implementation of a page rank
2. Make a version of page rank based on the references

Limitation:
1. At first, the user can enter the main url, but after that the program will choose url randomly in the database.
2. If the urls in the database was all visited the the program can prompt for new url.
3. The iteration will be limited to one per run.

Approach: 
* Iterative Approach - Iteratively update the rank of the page based on the page rank formula.
To get more stable results, more iteration was needed.

Formula:
* PageRank(Page) = For n times of iteration((PR(T1)/C(T1) + PR(T2)/C(T2) + ... + PR(Tn)/C(T2)))

Steps in page rank database making:
1. Make a python file that will create the page rank database
2. Import needed modules: sqlite3, sys, own library (sqlite3 most important)
3. Create two tables: table1 = urls, visited, old rank, new rank  table2= url_id, outbound links
5. Make database functions that can help in solving minute problems
6. Make a while loop that runs based on the user
7. Inside the loop call all the functions

Steps in page ranksolver:
1. Understand the computation for the page rank
2. Make functions that can get previous rank, inbound links, outbound links etc.
3. Make a function that can compute the final page rank and a function that can update the database


References:

	1. Global Software Support - https://www.youtube.com/watch?v=P8Kt6Abq_rM&list=PLH7W8KdUX6P2n4XwDiKsEU6sBhQj5cAqa&index=4
	
	2. Chuck Severance - https://www.youtube.com/watch?v=9gtLOS87ZPs
	
	3. Page Rank Simulator - https://computerscience.chemeketa.edu/cs160Reader/_static/pageRankApp/index.html




