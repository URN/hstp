import hstp
from datetime import datetime
import unittest

import os

test_dir = os.path.dirname(os.path.realpath(__file__))


def get_test_file(filename):
    return os.path.join(test_dir, "data", filename)


class TestEpisodeValidation(unittest.TestCase):

    def test_no_audio(self):
        with self.assertRaises(ValueError):
            print()  # Inserts a newline
            e = hstp.Episode(
                hstp.Info(),
                "The Adventures of the Engineer's thumb",
                "adventures-engineers-thumb",
                None,
                datetime.now(),
                get_test_file("no_audio.mp3")
            )

    def test_valid_data(self):
        try:
            print()  # Inserts a newline
            e = hstp.Episode(
                hstp.Info(),
                "The Adventures of the Engineer's thumb",
                "adventures-engineers-thumb",
                None,
                datetime.now(),
                get_test_file("audio.mp3")
            )
            self.assertTrue(True)
        except ValueError:
            self.fail()


if __name__ == '__main__':
    unittest.main()
