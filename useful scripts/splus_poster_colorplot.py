from pygalfitm.VOs import splus

from pygalfitm import PyGalfitm
import splusdata

from astropy.io import fits
import os

import numpy as np
import cv2

from PIL import Image
import matplotlib.pyplot as plt
import matplotlib

import argparse

# Create the parser
parser = argparse.ArgumentParser(description='This is a script that uses pygalfitm to fit multiple objects in a given table.')

# Add the arguments
parser.add_argument('-R', '--ra', type=float, default=55.90420728, help='Right Ascension.')
parser.add_argument('-D', '--dec', type=float, default=-35.85392675, help='Declination.')

parser.add_argument('-C', '--cut_size', type=int, default=250, help='Box size of the images.')
parser.add_argument('-U', '--splususer', type=str, default=None, help='Splus.cloud user.')
parser.add_argument('-P', '--spluspassword', type=str, default=None, help='Splus.cloud password.')
parser.add_argument('-F', '--data_folder', type=str, default="../dev/data/", help='Data folder.')
parser.add_argument('-O', '--output_folder', type=str, default="../dev/outputs/", help='Output folder.')
parser.add_argument('-L', '--plot_path', type=str, default="../dev/outputs/pygalfitm.png", help='Plot folder.')
parser.add_argument('-G', '--galfit_path', type=str, default=None, help='Path to galfit executable.')

# Execute the parse_args() method
args = parser.parse_args()
matplotlib.use('Agg')

conn = splusdata.connect(args.splususer, args.spluspassword)

def open_file(path_to_file):
    im_frame = Image.open(path_to_file)
    np_frame = np.array(im_frame)
    return np_frame

def rgb_to_hue(rgb_color):
    """Convert an RGB color to HSV and return the hue value."""
    hsv_color = cv2.cvtColor(np.uint8([[rgb_color]]), cv2.COLOR_RGB2HSV)[0][0]
    return hsv_color[0]

def apply_colorfilter(im, target_color=(255, 255, 255), thresh=40, saturation_fraction=0.5):
    """
    Apply a color filter to a detected galaxy in the image.
    
    Parameters:
    - im: path to the image file.
    - target_color: a tuple representing the target RGB color. 
    """
    
    # Get the hue of the target color
    target_hue = rgb_to_hue(target_color)

    # Load the image
    img = cv2.imread(im)

    # Convert the image to grayscale for thresholding
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image
    _, thresh = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)

    # Find contours to identify the galaxy
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an empty mask
    mask = np.zeros_like(gray)

    # Fill the detected galaxy contour on the mask with white color
    cv2.drawContours(mask, contours, -1, 255, thickness=cv2.FILLED)

    # Convert the image to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Adjust the hue of the detected galaxy using the mask
    hsv[:,:,0] = np.where(mask == 255, target_hue, hsv[:,:,0])
    
    # Set a reduced saturation for the detected galaxy to get a lighter color
    hsv[:,:,1] = np.where(mask == 255, int(255 * saturation_fraction), hsv[:,:,1])

    # Convert back to BGR
    filtered_galaxy = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Use the mask to combine the filtered galaxy with the original image
    result = cv2.bitwise_and(filtered_galaxy, filtered_galaxy, mask=mask) + cv2.bitwise_and(img, img, mask=cv2.bitwise_not(mask))

    # Save the result
    cv2.imwrite(im, result)

DATA_FOLDER = args.data_folder
OUTPUT_FOLDER = args.output_folder

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

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

print("------------------------------------")
print("Getting splus information and images about object: ")
pygalgitm_object = splus.get_splus_class(
    name = "test", 
    ra = args.ra, ## Add your RA here 
    dec = args.dec, ## Add your DEC here
    cut_size = args.cut_size, ## Size of the cutout in pixels
    data_folder = DATA_FOLDER, 
    output_folder = OUTPUT_FOLDER, 
    remove_negatives = True,
    conn = conn, 
    bands=bands
)

print("------------------------------------")
print("Base config: ")
pygalgitm_object.print_base()

