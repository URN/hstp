import hstp
import hstp.utils
from dateutil.parser import parse
import os


class Reader:
    """ Read in an input tree to a station object """

    def __init__(self, info, input_path):
        self.info = info
        self.input_path = input_path

    def load_podcasts(self):
        """ loads the podcasts from the input tree"""
        pods = hstp.utils.subdirectories(self.input_path)
        self.podcasts = []

        for slug in pods:
            p = None
            with open(f"{self.input_path}/{slug}/description.txt") as desc:
                lines = desc.read().split("\n")
                title = lines[0]
                d = '\n'.join(lines[1:])

                p = hstp.Podcast(self.info, title, slug, d, f"{self.input_path}{slug}/image.jpg")
            
            eps = hstp.utils.subdirectories(f"{self.input_path}/{slug}")
            for ep_slug in eps:
                with open(f"{self.input_path}/{slug}/{ep_slug}/description.txt") as desc:
                    lines = desc.read().split("\n")
                    title = lines[0]
                    date = lines[1]
                    d = '\n'.join(lines[2:])

                    e = hstp.Episode(
                        self.info,
                        title,
                        ep_slug,
                        d,
                        parse(date),
                        f"{self.input_path}/{slug}/{ep_slug}/audio.mp3",
                        thumb=hstp.utils.path_or_none(f"{self.input_path}/{slug}/{ep_slug}/image.jpg")
                    )
                    p.add_episode(e)
            self.podcasts.append(p)
