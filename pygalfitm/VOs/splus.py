from astropy.io.fits import getheader
from astropy.io import fits

import pygalfitm
from pygalfitm import PyGalfitm
from pygalfitm.auxiliars import string_times_x, get_dims, get_exptime, unpack_file, check_vo_file, find_nearest_object
from pygalfitm.psf import make_psf

import pandas as pd
import numpy as np
import os


def get_splus_class(name, ra, dec, cut_size, data_folder, output_folder, conn, remove_negatives=True, bands = ["I", "R", "G"], zpfile = None,
    SPLUS_WAVELENGHTS = {
            "i": 7670.59, 
            "r": 6251.83, 
            "g": 4758.49, 
            "z": 8936.64,
            "u": 3533.29, 
            "J0378": 3773.13, 
            "J0395": 3940.70, 
            "J0410": 4095.27, 
            "J0430": 4292.39,
            "J0515": 5133.15,
            "J0660": 6613.88,
            "J0861": 8607.59
    }, 
    conv_box_const = 60,
    **kwargs):
    """Function to get splus data and process it with galfitm
    You may copy this code and adapt it to your needs

    Args:
        name (str): file base name, this will be used in all files produced
        ra (float): right ascension deg, center of image
        dec (float): declination deg, center of image
        cut_size (int): image size
        data_folder (str): folder path to save downloaded images to process
        output_folder (_type_): folder with galfitm outputs
        conn (splusdata.connect): splusdata logged in connection
        remove_negatives (bool): Removes negatives values from images downloaded
        bands (list, optional): splus bands. Defaults to ["I", "R", "G"].
        zpfile (str, optional): path to zeropoint file, if None it will automatically download it. Defaults to None.
        SPLUS_WAVELENGHTS (dict, optional): SPLUS wavelenghts. Defaults to { "i": 7670.59, "r": 6251.83, "g": 4758.49, "z": 8936.64, "u": 3533.29, "J0378": 3773.13, "J0395": 3940.70, "J0410": 4095.27, "J0430": 4292.39, "J0515": 5133.15, "J0660": 6613.88, "J0861": 8607.59 }.
        conv_box_const (int, optional): convolution box size. Defaults to 60.
    Returns:
        (pygalfitm.Pygalfitm) : Pygalfitm class with splus values. 
    """    

    ##Get wavelenghts, input_images, psf_images, filters, zps
    wavelenghts = ""
    input_images = ""
    psf_images = ""
    filters = ""
    zps = ""

    fwhmmeans = []
    conv_boxes = ""

    for band in bands:
        band = band.lower()
        try:
            f = conn.get_cut(ra, dec, cut_size, band.replace("j0", "f").upper())
            unpacked = fits.hdu.image.PrimaryHDU(data = f[1].data, header = f[1].header)
            if remove_negatives:
                unpacked.data = unpacked.data.clip(min=0)
            fits.hdu.hdulist.HDUList(hdus=[unpacked]).writeto(os.path.join(data_folder, f'{name}_{band.lower()}.fits'), overwrite=True)    
        
        except Exception as e:
            print(e)
        
        make_psf(os.path.join(data_folder, f'{name}_{band.lower()}.fits'), outfile=os.path.join(data_folder, f'psf_{name}_{band.lower()}.fits'))
        
        im_name = os.path.join(data_folder, f'{name}_{band.lower()}.fits')
        input_images += "," + im_name
        psf_images += "," + os.path.join(data_folder, f'psf_{name}_{band.lower()}.fits')
        filters += "," + str(band).lower()
        wavelenghts += "," + str(SPLUS_WAVELENGHTS[band.lower().lower().replace("f", "J0").replace("j0", "J0")])
        
        im_header = getheader(im_name)
        for key in im_header:
            if "FWHMMEAN" in key:
                fwhmmeans.append(im_header[key])

    fwhmmean = np.array(fwhmmeans).mean() * conv_box_const
    conv_boxes += f"{fwhmmean}   {fwhmmean}"

    input_images = input_images[1:]
    psf_images = psf_images[1:]
    filters = filters[1:]    
    wavelenghts = wavelenghts[1:]

    ## Get ZPs
    check_vo_file("VOs/splusZPs.csv", "https://splus.cloud/files/documentation/iDR4/tabelas/iDR4_zero-points.csv") ## Check if zps file exists
    df = pd.read_csv(os.path.join(pygalfitm.__path__[0], "VOs/splusZPs.csv"))
    header = getheader(os.path.join(data_folder, name + f"_{bands[0].lower()}.fits"))
    field = header['OBJECT']

    for band in bands:
        zps += "," + str(df[df['Field'] == field.replace("_", "-")][f'ZP_{band.lower().replace("f", "J0").replace("j0", "J0")}'].values[0])
    zps = zps[1:]

    ## Get axis_ratios, effective_rs, position_angles, mags
    axis_ratios : str = ""
    effective_rs : str = ""
    position_angles : str = ""
    mags : str = ""

    for band in bands:

        band = band.lower().replace("j0", "J0").replace("f", "J0")
        table = conn.query(f"""
            select ra_{band}, dec_{band}, B_{band}, A_{band}, FLUX_RADIUS_50_{band}, THETA_{band}, {band}_auto
            from "idr4_single"."idr4_single_{band.lower()}" as x
            where 
            1 = CONTAINS( POINT('ICRS', x.ra_{band}, x.dec_{band}), 
            CIRCLE('ICRS', {ra}, {dec}, 0.0015))
        """)

        obj = find_nearest_object(table.to_pandas(), ra, dec, ra_name=f"RA_{band}", dec_name=f"DEC_{band}")
        
        axis_ratios += "," + str( obj[f"B_{band}"]/obj[f"A_{band}"] )
        effective_rs += "," + str( obj[f"FLUX_RADIUS_50_{band}"] )
        position_angles += "," + str( obj[f"THETA_{band}"] )
        mags += "," + str( obj[f"{band}_auto"]  )

    axis_ratios = axis_ratios[1:]
    effective_rs = effective_rs[1:]
    position_angles = position_angles[1:]
    mags = mags[1:]

    ## Setup pygalfitm class
    pyg = pygalfitm.PyGalfitm()
    pyg.name = name
    pyg.feedme_path = os.path.join(output_folder, "galfit.feedme")
    pyg.activate_components()
    pyg.activate_components(["sersic"])

    pyg.set_base({
        "A": input_images,
        "A1": filters,
        "B": os.path.join(output_folder, name + "ss.fits"),
        "C": "none",
        "D": psf_images,
        "A2": wavelenghts,
        "H": f"1   {cut_size}  1   {cut_size}",
        "I": f"{cut_size} {cut_size}",
        "J": zps,
        "I": conv_boxes,
        "K": "0.55 0.55"
    })

    pyg.set_component("sersic", {
        "1": ( string_times_x(cut_size / 2, len(bands)), 1, "band" ),
        "2": ( string_times_x(cut_size / 2, len(bands)), 1, "band" ), 
        "3": ( mags, 3, "band" ), 
        "4": ( effective_rs, 2, "band" ),
        "5": ( string_times_x("4", len(bands)), 2, "band" ),
        "9": ( axis_ratios, 1, "band" ),
        "10": ( position_angles, 1, "band" )
    })
    
    return pyg
