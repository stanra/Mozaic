# Mozaic

**Cut big pictures in small pieces and only load specific parts.**


Some applications need to load pieces of a bigger image.
One picture should fit into the user's memory, so if all the requested pieces are from one single picture, there is no problem
Even if there are many pictures, if you can load them all or correctly preload the ones that will be called it will be easier too.

But in some situations, you don't know at all what the requested image will be, and you can't load all the pictures.

And loading a *big* picture in memory, simply for using a small part of it is quite inefficient.

<br>

So instead, I propose to use a **mozaic** !
You cut your big images into multiple tiles. A mozaic is simply a matrix of images.
The size and position of each tile is known, so instead of loading the whole picture, you simply load the tiles composing the image you requested and stitch them!

*Note : it is not guaranteed to be more efficient. Finding the tiles, loading them and stitching them may actually take more than simply loading a big picture, especially if the tiles are too small compared to the image requested.*
*But if you know in advance the application and can chose a good size for the tiles, I think it should be a bit faster*


# Some details

## Format

One picture is transformed into a folder containing the number of requested tiles, and a file `mozaic.info` containing the folowing information :

 * Original name of the picture (which should also be the name of the folder)
 * Format of the tiles (NOTE : Not sure it is any useful)
 * Original size
 * Mozaic size ( = the number of pictures, i.e. the *shape* of the mozaic)
 * base tile size ( it may be original size divided by number of pictures, but the size can only be an integer! So the base size is the floor of the expected size)
 * repartition, given as p/q ( since the base size is smaller than the real expected size, we need to correct it. Therefore p out of q images have the size (base size + 1).
 Some error might get propagated (a most, the offset will be p).
In most cases, it p might be small enough compared to the tiles' size, so we don't really care.

## Explanation

We can't just cut pixels, so the size of the tiles must be an Integer.
Because of that, we can't simply use the *expected size* ( = *original size* / *number of tiles* ).
So we use the floor of this expected size as the base size for the tiles.
We still want to have an *average size* equal to the *expected size*
Therefore, a portion of the tiles will have the sixe *base size* + 1.

*Note : Another solution would simply be to let the last image be significantly bigger than the others*

If we choose that `p` tiles have the size *base size* + 1 and `r` have the size *base size*, we can't just let the p first tiles to be the bigger ones.
If we do so, the propagated error will be quite important ! The tiles will have a strong offset that will have to be corrected.
So we want to find a better way to alternate between *big* and *small* images.
The last picture may need to correct a bit the size.

Note : There are other ways to handle this issue :

* keep all the pictures the same size (smaller than expected) and simply let the last one be bigger.
* keep all the pictures the same size (bigger than expected) and let the last image be smaller, or disappear if too small (bad solution imo)
* Do not care about having unbalanced repartition of bigger/smaller pictures.
* could have an alternance of alternance (just like the bissextil system) to ensure the lowest possible cumulated error at any time.
* The acceptable size error for the last picture may be a parameter

Some of them are as valid as the one I choose, and might be slightly better in some cases so I might implement them as well, and let the user choose.
Mine is probably one of the most complex to implement, and not the best choice if we want to correct the error while finding the tiles composing the requested window

Depending on the max offset, the size of the tiles and the expected size of the requested image, we may of may not need active correction. Based on this, it is possible for the user to make the best choice regarding the way the tile size error should be handled.
It also depends if the number of image is important, or if it is important or not that the images have all similar size.


## How is it done

We want `num` tiles of size `size`.
Actually, we want the tiles to have integer size with the average equal to `size`.
So we want `frac` images of size ```isize + 1``` and ```num - frac``` images of size ```isize```, with ```isize = floor(size)```.
`frac` is such that ``` frac *(isize + 1) + (num - frac) * isize = size * num```
So we have ```frac = num * (size - isize)

We can simply let the `frac` first pictures to be of size ```isize + 1 ```. But instead, let's find a good balanced reparition.

We have ```ratio = size - isize``` where `ratio` is the ratio of images ```isize + 1 ```
We want to find `p` and `q` such that ```p / q = ratio``` and `p` and `q` are as small as possible.
We let the precision of the ratio be `eps`
For example, if we want the accumulated error on the ratio at the last image to be 1 or less, the ```eps = 1/num```
To find p and q, we simply choose p as low as possible (start with 1 and then raise), find the best q, and compute the error.


Depending on the size of the picture and the number of tiles, `p` can still be quite big. Then when finding a window, we may want to use the actual size of the tiles.
That makes lots of unnecessary computations. If `p` is small enough, and the requested images too, then we don't need to correct at all, and can directly consider the tiles have the *expected size*

