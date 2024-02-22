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
    table_coords = SkyCoord(ra=table[ra_name]*u.degree, dec=table[dec_name]*u.degree, unit = (u.degree, u.degree))
    idx, sep, _ = target_coord.match_to_catalog_sky(table_coords)
    nearest_object = table.iloc[idx]
    return nearest_object


def remove_parentheses_and_brackets(s):
    """Removes any parts of a string that are inside parentheses or square brackets.

    Parameters:
    s (str): The input string.

    Returns:
    str: The input string with any parts inside parentheses or square brackets removed.

    Example:
    >>> remove_parentheses_and_brackets('Sersic index n (de Vaucouleurs n=4) [some notes]')
    'Sersic_index_n'
    """
    result = ''
    skip_parentheses = 0
    skip_brackets = 0
    for i in range(len(s)):
        if s[i] == '(':
            skip_parentheses += 1
        elif s[i] == ')':
            skip_parentheses -= 1
        elif s[i] == '[':
            skip_brackets += 1
        elif s[i] == ']':
            skip_brackets -= 1
        elif skip_parentheses == 0 and skip_brackets == 0:
            result += s[i]
    return result.strip().replace(" ", "_")

def clear_folder(folder_path):
    """
    Clears all files and folders inside a given folder.
    
    Args:
    - folder_path (str): The path of the folder to clear.
    """
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # If the folder doesn't exist, raise an error
        raise ValueError(f"The folder {folder_path} doesn't exist.")
    
    # Iterate over the contents of the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            # If the current item is a file, delete it
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # If the current item is a folder, clear it recursively
            elif os.path.isdir(file_path):
                clear_folder(file_path)
                os.rmdir(file_path)
        except Exception as e:
            # If there's an error deleting the file or folder, print a warning message
            print(f"Warning: Failed to delete {file_path}. Reason: {e}")
