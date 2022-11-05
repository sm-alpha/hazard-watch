#our eq app!

import json
import pandas as pd



def load_data(data):
    json_data = pd.json_normalize(data, record_path =['features'])
    return json_data
    
with open('shakemap_query_20221105.json','r') as f:
    data = json.loads(f.read())

eqdata = load_data(data)

for i in range(len(eqdata.index)):
    print(eqdata.iloc[i]["properties.mag"])
    print(eqdata.iloc[i]["properties.place"])