#TT EQ app!
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk

@st.experimental_singleton
def load_data():
    filename = 'shakemap_query_20221105.json'
    with open(filename,'r') as f:
        data = json.loads(f.read())
    eqdata = pd.json_normalize(data, record_path =['features'])
    return eqdata


def main():
    st.set_page_config(layout="wide", page_title="TT EQ Monitor", page_icon=":volcano:")
    
    x = st.slider('Trigger Intensity - MMI (modified mercalli intensity)')
    eqdata = load_data()
    if st.checkbox('Show my shake data: '):
        eqdata
    #st.write("Hello world!")
       
    

    #for i in range(len(eqdata.index)):
    #    print(eqdata.iloc[i]["properties.mag"])
    #   print(eqdata.iloc[i]["properties.place"])

if __name__=='__main__':
    main()
