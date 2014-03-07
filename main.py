import asyncio
import aiohttp

from bs4 import BeautifulSoup
import re

@asyncio.coroutine
def get_page(url):
	response = yield from aiohttp.request('GET', url)
	body = yield from response.read_and_close(decode = True)
	return body

@asyncio.coroutine
def get_areas(url):
	page = yield from get_page(url)
	soup = BeautifulSoup(page)
	links = soup.find_all(
		name = "a",
		href = re.compile("^[A-Z]+\.html$")
	)
	return list(set([l['href'] for l in links]))

@asyncio.coroutine
def get_subjects(url):
	print(url)
	return
	page = yield from get_page(url)
	soup = BeautifulSoup(page)

def scrape():
	domain = 'http://www.timetable.unsw.edu.au/current/'

	scraper = get_areas(domain + 'subjectSearch.html')
	loop = asyncio.get_event_loop()
	areas = loop.run_until_complete(scraper)

	scraper = asyncio.wait([get_subjects(domain + area) for area in areas])
	loop = asyncio.get_event_loop()
	subjects = loop.run_until_complete(scraper)

if __name__ == "__main__":
	scrape()
