from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = """This package will extract daily data from netCDF4 files downloaded at GES DISC database"
              Source citation: Brad Weir, Lesley Ott and OCO-2 Science Team (2022), OCO-2 GEOS Level 3 daily,
              0.5x0.625 assimilated CO2 V10r, Greenbelt, MD, USA, Goddard Earth Sciences Data
              and Information Services Center (GES DISC), Accessed: 10/31/2022,
              doi: 10.5067/Y9M4NM9MPCGH"""

# Setting up

setup(name='XCODEX',
      version=VERSION,
      author=['henriquefl24@git', "GlaucoRolim@git"],
      author_email=["<henrique.f.laurito@unesp.br>", "<glauco.rolim@unesp.br>"],
      description=DESCRIPTION,
      packages=find_packages(where='setup.py'),
      keywords=['python', 'NASA', 'GES DISC', 'XCO2', 'daily', 'OCO2', 'jupyter notebook'],
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Scientific Community",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3.9",
          "Operating System :: Unix",
          "Operating System :: MacOS :: MacOS X"
          "Operating System :: Microsoft :: Windows"
      ],
      package_dir={"": "src"},
      python_requires=">=3.9",
      install_requires=['pandas', 'numpy', 'netCDF4', 'plotly', 'jupyter']
      )
