"""
    Module to handle the cutting/stitching part of the application.
    It exposes two functions : divide (to create the tiles) and regroup (to stitch tiles together)

"""

from Mozaic import image_lib

import math

def save_mozaic(picture_file, mozaic, info)

    folder_name = _get_folder_name(picture_file)
    _save_tiles(mozaic, folder_name)
    _save_info(info, folder_name)
    return folder_name


def regroup():
    # todo
    pass


def stitch(tiles, dest):
    """
    stitch the tiles in the list 'tiles' and saves the picture at address dest.

    :param tiles: Matrix of the tiles to stitch together
    :param dest: address for the destination of the resulting picture
    :return: destpass
    """
    pass

