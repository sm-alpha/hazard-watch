
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_intensity(lat, long, event):
    prop_detail = pd.read_json(event["properties.detail"])
    url = prop_detail["properties"]["products"]["shakemap"][0]["contents"]["download/grid.xml"]["url"]
    s = requests.get(url).content
    shakemap_xml = BeautifulSoup(s)
    
    gd = shakemap_xml("grid_data")
    gd_array = gd[0].text.split('\n')

    del gd_array[0]
    del gd_array[-1]

    min_grid_pt_dist = 100000.00
    mmi = 0

    for i in range(len(gd_array.index)):
        

    return 0


