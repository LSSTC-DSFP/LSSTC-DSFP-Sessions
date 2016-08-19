import numpy as np

#
# Names of mask planes
#
maskPlanes = dict(
    BAD =      np.uint16(1 << 0),
    SATUR =    np.uint16(1 << 1),
    INTRP =    np.uint16(1 << 2),
    CR =       np.uint16(1 << 3),
    EDGE =     np.uint16(1 << 4),
    DETECTED = np.uint16(1 << 5),
    )

def setPixels(da, x, y, good):
    """Fix bad pixels in image.  The pixels are specified by (x, y); x[good] are good and the others are bad

    Well, we don't actually fix them, but set them to 1e6
    """
    bad = np.logical_not(good)

    da.image[y, x[bad]] = 1e6 + 0*x[bad]

def fixDefects(da, hlen=5, interpFunc=setPixels,
               badMask=maskPlanes["BAD"]|maskPlanes["SATUR"]|maskPlanes["CR"],
               verbose=False):
    """
    Fix the defects (as defined by the badMask) in an image

    The actual work is done by calling interpFunction(da, x, y, good) (see setPixels for details)
    """
    nx, ny = da.image.shape

    x = np.arange(0, nx)
    for y in range(ny):
        if verbose:
            print "%d\r" % y,; sys.stdout.flush()
        
        bad = (da.mask[y, x] & badMask) != 0
        xbad = x[bad]
        if len(xbad) == 0:
            continue

        i = 0
        while i < len(xbad):
            x0 = xbad[i]; i += 1
            while i < len(xbad) and xbad[i] == xbad[i - 1] + 1:
                i += 1

            x1 = xbad[i - 1]

            xstart = x0 - hlen
            if xstart < 0:
                xstart = 0
            xend = x1 + hlen
            if xend >= nx:
                xend = nx - 1

            xind = np.arange(xstart, xend + 1)
            good = np.logical_or(xind < x0, xind > x1)
            good = np.logical_and(good, (da.mask[y, xind] & badMask) == 0x0)

            interpFunc(da, xind, y, good)

    if verbose:
        print ""
