
import pandas as pd
import requests
from bs4 import BeautifulSoup
import math

def get_intensity(asset_lat, asset_lon, event):
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

    for i in range(len(gd_array)):
        pt_string = gd_array[i]
        grid_pt_string_array = pt_string.split(' ')
        grid_pt_lat = float(grid_pt_string_array[1])
        grid_pt_lon = float(grid_pt_string_array[0])

        grid_pt_dist = get_distance(grid_pt_lat,grid_pt_lon,asset_lat,asset_lon)
        
        if grid_pt_dist < min_grid_pt_dist:
            min_grid_pt_dist = grid_pt_dist
            mmi = grid_pt_string_array[2]

    return mmi

def get_distance(lat1,lon1,lat2,lon2):
    earth_radius = 6371; #km
    dLat = (math.pi / 180) * (lat2 - lat1)
    dLon = (math.pi / 180) * (lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos((math.pi / 180) * lat1) * math.cos((math.pi / 180) * lat2) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.asin(math.sqrt(a))
    d = (earth_radius * c) / 1.609344;   #return value in miles
    return d


