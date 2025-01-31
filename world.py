import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide", page_title="Global Weather Conditions")

@st.cache_data
def load_data():
    return pd.read_csv('world_weather_data_with_conditions.csv')

world_weather_data = load_data()

st.title("Global Weather Conditions Dashboard")

st.sidebar.header("Filter Options")
weather_filter = st.sidebar.multiselect(
    "Select Weather Conditions",
    options=sorted(world_weather_data['main_weather'].unique()),
    default=['Rain'] 
)

if weather_filter:
    filtered_weather_data = world_weather_data[world_weather_data['main_weather'].isin(weather_filter)]
else:
    filtered_weather_data = world_weather_data

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Weather Distribution Map")
    
    color_map = {
        'Clear': [255, 255, 0],      
        'Clouds': [128, 128, 128],   
        'Rain': [0, 191, 255],      
        'Snow': [255, 255, 255],     
        'Drizzle': [0, 255, 255],    
        'Fog': [169, 169, 169]       
    }

    layers = []
    for condition in weather_filter:
        if condition in color_map:
            condition_data = filtered_weather_data[filtered_weather_data['main_weather'] == condition]
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=condition_data,
                get_position="[LONG, LAT]",
                get_color=color_map[condition],
                get_radius=50000,
                pickable=True,
                opacity=0.8
            )
            layers.append(layer)

    view_state = pdk.ViewState(
        latitude=filtered_weather_data['LAT'].mean(),
        longitude=filtered_weather_data['LONG'].mean(),
        zoom=1.5
    )

    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={"text": "{Country}\n{main_weather}\n{weather_description}"}
    )

    st.pydeck_chart(deck)

    st.write("Weather Condition Colors:")
    legend_cols = st.columns(len(weather_filter))
    for i, condition in enumerate(weather_filter):
        with legend_cols[i]:
            color = color_map[condition]
            st.markdown(
                f'<div style="background-color: rgb({color[0]}, {color[1]}, {color[2]}); '
                f'padding: 10px; border-radius: 5px; text-align: center;">'
                f'{condition}</div>',
                unsafe_allow_html=True
            )

with col2:
    st.subheader("Weather Data Table")
    
    search = st.text_input("Search for a country:", "")
    
    display_df = filtered_weather_data
    if search:
        display_df = display_df[
            display_df['Country'].str.contains(search, case=False)
        ]

    st.dataframe(
        display_df[['Country', 'main_weather', 'weather_description']],
        height=400
    )
    
    st.subheader("Weather Statistics")
    weather_counts = filtered_weather_data['main_weather'].value_counts()
    st.write("Number of countries by selected weather condition(s):")
    st.bar_chart(weather_counts)

    total_countries = len(filtered_weather_data)
    st.write(f"Total countries with selected weather condition(s): {total_countries}")

st.markdown("---")
st.markdown("Data source: OpenWeatherMap API")