# -*- coding: utf-8 -*-
"""
@author: msh
"""

from PIL.ImageDraw import Draw as PIDraw
from PIL.Image import new as PInew

from numpy import ogrid
from numpy import sqrt
from numpy import power
from numpy import asarray as ar
from numpy import logical_not

from . import ast


class Mask:
    """Mask class"""

    def __init__(self, logger):
        self.logger = logger
        self.ima = ast.Image(self.logger)

    def apply(self, data, mask, the_value=0, bkg=None):
        """Applies a mask to a given data"""
        try:
            self.logger.log("Applying mask")
            copy_od_data = data.copy()
            if bkg is not None:
                copy_od_data[mask] = bkg[mask]
            else:
                copy_od_data[mask] = the_value

            return copy_od_data
        except Exception as expt:
            self.logger.log(expt)


class Geometric(Mask):
    """Geometric mask generator"""

    def circular(self, shape, center=None, radius=None,
                 bigger=0, auto=min, rev=False):
        """Creates a circular mask"""
        self.logger.log("Creating circular mask")
        try:
            h, w = shape
            if center is None:
                center = [int(w / 2), int(h / 2)]

            if radius is None:
                radius = auto(center[0], center[1], w - center[0], h - center[1])

            Y, X = ogrid[:h, :w]
            dist_from_center = sqrt(
                power(X - center[0], 2) + power(Y - center[1], 2))

            the_mask = dist_from_center <= radius + bigger

            if rev:
                return logical_not(the_mask)
            else:
                return the_mask
        except Exception as expt:
            self.logger.log(expt)

    def polygon(self, shape, points, rev=False):
        """Creates a polygonal mask"""
        self.logger.log("Creating ploy mask")
        try:
            img = PInew('L', (shape[1], shape[0]), 0)
            PIDraw(img).polygon(points, outline=1, fill=1)
            mask = ar(img)
            the_mask = mask == 1

            if rev:
                return logical_not(the_mask)
            else:
                return the_mask
        except Exception as expt:
            self.logger.log(expt)
