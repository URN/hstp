
def is_slug(string):
    """ Function to test if a URL slug is valid """
    return all([s in '0123456789-abcdefghijklmnopqrstuvwxyz' for s in string])
