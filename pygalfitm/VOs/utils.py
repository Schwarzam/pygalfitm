import numpy as np
from astropy.io import fits
from collections import OrderedDict
import glob
import os
import re
import multiprocessing as mp


def onlypos(x):
    if x > 0:
        return x
    else:
        return 0
    
# [1 / x if x != 0 else 0 for x in INPUT_weight]
def create_rms(x):
    if x != 0:
        return 1 / x
    else:
        return 0

def write_fits_content_firsthdu(f, filename, remove_negatives=True):
    """
    Write the content of the first HDU of a FITS file to a new file.

    Parameters:
    - f: `astropy.io.fits.HDUList` object representing the FITS file.
    - filename: Name of the output file to write the content to.
    - remove_negatives: Boolean indicating whether to remove negative values from the data. Default is True.

    Returns:
    None
    """
    ## This is needed because splus API provides fpacked compressed images,
    ## and pygalfitm does not support them, so we unpack them here
    unpacked = fits.hdu.image.PrimaryHDU(data=f[1].data, header=f[1].header)
    if remove_negatives:
        unpacked.data = unpacked.data.clip(min=0)
    fits.hdu.hdulist.HDUList(hdus=[unpacked]).writeto(filename, overwrite=True)


def create_sigma_image(weight_data, fits_data, out_filename):
    """
    Create a sigma image by combining weight data and FITS data.

    Parameters:
    weight_data (array-like): The weight data.
    fits_data (array-like): The FITS data.
    out_filename (str): The filename to save the sigma image.

    Returns:
    str: The filename of the saved sigma image.
    """
    # Invert each pixel in weight data
    vector_rms = np.vectorize(create_rms)
    RMS = vector_rms(weight_data)
    
    # Apply only positive function element-wise to the FITS data
    vector_onlypos = np.vectorize(onlypos)
    IM = vector_onlypos(fits_data)
    
    # Calculate Sigma and save to new FITS files
    SIGMA = np.sqrt(np.square(RMS) + IM)
    hdu_sigma = fits.PrimaryHDU(SIGMA)
    hdu_sigma.writeto(out_filename, overwrite=True)
    return out_filename

def create_rms_image(weight_data, out_filename):
    """
    Create an RMS image from the given weight data and save it to the specified output file.

    Parameters:
    weight_data (list): A list of weight data values.
    out_filename (str): The path to the output file where the RMS image will be saved.

    Returns:
    str: The path to the saved RMS image file.
    """
    # Invert each pixel in weight data
    vector_rms = np.vectorize(create_rms)
    RMS = vector_rms(weight_data)
    
    hdu_rms = fits.PrimaryHDU(RMS)
    hdu_rms.writeto(out_filename, overwrite=True)
    return out_filename

