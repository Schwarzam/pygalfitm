from astropy.io import fits
import requests
import os
import pygalfitm

from astropy.coordinates import SkyCoord
import astropy.units as u

def unpack_file(filename, output=None, output_folder=None, delete_compressed = False):
    import os
    """
    Funpack (uncompress) .fz file
    """

    if output_folder:
        output = os.path.join(output_folder, filename.replace('.fz', ''))
    elif not output:
        output = filename.replace('.fz', '')
        
    if delete_compressed:
        os.remove(filename)
    
    packed = fits.open(filename)
    unpacked = fits.hdu.image.PrimaryHDU(data = packed[1].data, header = packed[1].header)
    fits.hdu.hdulist.HDUList(hdus=[unpacked]).writeto(output, overwrite=True)

def string_times_x(string, x):
    res = ""
    for i in range(x): ## Use lambda instead
        res += "," + str(string) 
    return res[1: ]

def get_dims(filename):
    """Returns a tuple (width, height)"""
    hdulist = fits.open(filename)
    hdu = hdulist[0]
    ret = (hdu.header["NAXIS1"], hdu.header["NAXIS2"])
    hdulist.close()
    return ret

def get_exptime(filename):
    """Returns exposure-time from image header"""
    hdulist = fits.open(filename)
    hdu = hdulist[0]
    ret = hdu.header["EXPTIME"]
    hdulist.close()
    return ret




def check_vo_file(file, download_link):
    if not os.path.exists(os.path.join(pygalfitm.__path__[0], f'{file}')):
        print("Downloading " + file)
        r = requests.get(download_link)
        print("Writing " + os.path.join(pygalfitm.__path__[0], file))
        open(os.path.join(pygalfitm.__path__[0], file), "wb").write(r.content)
        print("Done!")


def find_nearest_object(table, ra, dec, ra_name = "ra", dec_name = "dec") :
    """
    Function to find the nearest object in a table based on Right Ascension and Declination.

    Parameters:
    table : pandas DataFrame
        DataFrame containing the table with objects.
    ra : float
        Right Ascension of the target position in degrees.
    dec : float
        Declination of the target position in degrees.

    Returns:
    nearest_object : pandas Series
        Series representing the nearest object in the table.
    """
    target_coord = SkyCoord(ra=ra*u.degree, dec=dec*u.degree)
    table_coords = SkyCoord(ra=table[ra_name]*u.degree, dec=table[dec_name]*u.degree)
    idx, sep, _ = target_coord.match_to_catalog_sky(table_coords)
    nearest_object = table.iloc[idx]
    return nearest_object
