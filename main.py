# -*- coding: utf-8 -*-
"""
@author: msh
"""
from numpy import mean, std

from myLib import env
from myLib import ast
from myLib import mask

from numpy import array as nar
from numpy import median

from matplotlib import pyplot as plt

logger = env.Logger(blabla=True, debugger=None)

img = ast.Image(logger)
geometric_mask = mask.Geometric(logger)
pho = ast.Photometry(logger)
fop = env.File(logger)


def combine_data(path, what_to_du="NONE"):
    files = fop.list_in_path(path)
    fts = ast.Fits(logger, fop.abs_path(files[0]))
    ret_image = []
    for it, file in enumerate(files[0:80:5], start=1):
        try:
            fts = ast.Fits(logger, fop.abs_path(file))
            if "MAG" == what_to_du.upper():
                ret_image.append(pho.mag(fts.data[0], 1))
            else:
                ret_image.append(fts.data[0])
            logger.log(it)
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            logger.log(e)

    ret_image = nar(ret_image)
    image2write = median(ret_image, axis=0)

    fop.save_numpy("E:/dt/{}.img".format(what_to_du), image2write)


def show(path, cm="Greys"):
    data = fop.read_array(path)

    mask = geometric_mask.circular(data.shape, rev=True)
    use_data = geometric_mask.apply(data, mask, the_value=None)

    m, s = mean(use_data), std(use_data)
    plt.title("The Image")
    plt.imshow(use_data, cmap=cm, interpolation='nearest', vmin=data[mask].min(), vmax=data[mask].max(), origin='lower')
    plt.axis("off")

    plt.colorbar()
    plt.show()


def image(file):
    fts = ast.Fits(logger, fop.abs_path(file))

    mag = pho.mag(fts.data[0], 1)

    mask = geometric_mask.circular(fts.data[0].shape, rev=True)

    use_data = geometric_mask.apply(fts.data[0], mask, the_value=None)
    use_mag = geometric_mask.apply(mag, mask, the_value=None)

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

    ax1.axis('off')
    ax1.imshow(use_data, cmap="Greys_r", interpolation='nearest', origin='lower')
    ax1.set_title('FLUX')

    ax2.axis('off')
    ax2.imshow(use_mag, cmap="Greys", interpolation='nearest', origin='lower')
    ax2.set_title('MAG')
    plt.show()


if __name__ == "__main__":
    # combine_data("E:/asc/2020-03-23/*.bz2", what_to_du="MAG")
    # show("E:/dt/FLUX.img", cm="Greys_r")
    image("E:/asc/2020-03-23/2020_03_23__22_05_15.fits.bz2")
    pass
