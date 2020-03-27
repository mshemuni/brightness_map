# -*- coding: utf-8 -*-
"""
@author: msh
"""
from numpy import mean, std

from myLib import env
from myLib import ast
from myLib import mask

from numpy import array as nar, where
from numpy import median

from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

logger = env.Logger(blabla=True, debugger=None)

img = ast.Image(logger)
geometric_mask = mask.Geometric(logger)
pho = ast.Photometry(logger)
fop = env.File(logger)

cdict = {'red': ((0.0, 1.0, 1.0),
                 (0.1, 1.0, 1.0),  # red
                 (0.4, 1.0, 1.0),  # violet
                 (1.0, 0.0, 0.0)),  # blue

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue': ((0.0, 0.0, 0.0),
                  (0.1, 0.0, 0.0),  # red
                  (0.4, 1.0, 1.0),  # violet
                  (1.0, 1.0, 0.0))  # blue
         }
my_color_map = LinearSegmentedColormap('BlueRed1', cdict)

def combine_data(path, what_to_du="NONE"):
    files = fop.list_in_path(path)
    fts = ast.Fits(logger, fop.abs_path(files[0]))
    ret_image = []
    for it, file in enumerate(files, start=1):
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

    fop.save_numpy("{}.img".format(what_to_du), image2write)

def combine_data_bkg(path, what_to_du="NONE"):
    files = fop.list_in_path(path)
    fts = ast.Fits(logger, fop.abs_path(files[0]))
    ret_image = []
    for it, file in enumerate(files, start=1):
        try:
            fts = ast.Fits(logger, fop.abs_path(file))
            if "MAG" == what_to_du.upper():
                ret_image.append(img.background(pho.mag(fts.data[0], 1), bw=32))
            else:
                ret_image.append(img.background(fts.data[0], bw=32))
            logger.log(it)
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            logger.log(e)

    ret_image = nar(ret_image)
    image2write = median(ret_image, axis=0)

    fop.save_numpy("{}_BKG.img".format(what_to_du), image2write)


def show(flux, mag, cm="Greys"):
    flux_data = fop.read_array(flux)
    mag_data = fop.read_array(mag)

    mask_coorinates = tuple(map(tuple, fop.read_array("coordinates.dat")))

    mask = geometric_mask.polygon(flux_data.shape, mask_coorinates, rev=True)
    mask_rev = geometric_mask.polygon(flux_data.shape, mask_coorinates, rev=False)

    use_flux_data = geometric_mask.apply(flux_data, mask, the_value=None)
    use_mag_data = geometric_mask.apply(mag_data, mask, the_value=None)


    for i in range(100):
        logger.log("iteration {}".format(i))
        mask[use_mag_data==use_mag_data[mask_rev].min()] = True
        mask_rev[use_mag_data==use_mag_data[mask_rev].min()] = False

        # mask[use_mag_data < 16] = True
        # mask_rev[use_mag_data < 16] = False

        use_flux_data = geometric_mask.apply(flux_data, mask, the_value=None)
        use_mag_data = geometric_mask.apply(mag_data, mask, the_value=None)

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

    ax1.axis('off')
    # vmin=use_data[mask].min(), vmax=use_data[mask].max()

    m, s = mean(use_flux_data[mask_rev]), std(use_flux_data[mask_rev])
    subplot1 = ax1.imshow(use_flux_data, vmin=m - s, vmax=m + s,
                          cmap="Greys_r", interpolation='nearest', origin='lower')
    ax1.set_title('FLUX')
    plt.colorbar(subplot1, ax=ax1, orientation='horizontal')

    ax2.axis('off')
    subplot2 = ax2.imshow(use_mag_data, vmin=use_mag_data[mask_rev].min(), vmax=use_mag_data[mask_rev].max(),
                          cmap=my_color_map, interpolation='nearest', origin='lower')
    ax2.set_title('MAG')
    plt.colorbar(subplot2, ax=ax2, orientation='horizontal')
    plt.tight_layout()
    plt.show()

def show_bkg(flux, mag, cm="Greys"):
    flux_data = fop.read_array(flux)
    mag_data = fop.read_array(mag)

    mask_coorinates = tuple(map(tuple, fop.read_array("coordinates.dat")))

    mask = geometric_mask.polygon(flux_data.shape, mask_coorinates, rev=True)
    mask_rev = geometric_mask.polygon(flux_data.shape, mask_coorinates, rev=False)

    use_flux_data = geometric_mask.apply(flux_data, mask, the_value=None)
    use_mag_data = geometric_mask.apply(mag_data, mask, the_value=None)

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

    ax1.axis('off')
    # vmin=use_data[mask].min(), vmax=use_data[mask].max()

    m, s = mean(use_flux_data[mask_rev]), std(use_flux_data[mask_rev])
    subplot1 = ax1.imshow(use_flux_data, vmin=m - s, vmax=m + s,
                          cmap="Greys_r", interpolation='nearest', origin='lower')
    ax1.set_title('FLUX')
    plt.colorbar(subplot1, ax=ax1, orientation='horizontal')

    ax2.axis('off')
    subplot2 = ax2.imshow(use_mag_data, vmin=use_mag_data[mask_rev].min(), vmax=use_mag_data[mask_rev].max(),
                          cmap=my_color_map, interpolation='nearest', origin='lower')
    ax2.set_title('MAG')
    plt.colorbar(subplot2, ax=ax2, orientation='horizontal')
    plt.tight_layout()
    plt.show()


def image(file):
    fts = ast.Fits(logger, fop.abs_path(file))

    mag = pho.mag(fts.data[0], 1)

    mask = geometric_mask.circular(fts.data[0].shape, rev=True)
    mask_rev = geometric_mask.circular(fts.data[0].shape, rev=False)

    use_data = geometric_mask.apply(fts.data[0], mask, the_value=None)
    use_mag = geometric_mask.apply(mag, mask, the_value=None)

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

    ax1.axis('off')
    # vmin=use_data[mask].min(), vmax=use_data[mask].max()

    m, s = mean(use_data[mask_rev]), std(use_data[mask_rev])
    subplot1 = ax1.imshow(use_data, vmin=m - s, vmax=m + s,
                          cmap="Greys_r", interpolation='nearest', origin='lower')
    ax1.set_title('FLUX')
    plt.colorbar(subplot1, ax=ax1, orientation='horizontal')

    ax2.axis('off')
    subplot2 = ax2.imshow(use_mag, vmin=use_mag[mask_rev].min(), vmax=use_mag[mask_rev].max(),
                          cmap=my_color_map, interpolation='nearest', origin='lower')
    ax2.set_title('MAG')
    plt.colorbar(subplot2, ax=ax2, orientation='horizontal')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # combine_data("/home/msh/Documents/data/2020*.fits.bz2", what_to_du="MAG")
    # combine_data_bkg("/home/msh/Documents/data/2020*.fits.bz2", what_to_du="FLUX")
    # show("data/FLUX.img", "data/MAG.img")
    show_bkg("data/FLUX_BKG.img", "data/MAG_BKG.img")
    # image("/home/msh/Documents/data/2020_03_23__21_16_35.fits.bz2")
    pass