print("------------------------------------")
print("Sersic component config: ")
pygalgitm_object.print_component("sersic")

print("------------------------------------")
print("Running GALFITM...")
pygalgitm_object.write_feedme()
_ = pygalgitm_object.run()

filters = pygalgitm_object.base['A1']['value'].split(",") 
for key, band in enumerate(filters): 
    filters[key] = band.strip()

input_data = {f: fits_cube[i + 1].data for i, f in enumerate(filters)}
model_data = {f: fits_cube[i + len(filters) + 1].data for i, f in enumerate(filters)}
residual_data = {f: fits_cube[i + 2*len(filters) + 1].data for i, f in enumerate(filters)}

colors = {
    'i': (97, 0, 0),
    'r': (255, 99, 0),
    'g': (0, 195, 255),
    'z': (97, 0, 0),
    'u': (97, 0, 97),
    'j0378': (97, 0, 97),
    'j0395': (127, 0, 157),
    'j0410': (126, 0, 217),
    'j0430': (64, 0, 255),
    'j0515': (22, 255, 0),
    'j0660': (232, 0, 0),
    'j0861': (97, 0, 0)
}

thresholds = {
    'i': 43,
    'r': 40,
    'g': 40,
    'z': 48,
    'u': 60,
    'j0378': 110,
    'j0395': 120,
    'j0410': 71,
    'j0430': 65,
    'j0515': 50,
    'j0660': 42,
    'j0861': 40  
}

join(OUTPUT_FOLDER, f"input_{key}.fits")
from os.path import join

print("------------------------------------")
print("Extracting results data and applying color filters")
for key in input_data:
    input_name = join(OUTPUT_FOLDER, f"input_{key}.fits")
    model_name = join(OUTPUT_FOLDER, f"model_{key}.fits")
    residual_name = join(OUTPUT_FOLDER, f"residual_{key}.fits")

    input_im = join(OUTPUT_FOLDER, f"input_{key}.png")
    model_im = join(OUTPUT_FOLDER, f"model_{key}.png")
    residual_im = join(OUTPUT_FOLDER, f"residual_{key}.png")

    fits.PrimaryHDU(data = input_data[key]).writeto(input_name, overwrite = True)
    fits.PrimaryHDU(data = model_data[key]).writeto(model_name, overwrite = True)
    fits.PrimaryHDU(data = residual_data[key]).writeto(residual_name, overwrite = True)
    
    os.system(f"fitspng -o {input_im} {input_name}")
    os.system(f"fitspng -o {model_im} {model_name}")
    os.system(f"fitspng -o {residual_im} {residual_name}")
    
    apply_colorfilter(input_im, colors[key], 10, 0.5)
    apply_colorfilter(model_im, colors[key], 10, 0.5)
    apply_colorfilter(residual_im, colors[key], 10, 0.5)

ainput_data = {f: open_file(join(OUTPUT_FOLDER, "input_{f}.png")) for i, f in enumerate(filters)}
amodel_data = {f: open_file(join(OUTPUT_FOLDER, "model_{f}.png")) for i, f in enumerate(filters)}
aresidual_data = {f: open_file(join(OUTPUT_FOLDER, "residual_{f}.png")) for i, f in enumerate(filters)}

fig, axs = plt.subplots(3, 12, figsize=(20, 5))  # Create 3x12 subplots

# Plotting images from dict1
for i, (key, value) in enumerate(ainput_data.items()):
    axs[0, i].imshow(value, cmap='gray')
    axs[0, i].axis('off')

# Plotting images from dict2
for i, (key, value) in enumerate(amodel_data.items()):
    axs[1, i].imshow(value, cmap='gray')
    axs[1, i].axis('off')

# Plotting images from dict3
for i, (key, value) in enumerate(aresidual_data.items()):
    axs[2, i].imshow(value, cmap='gray')
    axs[2, i].axis('off')


fig.patch.set_facecolor("none")
plt.tight_layout()

print("------------------------------------")
print("Saving plot")
fig.savefig(args.plot_path, transparent=True, dpi=300)

print("------------------------------------")
print("Done!")