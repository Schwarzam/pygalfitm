import numpy as np
from astropy.io import fits

def get_psf_data(filename):
    """
    Retrieves FWHM and beta parameters from the header of an input FITS file.

    Args:
        filename (str): Name of the input FITS file.

    Returns:
        Tuple[float, float]: A tuple containing the FWHM and beta parameters.

    Raises:
        IOError: If the input file cannot be read.

    """
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



def make_psf(filename, outfile=None, fwhm=None, beta=None, radius=10):
    """
    Creates a 2D point spread function (PSF) using the Moffat function.

    Args:
        filename (str): Name of the input file.
        outfile (str, optional): Name of the output file. Default is None.
        fwhm (float, optional): Full width at half maximum (FWHM) of the PSF. If not provided, it will be retrieved from the input file. Default is None.
        beta (float, optional): Beta parameter of the PSF. If not provided, it will be retrieved from the input file. Default is None.
        radius (int, optional): Radius of the PSF in pixels. Default is 10.

    Returns:
        numpy.ndarray: Array containing the 2D PSF.

    Raises:
        IOError: If the input file cannot be read.

    """
    if not fwhm or beta:
        psf_data = get_psf_data(filename)
        fwhm = psf_data[0]
        beta = psf_data[1]

    fwhm = fwhm/0.5
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



