import geopandas as gpd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import json
import dash_bootstrap_components as dbc
from flask_caching import Cache
from export_utils import export_to_shapefile
from regions import  get_region_center
import os
import plotly.graph_objects as go
from data_loader import load_shp
from layout import layout ,initial_fig_map, initial_fig_pie,initial_fig_bar# Import the layout

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Configure Caching
cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})

# Set the layout of the app
app.layout = layout

@cache.memoize(timeout=400)
def filter_data(region_selector, start_date, end_date, selected_types):
    gdf, geojson_data = load_shp(region_selector)
    
    # Filter the preloaded GeoDataFrame based on the selected date range and types
    start_date_str = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    end_date_str = pd.to_datetime(end_date).strftime('%Y-%m-%d')
    filtered_gdf = gdf[(gdf['issue_date'] >= start_date_str) & (gdf['issue_date'] <= end_date_str) & (gdf['type'].isin(selected_types))]
    
    return filtered_gdf, geojson_data

# Update dropdown options based on selected region
@app.callback(
    [Output('type-dropdown', 'options'),
     Output('date-picker', 'start_date'),
     Output('date-picker', 'end_date')],
    [Input('region-selector', 'value')]
)
def update_dropdown(region):
    if region is None:
        raise dash.exceptions.PreventUpdate
    gdf, _ = load_shp(region)
    return [{'label': t, 'value': t} for t in gdf['type'].unique()], gdf['issue_date'].min(), gdf['issue_date'].max()

# Define the callback to update the map and pie chart
@app.callback(
    [Output('auckland-map', 'figure'),
     Output('pie-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('gdf-data', 'data'),
     Output('alert', 'displayed'),
     Output('alert', 'message')],
    [Input('search-button', 'n_clicks')],
    [State('date-picker', 'start_date'),
     State('date-picker', 'end_date'),
     State('type-dropdown', 'value'),
     State('analysis', 'value'),
     State('region-selector', 'value')]
)
def update_map_and_pie_chart(n_clicks, start_date, end_date, selected_types, analysis, region_selector):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    if not selected_types:
  
        return initial_fig_map, initial_fig_pie, initial_fig_pie, None, True, "No land types selected. Please select at least one land type."

    filtered_gdf, geojson_data = filter_data(region_selector, start_date, end_date, selected_types)
    if filtered_gdf.empty :
            return initial_fig_map, initial_fig_pie, initial_fig_pie, None,False,''
    lat, lon = get_region_center(region_selector)
    
    if len(analysis)==1:
        analysis = analysis[0]
        fig_map = px.choropleth_mapbox(
            filtered_gdf,
            geojson=geojson_data,
            locations=filtered_gdf.index,
            hover_data={'id': True, 'issue_date': True, 'type': True, 'number_own': True, 'status': True},
            color=analysis,  # replace with the column you want to visualize
            center={'lat': lat, 'lon': lon},  
            mapbox_style="open-street-map",
            zoom=15,
            labels=None
        )
        fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend=None)
        fig_map.update(layout_coloraxis_showscale=False)
        fig_map.update_traces(showlegend=False)
        # Add custom legend annotations
        legend_items = []
        for i, val in enumerate(sorted(filtered_gdf[analysis].unique())):
            color = px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
            legend_items.append(f'<span style="color:{color};">■</span> {val}<br>')

        fig_map.add_annotation(
            x=0.01,
            y=0.99,
            xref='paper',
            yref='paper',
            text='<br>'.join(legend_items),
            showarrow=False,
            align='left',
            font=dict(size=12, color="black"),
            bgcolor="rgba(255, 255, 255, 0.7)",
            bordercolor="black",
            borderwidth=1,
            opacity=0.8,
            width=210    
        )

        count = filtered_gdf[analysis].value_counts().reset_index()
        count.columns = [analysis, 'count']

        if analysis == 'type':
            # Create the pie chart figure
            fig_pie = px.pie(filtered_gdf, names='type', title='Percentage of Different Types of Land')
            fig_pie.update_layout(
                paper_bgcolor='#F8EDE3',  
                plot_bgcolor='#F8EDE3'       
            )
            fig_bar = px.bar(count, x=analysis, y='count', title='Count of Land Type')
            fig_bar.update_layout(
                paper_bgcolor='#F8EDE3',  
                plot_bgcolor='#F8EDE3'       
            )
        else:
            fig_pie = px.pie(filtered_gdf, names='number_own', title='Owner Number Percentage')
            fig_pie.update_layout(
                paper_bgcolor='#F8EDE3',  
                plot_bgcolor='#F8EDE3'       
            )
            fig_bar = px.bar(count, x=analysis, y='count', title='Count of Different Owner Numbers')
            fig_bar.update_layout(
                paper_bgcolor='#F8EDE3',  
                plot_bgcolor='#F8EDE3'       
            )
    elif len(analysis) >1:
        fig_map = px.choropleth_mapbox(
            filtered_gdf,
            geojson=geojson_data,
            locations=filtered_gdf.index,
            hover_data={'id': True, 'issue_date': True, 'type': True, 'number_own': True, 'status': True},
            color=None,
            center={'lat': lat, 'lon': lon},  
            mapbox_style="open-street-map",
            zoom=15,
            labels=None
        )
        fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend=None)
        fig_map.update(layout_coloraxis_showscale=False)
        fig_map.update_traces(showlegend=False)
        fig_pie = px.histogram(filtered_gdf, x='type', color='number_own', barmode='group', title='Group Bar Plot of Owner Number within Land Types')
        fig_pie.update_layout(
            paper_bgcolor='#F8EDE3',  
            plot_bgcolor='#F8EDE3'   
        )
        fig_bar = px.density_heatmap(filtered_gdf,x='type', y='number_own', 
            title='Heatmap of Owner Number vs Land Types',
            labels={'type': 'Land Type', 'number_own': 'Owner Number'})
        fig_bar.update_layout(
            paper_bgcolor='#F8EDE3',  
            plot_bgcolor='#F8EDE3' 
        )
    else:
        
        return initial_fig_map,initial_fig_bar,initial_fig_pie,None,True,'Please select an analysis type'
        

    return fig_map, fig_pie, fig_bar, filtered_gdf.to_json(),False,None

@app.callback(
    Output('download_shp', 'data'),
    [Input('download_button', 'n_clicks')],
    [State('gdf-data', 'data')],
    prevent_initial_call=True
)
def down_data(n_clicks, gdf_json):
    if gdf_json is None:
        raise dash.exceptions.PreventUpdate

    gdf = gpd.GeoDataFrame.from_features(json.loads(gdf_json)["features"])

    shp_path = os.path.join(os.getcwd(), "exported_data.shp")
    export_to_shapefile(gdf, shp_path)
    return dcc.send_file(shp_path)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
