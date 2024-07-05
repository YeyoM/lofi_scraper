import json
import os
import sys
from unittest.mock import AsyncMock, MagicMock

import aiounittest
import bs4

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.scraper import get_hrefs, get_num_songs, save_data, scrape_song_data


class TestChillhopScraper(aiounittest.AsyncTestCase):
    def test_get_num_songs(self):
        html = """
        <div id="my-ch-playlist">
            <div class="track-model flex columns playit no-play"></div>
            <div class="track-model flex columns playit no-play"></div>
        </div>
        """
        soup = bs4.BeautifulSoup(html, "html.parser")
        num_songs = get_num_songs(soup)
        self.assertEqual(num_songs, 2)

    def test_get_num_songs_no_songs(self):
        html = """
        <div id="my-ch-playlist"></div>
        """
        soup = bs4.BeautifulSoup(html, "html.parser")
        num_songs = get_num_songs(soup)
        self.assertEqual(num_songs, 0)

    def test_save_data(self):
        data = [
            {
                "author": "Artist 1",
                "title": "Song 1",
                "id": "123",
                "path": "/path1",
                "url": "https://example.com/1",
            },
            {
                "author": "Artist 2",
                "title": "Song 2",
                "id": "456",
                "path": "/path2",
                "url": "https://example.com/2",
            },
        ]
        save_data(data)
        with open("data/scrapped_songs.json", "r") as f:
            saved_data = json.load(f)
            self.assertEqual(len(saved_data), 2)
            self.assertIn("Artist 1", saved_data[0]["author"])
            self.assertIn("Artist 2", saved_data[1]["author"])

    async def test_get_hrefs(self):
        # Mock the page content
        mock_page = AsyncMock()
        mock_page.content = AsyncMock(
            return_value="""
            <html>
                <a class="single-post-model" href="/post1"></a>
                <a class="single-post-model" href="/post2"></a>
            </html>
        """
        )

        hrefs = await get_hrefs(mock_page, 1)
        self.assertEqual(hrefs, ["/post1", "/post2"])

    async def test_scrape_song_data(self):
        mock_page = AsyncMock()
        mock_page.content = AsyncMock(
            return_value="""
            <html>
                <div id="my-ch-playlist">
                    <div class="track-model flex columns playit no-play"></div>
                </div>
                <div class="p-track-title">Title 1</div>
                <div class="p-track-artist">Artist 1</div>
                <audio id="playerAudio" src="https://example.com/path1.mp3"></audio>
                <a id="p-btn-next"></a>
            </html>
        """
        )
        mock_page.querySelector = AsyncMock(return_value=MagicMock())
        mock_page.evaluate = AsyncMock(return_value="https://example.com/path1.mp3")
        mock_page.querySelectorEval = AsyncMock(
            side_effect=["Title 1", "Artist 1"]  # p-track-title  # p-track-artist
        )
        mock_page.click = AsyncMock()

        data = await scrape_song_data(mock_page, "/post1")
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["author"], "Artist 1")
        self.assertEqual(data[0]["title"], "Title 1")
        self.assertEqual(data[0]["path"], "https://example.com/path1.mp3")


if __name__ == "__main__":
    aiounittest.main()
