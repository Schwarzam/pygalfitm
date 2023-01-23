import os

class PyGalfitm:
    """PyGalfitM wrapper class. 
    """    
    def __init__(self):
        """Here we initialize the class with default values for the base and components. 

        Base values are in self.base variable 

        Components are stored in self.components_config
        """        
        self.feedme_path = "galfit.feedme"
        self.executable = "./new_tests/galfitm-1.4.4-osx"

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


    def activate_components(self, component_s = None):
        """This function is used to activate one or more components. 
        You may pass just a string with the component name, or a list. 

        If left in blank, the active components are reseted. 
        Args:
            component_s (list or str, optional): Component name or list. Defaults to None.

        Raises:
            Exception: Not valid component
        """        
        if component_s is None:
            self.activate_components = []
            return
        if isinstance(component_s, list):
            for comp in component_s:
                if comp in self.components:
                    if comp not in self.active_components:
                        self.active_components.append(comp)
                else:
                    raise Exception(f"Not valid component - {comp}")
        else:
            if component_s in self.components:
                if component_s not in self.active_components:
                    self.active_components.append(component_s)
            else:
                raise Exception(f"Not valid component - {component_s}")


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
                final = i + ") " + config[i]['col1'].ljust(35) + " " + config[i]['col2'].ljust(5) + config[i]['col3'].ljust(10) + " # " + config[i]['comment']
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

            f.write("0) " + component_name + "\n")
            for i in self.components_config[component_name]:
                final = i + ") " + config[i]['col1'].ljust(35) + " " + config[i]['col2'].ljust(5) + config[i]['col3'].ljust(10) + " # " + config[i]['comment'] + "\n"
                f.write(final)

            f.close()
    
    def run(self):
        """Run galfitm

        Returns:
            str: output of run.
        """        
        import subprocess
        output = subprocess.check_output(f'{self.executable} {self.feedme_path}', shell=True).decode("UTF-8")
        
        return output