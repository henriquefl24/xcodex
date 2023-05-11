![](logo_gas.jpg) <br>

# **Welcome to XCODEX - XCO2 Daily EXtractor**

Hi there! My name is Henrique.

The creation of this Python package was intended to create a simple solution for extracting daily data from XCO2 retrieved from the GES DISC platform.

I will attach the links containing the GitHub profile of the researchers who helped me in the development of this package along with graphical visualization of the data and the citation of the OCO-2 project.

I hope it's useful to you. **Long live science!**

## *Instaling the package*

To install the package, use the command:

<br>`pip install xcodex`


## *Using XCODEX*

First of all, import these two libraries
```
import pandas as pd
from glob import glob
from xcodex import xco2_extract`
```

```
arquive_folder = glob(r"path\to\file\...\*.nc4"))

df = xco2_extract(
                  path=arquive_folder,
                  start="1st of January, 2015",
                  end=365,
                  missing_data=True,
                  Mauna_Loa=[19.479488, -155.602829]
                  )
                  
df.to_excel("article_ptI.xlsx") # Save to a Dataframe if you will                 
```
Note1: The location used in this example was Mauna Loa. Any location can be used<br>
as long the format "Location[lat, lon]" is respected. The values of <br>
latitude and longitude must be in decimal degrees.

for more information, please execute the command: <br>

`help(xco2_extractor)`

Finally, you will have a `pandas.Dataframe` as result. Now it's up to you how you'll <br>
handle it. I recomend checking the `Github profiles` below for data visualization.

### *GitHub profiles*:

https://github.com/GlaucoRolim (Co-author) <br>
https://github.com/kyuenjpl/ARSET_XCO2 <br>
https://github.com/sagarlimbu0/OCO2-OCO3

### *Please, cite this package as:*

Laurito, H., Rolim, G., 2023. Extracting XCO2-NASA Daily data with XCODEX:
A Python package designed for data extraction and structuration.<br>
Jaboticabal, SP, BR, Computers and Electronics in Agriculture,
Accessed: dd/mm/yyyy,
doi:

### **Data source citation**:

Brad Weir, Lesley Ott and OCO-2 Science Team (2022), OCO-2 GEOS Level 3 daily,
0.5x0.625 assimilated CO2 V10r, Greenbelt, MD, USA, Goddard Earth Sciences Data
and Information Services Center (GES DISC), Accessed: 10/31/2022,
doi: 10.5067/Y9M4NM9MPCGH
