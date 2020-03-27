# -*- coding: utf-8 -*-
"""
@author: msh
"""
from myLib import env
logger = env.Logger(blabla=True)

fop = env.File(logger)

import cv2
import numpy as np
from matplotlib import pyplot as plt

def edge_finder():
    img = cv2.imread('center.png',0)
    edges = cv2.Canny(img,100,200)
    xs, ys = np.where(edges>0)

    xs = xs.reshape((xs.size, 1))
    ys = ys.reshape((ys.size, 1))
    coordinates = np.hstack((ys, xs))

    print(coordinates)
    fop.save_numpy("coordinates.dat", coordinates)

def landolt_parser():
    with open("labdolt2use", "w") as f2w:
        with open("landolt", "r") as the_file:
            for line in the_file:
                the_line = line.strip()
                ln = the_line.split("\t")

                if ln[0] == "Star " and len(ln) == 18:
                    print(len(ln), the_line)
                    # f2w.write("{}\n".format(",".join(ln)))

if __name__ == "__main__":
    pass
