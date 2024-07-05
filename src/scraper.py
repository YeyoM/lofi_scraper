# scraper.py
import asyncio
import json
import os

import bs4
import pyppeteer


# Function to save the data to a JSON file
def save_data(data: list):
    os.makedirs("data", exist_ok=True)
    with open("data/scrapped_songs.json", "w") as f:
        json.dump(data, f, indent=4)


# Function to get the number of songs
def get_num_songs(soup):
    parent_div = soup.find("div", id="my-ch-playlist")
    if parent_div and isinstance(parent_div, bs4.Tag):
        inner_divs = parent_div.find_all(
            "div", class_="track-model flex columns playit no-play"
        )
        return len(inner_divs)
    return 0


# Function to get hrefs
async def get_hrefs(page, pages):
    hrefs = []
    for i in range(1, pages + 1):
        await page.goto(f"https://chillhop.com/releases?page={i}")
        html = await page.content()
        soup = bs4.BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", class_="single-post-model"):
            hrefs.append(a["href"])
    return hrefs


# Function to scrape song data
async def scrape_song_data(page, href):
    data = []
    await page.goto(f"https://chillhop.com{href}")
    html = await page.content()
    soup = bs4.BeautifulSoup(html, "html.parser")
    try:
        await page.click("a.pl-btn.playit")
    except:
        return data
    num_song = get_num_songs(soup)
    for i in range(num_song):
        track_data = {}
        audio = await page.querySelector("audio#playerAudio")
        src = await page.evaluate("(element) => element.src", audio)
        title = await page.querySelectorEval(
            "div.p-track-title", "element => element.innerText"
        )
        artist = await page.querySelectorEval(
            "div.p-track-artist", "element => element.innerText"
        )
        track_data["author"] = artist
        track_data["title"] = title
        track_data["id"] = src.split("/")[-1]
        track_data["path"] = src
        track_data["url"] = f"https://chillhop.com{href}"
        data.append(track_data)
        await page.click("a#p-btn-next")
    return data


# Running the scraper
async def chillhop_scraper():
    pages = 2
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    hrefs = await get_hrefs(page, pages)
    data = []
    for href in hrefs:
        song_data = await scrape_song_data(page, href)
        data.extend(song_data)
    await browser.close()
    save_data(data)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(chillhop_scraper())
