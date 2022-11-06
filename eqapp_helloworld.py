#TT EQ app!
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import json
import eqcalc

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
        lon[i], lat[i] = geo_coord[0], geo_coord[1]
    
    condensed_data = eqdata[["id", "properties.place", "properties.mag"]].copy()
    condensed_data["lat"] = lat
    condensed_data["lon"] = lon
    plot_data = pd.DataFrame(zip(lat,lon), columns = ("lat","lon"))
    data_dict = {"original_data": eqdata, "latitude":lat, "longitude": lon, 
                 "condensed_data": condensed_data, "plot_data" : plot_data}
    return data_dict

def plot_map(data, lat, lon, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["lon", "lat"],
                    radius=100,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=False,
                ),
            ],
        )
    )


# FILTER DATA FOR A SPECIFIC INTENSITY
@st.experimental_memo
def filterdata(condensed_data, threshold_intensity):
    return condensed_data[condensed_data["intensities"] > threshold_intensity]


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
    asset1_lon = -122.394160
    asset_location = {"lat":asset1_lat, "lon":-122.394160}

    intensity_dict = dict()
    eqdata = data_dict["original_data"]
    for i in range(len(eqdata.index)):
        event = eqdata.iloc[i]
        event_prop_types = event["properties.types"]

        if "shakemap" in event_prop_types:
            #get intensity at asset location
            event_intensity = eqcalc.get_intensity(asset1_lat,asset1_lon,event)
            intensity_dict[event["id"]] = event_intensity
        else:
            intensity_dict[event["id"]] = -1
       
    # LAYING OUT THE TOP SECTION OF THE APP
    row1_1, row1_2 = st.columns((2, 3))

    if not st.session_state.get("url_synced", False):
        try:
            x = int(st.experimental_get_query_params()["intensity"][0])
            st.session_state["intensity"] = x
            st.session_state["url_synced"] = True
        except KeyError:
            pass

    # IF THE SLIDER CHANGES, UPDATE THE QUERY PARAM
    def update_query_params():
        intensity_selected = st.session_state["intensity"]
        st.experimental_set_query_params(intensity=intensity_selected)
   
    
    with row1_1:
        st.title("Thornton Tomasetti - Hazard Monitor")
        intensity_selected = st.slider('Trigger Intensity - MMI (modified mercalli intensity)', min_value=1,   
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

    zoom_level = 7
    #df = pd.DataFrame(plot_data,columns=['lat', 'lon'])
    st.write("**San Francisco**")
    st.map(plot_data, zoom = zoom_level)
    #map(filterdata(data, mag_selected), san_francisco[0], san_francisco[1], zoom_level)
    if st.checkbox('Show my shake data: '):
        condensed_data
        


if __name__=='__main__':
    main()
