from bs4 import BeautifulSoup
from datetime import datetime
import requests

class Artist:
    def __init__(self, username):
        self.username = username

        self.refresh()

    def refresh(self):
        response = requests.get(f"https://{self.username}.newgrounds.com/")
        response.raise_for_status()

        self._response = response
        self._populate_fields()

    def _populate_fields(self):
        soup = BeautifulSoup(self._response.content, "html.parser")

        self.username = soup.find("title").text

        user_stats = soup.find("div", {"id": "userstats"})

        age_and_gender = user_stats.find("i", {"class": "fa fa-user"}).parent.text.strip()
        location = user_stats.find("i", {"class": "fa fa-map-marker"}).parent.text.strip()
        joined_date = user_stats.find("i", {"class": "fa fa-calendar"}).parent.text.strip()

        self.bio = user_stats.find("blockquote").text
        age_and_gender = age_and_gender.split()
        self.age = int(age_and_gender[1][:-1])
        self.gender = age_and_gender[2].lower()
        self.date_joined = datetime.strptime(joined_date[10:], "%m/%d/%y")
