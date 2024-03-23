from bs4 import BeautifulSoup
import requests

class Movie:
    def __init__(self, portal_id):
        self.id = portal_id
        
        self.refresh()

    def refresh(self):
        response = requests.get(f"https://newgrounds.com/portal/view/{self.id}")
        response.raise_for_status()

        self._response = response
        self._populate_fields()

    def _populate_fields(self):
        soup = BeautifulSoup(self._response.content, "html.parser")

        self.name = soup.find("title").text

        self.artists = []
        for element in soup.find_all("div", {"class": "item-user"}):
            self.artists.append(element.find("h4").find("a").text)
        self.artist = self.artists[0]

        sidestats = soup.find("div", {"id": "sidestats"})

        social_statistics = sidestats.find("dl")

        views = social_statistics.find("dt", string="Views").find_next("dd").text
        faves_text_element = social_statistics.find("dt", string="Faves:")

        if faves_text_element:
            faves = faves_text_element.find_next("dd").find("a").text
            votes_text_element = social_statistics.find("dt", string="Votes")
            if votes_text_element:
                votes = votes_text_element.find_next("dd").text
                self.votes = int(votes.replace(",", ""))
            else:
                self.votes = None
            score = soup.find("meta", {"itemprop": "ratingValue"}).attrs["content"]

            self.faves = int(faves.replace(",", ""))
            self.score = float(score) / 10
        else:
            self.faves = None
            self.votes = None
            self.score = None

        self.views = int(views.replace(",", ""))
