"""
    Module that handles the most part of the work. The functions exposed here will basically be the entry functions
    for the user.
"""

from Mozaic import image_inout, image_lib

import math, datetime


def cut(picture_file, tile_size):
    """
    Cuts the picture at address `picture_file` into tiles that have the size `tile_size`.
    The tiles will be saved as image file with arbitrary name in a folder.
    Returns the address of the folder containing the tiles.

    `tile_size` must be smaller than the given picture.

    :param picture_file: Address of the picture
    :param tile_size: tuple giving the expected size of each tile
    :return: address of the created folder containing all the tiles
    """
    picture = image_lib.open(picture_file)

    num_tile = tuple(int(math.ceil(p_s / t_s)) for p_s, t_s in zip(image_lib.get_shape(picture), tile_size))

    mozaic = {}
    curr_x = 0
    for ix in range(num_tile[0]):
        end_x = curr_x + tile_size[0]
        curr_y = 0
        for iy in range(num_tile[1]):
            end_y = curr_y + tile_size[1]
            mozaic[(ix, iy)] = picture[curr_x:end_x, curr_y:end_y] # TODO

            curr_y = end_y
        curr_x = end_x

    info = {
        'original_size': picture.shape,
        'num_tiles': num_tile,
        'tile_size': tile_size,
        'creation_date': datetime.datetime.now()
    }

    folder_name = image_inout.save_mozaic(picture_file, mozaic, info)

    return folder_name


def get(picture, top_left, down_right, save=False):
    res_mozaic = find(picture,top_left,down_right)

    if save:
        image_inout.stitch(res_mozaic,save)
        return save
    else:
        return res_mozaic


def find(picture, top_left, down_right):
    """
    Finds the rectangle defined by the points 'top_left' and 'down_right' in the picture `picture`.

    :param picture: address of the folder created by tiling a picture.
    :param top_left: position of the top_left corner of the requested rectangle region
    :param down_right: position of the top_left corner of the requested rectangle region
    :return: a 2D list (matrix) containing the name of the tiles that make the requested rectangle
    """

    info = image_inout.get_info(picture)
    top_left_tile = tuple(tile // size for tile, size in zip(top_left, info['tile_size']))
    down_right_tile = tuple(tile // size for tile, size in zip(down_right, info['tile_size']))

    # TODO : create a matrix with the name of the tiles to put together
    pass

