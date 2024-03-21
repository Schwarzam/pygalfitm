import os
import sys
import copy

import requests

from astropy.io import fits
from astropy.table import Table

import pygalfitm

from pygalfitm.plot import gen_plot, gen_color_plot
from pygalfitm.auxiliars import remove_parentheses_and_brackets

from pygalfitm.log import control

class PyGalfitm:
    """PyGalfitM wrapper class. 
    """    
    def __init__(self, executable : str = os.path.join(pygalfitm.__path__[0], "galfitm")):   
        """Here we initialize the class with default values for the base and components. 

        Base values are in self.base variable 

        Components are stored in self.components_config

        Args:
            executable (str, optional): Path pointing to galfitm executable, if left as default downloads the executable depending on the OS. Defaults to os.path.join(pygalfitm.__path__[0], "galfitm").
        """        
        self.feedme_path = "galfit.feedme"
        self.executable = executable

        self.name = ""

        self.base = {
            "A": {"value": "", "comment": "Input data image (FITS file)"},
            "A1": {"value": "g, r, i", "comment": "Nick names (band labels) "},
            "A2": {"value": "4770, 6231, 7625", "comment": "Effective wavelenghts"}, 
            "B": {"value": "4770, 6231, 7625", "comment": "Output data image block"}, 
            "C": {"value": "", "comment": "Sigma image name (made from data if blank or 'none')"},
            "D": {"value": "", "comment": "Input PSF image and (optional) diffusion kernel"}, 
            "E": {"value": "1", "comment": "PSF fine sampling factor relative to data "}, 
            "F": {"value": "none", "comment": "Bad pixel mask (FITS image or ASCII coord list)"}, 
            "G": {"value": "none", "comment": "File with parameter constraints (ASCII file) "},
            "H": {"value": "1    200  1  200", "comment": "Image region to fit (xmin xmax ymin ymax)"},
            "I": {"value": "200  200", "comment": "Size of the convolution box (x y)"},
            "J": {"value": "0,0,0", "comment": "Magnitude photometric zeropoint"},
            "K": {"value": "0.55  0.55", "comment": "Plate scale (dx dy)   [arcsec per pixel]"},
            "O": {"value": "regular", "comment": "Display type (regular, curses, both)"}, 
            "P": {"value": "0", "comment": "Choose: 0=optimize, 1=model, 2=imgblock, 3=subcomps"}, 
            "U": {"value": "0", "comment": ""}
        }

        self.components_config = {
            "sky" : {
                "1": {"col1": "BKGG,BKGR,BKGI", "col2": "0", "col3": "band", "comment": "Sky background at center of fitting region [ADUs]"},
                "2": {"col1": "0,0,0", "col2": "0", "col3": "band", "comment": "dsky/dx (sky gradient in x) [ADUs/pix]"},
                "3": {"col1": "0,0,0", "col2": "0", "col3": "band", "comment": "dsky/dy (sky gradient in y) [ADUs/pix]"},
                "Z": {"col1": "0", "col2": "", "col3": "", "comment": "Skip this model in output image? (yes=1, no=0)"}
            },
            "sersic" : {
                "1":  {"col1": "200.0,200.0,200.0", "col2": "1", "col3": "band", "comment": "Position x [pixel]"},
                "2":  {"col1": "200.0,200.0,200.0", "col2": "1", "col3": "band", "comment": "Position y [pixel]"},
                "3":  {"col1": "0,0,0", "col2": "3", "col3": "band", "comment": "Integrated magnitude"},
                "4":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "R_e (effective radius) [pix]"},
                "5":  {"col1": "4", "col2": "2", "col3": "band", "comment": "Sersic index n (de Vaucouleurs n=4)"},
                "9":  {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Axis ratio (b/a)"},
                "10": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Position angle (PA) [deg: Up=0, Left=90]"},
                "Z":  {"col1": "0", "col2": "", "col3": "", "comment": "Skip this model in output image? (yes=1, no=0)"}
            },
            "expdisk" : {
                "1":  {"col1": "300", "col2": "1", "col3": "band", "comment": "Position x [pixel]"},
                "2":  {"col1": "357.4", "col2": "1", "col3": "band", "comment": "Position y [pixel]"},
                "3":  {"col1": "0,0,0", "col2": "3", "col3": "band", "comment": "Integrated magnitude"},
                "4":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "R_s (disk scale lengths) [pix]"},
                "9":  {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Axis ratio (b/a)"},
                "10": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Position angle (PA) [deg: Up=0, Left=90]"},
                "Z":  {"col1": "0", "col2": "", "col3": "", "comment": "Skip this model in output image? (yes=1, no=0)"}
            },
            "moffat" : {
                "1":  {"col1": "300", "col2": "1", "col3": "band", "comment": "Position x [pixel]"},
                "2":  {"col1": "357.4", "col2": "1", "col3": "band", "comment": "Position y [pixel]"},
                "3":  {"col1": "0,0,0", "col2": "3", "col3": "band", "comment": "Total magnitude"},
                "4":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "FWHM"},
                "5":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "powerlaw"},
                "9":  {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Axis ratio (b/a)"},
                "10": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Position angle (PA) [deg: Up=0, Left=90]"},
                "Z":  {"col1": "0", "col2": "", "col3": "", "comment": "Skip this model in output image? (yes=1, no=0)"}
            },
            "ferrer" : {
                "1":  {"col1": "300", "col2": "1", "col3": "band", "comment": "Position x [pixel]"},
                "2":  {"col1": "357.4", "col2": "1", "col3": "band", "comment": "Position y [pixel]"},
                "3":  {"col1": "0,0,0", "col2": "3", "col3": "band", "comment": "Central surface brghtness [mag/arcsec^2]"},
                "4":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "Outer truncation radius  [pix]"},
                "5":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "Alpha (outer truncation sharpness) "},
                "6":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "Beta (central slope)"},
                "9":  {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Axis ratio (b/a)"},
                "10": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Position angle (PA) [deg: Up=0, Left=90]"},
                "Z":  {"col1": "0", "col2": "", "col3": "", "comment": "Skip this model in output image? (yes=1, no=0)"}
            },
            "psf" : {
                "1": {"col1": "0,0,0", "col2": "0", "col3": "band", "comment": "position x [pixel]"},
                "2": {"col1": "0,0,0", "col2": "0", "col3": "band", "comment": "position y [pixel]"},
                "3": {"col1": "0,0,0", "col2": "0", "col3": "band", "comment": "total magnitude "},
                "Z": {"col1": "0", "col2": "", "col3": "", "comment": "Skip this model in output image? (yes=1, no=0)"}
            },
            "nuker" : {
                "1":  {"col1": "300.", "col2": "1", "col3": "band", "comment": "Position x [pixel]"},
                "2":  {"col1": "357.4", "col2": "1", "col3": "band", "comment": "Position y [pixel]"},
                "3":  {"col1": "0,0,0", "col2": "3", "col3": "band", "comment": "mu(Rb)            [surface brightness mag. at Rb]"},
                "4":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "Rb               [pixels]"},
                "5":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "alpha  (sharpness of transition)"},
                "6":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "beta   (outer powerlaw slope)"},
                "7":  {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "gamma  (inner powerlaw slope)"},
                "9": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "axis ratio (b/a)"},
                "10": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Position angle (PA) [deg: Up=0, Left=90]"},
                "Z":  {"col1": "0", "col2": "", "col3": "", "comment": "Skip this model in output image? (yes=1, no=0)"}
            },
            "corser" : {
                "1":  {"col1": "300.", "col2": "1", "col3": "band", "comment": "Position x [pixel]"},
                "2":  {"col1": "357.4", "col2": "1", "col3": "band", "comment": "Position y [pixel]"},
                "3":  {"col1": "0,0,0", "col2": "3", "col3": "band", "comment": "mu(Rb)            [surface brightness mag. at Rb]"},
                "4":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "Rb               [pixels]"},
                "5":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "alpha  (sharpness of transition)"},
                "6":  {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "gamma  (inner powerlaw slope)"},
                "7": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "R_e (half-light radius)   [pix]"},
                "8": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Sersic index n (de Vaucouleurs n=4) "},
                "9": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "axis ratio (b/a)"},
                "10": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Position angle (PA) [deg: Up=0, Left=90]"},
                "Z":  {"col1": "0", "col2": "", "col3": "", "comment": "Skip this model in output image? (yes=1, no=0)"}
            },
            "devauc" : {
                "1":  {"col1": "300.", "col2": "1", "col3": "band", "comment": "Position x [pixel]"},
                "2":  {"col1": "357.4", "col2": "1", "col3": "band", "comment": "Position y [pixel]"},
                "3":  {"col1": "0,0,0", "col2": "3", "col3": "band", "comment": "Total magnitude"},
                "4":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "Rs               [Pixels]"},
                "9":  {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Axis ratio (b/a)"},
                "10": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Position angle (PA) [deg: Up=0, Left=90]"},
                "Z":  {"col1": "0", "col2": "", "col3": "", "comment": "Skip this model in output image? (yes=1, no=0)"}
            },
            "edgedisk" : {
                "1":  {"col1": "300.", "col2": "1", "col3": "band", "comment": "Position x [pixel]"},
                "2":  {"col1": "357.4", "col2": "1", "col3": "band", "comment": "Position y [pixel]"},
                "3":  {"col1": "0,0,0", "col2": "3", "col3": "band", "comment": "central surface brightness  [mag/arcsec^2]"},
                "4":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "disk scale-height    [Pixels]"},
                "5":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "disk scale-length    [Pixels]"},
                "10": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Position angle (PA) [deg: Up=0, Left=90]"},
                "Z":  {"col1": "0", "col2": "", "col3": "", "comment": "Skip this model in output image? (yes=1, no=0)"}
            },
            "gaussian" : {
                "1":  {"col1": "300.", "col2": "1", "col3": "band", "comment": "Position x [pixel]"},
                "2":  {"col1": "357.4", "col2": "1", "col3": "band", "comment": "Position y [pixel]"},
                "3":  {"col1": "0,0,0", "col2": "3", "col3": "band", "comment": "Total magnitude"},
                "4":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "FWHM               [pixels]"},
                "9":  {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Axis ratio (b/a)"},
                "10": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Position angle (PA) [deg: Up=0, Left=90]"},
                "Z":  {"col1": "0", "col2": "", "col3": "", "comment": "Skip this model in output image? (yes=1, no=0)"}
            },
            "king" : {
                "1":  {"col1": "300", "col2": "1", "col3": "band", "comment": "Position x [pixel]"},
                "2":  {"col1": "357.4", "col2": "1", "col3": "band", "comment": "Position y [pixel]"},
                "3":  {"col1": "0,0,0", "col2": "3", "col3": "band", "comment": "mu(0)"},
                "4":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "Rc"},
                "5":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "Rt"},
                "6":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "alpha"},
                "9":  {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Axis ratio (b/a)"},
                "10": {"col1": "0,0,0", "col2": "1", "col3": "band", "comment": "Position angle (PA) [deg: Up=0, Left=90]"},
                "Z":  {"col1": "0", "col2": "", "col3": "", "comment": "Skip this model in output image? (yes=1, no=0)"}
            }
        }

        self.components = [
            "sersic",
            "expdisk", 
            "moffat",
            "ferrer",
            "psf",
            "sky"
        ]

        self.active_components = []

    def check_executable(self):
        if not os.path.exists(self.executable):
            control.info("Executable path not found. ")
            while True:
                i = input("Do you want to download the executable? (y/n): ")
                if i == "y":
                    break 
                elif i == "n":
                    return
            
            if sys.platform == "darwin":
                control.info("Downloading galfitm executable from " + "https://www.nottingham.ac.uk/astronomy/megamorph/exec/galfitm-1.4.4-osx")
                r = requests.get("https://www.nottingham.ac.uk/astronomy/megamorph/exec/galfitm-1.4.4-osx")
                open(os.path.join(pygalfitm.__path__[0], "galfitm"), "wb").write(r.content)
            
            if sys.platform == "linux":
                control.info("Downloading galfitm executable from " + "https://www.nottingham.ac.uk/astronomy/megamorph/exec/galfitm-1.4.4-linux-x86_64")
                r = requests.get("https://www.nottingham.ac.uk/astronomy/megamorph/exec/galfitm-1.4.4-linux-x86_64")
                open(os.path.join(pygalfitm.__path__[0], "galfitm"), "wb").write(r.content)
                
            control.warn(f"""PLEASE RUN:
                chmod +x {os.path.join(pygalfitm.__path__[0], "galfitm")}
            """)

            raise Exception(f"Run chmod +x {os.path.join(pygalfitm.__path__[0], 'galfitm')}")

    def activate_components(self, component_s : list = None):
        """This function is used to activate one or more components. 
        You may pass just a string with the component name, or a list. 

        If left in blank, the active components are reseted. 
        Args:
            component_s (list or str, optional): Component name or list. Defaults to None.

        Raises:
            Exception: Not valid component
        """        
        if component_s is None:
            self.active_components = []
            return

        if isinstance(component_s, list):
            for comp in component_s:
                if comp in self.components:
                    count = 0 
                    for i in self.active_components:
                        if comp in i:
                            count += 1

                    if count == 0:
                        self.active_components.append(comp)
                    else:
                        self.active_components.append(str(comp) + str(count))
                        self.components_config[str(comp) + str(count)] = copy.deepcopy(self.components_config[str(comp)])
                        control.info("Added component as " + str(comp) + str(count))
                else:
                    raise Exception(f"Not valid component - {comp}")
        else:
            raise Exception(f"Parameter should be a list.")


    def set_base(self, item, value=""):
        """Function used to alter base values. 
        It's possible to pass only one value by giving the item and value to alter, or a dict with all keys and respective values.

        Ex:
            p.set_base("A1", "X")
            p.set_base("B", "Y")

            p.set_base({
                "A1": X
                "B": Y
                "C": Z
            })

        Args:
            item (str or dict): str of item name, or dict with infos.
            value (str, optional): value referred to item name. Defaults to "".

        Raises:
            KeyError: Parameter not valid
        """        
        if isinstance(item, dict):
            for i in item:
                self.base[i]["value"] = str(item[i])
        else:
            if item in self.base:
                self.base[item]["value"] = str(value)
            else:
                raise KeyError("Parameter not found in galfitm feedme base config.")
        
    def set_component(self, component, item, value = None, column = 1):
        """Function used to alter component values
        It's possible to pass only one value by giving the item and value to alter, or a dict with all keys and respective values.

        Ex:
            p.set_component("sersic", "1", "X", column=1)
            p.set_component("sersic", "1", "band", column=3)

            p.set_component("sersic", "2", "Y")
            
                OR

            p.set_component("sersic", {
                "A1": X
                "B": Y
                "C": Z
            })

                OR
            
            p.set_component("sersic", {
                "A1": (X, 1, band)
                "B": (Y, 1, band)
                "C": Z
            })

        Args:
            component (str): component name
            item (str or dict): item to change or dict with all infos. 
            value (str): Value referred in item (just used in case item is str).
            column (int, optional): Select column of change, 1, 2 or 3. Defaults to 1.

        Raises:
            Exception: Component not found.
        """        
        if column in [1, 2, 3]:
            column = 'col' + str(column)
        else:
            raise Exception("Column not valid.")
        if component in self.components_config:
            if isinstance(item, dict):
                for i in item:
                    if isinstance(item[i], tuple):
                        if len(item[i]) > 3:
                            raise Exception("Tuple not valid " + str(item[i]))
                        for key, val in enumerate(item[i]):
                            self.components_config[component][i]["col" + str(key + 1)] = str(val)
                    else:
                        self.components_config[component][i][column] = str(item[i])
            else:
                if item in self.components_config[component]:
                    self.components_config[component][item][column] = str(value)
        else:
            raise KeyError("Component not found.")


    def write_feedme(self, feedme_path = None):
        """Writes final feedme

        Args:
            feedme_path (str, optional): file path, if none select default file path. Defaults to None.
        """        
        if feedme_path is None:
            feedme_path = self.feedme_path
        else:
            self.feedme_path = feedme_path

        self.write_base(feedme_path)

        for component in self.active_components:
            self.write_component(component, feedme_path)
    
    def print_component(self, component):
        """Prints selected component to visualize informations

        Args:
            component (str): component name

        Raises:
            KeyError: Component not found.
        """        
        config = self.components_config[component]
        if component in self.components_config:
            for i in self.components_config[component]:
                final = i + ") " + config[i]['col1'].ljust(35) + " " + config[i]['col2'].ljust(5) + " " + config[i]['col3'].ljust(10) + " # " + config[i]['comment']
                print(final)
        else:
            raise KeyError("Component not found.")
    
    def print_base(self):
        """Prints base params to visualize informations
        """        
        for param in self.base:
            final = str(param) + ") " + str(self.base[param]["value"]).ljust(32) + " # " + str(self.base[param]["comment"])
            print(final)


    def write_base(self, feedme_path = None):
        if feedme_path is None:
            feedme_path = self.feedme_path
        file = open(feedme_path, "w")
        for param in self.base:
            final = str(param) + ") " + str(self.base[param]["value"]).ljust(32) + " # " + str(self.base[param]["comment"]) + "\n"
            file.write(final)
        file.close()
    
    def write_component(self, component_name, feedme_path = None):
        if feedme_path is None:
            feedme_path = self.feedme_path

        if component_name in self.active_components:
            config = self.components_config[component_name]
            f = open(feedme_path, "a")
            f.write("\n\n\n")

            f.write("0) " + component_name.translate({ord(ch): None for ch in '0123456789'}) + "\n")
            for i in self.components_config[component_name]:
                final = i + ") " + config[i]['col1'].ljust(35) + " " + config[i]['col2'].ljust(5) + config[i]['col3'].ljust(10) + " # " + config[i]['comment'] + "\n"
                f.write(final)

            f.close()
    
    def check_number_of_filters(self):
        """Check parameter by parameter from active components that have correct number of bands. 
        """        
        nbands = len(self.base["A1"]["value"].split(","))
        correct = True

        for component in self.active_components:
            for att in self.components_config[component]:
                length = len(self.components_config[component][att]["col1"].split(","))
                if length == 1: ## These is due to the skip image parameter
                    continue
                degrees = int(self.components_config[component][att]["col2"].split(",")[0])
                if length > 1 and length < degrees:
                    control.info("Higher degrees of freedom than params in component: " + component + " - (" + att + ")")
                    correct = False

                if length > 1 and length != nbands:
                    control.info("Number of parameters incorrect in component: " + component + " - (" + att + ")")
                    correct = False
        

        return correct


    def run(self):
        """Run galfitm

        Returns:
            str: output of run.
        """        
        import subprocess

        if not self.check_number_of_filters():
            control.info("Warning! Running with possibly wrong parameters on components.")

        self.check_executable()
        try:
            output = subprocess.check_output(f'{self.executable} {self.feedme_path}', shell=True).decode("UTF-8")
        except subprocess.CalledProcessError as e:
            output = e.output.decode("UTF-8")
            control.info(output)
            raise Exception("Error running galfitm.")

        return output
    
    def gen_plot(self, component_selected = "sersic", plot_parameters = [], plotsize_factor = (1, 1), 
             colorbar = True, lupton_stretch = 0.2, lupton_q = 8, fig_filename = None, return_plot = False, **kwargs):        
        """
            Generate a plot to visualize the input, model, and residual data of a PyGalfit model.
            
            Parameters:
                - pygalfit (object): the PyGalfit model object, which contains the input and output data from the PyGalfit fitting.
                - component_selected (str): the name of the PyGalfit component to plot (default is "sersic").
                - plot_parameters (List[str]): a list of parameters to plot for the selected component (default is an empty list).
                - plotsize_factor (Tuple[float, float]): a tuple specifying the size of the plot, default is (1,1).
                - colorbar (bool): a boolean indicating whether to show the color bar on the plot (default is True).
                - lupton_stretch (float): a float specifying the stretch factor used for the Lupton RGB image (default is 0.2).
                - lupton_q (int): an integer specifying the Q factor used for the Lupton RGB image (default is 8).
                - fig_filename (str): a string specifying the filename to save the plot to (default is None).
                - return_plot (bool): a boolean indicating whether to return the plot object instead of showing it (default is False).
                
            Returns:
                - fig (plt.Figure): the matplotlib Figure object, only if `return_plot` is True.
        """
        return gen_plot(self, component_selected, plot_parameters, plotsize_factor, 
             colorbar, lupton_stretch, lupton_q, fig_filename, return_plot, **kwargs)

    def gen_color_plot(self, band_combinations=["i,r,g", "u,f378,f395"], lupton_stretch=3.5, lupton_Q=8, return_plot=False, fig_filename=None):
        """Generate a color plot to visualize the input, model, and residual data of a PyGalfit model combining 3 filters.

        Args:
            pygalfit (_type_): the PyGalfit model object, which contains the input and output data from the PyGalfit fitting.
            band_combinations (list, optional): Combination of filters to create colors, order R G B. Defaults to ["i,r,g", "u,f378,f395"].
            lupton_stretch (float, optional): Make lupton function stretch. Defaults to 3.5.
            lupton_Q (int, optional): Make lupton function Q. Defaults to 8.
            return_plot (bool, optional): a boolean indicating whether to return the plot object instead of showing it (default is False).
            fig_filename (_type_, optional): a string specifying the filename to save the plot to (default is None).

        """
            
        gen_color_plot(self, band_combinations=band_combinations, lupton_stretch=3.5, lupton_Q=8, return_plot=False, fig_filename=None)


    def create_result_table(self):
        """
        Creates a Pandas DataFrame containing result data for components 
        and their corresponding values for each band.

        This function reads the band data from the 'base' attribute and component data from the 'components_config' attribute.
        It iterates through each component and its keys, extracting values for each band, and then combines them into a dictionary.
        Finally, it converts the dictionary into a Pandas DataFrame and returns it.

        Returns:
        pd.DataFrame: A DataFrame containing result data for components and their corresponding values for each band, with column names in the format "component_col_name_band".
        """
        import pandas as pd

        bands = self.base["A1"]["value"].strip().split(",")
        data = {}
        
        

        for component in self.components_config:
            for key in self.components_config[component]:
                col_name = remove_parentheses_and_brackets(self.components_config[component][key]["comment"])
                if "--" in col_name:
                    continue
                
                values = self.components_config[component][key]["col1"].strip().split(",")
                if len(values) == len(bands):
                    
                    for band in bands:
                        data[f"{component}_{col_name}_{band}"] = values[bands.index(band)]


        values = self.base["J"]["value"].strip().split(",")
        for band, value in zip(bands, values):
            data[f"ZP_{band}"] = value

        df = pd.DataFrame.from_dict({os.path.basename(self.name): data})
        return df

    def create_fits_table(self, out_table):
        """
        Create or update a FITS table from component configuration data.

        Parameters
        ----------
        out_table : str
            The path to the output FITS file. If the file already exists, it is updated with new data.
            Otherwise, a new file is created.

        Returns
        -------
        None

        Notes
        -----
        Each band is treated as a separate binary table within the FITS file (an HDU, or Header/Data Unit).
        If the file does not exist, it is created with HDUs for each band. If the file does exist, it is 
        opened for update and the existing HDUs are updated with new rows of data.

        If the existing file has a different number of HDUs than expected based on the number of bands, 
        a message is printed and no changes are made.


        Raises
        ------
        IOError
            If the out_table file path is not writable or if there's an error in opening the FITS file.
        """
        bands = self.base["A1"]["value"].strip().split(",")
        nbands = len(bands)
        data = {}
        for band in bands:
            data[band] = {}

        for component in self.components_config:
            for key in self.components_config[component]:
                col_name = remove_parentheses_and_brackets(self.components_config[component][key]["comment"])
                if "--" in col_name:
                    continue

                values = self.components_config[component][key]["col1"].strip().split(",")
                if len(values) == len(bands):
                    for band in bands:
                        col = f"{component}_{col_name}"
                        data[band]["ID"] = [self.name]
                        data[band][col] = [float(values[bands.index(band)]) + 1]

        values = self.base["J"]["value"].strip().split(",")
        for band, value in zip(bands, values):
            data[band][f"ZP"] = [float(value)]

        if not os.path.exists(out_table):
            cube = fits.HDUList([])
            for band in data:
                table = Table(data[band])
                hdu = fits.BinTableHDU(name=band, data=table)
                cube.append(hdu)
                
            cube.writeto(out_table)
        
        else:
            cube = fits.open(out_table, mode="update")
            if len(cube) == (nbands + 1):
                for key, hdu in enumerate(cube):
                    if key == 0:
                        continue
                    table = Table(cube[key].data.copy())
                    table.add_row(data[cube[key].name.lower()])             
                    cube[key] = fits.BinTableHDU(data=table, name=cube[key].name)
                cube.flush()
            else:
                control.info("Cube not compatible, different number of hdus and bands to save.")
