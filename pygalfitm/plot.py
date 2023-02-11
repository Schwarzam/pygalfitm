from astropy.io import fits
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from astropy.visualization import make_lupton_rgb

def gen_plot(pygalfit, component_selected = "sersic", plot_parameters = [], plotsize_factor = (1, 1), 
             colorbar = True, lupton_stretch = 0.2, lupton_q = 8, fig_filename = None, return_plot = False):
    """Copy from pygalfitm.read.gen_plot()
    """    

    filters = pygalfit.base['A1']['value'].split(",") 
    for key, band in enumerate(filters): 
        filters[key] = band.strip()
    
    fits_cube = fits.open(pygalfit.base["B"]["value"].strip())

    plot_data = {}
    for band in filters:
        plot_data[band] = []

    
    for key, param in enumerate(plot_parameters):

        values = pygalfit.components_config[component_selected][str(param)]["col1"].split(",")
        comment = pygalfit.components_config[component_selected][str(param)]["comment"]

        if comment.strip() == "":
            raise Exception("Please insert labels manually")

        for key_band, band in enumerate(filters):

            plot_data[band].append( (values[key_band], comment) )
    
    n_filters = len(filters)
    filters_index = 0
    band_index = 0

    fig = plt.figure(figsize=(n_filters * 4 * plotsize_factor[0], 12 * plotsize_factor[1]), facecolor='white')

    y_label = ["INPUT", "MODEL", "RESIDUAL"]
    y_label_index = 0

    actual_filter = ""
    for i in range(1, n_filters * 3 + 1):
        ax = fig.add_subplot(3, n_filters, i)
        im_data = make_lupton_rgb(fits_cube[i].data, fits_cube[i].data, fits_cube[i].data, stretch=lupton_stretch, Q=lupton_q)
        im = ax.imshow(im_data, cmap='gray', interpolation='none')
        
        ax.set_xticks([])
        ax.set_yticks([])
        
        if i % n_filters == 1:
            ax.set_ylabel(y_label[y_label_index], rotation=90, size='large')
            y_label_index += 1

        if i <= n_filters:
            string = ""
            for info in plot_data[filters[filters_index]]:
                string = string + f'{info[0]} {info[1].lstrip().split("[")[0]}\n'
            ax.set_title(f"""

{filters[filters_index]}
{string}
            """, loc='left')
            
            filters_index += 1

        if i % 3 == 1:
            actual_filter = filters[band_index]
            band_index += 1
        
        if colorbar:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes('right', size='3%', pad=0.05)
            fig.colorbar(im, cax=cax, orientation='vertical')

    fig.tight_layout()
    plt.subplots_adjust(hspace=0.05)

    if fig_filename and not return_plot:
        plt.imsave(fig_filename)
        plt.close(fig)
        return 
    
    elif fig_filename and return_plot:
        plt.imsave(fig_filename)

    if return_plot:
        return fig
    else:
        plt.show()