# Global Weather Conditions Dashboard

An interactive dashboard built with Streamlit that visualizes global weather conditions using maps, charts, and filterable data tables.

## Features

- Interactive world map showing weather conditions
- Color-coded weather visualization
- Filterable weather conditions
- Country search functionality
- Weather statistics and charts
- Responsive layout with side-by-side displays

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Tenkris/weather-application
cd weather-dashboard
```

2. Create and activate a virtual environment:

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Requirements.txt Content

Create a `requirements.txt` file with the following dependencies:

```
streamlit>=1.20.0
pandas>=1.5.0
pydeck>=0.8.0
```

## Data Requirements

The application expects a CSV file named `world_weather_data_with_conditions.csv` in the project root directory with the following columns:

- Country
- LAT (Latitude)
- LONG (Longitude)
- main_weather
- weather_description

## Running the Application

1. Ensure your virtual environment is activated
2. Run the Streamlit application:

```bash
streamlit run app.py
```

3. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Usage

1. Use the sidebar to filter weather conditions
2. Interact with the map to view specific location details
3. Search for countries using the search bar
4. View weather statistics in the right panel
5. Examine the detailed data table for specific information

## Map Color Coding

- Clear: Yellow
- Clouds: Gray
- Rain: Deep Sky Blue
- Snow: White
- Drizzle: Cyan
- Fog: Dark Gray

## Data Source

Weather data is sourced from the OpenWeatherMap API. Ensure you have the required CSV file with up-to-date weather information before running the application.

## Contributing

Feel free to submit issues and pull requests to improve the dashboard.
