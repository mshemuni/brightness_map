# -*- coding: utf-8 -*-
"""
@author: msh
"""
from myLib import env
from myLib import ast

logger = env.Logger(blabla=True, debugger=None)

if __name__ == "__main__":
    fts = ast.Fits(logger, "/home/msh/Documents/data/2017_07_04__22_40_29.fits.gz")
    img = ast.Image(logger)
    pho = ast.Photometry(logger)
    bkg = img.background(fts.data[0], bw=4)
    #img.show(bkg)
    ph = pho.mag(bkg, fts.header["EXPOSURE"])
    #print(ph.min())
    img.show_compair(bkg, ph , color1="Greys_r", color2="coolwarm_r")
