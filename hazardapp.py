#our eq app!

import json
import pandas as pd
import eqcalc as eqc
import xml.etree.ElementTree as et
import requests
from bs4 import BeautifulSoup
import eqcalc

def load_data(data):
    json_data = pd.json_normalize(data, record_path =['features'])
    return json_data
    
with open('shakemap_query_20221105.json','r') as f:
    data = json.loads(f.read())

eqdata = load_data(data)

#TT SF office
asset1_lat = 37.789480
asset1_lon = -122.394160

intensity_dict = dict()

for i in range(len(eqdata.index)):
    event = eqdata.iloc[i]
    event_prop_types = event["properties.types"]

    if "shakemap" in event_prop_types:
        #get intensity at asset location
        event_intensity = eqcalc.get_intensity(asset1_lat,asset1_lon,event)
        intensity_dict[event["id"]] = 1.2
    else:
        intensity_dict[event["id"]] = -1

