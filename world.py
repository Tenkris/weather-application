# import streamlit as st
# import pandas as pd
# import pydeck as pdk


# st.set_page_config(layout="wide", page_title="Global Weather Conditions")

# @st.cache_data   
# def load_data():
#     return pd.read_csv('world_weather_data_with_conditions.csv')

# world_weather_data = load_data()

# st.title("Global Weather Conditions Dashboard")

# col1, col2 = st.columns([2, 1])

# with col1:
#     st.subheader("Weather Distribution Map")
    
#     color_map = {
#         'Clear': [255, 255, 0],      
#         'Clouds': [128, 128, 128],   
#         'Rain': [0, 0, 255],         
#         'Snow': [255, 255, 255],     
#         'Drizzle': [0, 255, 255],    
#         'Fog': [169, 169, 169]      
#     }

#     # Create a list of layers for each weather condition
#     layers = []
#     for condition, color in color_map.items():
#         condition_data = world_weather_data[world_weather_data['main_weather'] == condition]
#         layer = pdk.Layer(
#             "ScatterplotLayer",
#             data=condition_data,
#             get_position="[LONG, LAT]",
#             get_color=color,
#             get_radius=50000,
#             pickable=True,
#             opacity=0.8
#         )
#         layers.append(layer)

#     # Set the initial view state
#     view_state = pdk.ViewState(
#         latitude=world_weather_data['LAT'].mean(),
#         longitude=world_weather_data['LONG'].mean(),
#         zoom=1.5
#     )

#     # Create the deck
#     deck = pdk.Deck(
#         layers=layers,
#         initial_view_state=view_state,
#         tooltip={"text": "{Country}\n{main_weather}\n{weather_description}"}
#     )

#     # Render the deck
#     st.pydeck_chart(deck)

#     # Add legend
#     st.write("Weather Condition Colors:")
#     legend_cols = st.columns(len(color_map))
#     for i, (condition, color) in enumerate(color_map.items()):
#         with legend_cols[i]:
#             st.markdown(
#                 f'<div style="background-color: rgb({color[0]}, {color[1]}, {color[2]}); '
#                 f'padding: 10px; border-radius: 5px; text-align: center;">'
#                 f'{condition}</div>',
#                 unsafe_allow_html=True
#             )

# with col2:
#     st.subheader("Weather Data Table")
    
#     search = st.text_input("Search for a country:", "")
    
#     if search:
#         filtered_df = world_weather_data[
#             world_weather_data['Country'].str.contains(search, case=False)
#         ]
#     else:
#         filtered_df = world_weather_data

#     st.dataframe(
#         filtered_df[['Country', 'main_weather', 'weather_description']],
#         height=400
#     )
    
#     st.subheader("Weather Statistics")
#     weather_counts = world_weather_data['main_weather'].value_counts()
#     st.write("Number of countries by weather condition:")
#     st.bar_chart(weather_counts)

# st.markdown("---")
# st.markdown("Data source: OpenWeatherMap API")

import streamlit as st
import pandas as pd
import pydeck as pdk

# Set page configuration
st.set_page_config(layout="wide", page_title="Global Weather Conditions")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv('world_weather_data_with_conditions.csv')

world_weather_data = load_data()

# Main title
st.title("Global Weather Conditions Dashboard")

# Sidebar for filtering
st.sidebar.header("Filter Options")
weather_filter = st.sidebar.multiselect(
    "Select Weather Conditions",
    options=sorted(world_weather_data['main_weather'].unique()),
    default=['Rain']  # Default to showing rain
)

# Filter data based on selected weather conditions
if weather_filter:
    filtered_weather_data = world_weather_data[world_weather_data['main_weather'].isin(weather_filter)]
else:
    filtered_weather_data = world_weather_data

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Weather Distribution Map")
    
    color_map = {
        'Clear': [255, 255, 0],      # Yellow
        'Clouds': [128, 128, 128],   # Gray
        'Rain': [0, 0, 255],         # Blue
        'Snow': [255, 255, 255],     # White
        'Drizzle': [0, 255, 255],    # Cyan
        'Fog': [169, 169, 169]       # Dark Gray
    }

    # Create layers only for selected weather conditions
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

    # Set the initial view state
    view_state = pdk.ViewState(
        latitude=filtered_weather_data['LAT'].mean(),
        longitude=filtered_weather_data['LONG'].mean(),
        zoom=1.5
    )

    # Create the deck
    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={"text": "{Country}\n{main_weather}\n{weather_description}"}
    )

    # Render the deck
    st.pydeck_chart(deck)

    # Add legend for selected weather conditions
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
    
    # Add a search box for filtering countries
    search = st.text_input("Search for a country:", "")
    
    # Filter the dataframe based on search
    display_df = filtered_weather_data
    if search:
        display_df = display_df[
            display_df['Country'].str.contains(search, case=False)
        ]

    # Display the filtered table
    st.dataframe(
        display_df[['Country', 'main_weather', 'weather_description']],
        height=400
    )
    
    # Display weather statistics for filtered data
    st.subheader("Weather Statistics")
    weather_counts = filtered_weather_data['main_weather'].value_counts()
    st.write("Number of countries by selected weather condition(s):")
    st.bar_chart(weather_counts)

    # Display total count
    total_countries = len(filtered_weather_data)
    st.write(f"Total countries with selected weather condition(s): {total_countries}")

# Footer
st.markdown("---")
st.markdown("Data source: OpenWeatherMap API")