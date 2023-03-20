# Import the necessary modules and libraries
from pygalfitm.VOs import splus
from pygalfitm.read import read_output_to_class

from pygalfitm.auxiliars import clear_folder

import pandas as pd
import splusdata
import os

# Connect to the S-PLUS database
conn = splusdata.connect()

# Read the input file as a pandas dataframe
df = pd.read_csv("blueE_test_galfitm.csv")

# Define the list of filters used in the image
bands = ["z", "i", "r", "g", "u"]

# Define the input and output folders
DATA_FOLDER = "../data/"
OUTPUT_FOLDER = "../outputs/"

# Create the input and output folders if they don't already exist, if they exist, clear them
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
else: 
    clear_folder(DATA_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
else: 
    clear_folder(OUTPUT_FOLDER)

# Iterate over the rows of the input dataframe
for key, value in df.iterrows():
    # Extract the object name, RA, and Dec
    name = value["ID"]
    ra = value["RA"]
    dec = value["DEC"]

    # Define the size of the image cutout
    cut_size = 200

    # Define the output folder for the current object
    outfolder = os.path.join(OUTPUT_FOLDER, name)
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    try: 
        # Call the function to create the GalFitM input file for the current object
        pygal_obj = splus.get_splus_class(
            name, ra, dec, cut_size, 
            data_folder=DATA_FOLDER,
            output_folder=outfolder,
            conn=conn,
            remove_negatives=True, 
            bands = bands
        )
    except:
        # Continue with the next object if there's an error creating the GalFitM input file
        print("Error on object", name, "continuing with the next object...")
        continue

    # Write the input file for GalFitM and run GalFitM
    pygal_obj.write_feedme()
    _ = pygal_obj.run()

    # Read the output file from GalFitM and store the results in a class object
    result_obj = read_output_to_class(os.path.join(outfolder, f"{name}ss.galfit.01.band"))
    
    # Create a pandas dataframe containing the results
    res_df = result_obj.create_result_table()

    # Save the results to the output file
    if not os.path.exists(os.path.join(OUTPUT_FOLDER, f"all_results.csv")):
        # If the output file doesn't exist, create it and write the results
        res_df.to_csv(os.path.join(OUTPUT_FOLDER, f"all_results.csv"))
    else:
        # If the output file already exists, read it into a dataframe, concatenate the new results, and write the combined dataframe
        df = pd.read_csv(os.path.join(OUTPUT_FOLDER, f"all_results.csv"), index_col=0)
        df = pd.concat([df, res_df], axis=1)
        df.to_csv(os.path.join(OUTPUT_FOLDER, f"all_results.csv"))
