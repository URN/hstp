import os
from datetime import datetime
from dateutil import parser
from mutagen.mp3 import MP3

from .utils import is_slug


class Episode:
    """ Class containing the information for a single podcast episode"""

    @classmethod
    def load(cls, info, data, path):
        """ Loads an episode from a dict """
        e = cls(
            info,
            name=data["name"],
            slug=data["slug"],
            description=data["description"],
            date=parser.isoparse(data["date"]),
            file=f"{path}/{data['slug']}.mp3",
            thumb=f"{path}/{data['slug']}.jpg"
        )

        return e

    def __init__(self, info, name, slug, description, date, file, thumb=None):
        self.info = info

        # Check Arguments
        valid = True

        if not name or not isinstance(name, str):
            info.error(
                f"Name is required to be a string, got {type(name)}"
            )
            valid = False

        if not slug or not isinstance(slug, str):
            info.error(
                f"Slug is required to be a string, got {type(slug)}"
            )
            valid = False
        elif not is_slug(slug):
            info.error(f"Slug `{slug}` is not valid")
            valid = False

        if not description:
            info.warn(f"A description is highly reccommended.")
        elif not isinstance(description, str):
            info.error(
                f"Description is required to be a string, "
                f"got {type(description)}"
            )
            valid = False

        if not date or not isinstance(date, datetime):
            info.error(
                f"Date is required to be a datetime, got {type(date)}"
            )
            valid = False
        else:
            now = datetime.now().astimezone()
            d = date.astimezone()
            if d > now:
                info.warn(
                    f"Date `{d}` is in the future, "
                    f"proceed with caution"
                )

        if not file or not isinstance(file, str):
            info.error(
                f"File is required to be a string, got {type(file)}"
            )
            valid = False
        else:
            if not file.endswith(".mp3"):
                info.warn(
                    f"File `{file}` does not have extension mp3, "
                    f"proceed with caution"
                )
            if not os.path.isfile(file):
                info.error(f"File `{file}` does not exist")
                valid = False
            else:
                try:
                    x = MP3(file)
                    self.duration = x.info.length
                except Exception as e:
                    info.error(f"File `{file}` is not a valid mp3 file")
                    valid = False
                self.content_length = os.path.getsize(file)

        if not thumb:
            info.warn(f"A thumbnail is highly reccommended.")
            self.has_image = False
        elif not isinstance(thumb, str):
            info.error(
                f"Thumbnail is required to be a string, "
                f"got {type(thumb)}"
            )
            valid = False
        else:
            if not thumb.endswith(".jpg"):
                info.warn(
                    f"Thumbnail `{thumb}` does not have extension jpg, "
                    f"proceed with caution"
                )
            if not os.path.isfile(thumb):
                info.error(f"Thumbnail `{thumb}` does not exist")
                valid = False

            self.has_image = True

        if not valid:
            raise ValueError("Invalid Episode")

        self.name = name
        self.slug = slug
        self.description = description
        self.date = date
        self.file = file
        self.thumb = thumb

    def dump(self):
        """ Dump the episode to a dict """
        return {
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "date": self.date.astimezone().isoformat(),
            "has-image": self.has_image,
            "content-length": self.content_length
        }
