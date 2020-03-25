# -*- coding: utf-8 -*-
"""
@author: msh
"""
from astropy.io import fits as fts
from matplotlib import pyplot as plt

from numpy import array as nar
from numpy import dstack, mean, std, log10

from skimage.color import rgb2gray as r2g

from sep import Background


class Fits:
    def __init__(self, logger, file, method="readonly"):
        self.logger = logger
        self.file = file
        self.open_method = method
        self.hdu = fts.open(self.file, self.open_method)

    @property
    def data(self):
        try:
            return self.hdu[0].data.astype(float)
        except Exception as expt:
            self.logger.log(expt)
    @property
    def header(self):
        try:
            ret = {}
            for key, header in self.hdu[0].header.items():
                ret[key] = header
            return ret
        except Exception as expt:
            self.logger.log(expt)


class Photometry:
    def __init__(self, logger):
        self.logger = logger

    def mag(self, data, expt, ZMag=25):
        try:
            data[data<=0] = 1
            print(data.min())
            return -2.5 * log10(data/expt) + ZMag
        except Exception as expt:
            self.logger.log(expt)


class Image:
    def __init__(self, logger):
        self.logger = logger

    def array2rgb(self, array):
        try:
            return dstack((array[0], array[1], array[2]))
        except Exception as expt:
            self.logger.log(expt)

    def background(self, data, bw=16, as_array=True):
        try:
            if len(data.shape) == 2:
                if as_array:
                    return nar(Background(data, bw=bw))

                return Background(self.data)
            else:
                self.logger.log("Bad dimensioned data")
        except Exception as expt:
            self.logger.log(expt)

    def normalize(self, array, lindex=0):
        try:
            ret = []
            the_max = array.max()
            the_min = array.min()
            for layer in range(array.shape[lindex]):
                if lindex == 0:
                    the_array = array[layer]
                elif lindex == 1:
                    the_array = array[:, layer, :]
                elif lindex == 2:
                    the_array = array[:, :, layer]
                else:
                    break
                new_layer = (the_array - the_min) / (the_max - the_min)
                ret.append(new_layer)

            ret = nar(ret)
            return ret
        except Exception as expt:
            self.logger.log(expt)

    def rgb2gray(self, rgb_data):
        try:
            return r2g(rgb_data)
        except Exception as expt:
            self.logger.log(expt)

    def show(self, data, grayscaled=True, color="Greys"):
        try:
            if len(data.shape) == 2:
                self.logger.log("A 2D Image")
                m, s = mean(data), std(data)
                plt.title("The Image")
                plt.imshow(data, cmap=color, interpolation='nearest', vmin=m - s, vmax=m + s, origin='lower')
                plt.show()

            elif len(data.shape) == 3:
                rgb = self.array2rgb(data)
                if grayscaled:
                    self.logger.log("Grayscale 3D Image")
                    grays = self.rgb2gray(rgb)
                    m, s = mean(grays), std(grays)
                    plt.title("The Image")
                    plt.imshow(grays, cmap=color, interpolation='nearest', vmin=m - s, vmax=m + s, origin='lower')
                    plt.show()
                else:
                    self.logger.log("Show Colored")
                    plt.title("The Image")
                    plt.imshow(self.normalize(rgb))
                    plt.show()
            else:
                self.logger.log("Bad dimensioned data")

        except Exception as expt:
            self.logger.log(expt)

    def show_compair(self, data, other, grayscaled1=True, grayscaled2=True, color1="Greys", color2="Greys"):
        try:
            _, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)
            ax1.axis('off')
            ax2.axis('off')

            if len(data.shape) == 2:
                self.logger.log("A 2D Image")
                m, s = mean(data), std(data)
                ax1.imshow(data, cmap=color1, interpolation='nearest', vmin=m - s, vmax=m + s, origin='lower')

            elif len(data.shape) == 3:
                rgb = self.array2rgb(data)
                if grayscaled1:
                    self.logger.log("Grayscale 3D Image")
                    grays = self.rgb2gray(rgb)
                    m, s = mean(grays), std(grays)
                    ax1.imshow(grays, cmap=color1, interpolation='nearest', vmin=m - s, vmax=m + s, origin='lower')

                else:
                    self.logger.log("Show Colored")
                    ax1.imshow(self.normalize(rgb))

            if len(other.shape) == 2:
                self.logger.log("A 2D Image")
                m, s = mean(other), std(other)
                ax2.imshow(other, cmap=color2, interpolation='nearest', vmin=m - s, vmax=m + s, origin='lower')

            elif len(other.shape) == 3:
                other_rgb = self.array2rgb(other)
                if grayscaled2:
                    self.logger.log("Grayscale 3D Image")
                    other_grays = self.rgb2gray(other_rgb)
                    m, s = mean(other_grays), std(grays)
                    ax2.imshow(other_grays, cmap=color2, interpolation='nearest', vmin=m - s, vmax=m + s, origin='lower')

                else:
                    self.logger.log("Show Colored")
                    ax2.imshow(self.normalize(other_rgb))

            else:
                self.logger.log("Bad dimensioned data")

            plt.show()

        except Exception as expt:
            self.logger.log(expt)
