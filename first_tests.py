def _get_lowest_fraction(ratio, eps):
    if ratio == 0:
        return 0, 1
    # r = p/q
    # prec = r - p'/q'
    p = 0
    prec = 1
    while prec > eps:
        p += 1
        q = round(p / ratio)
        prec = abs(ratio - p / q)
    return p, q



def cut(picture, div_x, div_y):
    x_len, y_len = picture.shape
    size_x, size_y = x_len / div_x, y_len / div_y

    # we want `div` images of size `size`
    # images can only have int sizes
    # so we want the averages of sizes to be `size`
    # we want `frac` images of size `isize + 1` and `div-frac` images of size `isize` (`isize` = floor(`size`))
    # such that the size average is `size` ( so frac*(isize+1) + (div - frac)*isize = size * div )
    # so we have   `frac` = `div` * (`size` - `isize`)
    # so we have `ratio` = `size` - `isize`
    isize_x, isize_y = int(size_x), int(size_y)
    ratio_x, ratio_y = size_x - isize_x, size_y - isize_y
    # so if we write `ratio` = `p`/`q` then `p` out of `q` images are of size (isize + 1)

    # we want them as small as possible to ensure 'balanced' repartition.
    # we already know that `p`=`frac` and `q`=`div` is a solution, but we want it smaller even if there is slight error
    # This approximation will be solved in the last window, so if we want the error at last window to be < 1 ,
    # then we need to chose an accuracy = 1/div
    # This means that the higher the number of window, the more the alternance is 'long'
    # The local error might be big and it could be an issue
    # The function in charge or recomposing pictures might have 2 mode :
    # A fast mode that doesn't make the correction, which is ok if the expected size of requested picture is larger than p
    # A safe mode that take into account the correction to ensure the returned sub-picture does contain the requested image
    fraction_x, fraction_y = _get_lowest_fraction(ratio_x, 1.0/div_x), _get_lowest_fraction(ratio_y, 1.0/div_y)



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

            mozaic['{}-{}'.format(ix, iy)] = ((curr_x, curr_y), (end_x, end_y))

            curr_y = end_y
        curr_x = end_x

    return mozaic



if __name__ == '__main__':
    import numpy as np

    cut(np.zeros((10, 10)), 6, 6)
