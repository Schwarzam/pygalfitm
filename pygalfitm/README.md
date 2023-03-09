<a id="pygalfitm"></a>

# pygalfitm

<a id="pygalfitm.PyGalfitm"></a>

## PyGalfitm Objects

```python
class PyGalfitm()
```

PyGalfitM wrapper class.

<a id="pygalfitm.PyGalfitm.__init__"></a>

#### \_\_init\_\_

```python
def __init__(executable=os.path.join(pygalfitm.__path__[0], "galfitm"))
```

Here we initialize the class with default values for the base and components.

Base values are in self.base variable 

Components are stored in self.components_config

<a id="pygalfitm.PyGalfitm.activate_components"></a>

#### activate\_components

```python
def activate_components(component_s: list = None)
```

This function is used to activate one or more components.
You may pass just a string with the component name, or a list.

If left in blank, the active components are reseted.

**Arguments**:

- `component_s` _list or str, optional_ - Component name or list. Defaults to None.
  

**Raises**:

- `Exception` - Not valid component

<a id="pygalfitm.PyGalfitm.set_base"></a>

#### set\_base

```python
def set_base(item, value="")
```

Function used to alter base values.
It's possible to pass only one value by giving the item and value to alter, or a dict with all keys and respective values.

Ex:
p.set_base("A1", "X")
p.set_base("B", "Y")

p.set_base({
"A1": X
"B": Y
"C": Z
})

**Arguments**:

- `item` _str or dict_ - str of item name, or dict with infos.
- `value` _str, optional_ - value referred to item name. Defaults to "".
  

**Raises**:

- `KeyError` - Parameter not valid

<a id="pygalfitm.PyGalfitm.set_component"></a>

#### set\_component

```python
def set_component(component, item, value=None, column=1)
```

Function used to alter component values
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

**Arguments**:

- `component` _str_ - component name
- `item` _str or dict_ - item to change or dict with all infos.
- `value` _str_ - Value referred in item (just used in case item is str).
- `column` _int, optional_ - Select column of change, 1, 2 or 3. Defaults to 1.
  

**Raises**:

- `Exception` - Component not found.

<a id="pygalfitm.PyGalfitm.write_feedme"></a>

#### write\_feedme

```python
def write_feedme(feedme_path=None)
```

Writes final feedme

**Arguments**:

- `feedme_path` _str, optional_ - file path, if none select default file path. Defaults to None.

<a id="pygalfitm.PyGalfitm.print_component"></a>

#### print\_component

```python
def print_component(component)
```

Prints selected component to visualize informations

**Arguments**:

- `component` _str_ - component name
  

**Raises**:

- `KeyError` - Component not found.

<a id="pygalfitm.PyGalfitm.print_base"></a>

#### print\_base

```python
def print_base()
```

Prints base params to visualize informations

<a id="pygalfitm.PyGalfitm.check_number_of_filters"></a>

#### check\_number\_of\_filters

```python
def check_number_of_filters()
```

Check parameter by parameter from active components that have correct number of bands.

<a id="pygalfitm.PyGalfitm.run"></a>

#### run

```python
def run()
```

Run galfitm

**Returns**:

- `str` - output of run.

<a id="pygalfitm.PyGalfitm.gen_plot"></a>

#### gen\_plot

```python
def gen_plot(component_selected="sersic",
             plot_parameters=[],
             plotsize_factor=(1, 1),
             colorbar=True,
             lupton_stretch=0.2,
             lupton_q=8,
             fig_filename=None,
             return_plot=False,
             **kwargs)
```

Generate a plot to visualize the input, model, and residual data of a PyGalfit model.

**Arguments**:

  - pygalfit (object): the PyGalfit model object, which contains the input and output data from the PyGalfit fitting.
  - component_selected (str): the name of the PyGalfit component to plot (default is "sersic").
  - plot_parameters (List[str]): a list of parameters to plot for the selected component (default is an empty list).
  - plotsize_factor (Tuple[float, float]): a tuple specifying the size of the plot, default is (1,1).
  - colorbar (bool): a boolean indicating whether to show the color bar on the plot (default is True).
  - lupton_stretch (float): a float specifying the stretch factor used for the Lupton RGB image (default is 0.2).
  - lupton_q (int): an integer specifying the Q factor used for the Lupton RGB image (default is 8).
  - fig_filename (str): a string specifying the filename to save the plot to (default is None).
  - return_plot (bool): a boolean indicating whether to return the plot object instead of showing it (default is False).
  

**Returns**:

  - fig (plt.Figure): the matplotlib Figure object, only if `return_plot` is True.

