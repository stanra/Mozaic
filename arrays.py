import datetime
import numpy as np
from first_tests import _get_lowest_fraction


def cut(picture, param_x, param_y, mode, fixed_size):
    if mode == 'number':
        num_tile = param_x, param_y
        expected_size = tuple(size_val / num_val for size_val, num_val in zip(picture.shape, num_tile))
        tile_size = tuple(int(s) for s in expected_size)
        if fixed_size:
            fraction = tuple( (0,num) for num in num_tile) #0 are bigger in one cycle, one cycle is total length
        else:
            ratio = tuple(e_s - t_s for e_s, t_s in zip(expected_size, tile_size))
            fraction = tuple(_get_lowest_fraction(r, 1.0 / p) for r,p in zip(ratio, num_tile))

    elif mode == 'size':
        tile_size = param_x, param_y
        num_tile = tuple(p_s//t_s for p_s, t_s in zip(picture.shape, tile_size))
        fraction = tuple( (0,num) for num in num_tile) # maybe should num-1 but it doesn't actually change anything
    else:
        raise ValueError('Valid modes : "number" or "size"')

    mozaic = {}
    curr_x = 0
    fraction_x, fraction_y = fraction
    for ix in range(num_tile[0]):
        x_adjust = 1 if ix % fraction_x[1] < fraction_x[0] else 0
        real_size_x = tile_size[0] + x_adjust
        end_x = curr_x + real_size_x
        curr_y = 0
        for iy in range(num_tile[1]):
            y_adjust = 1 if iy % fraction_y[1] < fraction_y[0] else 0
            real_size_y = tile_size[1] + y_adjust
            end_y = curr_y + real_size_y

            mozaic[(ix,iy)] = picture[curr_x:end_x, curr_y:end_y]

            curr_y = end_y
        curr_x = end_x

    info = {
        'fraction': fraction,
        'original_size': picture.shape,
        'num_tiles': num_tile,
        'tile_size': tile_size,
        'creation_date': datetime.datetime.now()
    }

    return mozaic, info



def stitch(mozaic, info, top_left, down_right, fixed_size):

    # V1 : consider all tile have same size --> it is faster.
    if fixed_size:
        top_left_tile = (tile // size for tile, size in zip(top_left, info['tile_size']))
        down_right_tile = (tile // size for tile, size in zip(down_right, info['tile_size']))
    else:
        top_left_tile = _get_tile_including(top_left, info)
        down_right_tile = _get_tile_including(down_right, info)

    lines = []
    i = 0
    for tile_x in range(top_left_tile[0], down_right_tile[0]):
        cur_line = mozaic[(tile_x,top_left_tile[1])]
        for tile_y in range(top_left_tile[1]+1, down_right_tile[1]):
            cur_line = np.concatenate((cur_line, mozaic[(tile_x,tile_y)]),axis=1)
        lines.append(cur_line)

    return np.concatenate(lines, axis=0)


def _get_tile_including(point, info):
    # Note : may have an error : if we are at tile number t, then there are only t-1 tiles behind me !
    # But since indexes start at 0 and p and q are 'numbers' it should be included already ?

    # The implementation under is really inefficient
    # could easily check if q == num_tile and p==0 to do it differently
    # but the time saved is not going to be a lot and the code will get more annoying.


    tile_size_avg = tuple(pic_size / num_tile for pic_size, num_tile in zip(info['original_size'], info['tile_size']))
    expected_real_pos = tuple( point_pos / tile_size for point_pos, tile_size in zip(point, tile_size_avg))

    result = (None,None)
    for i in (0,1): # We treat x and y separately
        p,q = info['fraction'][i]
        tile_size = info['tile_size'][i]
        index_guessed_tile = int(expected_real_pos[i])
        while True:
            num_finished_cycle = index_guessed_tile // q
            p_prime = index_guessed_tile % q # p_prime is the position in the current cycle

            pos_guessed_tile = num_finished_cycle * tile_size_avg[i] +\
                                    (tile_size+1) * min(p,p_prime) + tile_size * max(p_prime-p,0)
            error = point[i] - pos_guessed_tile

            if error < 0: # The tile starts 'after the point'
                index_guessed_tile -= 1
            else:
                this_tile_size = tile_size
                if p_prime < p:
                    this_tile_size += 1
                if error > this_tile_size: # The point is after the tile
                    index_guessed_tile += 1
                else:
                    result[i] = index_guessed_tile
                    break

    return result





