from astropy.io import fits
import requests
import os
import pygalfitm

from astropy.coordinates import SkyCoord
import astropy.units as u

def unpack_file(filename, output=None, output_folder=None, delete_compressed=False):
    """
    Uncompresses an input .fz file and writes the uncompressed data to a new file.

    Args:
        filename (str): Name of the input .fz file.
        output (str, optional): Name of the output file. If not provided, the output file will be named using the
            input filename with the .fz extension removed.
        output_folder (str, optional): Name of the folder to write the output file to. If not provided, the output file
            will be written to the same folder as the input file.
        delete_compressed (bool, optional): If True, the input file will be deleted after it has been uncompressed.

    Returns:
        None.

    Raises:
        FileNotFoundError: If the input file cannot be found.
        OSError: If the output file cannot be written.

    """

    if not os.path.exists(filename):
        raise FileNotFoundError(f"The input file {filename} cannot be found.")

    if output_folder:
        output = os.path.join(output_folder, filename.replace('.fz', ''))
    elif not output:
        output = filename.replace('.fz', '')

    packed = fits.open(filename)
    unpacked = fits.hdu.image.PrimaryHDU(data=packed[1].data, header=packed[1].header)
    fits.hdu.hdulist.HDUList(hdus=[unpacked]).writeto(output, overwrite=True)

    if delete_compressed:
        os.remove(filename)


def string_times_x(string, x):
    """
    Returns a string that consists of `string` repeated `x` times, separated by commas.

    Args:
        string (str): The string to be repeated.
        x (int): The number of times to repeat `string`.

    Returns:
        str: A string that consists of `string` repeated `x` times, separated by commas.

    """
    res = ""
    for i in range(x):
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
    """
    Checks if a file required for the pygalfitm package is available. If the file is not present, the function downloads
    it from a provided URL and saves it in the pygalfitm directory.

    Args:
        file (str): Name of the file to check.
        download_link (str): URL where the file can be downloaded from.

    Returns:
        None.

    Raises:
        requests.exceptions.RequestException: If there was an error downloading the file.
        IOError: If the file cannot be written.

    """
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
