import hstp
import hstp.utils
from dateutil.parser import parse
import os
import json
from shutil import copyfile


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

                p = hstp.Podcast(self.info, title, slug, d,
                                 f"{self.input_path}/{slug}/image.jpg")

            links_path = f"{self.input_path}/{slug}/links.txt"
            if os.path.exists(links_path):
                with open(links_path) as desc:
                    lines = desc.read().split("\n")
                    self.links = dict()
                    for line in lines:
                        s = line.split(" ")
                        self.links[" ".join(s[1:])] = s[0]

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
                        hstp.utils.path_or_none(
                            f"{self.input_path}/{slug}/{ep_slug}/image.jpg"
                        )
                    )
                    p.add_episode(e)
            self.podcasts.append(p)

    def save(self, output_path):
        """ saves the output tree """

        # hstp.json
        hstp_out = dict()
        hstp_out['podcasts'] = []
        for p in self.podcasts:
            hstp_out['podcasts'].append(p.dump(False))
            with open(f"{output_path}/{p.slug}.json", 'w') as f:
                f.write(json.dumps(p.dump(True)))

            if not os.path.exists(f"{output_path}/{p.slug}"):
                os.makedirs(f"{output_path}/{p.slug}")

            copyfile(p.thumb, f"{output_path}/{p.slug}.jpg")

            for e in p.episodes.values():
                copyfile(e.file, f"{output_path}/{p.slug}/{e.slug}.mp3")
                if e.thumb is not None:
                    copyfile(e.thumb, f"{output_path}/{p.slug}/{e.slug}.jpg")

        hstp_out['podcasts'].sort(key=lambda x: x['last-updated'])
        hstp_out['podcasts'].reverse()

        with open(f"{output_path}/hstp.json", 'w') as f:
            f.write(json.dumps(hstp_out))
