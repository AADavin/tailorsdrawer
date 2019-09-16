
import os
from math import log, exp, tan, atan, ceil
from PIL import Image


# circumference/radius
tau = 6.283185307179586
# One degree in radians, i.e. in the units the machine uses to store angle,
# which is always radians. For converting to and from degrees. See code for
# usage demonstration.
DEGREE = tau/360

ZOOM_OFFSET = 8


# Max width or height of a single image grabbed from Google.
MAXSIZE = 640
# For cutting off the logos at the bottom of each of the grabbed images.  The
# logo height in pixels is assumed to be less than this amount.
LOGO_CUTOFF = 50


def latlon2pixels(lat, lon, zoom):
    mx = lon
    my = log(tan((lat + tau/4)/2))
    res = 2**(zoom + ZOOM_OFFSET) / tau
    px = mx*res
    py = my*res
    return px, py

def pixels2latlon(px, py, zoom):
    res = 2**(zoom + ZOOM_OFFSET) / tau
    mx = px/res
    my = py/res
    lon = mx
    lat = 2*atan(exp(my)) - tau/4
    return lat, lon


def get_maps_image(NW_lat_long, SE_lat_long, zoom=18):

    ullat, ullon = NW_lat_long
    lrlat, lrlon = SE_lat_long

    # convert all these coordinates to pixels
    ulx, uly = latlon2pixels(ullat, ullon, zoom)
    lrx, lry = latlon2pixels(lrlat, lrlon, zoom)

    # calculate total pixel dimensions of final image
    dx, dy = lrx - ulx, uly - lry

    # calculate rows and columns
    cols, rows = ceil(dx/MAXSIZE), ceil(dy/MAXSIZE)

    # calculate pixel dimensions of each small image
    width = ceil(dx/cols)
    height = ceil(dy/rows)
    heightplus = height + LOGO_CUTOFF

    print(rows)
    print(cols)
    print(cols*rows)
    mpath = "/Users/davin/Desktop/ETE/WorldMap/"
    tiles = [x for x in os.listdir(mpath) if "png" in x and "Whole" not in x]

    print(len(tiles))

    print(dx)
    print(dy)

    # assemble the image from stitched
    final = Image.new('RGB', (int(dx), int(dy)))
    for x in range(50):
        for y in range(42):

            im = Image.open(os.path.join(mpath, "x_y.png".replace("x", str(x)).replace("y", str(y))))
            final.paste(im, (int(x*width), int(y*height)))
        #final.save("/Users/davin/Desktop/ETE/WorldMap/WholeMap2.png")


NW_lat_long = (85 * DEGREE, -180 * DEGREE)
SE_lat_long = (-75 * DEGREE, 180 * DEGREE)


get_maps_image(NW_lat_long, SE_lat_long, 7)
