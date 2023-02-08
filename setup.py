import setuptools

setuptools.setup(
     name='pygalfitm',
     version='0.1',
     packages = setuptools.find_packages(),
     author="Gustavo Schwarz",
     author_email="gustavo.b.schwarz@gmail.com",
     description="Python3 GalfitM wrapper",
     url="https://github.com/schwarzam/pygalfitm",
     install_requires = ['astropy', 'pandas', 'numpy', 'requests'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: Apache Software License"
     ],
 )
#python3 setup.py bdist_wheel
#python3 -m twine upload dist/*