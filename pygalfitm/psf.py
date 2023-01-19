import numpy as np
from astropy.io import fits

def get_psf_data(filename):
    """Returns x0,y0 from image header"""
    hdulist = fits.open(filename)
    hdu = hdulist[0]
    
    ret = [None, None]
    for i in hdu.header:
        if 'FWHMMEAN' in i:
            ret[0] = hdu.header[i]
        if 'FWHMBETA' in i:
            ret[1] = hdu.header[i]
            
    hdulist.close()
    return tuple(ret)

def make_psf(filename, outfile=None, fwhm=None, beta=None, radius = 10):
    
    if not fwhm or beta:
        psf_data = get_psf_data(filename)
        fwhm = psf_data[0]
        beta = psf_data[1]

    fwhm = fwhm/0.5
    #beta = beta/0.5 
    alpha = fwhm / (2 * np.sqrt(np.power(2., 1/beta) - 1.))
    r = np.linspace(-radius, radius, 2 * radius + 1)
    X, Y = np.meshgrid(r, r)
    R = np.sqrt(X**2 + Y**2)
    I = (beta - 1.) / (np.pi * alpha**2) * \
        np.power(1. + np.power(R / alpha, 2), -beta)
    
    if outfile:
        hdu = fits.PrimaryHDU(I)
        hdulist = fits.HDUList([hdu])
        hdulist.writeto(outfile, overwrite=True)

    return I