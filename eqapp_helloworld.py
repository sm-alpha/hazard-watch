#TT EQ app!
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import json
import plotly.express as px

@st.experimental_singleton
def load_data():
    filename = 'shakemap_query_20221105.json'
    with open(filename,'r') as f:
        data = json.loads(f.read())
    eqdata = pd.json_normalize(data, record_path =['features'])
    n_data_points = len(eqdata)
    lat = [0]*n_data_points
    lon = [0]*n_data_points
    for i, geo_coord in eqdata["geometry.coordinates"].items():
        lon[i], lat[i] = float(geo_coord[0]), float(geo_coord[1])
    
    condensed_data = eqdata[["id", "properties.place", "properties.mag"]].copy()
    condensed_data["lat"] = lat
    condensed_data["lon"] = lon
    plot_data = pd.DataFrame(zip(lat,lon), columns = ("lat","lon"))
    data_dict = {"original_data": eqdata, "latitude":lat, "longitude": lon, 
                 "condensed_data": condensed_data, "plot_data" : plot_data}
    return data_dict


# FILTER DATA FOR A SPECIFIC INTENSITY
@st.experimental_memo
def filterdata(df, threshold_magnitude):
    return df[df["properties.mag"] > threshold_magnitude]


# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
@st.experimental_memo
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))


def main():
    st.set_page_config(page_title="TT Hazard Monitor", page_icon=":volcano:")
    data_dict = load_data()
    plot_data = data_dict["plot_data"]
    condensed_data = data_dict["condensed_data"]
    #TT SF office
    asset1_lat = 37.789480
    asset1_long = -122.394160
    asset_location = {"lat":asset1_lat, "lon":-122.394160}
    #if st.checkbox('Show my shake data: '):
    #    eqdata
    #st.write("Hello world!")
       
    #for i in range(len(eqdata.index)):
    #   print(eqdata.iloc[i]["properties.mag"])
    #   print(eqdata.iloc[i]["properties.place"])


    # LAYING OUT THE TOP SECTION OF THE APP
    row1_1, row1_2 = st.columns((2, 3))

    if not st.session_state.get("url_synced", False):
        try:
            mag = int(st.experimental_get_query_params()["mag"][0])
            st.session_state["mag"] = mag
            st.session_state["url_synced"] = True
        except KeyError:
            pass

    # IF THE SLIDER CHANGES, UPDATE THE QUERY PARAM
    def update_query_params():
        threshold_magnitude = st.session_state["mag"]
        st.experimental_set_query_params(mag=threshold_magnitude)

    
    
    with row1_1:
        st.title("Thornton Tomasetti - Hazard Monitor")
        mag_selected = st.slider('Trigger Intensity - MMI (modified mercalli intensity)', min_value=1,   
                       max_value=12, value=6, key="thresh_intensity", on_change=update_query_params)


    with row1_2:
        st.write(
            """
        ##
        Assesing shake map based MMI intensities at your chosen location based on trigger magnitudes.
        By moving the slider on the left you can set different magnitudes as threshold for triggers.
        """
        )

    # SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
    san_francisco = [37.7749, -122.4194]

    
    st.write("**San Francisco**")
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=condensed_data,
                get_position='[lon, lat]',
                #get_color='[properties.mag]',
                get_radius=200,
            ),
        ],
    ))
    
    
    


if __name__=='__main__':
    main()
