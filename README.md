# pygalfitm

Pygalfitm is a Python package that provides an interface to run the GALFITM software, a widely used tool in astrophysics for fitting 2D surface brightness distributions of galaxies. Pygalfitm simplifies the process of preparing input files, running GALFITM, and post-processing the output results.

Pygalfitm is built on top of the Python subprocess module, which allows for easy integration with other Python packages, such as Numpy and Matplotlib. It provides a set of classes and functions to define the GALFITM input parameters and run the fitting process, as well as a set of utilities to visualize the results.

The Pygalfitm class provides an easy-to-use interface to interact with the GALFITM software. It includes functions to activate and set component parameters, write the input files, and run GALFITM. Additionally, it provides a function to generate plots to visualize the input, model, and residual data of the fitted galaxy.

Pygalfitm can be installed using pip:

### Examples

A good example of how it works is inside **example.ipynb** and **example-splus** notebook.

There is also a folder with some usefull scripts inside dev/scripts (working with tables and so on...)

```
python3 setup.py build

python3 setup.py install
```

#### Check out GALFITM page

https://www.nottingham.ac.uk/astronomy/megamorph/

#### Contributing

Contributions are welcome and greatly appreciated.

#### LICENSE 

Pygalfitm is distributed under the MIT License.