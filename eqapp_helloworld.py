#TT EQ app!
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import json

@st.experimental_singleton
def load_data():
    filename = 'shakemap_query_20221105.json'
    with open(filename,'r') as f:
        data = json.loads(f.read())
    eqdata = pd.json_normalize(data, record_path =['features'])
    return eqdata
    # FUNCTION FOR AIRPORT MAPS
    def map(data, lat, lon, zoom):
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
                        extruded=True,
                    ),
                ],
            )
        )


# FILTER DATA FOR A SPECIFIC HOUR, CACHE
@st.experimental_memo
def filterdata(df, threshold_magnitude):
    return df[df["properties.mag"] > threshold_magnitude]


# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
@st.experimental_memo
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))


def main():
    st.set_page_config(page_title="TT Hazard Monitor", page_icon=":volcano:")
    eqdata = load_data()
    asset_location = {"lat":37.7749, "lon":-122.4194}
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
                       max_value=12, value=6, key="pickup_hour", on_change=update_query_params)


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

    zoom_level = 12
    df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
    st.write("**San Francisco**")
    st.map(df)
    #map(filterdata(data, mag_selected), san_francisco[0], san_francisco[1], zoom_level)

    


if __name__=='__main__':
    main()
