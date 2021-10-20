import hstp
import os


class Reader:
    """ Read in an input tree to a station object """

    def __init__(self, info, input_path):
        self.info = info
        self.input_path = input_path

    def load_podcasts(self):
        """ loads the podcasts from the input tree"""
        dirs = [x for x in os.listdir(self.input_path) if os.isdir(x)]
        print(dirs)
