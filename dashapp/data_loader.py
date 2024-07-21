import geopandas as gpd
import os
import json
import pandas as pd
def load_shp(region_folder):
    base_path = os.path.dirname(os.path.abspath(__file__))
    shp_path = os.path.join(base_path, "region_data", region_folder, "nz-property-titles.shp")

    if not os.path.exists(shp_path):
        print(f"Shapefile not found at path: {shp_path}")
        return None, None

    gdf = gpd.read_file(shp_path)

    # Convert the issue_date to datetime format
    gdf['issue_date'] = pd.to_datetime(gdf['issue_date'])

    # Convert the issue_date to string format
    gdf['issue_date'] = gdf['issue_date'].dt.strftime('%Y-%m-%d')

    return gdf, json.loads(gdf.to_json())
