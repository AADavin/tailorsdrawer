#!/usr/bin/env python
"""
Taken from StackOverFlow, writen by enigmaticPhysicist
Adapted to download a World Map

Stitch together Google Maps images from lat, long coordinates
Based on work by heltonbiker and BenElgar
Changes:
* updated for Python 3
* added Google Maps API key (compliance with T&C, although can set to None)
* handle http request exceptions

With contributions from Eric Toombs.
Changes:
* Dramatically simplified the maths.
* Set a more reasonable default logo cutoff.
* Added global constants for logo cutoff and max image size.
* Translated a couple presumably Portuguese variable names to English.
"""

import requests
from io import BytesIO
from math import log, exp, tan, atan, ceil
from PIL import Image
import sys

# circumference/radius
tau = 6.283185307179586
# One degree in radians, i.e. in the units the machine uses to store angle,
# which is always radians. For converting to and from degrees. See code for
# usage demonstration.
DEGREE = tau/360

ZOOM_OFFSET = 8


with open("/Users/davin/Desktop/ETE/WorldMap/MapsAPI.txt") as f:
    GOOGLE_MAPS_API_KEY = f.readline().strip()

# Max width or height of a single image grabbed from Google.
MAXSIZE = 640
# For cutting off the logos at the bottom of each of the grabbed images.  The
# logo height in pixels is assumed to be less than this amount.
LOGO_CUTOFF = 60


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

    if True:

        # assemble the image from stitched
        final = Image.new('RGB', (int(dx), int(dy)))
        for x in range(cols):
            for y in range(rows):
                dxn = width * (0.5 + x)
                dyn = height * (0.5 + y)
                latn, lonn = pixels2latlon(
                        ulx + dxn, uly - dyn - LOGO_CUTOFF/2, zoom)
                position = ','.join((str(latn/DEGREE), str(lonn/DEGREE)))
                print(x, y, position)
                urlparams = {
                        'center': position,
                        'zoom': str(zoom),
                        'size': '%dx%d' % (width, heightplus),
                        'maptype': 'satellite',
                        'sensor': 'false',
                        'scale': 1
                    }
                if GOOGLE_MAPS_API_KEY is not None:
                    urlparams['key'] = GOOGLE_MAPS_API_KEY

                url = 'http://maps.google.com/maps/api/staticmap'
                try:
                    response = requests.get(url, params=urlparams)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(e)
                    sys.exit(1)

                im = Image.open(BytesIO(response.content))
                im.save("/Users/davin/Desktop/ETE/WorldMap/%s_%s.png" % (str(x), str(y)))
                final.paste(im, (int(x*width), int(y*height)))
        final.save("/Users/davin/Desktop/ETE/WorldMap/WholeMap.png")
        return final

############################################

if __name__ == '__main__':

    NW_lat_long = (85 * DEGREE, -180 * DEGREE)
    SE_lat_long = (-75 * DEGREE, 180 * DEGREE)

    #NW_lat_long = (-35 * DEGREE, 76*DEGREE)
    #SE_lat_long = (-75*DEGREE, 96*DEGREE)

    zoom = 7   # be careful not to get too many images!

    result = get_maps_image(NW_lat_long, SE_lat_long, zoom=zoom)
    #result.show()
