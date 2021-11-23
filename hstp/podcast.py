import os
from datetime import datetime

from .utils import is_slug

from lxml.etree import Element, SubElement, QName, tounicode


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

    def dump_rss(self):
        """ Dumps the podcast to an RSS feed """
        data = {
            "webroot": "https://podcasts.urn1350.net",
            "lang": "en",
            "author": "urn1350",
            "website": "https://urn1350.net/podcasts/{slug}#{episode}"
        }

        NSMAP = {
            "atom": "http://www.w3.org/2005/Atom",
            "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
            "dcterms": "http://purl.org/dc/terms/",
            "spotify": "http://www.spotify.com/ns/rss",
            "psc": "http://podlove.org/simple-chapters",
        }

        root = Element("rss", nsmap=NSMAP)
        root.set("version", "2.0")

        c = SubElement(root, "channel")
        SubElement(c, "title").text = self.name
        SubElement(c, "description").text = self.description
        SubElement(c, "link").text = f"{data['webroot']}/{self.slug}.xml"
        SubElement(c, "language").text = data['lang']
        SubElement(c, QName(NSMAP['itunes'], "author")).text = data['author']
        SubElement(c, QName(NSMAP['itunes'], "image")).set("href", f"{data['webroot']}/{self.slug}.jpg")
        SubElement(c, QName(NSMAP['itunes'], "explicit")).text = "no"
        SubElement(c, QName(NSMAP['itunes'], "category")).text = "Technology" # Load from somewhere
        SubElement(c, QName(NSMAP['itunes'], "type")).text = "episodic"
        SubElement(c, QName(NSMAP['itunes'], "countryOfOrigin")).text = "GB US" # British, but will promote to US

        for e in self.episodes.values():
            i = SubElement(c, "item")
            g = SubElement(i, "guid")
            g.text = data["website"].format(slug=self.slug, episode=e.slug)
            g.set("isPermaLink", "true")

            enc = SubElement(i, "enclosure")
            enc.set("url", f"{data['webroot']}/{self.slug}/{e.slug}.mp3")
            enc.set("length", str(e.content_length))
            enc.set("type", "audio/mpeg")

            SubElement(i, "pubDate").text = e.date.astimezone().isoformat()
            SubElement(i, "title").text = e.name
            SubElement(i, "description").text = e.description
            SubElement(i, QName(NSMAP['itunes'], "duration")).text = str(int(e.duration + 0.5))
            SubElement(i, QName(NSMAP['itunes'], "explicit")).text = "no"
            if e.has_image:
                SubElement(i, QName(NSMAP['itunes'], "image")).set(
                    "href",
                    f"{data['webroot']}/{self.slug}/{e.slug}.jpg"
                )
            else:
                SubElement(i, QName(NSMAP['itunes'], "image")).set(
                    "href",
                    f"{data['webroot']}/{self.slug}.jpg"
                )

        return root
