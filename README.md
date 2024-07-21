# Auckland Development Map Dashboard

This project is a web-based dashboard built with Dash and Plotly to visualize property data in different regions of Auckland. The dashboard allows users to select date ranges, regions, land types, and analysis types to generate interactive maps and charts. The data can also be downloaded in Shapefile format.

## Features

- **Interactive Map**: Visualize property data on an interactive map.
- **Date Range Selector**: Filter data based on selected date ranges.
- **Region Selector**: Choose different regions of Auckland to view specific data. (Only avaliable for Bucklands Beach and Highland Park)
- **Land Type Selector**: Filter data by land types.
- **Analysis Types**: Select between different analysis types (Land Type, Owner Number).
- **Dynamic Graphs**: Display bar charts, pie charts, and heatmaps based on selected analysis types.
- **Data Download**: Export filtered data as a Shapefile.

## Project Structure
```text
.
├── app.py # Main application script
├── callbacks.py # Callback functions for interactivity
├── data_loader.py # Functions to load and process data
├── export_utils.py # Utility functions for exporting data
├── layout.py # Layout definition for the dashboard
├── regions.py # Functions to handle region data
├── assets
│ └── style.css # Custom CSS styles
├── region_data # Directory containing region-specific data
│ ├── Bucklands_Beach
│ │ └── nz-property-titles.shp
│ ├── Highland_Park
│ │ └── nz-property-titles.shp
│ └── ... # Other regions
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```
### Prerequisites

- Python 3.7 or higher
- `pip` package manager

