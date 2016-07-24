import numpy as np
from first_tests import _get_lowest_fraction

def cut(picture, div_x, div_y):
    x_len, y_len = picture.shape
    size_x, size_y = x_len / div_x, y_len / div_y

    isize_x, isize_y = int(size_x), int(size_y)
    ratio_x, ratio_y = size_x - isize_x, size_y - isize_y
    fraction_x, fraction_y = _get_lowest_fraction(ratio_x, 1.0 / div_x), _get_lowest_fraction(ratio_y, 1.0 / div_y)

    info = {
        'fraction_x':fraction_y, 'fraction_y':fraction_y,
        'original_size':(x_len,y_len), 'num_tiles':(div_x,div_y)
    }

    mozaic = {}
    curr_x = 0
    for ix in range(div_x):
        x_adjust = 1 if ix % fraction_x[1] < fraction_x[0] else 0
        real_size_x = isize_x + x_adjust
        end_x = curr_x + real_size_x
        curr_y = 0
        for iy in range(div_y):
            y_adjust = 1 if iy % fraction_y[1] < fraction_y[0] else 0
            real_size_y = isize_y + y_adjust
            end_y = curr_y + real_size_y

            mozaic[(ix,iy)] = picture[curr_x:end_x,curr_y:end_y]

            curr_y = end_y
        curr_x = end_x

    return mozaic, info


def stitch(mozaic, info, top_left, size):

    average_size = [ info['original_size'][i]/info['num_tiles'][i] for i in (0,1) ]

    top_left_tile = [ int(top_left[i]/average_size[i]) for i in (0,1) ]
    num_tiles = [ int(size[i]/average_size[i]) + 1 for i in (0,1) ]
    last_tile = [top_left_tile[i] + num_tiles[i] for i in (0,1)]
    down_right_tile = [info['num_tiles'][i] if info['num_tiles'][i] < last_tile[i] else last_tile[i] for i in (0,1)]


    lines = []
    i=0
    for tile_x in range(top_left_tile[0], down_right_tile[0]):
        cur_line = mozaic[(tile_x,top_left_tile[1])]
        for tile_y in range(top_left_tile[1]+1, down_right_tile[1]):
            cur_line = np.concatenate((cur_line, mozaic[(tile_x,tile_y)]),axis=1)
        lines.append(cur_line)

    return np.concatenate(lines, axis=0)


# TODO : option to correct the size approximation (will become a lot less good looking ahah)


