from dataclasses import dataclass
from urllib.parse import unquote
import re
import json
import requests

@dataclass
class _Spectrograph:
    full_url: str
    condensed_url: str

class Audio:
    def __init__(self, song_id):
        self.id = song_id

        self.refresh()

    def refresh(self):
        response = requests.get(f"https://newgrounds.com/audio/listen/{self.id}")
        response.raise_for_status()

        data = re.search(r"var embed_controller = new embedController\((.*?)\);", response.text).group(1)
        data = re.sub(r',"html".*', "", data, 1) + "}]"
        data = unquote(data)

        self._populate_fields(json.loads(data)[0])

    def _populate_fields(self, data):
        self.name = data["params"]["name"]
        self.artist = data["params"]["artist"]

        self.length = data["params"]["duration"]
        self.size = data["filesize"]
        self.is_loop = bool(data["params"]["loop"])

        self.spectrograph = _Spectrograph(
            "https:" + data["params"]["images"]["listen"]["playing"]["url"],
            "https:" + data["params"]["images"]["condensed"]["playing"]["url"]
        )
        self.download_url = data["url"]
