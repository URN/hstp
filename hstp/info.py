import simple_colors as colour


class Info:
    """ Class containing logging functions """
    def __init__(self):
        pass

    def warn(self, message):
        """ Prints Warning Message to console """
        print(colour.yellow("WARNING: ", "bold") + message)

    def error(self, message):
        """ Prints Error Message to console """
        print(colour.red("ERROR: ", "bold") + message)

    def debug(self, message):
        """ Prints Debug Message to console """
        print(colour.blue("DEBUG: ", "bold") + message)
