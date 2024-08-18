[![logo-gas-removebg-preview.png](https://i.postimg.cc/gjptBxF4/logo-gas-removebg-preview.png)](https://postimg.cc/vgPv4Hm6)

### *Please, cite this package as:*

Laurito, H., La Scala, N., Rolim, G. S., 2023. Extracting XCO2-NASA Daily data with XCODEX:
A Python package designed for data extraction and structuration. Jaboticabal, SP, BR, (...)

# **Welcome to XCODEX - XCO2 Daily EXtractor**

Hi there! My name is Henrique.

The creation of this Python package was intended to create a simple solution for extracting daily data from XCO2 retrieved from the GES DISC platform.

I will attach the links containing the GitHub profile of the researchers who helped me in the development of this package along with graphical visualization of the data and the citation of the OCO-2 project.

I hope it's useful to you. **Long live science!**

## *Installing the package*

To install the package, use the command:
```angular2html
pip install xcodex
```
## *Using XCODEX*

There's the possibility to download the .nc4 files directly here:
```angular2html
# Setting historical serie

from xcodex.main import download_file

start_date = "1st of January, 2022"
end_date = "31st of January, 2022"

# Downloading .nc4 files
download_file(start_date, end_date) 
```
__Note that ERROR 401 usually is related to unavailable data.__

Once the download is completed, a ``downloaded_data`` folder will be created in your current path.
<br>After that, let's use ``xco2_extract()`` to retrieve XCO2 data from the .nc4 files:
<br> 

```angular2html
from glob import glob
from os.path import join
from os import getcwd

# Selecting the folder with .nc4 files

arquive_folder = glob(join(getcwd(), "downloaded_data", "*.nc4")) 

# Setting desired locations to build a time series XCO2 data

locations = dict(Mauna_loa=[19.479488, -155.602829],
                 New_York=[40.712776, -74.005974],
                 Paris=[48.856613, 2.352222])

from xcodex.main import xco2_extract

df = xco2_extract(path=arquive_folder,
                  start=start_date,
                  end=end_date,
                  missing_data=False,
                  **locations); df # Extracting XCO2
      
```
Note1: The location used in this example was Mauna Loa, New York and Paris. Any location can be used<br>
as long the format "Location[lat, lon]" is respected. The values of <br>
latitude and longitude must be in decimal degrees.

for more information, please execute the command: <br>

````angular2html
help(xco2_extractor)
````

Finally, you will have a `pandas.Dataframe` as result. Now it's up to you how you'll <br>
handle it. I recomend checking the `Github profiles` below for data visualization.

### Data visualization
Here we can plot in a map the locations:
````angular2html
## set mapbox access token

import plotly.express as px
import plotly.graph_objs as go

px.set_mapbox_access_token('pk.eyJ1Ijoic2FnYXJsaW1idTAiLCJhIjoiY2t2MXhhMm5mNnE5ajJ3dDl2eDZvNTM2NiJ9.1bwmb8HPgFZWwR8kcO5rOA')

# Plotly configs

fig= px.scatter_mapbox(df,
                              lat= 'lat',
                              lon= 'lon',
                              color= 'xco2',
                              zoom= .85,
                              width=960,
                              height=540,
                              size_max=10,
                              hover_name='city',
                              color_continuous_scale=px.colors.cyclical.IceFire)

fig.update_layout(mapbox_style="dark") #"open-street-map"


layout = go.Layout(margin=go.layout.Margin(
    l=0,
    r=0,
    b=0,
    t=0))


fig.update_layout(layout,
                  autosize=False,
                  height=540,
                  width=960,
                  hovermode="closest")

# Saving the output image

#fig.write_html('xcodex_map.html')
#fig.write_image("xcodex_map.png", scale=2)

fig.show()
````
And finally a way to observe the XCO2 behavior during the time serie:
````angular2html
# Showing XCO2 behavior in time serie

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10,5))

sns.set_theme(font_scale=1, style="white")

sns.lineplot(data=df,
             x="jd",
             y='xco2',
             hue='city',
             errorbar=('ci',0),
             palette="tab10")

plt.xlabel("")
plt.ylabel("XCO2 (ppm)")

plt.xlim(min(df.jd), max(df.jd))
plt.ylim(min(df.xco2), max(df.xco2))

sns.despine(right=False,
            top=False)

plt.legend(ncol=3)

plt.tight_layout()

#plt.savefig("xcodex_locations.png", dpi=300)

plt.show()
````
### *GitHub profiles*:

https://github.com/GlaucoRolim (Co-author) <br>
https://github.com/kyuenjpl/ARSET_XCO2 <br>
https://github.com/sagarlimbu0/OCO2-OCO3

### **Data source citation**:

Brad Weir, Lesley Ott and OCO-2 Science Team (2022), OCO-2 GEOS Level 3 daily,
0.5x0.625 assimilated CO2 V10r, Greenbelt, MD, USA, Goddard Earth Sciences Data
and Information Services Center (GES DISC), Accessed: 10/31/2022,
doi: 10.5067/Y9M4NM9MPCGH
