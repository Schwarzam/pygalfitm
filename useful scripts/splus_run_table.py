import pygalfitm
import pandas as pd
import os
import splusdata

from pygalfitm.read import read_output_to_class
import matplotlib

import argparse

# Create the parser
parser = argparse.ArgumentParser(description='This is a script that uses pygalfitm to fit multiple objects in a given table.')

# Add the arguments
parser.add_argument('table_path', type=str, help='path to the table')
parser.add_argument('-C', '--cut_size', type=int, default=200, help='Box size of the images.')
parser.add_argument('-U', '--splususer', type=str, default=None, help='Splus.cloud user.')
parser.add_argument('-P', '--spluspassword', type=str, default=None, help='Splus.cloud password.')
parser.add_argument('-F', '--data_folder', type=str, default="../data/", help='Data folder.')
parser.add_argument('-O', '--output_folder', type=str, default="../outputs/", help='Output folder.')
parser.add_argument('-G', '--galfit_path', type=str, default=None, help='Path to galfit executable.')

# Execute the parse_args() method
args = parser.parse_args()
matplotlib.use('Agg')

conn = splusdata.connect(args.splususer, args.spluspassword)

df = pd.read_csv(args.table_path)

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
}

sorted_wavelengths = sorted(SPLUS_WAVELENGHTS, key=SPLUS_WAVELENGHTS.get)
bands = sorted_wavelengths

def get_column_labels(columns):
    dec_col = ''
    ra_col = ''
    ID_col = ''
    for cols in columns:
        if 'dec' in cols.lower():
            dec_col = cols
        if 'ra' in cols.lower():
            ra_col = cols
        if 'id' in cols.lower():
            ID_col = cols
    
    return ra_col, dec_col, ID_col

DATA_FOLDER = args.data_folder
OUTPUT_FOLDER = args.output_folder

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

ra_col, dec_col, ID_col = get_column_labels(df.columns)

for key, value in df.iterrows():
    name = value[ID_col]
    ra = value[ra_col]
    dec = value[dec_col]
    
    print("====================================")
    print(f"Starting {name}")

    cut_size = int(args.cut_size)

    outfolder = os.path.join(OUTPUT_FOLDER, name)
    datafolder = os.path.join(DATA_FOLDER, name)
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    if not os.path.exists(datafolder):
        os.makedirs(datafolder)
    
    try: 
        pygal_obj = pygalfitm.splus.get_splus_class(
            name, ra, dec, cut_size, 
            data_folder=datafolder,
            output_folder=outfolder,
            conn=conn,
            remove_negatives=True, 
            bands = bands
        )
        
    except Exception as e:
        print(e)
        print(f"Skipping {name}")
        print("====================================")
        continue
    
    pygal_obj.write_feedme()
    pygal_obj.create_fits_table(os.path.join(OUTPUT_FOLDER, "before_fit.fits"))
    
    if args.galfit_path is not None:
        pygal_obj.executable = args.galfit_path

    _ = pygal_obj.run()

    os.path.join(outfolder, f"{name}ss.galfit.01.band")
    result_obj = read_output_to_class(os.path.join(outfolder, f"{name}ss.galfit.01.band"))
    
    plot = result_obj.gen_plot(
        "sersic", 
        return_plot = True, 
        plot_parameters=[3, 4, 5, 9], 
        colorbar=True
    )
    plot.savefig(os.path.join(outfolder, f"{name}_plot.pdf"))
    
    result_obj.create_fits_table(os.path.join(OUTPUT_FOLDER, "after_fit.fits"))
    
    print(f"Finished {name}")
    print("====================================")

