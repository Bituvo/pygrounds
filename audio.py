from datetime import datetime
from bs4 import BeautifulSoup
from utils import *
import requests
import re

class Audio:
    def __init__(self, song_id):
        self.id = song_id

        self.refresh()

    def refresh(self):
        response = requests.get(f"https://newgrounds.com/audio/listen/{self.id}")
        response.raise_for_status()

        self._response = response
        self._populate_fields()

    def _populate_fields(self):
        soup = BeautifulSoup(self._response.content, "html.parser")

        self.name = soup.find("meta", {"property": "og:title"}).attrs["content"]

        self.artists = []
        for element in soup.find_all("div", {"class": "item-user"}):
            self.artists.append(element.find("h4").find("a").text)
        self.artist = self.artists[0]

        sidestats = soup.find("div", {"id": "sidestats"})

        social_statistics = sidestats.find("dl")

        listens = social_statistics.find("dt", string="Listens").find_next("dd").text
        faves_text_element = social_statistics.find("dt", string="Faves:")

        if faves_text_element:
            faves = faves_text_element.find_next("dd").find("a").text
            votes = social_statistics.find("dt", string="Votes").find_next("dd").text
            score = soup.find("meta", {"itemprop": "ratingValue"}).attrs["content"]

            self.faves = int(faves.replace(",", ""))
            self.votes = int(votes.replace(",", ""))
            self.score = float(score) / 10
        else:
            self.faves = None
            self.votes = None
            self.score = None

        self.listens = int(listens.replace(",", ""))

        file_info = social_statistics.find_next("dl")

        date_element = file_info.find("dt", string="Uploaded").find_next("dd")
        time_element = date_element.find_next("dd")
        audio_type_element = file_info.find("dt", string="File Info").find_next("dd")
        file_size_element = audio_type_element.find_next("dd")
        duration_element = file_size_element.find_next("dd")

        self.genre = file_info.find("a").text
        self.date_published = parse_time(date_element.text, time_element.text)
        self.audio_type = audio_type_element.text.strip().lower()
        self.file_size = file_size_element.text.strip()
        self.duration = parse_duration(duration_element.text.strip())

        tags_list = sidestats.find("dd", {"class": "tags"})
        if tags_list:
            self.tags = [tag.text for tag in tags_list.find_all("a")]
        else:
            self.tags = []

        author_comments_div = soup.find("div", {"id": "author_comments"})
        short_description_element = soup.find("meta", {"name": "twitter:description"})
        if author_comments_div:
            self.author_comments_html = author_comments_div.decode_contents().strip()
        else:
            self.author_comments_html = None
        if short_description_element:
            self.short_description = short_description_element.attrs["content"]
        else:
            self.short_description = None

        frontpaged_element = soup.find("li", {"class": "frontpage"})
        if frontpaged_element:
            self.frontpaged = True
            date_frontpaged = frontpaged_element.find("a").text
            self.date_frontpaged = datetime.strptime(date_frontpaged, "%B %d, %Y")
        else:
            self.frontpaged = False
            self.date_frontpaged = None

        match = re.search(r'"url":"(https:\\/\\/audio.ng[^"]*)', self._response.text)
        url = match.group(1)
        self.download_url = url.replace("\\/", "/")

        self.track_image = soup.find("meta", {"property": "og:image"}).attrs["content"]

        for attr in dir(self):
            if not attr.startswith("_"):
                print(f"self.{attr} -> {getattr(self, attr)}")

song = Audio(1293015)
