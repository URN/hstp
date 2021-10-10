import hstp
from datetime import datetime
from dateutil import parser
import unittest

import os

test_dir = os.path.dirname(os.path.realpath(__file__))


def get_test_file(filename):
    return os.path.join(test_dir, "data", filename)


class TestPodcastValidation(unittest.TestCase):
    def test_valid_data(self):
        try:
            print()  # Inserts a newline
            e1 = hstp.Episode(
                hstp.Info(),
                "The Adventures of the Engineer's thumb",
                "adventures-engineers-thumb",
                "Description",
                parser.parse("1892-03-01"),
                get_test_file("audio.mp3")
            )

            e2 = hstp.Episode(
                hstp.Info(),
                "The Hound of the Baskervilles",
                "hound-baskervilles",
                "Description",
                parser.parse("1902-04-01"),
                get_test_file("audio.mp3")
            )

            p = hstp.Podcast(
                hstp.Info(),
                "Holme's",
                "adventures-engineers-thumb",
                "Podcast Description",
                get_test_file("logo.jpg")
            )

            p.add_episode(e1)
            p.add_episode(e2)

            print(p.dump())
        except ValueError:
            self.fail()


if __name__ == '__main__':
    unittest.main()
