from dash import dcc, html
import dash_bootstrap_components as dbc
from regions import extract_region
# Create placeholder figure
import plotly.graph_objects as go

def create_placeholder_figure():
    fig = go.Figure()
    # Add center text
    fig.add_annotation(
        x=0.5, y=0.5,
        xref='paper', yref='paper',
        text="Graph",
        showarrow=False,
        font=dict(size=20)
    )

    fig.update_layout(
        paper_bgcolor='#F8EDE3',  # Set the background color for the entire figure
        plot_bgcolor='#F8EDE3', 
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig

# Initial placeholder figures
initial_fig_pie = create_placeholder_figure()
initial_fig_bar = create_placeholder_figure()

# Initial map figure
import plotly.express as px
initial_fig_map = px.choropleth_mapbox(
    center={"lat": -36.8485, "lon": 174.7633},
    mapbox_style="open-street-map",
    zoom=15
)
initial_fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

layout = dbc.Container([
    
    dcc.Store(id='gdf-data'),  # Store the GeoDataFrame
    dcc.ConfirmDialog(
        id='alert',
        message='',
    ),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Auckland Development Map", id='title'),
                html.Div([
                html.Label("Select Date Range:"),
                dcc.DatePickerRange(
                    id='date-picker',
                    start_date_placeholder_text="Start Period",
                    end_date_placeholder_text="End Period",
                    display_format='YYYY-MM-DD'
                )],id = 'first_container'),
                html.Div([
                html.Label("Select Region"),
                dcc.Dropdown(
                    id='region-selector',
                    options=extract_region(),
                    value='Bucklands Beach'
                )],id = 'second_container'),
                html.Div([
                html.Label("Select Land Types:"),
                dcc.Dropdown(
                    id='type-dropdown',
                    options=[],
                    value=[],
                    multi=True
                )],id = 'third_container'),
                html.Div([
                
                html.Label("Select Analysis Types:"),
                dcc.Checklist(
                    id='analysis',
                    options=[
                        {'label': 'Land Type', 'value': 'type'},
                        {'label': 'Owner Number', 'value': 'number_own'}
                    ],
                    value=['type'],
                    labelStyle={'display': 'inline-block'},
                    className='analysis-radioitems'
                ),
                html.Span("?", id="tooltip-target", className="tooltip-button"),
                dbc.Tooltip(
                    "Select one analysis type, there would be a pie chart and bar chart. Select two analysis types, there would be a heatmap and group bar chart",
                    target="tooltip-target",
                    placement="right"
                ),
                ], id='fourth_container'),
                html.Div([
                    html.Button("Search", id='search-button'),
                    html.Button("Download Data", id="download_button")
                ], style={'display': 'flex', 'justify-content': 'space-between'}),
                dcc.Download(id="download_shp")
                

            ]),
            
        ], id = 'side_bar',width=3),
        dbc.Col([
            dcc.Loading(
                id='loading_auckland_map',
                children=dcc.Graph(id='auckland-map', figure=initial_fig_map),
                
            ),
            dcc.Loading(
                children=html.Div(id="chart-wrapper", children=[
                    dcc.Graph(id='pie-chart', figure=initial_fig_pie, style={'display': 'inline-block', 'width': '50%'}),
                             
                    dcc.Graph(id='bar-chart', figure=initial_fig_pie, style={'display': 'inline-block', 'width': '50%'})
                ]),
                id='loading_pie_chart'
            )
        ], id='content-column')
    ])
], id = 'body',fluid=True)
