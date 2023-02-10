from pygalfitm import PyGalfitm

from astropy.io import fits

def read_output_to_class(filename):
    out = open(filename, "r").read()

    base = {}
    components = {}

    in_base = True
    in_current_component = ""

    current_component = ""
    
    for line in out.split("\n"):
        line.lstrip().split(" ")[0].replace(")", "")
        
        letter = line.lstrip().split(" ")[0].replace(")", "")
        
        if letter == "" or letter == "#" or len(letter) > 3:
            continue
            
        if letter == "0":
            [_, line_rest] = line.lstrip().split(" ", 1)
            [current_component, line_rest] = line_rest.split(" ", 1)
            
            if current_component in components:
                counter = 0
                for comp in components:
                    if current_component in comp:
                        counter += 1

                if counter != 0:
                    in_current_component = current_component + str(counter)
            else:
                in_current_component = current_component

            components[in_current_component] = {}
            in_base = False

        
        if in_base:
            base[letter] = {}

            [_, line_rest] = line.lstrip().split(" ", 1)
            [value, line_rest] = line_rest.lstrip().split("#", 1)
            comment = line_rest.lstrip().strip().strip("#")

            base[letter]['value'] = value
            base[letter]['comment'] = comment

        else:
            if letter == "0":
                continue
            [_, line_rest] = line.lstrip().split(" ", 1)
            [col1, line_rest] = line_rest.lstrip().split(" ", 1)
            [col2, line_rest] = line_rest.lstrip().split(" ", 1)
            [col3, line_rest] = line_rest.lstrip().split(" ", 1)
            comment = line_rest.lstrip().strip().strip("#")[1:]

            components[in_current_component][letter] = {}

            components[in_current_component][letter]["col1"] = col1
            components[in_current_component][letter]["col2"] = col2
            components[in_current_component][letter]["col3"] = col3
            components[in_current_component][letter]["comment"] = comment

        pyg = PyGalfitm()
        pyg.base = base
        pyg.components_config = components

    return pyg