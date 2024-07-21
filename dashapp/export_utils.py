import geopandas as gpd
import pandas as pd

def export_to_csv(gdf, filepath):
    """Export GeoDataFrame to CSV."""
    gdf.to_csv(filepath, index=False)
    print(f"Data exported to CSV at {filepath}")

def export_to_shapefile(gdf, filepath):
    """Export GeoDataFrame to Shapefile."""
    gdf.to_file(filepath, driver='ESRI Shapefile')
    print(f"Data exported to Shapefile at {filepath}")
