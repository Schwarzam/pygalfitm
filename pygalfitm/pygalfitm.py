import os

import os

class PyGalfitm:
    def __init__(self):
        self.feedme_path = "galfit.feedme"

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
                "5":  {"col1": "0,0,0", "col2": "2", "col3": "band", "comment": "Sersic index n (de Vaucouleurs n=4)"},
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
        if component_s is None:
            self.activate_components = []
        if isinstance(component_s, list):
            for comp in component_s:
                if comp in self.components:
                    if comp not in self.active_components:
                        self.active_components.append(comp)
                else:
                    raise Exception(f"Not valid component - {comp}")
        else:
            if component_s in self.components:
                if component_s not in self.activate_components:
                    self.active_components.append(component_s)
            else:
                raise Exception(f"Not valid component - {comp}")


    def set_base(self, item, value):
        if item in self.base:
            self.base[item]["value"] = value
        else:
            raise KeyError("Parameter not found in galfitm feedme base config.")
    
    def set_component(self, component, item, value, column = 1):
        if column in [1, 2, 3]:
            column = 'col' + str(column)
        else:
            raise Exception("Column not valid.")
        if component in self.components_config:
            if item in self.components_config[component]:
                self.components_config[component][item][column] = value
        else:
            raise KeyError("Component not found.")


    def write_feedme(self, feedme_path = None):
        if feedme_path is None:
            feedme_path = self.feedme_path
        self.write_base(feedme_path)

        for component in self.active_components:
            self.write_component(component, feedme_path)
    
    def print_component(self, component):
        config = self.components_config[component]
        if component in self.components_config:
            for i in self.components_config[component]:
                final = i + ") " + config[i]['col1'].ljust(35) + " " + config[i]['col2'].ljust(5) + config[i]['col3'].ljust(10) + " " + config[i]['comment']
                print(final)
        else:
            raise KeyError("Component not found.")


    def write_base(self, feedme_path = None):
        if feedme_path is None:
            feedme_path = self.feedme_path
        file = open(feedme_path, "w")
        for param in self.base:
            final = str(param) + ") " + str(self.base[param]["value"]).ljust(32) + "# " + str(self.base[param]["comment"]) + "\n"
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
                final = i + ") " + config[i]['col1'].ljust(35) + " " + config[i]['col2'].ljust(5) + config[i]['col3'].ljust(10) + " " + config[i]['comment'] + "\n"
                f.write(final)

            f.close()
    
    