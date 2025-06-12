# pygalfitm

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15648590.svg)](https://doi.org/10.5281/zenodo.15648590)

**Pygalfitm** is a Python package that provides an interface to run the GALFITM software, a widely used tool in astrophysics for fitting 2D surface brightness distributions of galaxies. Pygalfitm simplifies the process of preparing input files, executing GALFITM, and post-processing the output results.

The package is built on top of Python’s `subprocess` module and integrates easily with libraries such as NumPy and Matplotlib. It includes tools to define GALFITM input parameters, run the fitting process, and generate visualizations of the input, model, and residual images.

## Installation

Using pip:

```bash
pip3 install pygalfitm
````

Or from source:

```
python3 setup.py build
python3 setup.py install
```

## Examples

Usage examples are provided in:
	•	example.ipynb – basic usage example
	•	example-splus.ipynb – application to S-PLUS data
	•	dev/scripts/ – utility scripts for working with tables and batch processing

## Citation

If you use pygalfitm in your work, citation is optional but appreciated. You may cite it as:

@software{pygalfitm_software,
  author       = {Oliveira Schwarz, G. B. and
                  Cortesi, A. and
                  Okiyama, L.},
  title        = {pygalfitm},
  month        = feb,
  year         = 2023,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.15648590},
  url          = {https://doi.org/10.5281/zenodo.15648590}
}

Please also cite the original GALFITM software if you use this interface:

Bamford, S. P., Häußler, B., Rojas, A. L., Borch, A., et al. (2011).
MegaMorph: multi-wavelength measurement of galaxy structure with GALFITM.
MNRAS, 427, 138.

GALFITM is developed by the MegaMorph project. For more information, visit:
https://www.nottingham.ac.uk/astronomy/megamorph/

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome and appreciated.