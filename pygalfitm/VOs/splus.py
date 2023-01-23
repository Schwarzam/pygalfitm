from astropy.io.fits import getheader

import pygalfitm
from pygalfitm import PyGalfitm
from pygalfitm.auxiliars import string_times_x, get_dims, get_exptime, unpack_file, check_vo_file
from pygalfitm.psf import make_psf

import pandas as pd
import os



def get_splus(name, ra, dec, cut_size, data_folder, output_folder, conn, bands = ["I", "R", "G"], zpfile = None,
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
    **kwargs):


    ##Get wavelenghts, input_images, psf_images, filters, zps
    wavelenghts = ""
    input_images = ""
    psf_images = ""
    filters = ""
    zps = ""

    for band in bands:
        band = band.lower()
        try:
            conn.get_cut(ra, dec, 200, band.upper(), filepath=os.path.join(data_folder, f'{name}_{band.lower()}.fits'))
        except Exception as e:
            print(e)
        
        try:
            unpack_file(os.path.join(data_folder, f'{name}_{band.lower()}.fits.fz'))
        except Exception as e:
            print(e)
            print("Make sure you have fpack (cfitsio) in your system alias.")
        
        make_psf(os.path.join(data_folder, f'{name}_{band.lower()}.fits'), outfile=os.path.join(data_folder, f'psf_{name}_{band.lower()}.fits'))

        input_images += "," + os.path.join(data_folder, f'{name}_{band.lower()}.fits')
        psf_images += "," + os.path.join(data_folder, f'psf_{name}_{band.lower()}.fits')
        filters += "," + str(band).lower()
        wavelenghts += "," + str(SPLUS_WAVELENGHTS[band.lower().replace("f", "J0")])

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
        zps += "," + str(df[df['Field'] == field.replace("_", "-")][f'ZP_{band.lower().replace("f", "J0")}'].values[0])
    zps = zps[1:]

    ## Get axis_ratios, effective_rs, position_angles, mags
    axis_ratios : str = ""
    effective_rs : str = ""
    position_angles : str = ""
    mags : str = ""

    for band in bands:
        band = band.lower()

        table = conn.query(f"""
            select * from "idr4_single"."idr4_single_{band}" as x
            where 
            1 = CONTAINS( POINT('ICRS', x.ra_{band}, x.dec_{band}), 
            CIRCLE('ICRS', {ra}, {dec}, 0.0015))
        """)
        
        axis_ratios += "," + str( table[0][f"B_{band}"]/table[0][f"A_{band}"] )
        effective_rs += "," + str( table[0][f"FLUX_RADIUS_50_{band}"] )
        position_angles += "," + str( table[0][f"THETA_{band}"] )
        mags += "," + str( table[0][f"{band}_auto"]  )

    axis_ratios = axis_ratios[1:]
    effective_rs = effective_rs[1:]
    position_angles = position_angles[1:]
    mags = mags[1:]


    ## Setup pygalfitm class
    pyg = pygalfitm.PyGalfitm()
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
        "K": "0.55 0.55"
    })

    pyg.set_component("sersic", {
        "1": ( string_times_x(cut_size / 2, 3), 1, "band" ),
        "2": ( string_times_x(cut_size / 2, 3), 1, "band" ), 
        "3": ( mags, 3, "band" ), 
        "4": ( effective_rs, 2, "band" ),
        "5": ( string_times_x("4", 3), 2, "band" ),
        "9": ( axis_ratios, 1, "band" ),
        "10": ( position_angles, 1, "band" )
    })

    pyg.write_feedme()
    _ = pyg.run()
