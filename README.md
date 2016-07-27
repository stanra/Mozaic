
Reorganize the README :

Title
one sentence explanation
Longer description
use case
detail on how to use the package
detail about implemetation

# Mozaic

**Cut big pictures in small pieces and only load specific parts.**


Some applications need to load pieces of a bigger image.
One picture should fit into the user's memory, so if all the requested pieces are from one single picture, there is no problem
Even if there are many pictures, if you can load them all or correctly preload the ones that will be called it will be easier too.

But in some situations, you don't know at all what the requested image will be, and you can't load all the pictures.

And loading a *big* picture in memory, simply for using a small part of it is quite inefficient.

<br>

So instead, I suggest to use a **mozaic** !
You cut your big images into multiple tiles. A mozaic is simply a matrix of images.
The size and position of each tile is known, so instead of loading the whole picture, you simply load the tiles composing the image you requested and stitch them!

*Note : it is not guaranteed to be more efficient. Finding the tiles, loading them and stitching them may actually take more than simply loading a big picture, especially if the tiles are too small compared to the image requested.*
*But if you know in advance the application and can chose a good size for the tiles, I think it should be a bit faster*


< find and describe some possible use case : houses on a map, stars, etc...>

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

### Cut

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
We know that at worst `p` will be equal to `frac`, since ```ratio = frac / num```

Depending on the size of the picture and the number of tiles, `p` can still be quite big. Then when finding a window, we may want to use the actual size of the tiles.
That makes lots of unnecessary computations. If `p` is small enough, and the requested images too, then we don't need to correct at all, and can directly consider the tiles have the *expected size*

### stitch

We want to find the position x. We know that for every `q` pictures, the size average of the windows is exact (with an accumulated error < 1, so it disappears when taking floor.

The expected 'real' tile-position of the point x is ` x / avg `, where `avg = total size / num of tiles` .
So, if all the tiles had the expected size, the the point x would be in `ix = int(x/avg)`

The real position of the beginning of the tile `ix` is `pos' = (ix // q) * avg + (tile_size+1) * min(p,p') + max(p'-p,0)*tile_size`
so the error is `err = pos'-x` .

If `err > 0` then the chosen tile is actually after so we should choose a smaller `ix` and compute the error again
If `err < 0` and `abs(err) > tile_size` then the chosen `ix` is too small, and x is actually in the next tile. So we chose `ix+=1` and compute the error again
If `err < 0` and `abs(err) < tile_size` then it's ok

We need to do this for the starting and the finishing tile. Using the size instead of the finishing tile is a bad idea because the counting doesn't start at a complete cycle.

> Note : could (should?) use the actual size average on one cycle instead of `avg`

> Note : Should first implement the 'optimist' method and the 'correct' one separately, but there are actually many common points.

> Note : Depending on the choice of the ratio, we might have to compute again once or many times. But I am confident that it will never be needed to loop too long
> In particular, it is sure that the number of iteration needed is lower than if we naively looped over all tiles position until we find the one containing x (proof ?)

Note :

1. for the wished precision of the fraction, what I do now is 1/total num of pictures
If I want the total accumulated error on the fraction to be 1 at most, then I want an error of `1/number of cycle`, with `number of cycle = `num of tiles // q` (`q` is still the length of one cycle)
It gives me a higer tolearance for the fraction, wich should give smaller fractions and therefore a more balanced . And it also ensure that the error due to fraction error is less than one at any time, so it will not influence the integer position.
Another solution to have even higher tolerance for the fraction would be to have an error < 1 for each cycle! But that would require to be more careful, since the accumulated error can get quite big. So when stitching, we would have to take it into account.

2. Currently, my lowest fraction tries to have the smallest `p` as possible. I actually want the smallest cycle possible, so I should rather get the smallest `q` as possible. Most of the time (all the time ?) it will give the same result.



Note :

Cool stuff to try :

* Depending on hardware, could gain a lot by parallelism
* Implementations in C++,
* CLI interface
* Libraries interfaces
* Server/Client architecture to easily provide cross language interface
* functional implementation in Haskell
* implementation in Go (concurrent, goroutines)

* Automatic 'clever' grid (seems too hard for not so much improvement ?)
*