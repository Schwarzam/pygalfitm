from pygalfitm.VOs import splus

from pygalfitm import PyGalfitm
import splusdata

conn = splusdata.connect()

import os

DATA_FOLDER = "./data"
OUTPUT_FOLDER = "./outputs"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

pygalgitm_object = splus.get_splus_class(
    name = "test", 
    ra = 51.30076502619, 
    dec = -32.9024762233, 
    cut_size = 200, 
    data_folder = DATA_FOLDER, 
    output_folder = OUTPUT_FOLDER, 
    remove_negatives = True,
    conn = conn, 
    bands=["u", "r", "z"]
)

pygalgitm_object.active_components = ["sersic"]

pygalgitm_object.print_base()

pygalgitm_object.print_component("sersic")

pygalgitm_object.write_feedme()
_ = pygalgitm_object.run()


print("Done!")

