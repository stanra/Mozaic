import numpy as np


def cut(picture, div_x, div_y):
    x_len, y_len = picture.shape()
    size_x, size_y = x_len / div_x, y_len / div_y
    frac_x, frac_y = (size_x - int(size_x)), (size_y - int(size_y))  # every 1/frac_ pictures should have size_ +1
    ratio_x, ratio_y = round(1.0/frac_x), round(1.0/frac_y)
    
    mozaic = {}
    curr_x = 0
    for ix in range(size_x):
      x_adjust = 1 if ix mod ratio_x == 0 else 0
      real_size_x = size_x + x_adjust
      end_x = curr_x + real_size_x
      curr_y = 0
      for iy in range(size_y):
        y_adjust = 1 if ix mod ratio_x == 0 else 0
        real_size_y = size_y + y_adjust
        end_y = curr_y + real_size_y
        
        mozaic['{}-{}'.format(ix,iy)] = ( (curr_x, curr_y), (end_x, end_y) )
        
        curr_y = end_y 
      curr_x = end_x
        
        
  # TODO : Need to shorten or extend the last picure because of imprecisions !
  
  
