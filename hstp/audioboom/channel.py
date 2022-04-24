from hstp.audioboom import *
import hstp.audioboom
import hstp.audioboom.utils as utils

from os.path import join, exists, relpath
from os import mkdir
import requests
import time


class Channel:
    """ Representation of an audioboom channel"""

    def __init__(self, id):
        self.id = id

        # get info from API
        data = utils.make_request(f"/channels/{id}")["channel"]

        self.title = data["title"]
        self.description = data["description"]
        self.thumbnail = data["urls"]["logo_image"]["original"]

    def get_playlists(self):
        data = utils.make_request(f"/channels/{self.id}/playlists")
        self.playlists = []
        for p in data["playlist"]:
            self.playlists.append(audioboom.Playlist(p))

    def get_episodes(self):
        i = 0
        self.episodes = []
        while True:
            i += 1

            data = utils.make_request(
                f"/channels/{self.id}/audio_clips"
                f"?page[items]=150&page[number]={i}"
            )["audio_clips"]

            if len(data) == 0:
                return

            for ep in data:
                self.episodes.append(audioboom.Episode(ep))

    def save(self, root):
        # create hstp_root.txt
        with open(join(root, "hstp_root.txt"), 'a'):
            pass

        path = join(root, "default")

        if not exists(path):
            mkdir(path)

        with open(join(path, "description.txt"), "w") as f:
            f.write(f"{self.title}\n{self.description}")

        with open(join(path, "image.jpg"), 'wb') as f:
            i = requests.get(self.thumbnail, allow_redirects=True)
            f.write(i.content)

        consumed = []

        for p in self.playlists:
            path_ = join(root, p.slug)
            if exists(path_):
                raise ValueError("slug already exists")

            mkdir(path_)
            with open(join(path_, "description.txt"), "w") as f:
                f.write(f"{p.title}\n{p.description}")

            if p.thumbnail:
                with open(join(path_, "image.jpg"), 'wb') as f:
                    i = requests.get(p.thumbnail, allow_redirects=True)
                    f.write(i.content)

            j = 0
            while True:
                j += 1
                data = utils.make_request(
                    f"/playlists/{p.id}"
                    f"?page[items]=150&page[number]={j}"
                )["playlist"]["memberships"]

                if len(data) == 0:
                    break

                for ep in data:
                    id = ep["audio_clip"]["id"]
                    if id in consumed:
                        continue
                    ep_ = [e for e in self.episodes if e.id == id][0]
                    path__ = join(path_, ep_.slug)
                    self.save_episode(path__, ep_, root)
                    consumed.append(ep_.id)

        # save unused episodes
        for ep in self.episodes:
            if ep.id in consumed:
                continue
            path_ = join(path, ep.slug)

            while exists(path_):
                ep.slug += '-'
                path_ = join(path, ep.slug)

            mkdir(path_)
            self.save_episode(path_, ep, root)

    def save_episode(self, path, ep, root):
        print(f"Saving {ep.title} to {path}")
        if not exists(path):
            mkdir(path)

        with open(join(path, "description.txt"), "w") as f:
            f.write(f"{ep.title}\n{ep.date}\n{ep.description}")

        if ep.thumbnail:
            pass
            with open(join(path, "image.jpg"), 'wb') as f:
                i = requests.get(ep.thumbnail, allow_redirects=True)
                f.write(i.content)

        # Does not download the audios, just outputs a list to be used in download_tool.py
        # with open(join(path, "audio.mp3"), 'wb') as f:
        #    pass
        #    a = requests.get(ep.mp3, allow_redirects=True)
        #    f.write(a.content)

        with open(join(root, "downloads.txt"), 'a') as f:
            out = join(relpath(path, root), "audio.mp3")
            f.write(f"{ep.mp3}\t{out}\n")
