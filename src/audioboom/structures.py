import json

from audioboom import utils


class Episode:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"] if "description" in data else ""
        urls = data["urls"]
        self.thumbnail = urls["image"] if "image" in urls else None
        self.mp3 = data["urls"]["high_mp3"]
        self.date = data["uploaded_at"]

        self.slug = utils.make_slug(self.title)


class Playlist:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"] if "description" in data else ""
        self.thumbnail = data["image"] if "image" in data else None

        self.slug = utils.make_slug(self.title)
