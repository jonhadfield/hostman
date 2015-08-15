import os


def is_readable(path=None):
    """ Test if the supplied filesystem path can be read
    :param path: A filesystem path
    :return: True if the path is a file that can be read. Otherwise, False
    """
    if os.path.isfile(path) and os.access(path, os.R_OK):
        return True
    return False


def is_writeable(path=None):
    """
    Test if the supplied filesystem path can be written to
    :param path: A filesystem path
    :return: True if the path is a file that can be written. Otherwise, False
    """
    if os.path.isfile(path) and os.access(path, os.W_OK):
        return True
