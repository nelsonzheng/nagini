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
    page = yield from get_page(url)
    soup = BeautifulSoup(page)
    links = soup.find_all(
        name = "a",
        href = re.compile("^[A-Z]{4}[0-9]{4}\.html$")
    )
    return list(set([l['href'] for l in links]))

def flatten(l):
    return [y for x in l for y in x]

def scrape():
    domain = 'http://www.timetable.unsw.edu.au/current/'
    loop = asyncio.get_event_loop()

    scraper = get_areas(domain + 'subjectSearch.html')
    areas = loop.run_until_complete(scraper)

    scraper = asyncio.wait([get_subjects(domain + area) for area in areas])
    done, _ = loop.run_until_complete(scraper)
    subjects = flatten(list(map(lambda f: f.result(), done)))
    print(len(subjects))

    loop.close()

if __name__ == "__main__":
    scrape()
