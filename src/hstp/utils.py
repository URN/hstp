import os
import shutil


def is_slug(string):
    """ Function to test if a URL slug is valid """
    return all([s in '0123456789-abcdefghijklmnopqrstuvwxyz' for s in string])


def subdirectories(dir):
    return [
        x
        for x in os.listdir(dir)
        if os.path.isdir(f"{dir}/{x}")
    ]


def path_or_none(file):
    if os.path.exists(file):
        return file


def copyfile(src, dst):
    if os.path.isfile(dst):
        return
        # Add more conditions here
        # if os.path.getsize(src) == os.path.getsize(dst):
        #    return
    shutil.copyfile(src, dst)
