import os
from datetime import datetime

from .utils import is_slug


class Podcast:
    def __init__(self, info, name, slug, description, thumb):
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
            info.warn(f"A description is highly recommended.")
        elif not isinstance(description, str):
            info.error(
                f"Description is required to be a string, "
                f"got {type(description)}"
            )
            valid = False

        if not thumb or not isinstance(description, str):
            info.error(
                f"Thumbnail is required to be a string, "
                f"got {type(description)}"
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

        if not valid:
            raise ValueError("Invalid Podcast")

        self.name = name
        self.slug = slug
        self.description = description
        self.thumb = thumb

        self.episodes = dict()

    def add_episode(self, episode):
        """ Adds an episode to the podcast """
        if episode.slug in self.episodes:
            self.info.warn(
                f"Episode `{episode.slug}` already exists, "
                f"overwriting"
            )
        self.episodes[episode.slug] = episode

    def dump(self, include_episodes=True):
        """ Dumps the podcast to a dict """
        dates = sorted([
            e.date.astimezone().isoformat()
            for e in self.episodes.values()
        ])

        data = {
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "last-updated": dates[-1],
            "first-episode": dates[0]
        }

        if include_episodes:
            e = [e.dump() for e in self.episodes.values()]
            e.sort(key=lambda x: x["date"])
            e.reverse()
            data["episodes"] = e

        return data
