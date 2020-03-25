# -*- coding: utf-8 -*-
"""
@author: msh
"""
from myLib import env
from myLib import ast
from myLib import mask

logger = env.Logger(blabla=True, debugger=None)

if __name__ == "__main__":
    fts = ast.Fits(logger, "/home/msh/Documents/data/2017_07_04__22_40_29.fits.gz")
    img = ast.Image(logger)
    geometric_mask = mask.Geometric(logger)
    pho = ast.Photometry(logger)

    the_mask = geometric_mask.circular(fts.data[0].shape, rev=True)
    masked_data = geometric_mask.apply(fts.data[0], the_mask)
    img.show(masked_data)
    bkg = img.background(masked_data, bw=16)
    # img.show(bkg)
    ph = pho.mag(bkg, fts.header["EXPOSURE"])
    print(ph.min())
    img.show_compair(geometric_mask.apply(bkg, the_mask),
                     geometric_mask.apply(ph, the_mask),
                     color1="Greys_r", color2="coolwarm_r")
