# In[]:
# Import required libraries

import pickle
import copy
import datetime as dt

import pandas as pd
import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html

# Multi-dropdown options
# from layout import LAYOUT
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES


# In[]:
# Create app

app = dash.Dash()
app.css.append_css({'external_url': 'http://tiny.cc/dashcss'})

# Create controls
county_options = [{'label': str(COUNTIES[county]), 'value': str(county)}
                  for county in COUNTIES]

well_status_options = [{'label': str(WELL_STATUSES[well_status]),
                        'value': str(well_status)}
                       for well_status in WELL_STATUSES]

well_type_options = [{'label': str(WELL_TYPES[well_type]),
                      'value': str(well_type)}
                     for well_type in WELL_TYPES]

# Load data
df = pd.read_csv('data/wellspublic.csv', low_memory=False)
df['Date_Well_Completed'] = pd.to_datetime(df['Date_Well_Completed'])
points = pickle.load(open("data/dataset.pkl", "rb"))

# Create global graph template
mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'  # noqa: E501

layout = dict(
    autosize=True,
    height=750,
    font=dict(
        family="Overpass",
        size=11,
        color='#CCCCCC',
    ),
    margin=dict(
        l=35,
        r=120,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    legend=dict(
        font=dict(size=10),
    ),
    title='Satellite Overview',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="dark",
        center=dict(
            lon=-77.16,
            lat=42.54,
        ),
        zoom=7,
    ),
)


# In[]:
# Create layout
app.layout = html.Div(
    [
        html.H2('New York Oil and Gas | Production Overview'),
        html.Div(
            [
                html.P('Filter by construction date:'),
                dcc.RangeSlider(
                    id='year_slider',
                    min=1900,
                    max=2017,
                    value=[1900, 2017],
                ),
            ],
            style={'margin-top': '20'}
        ),
        html.Div(
            [
                html.P('Filter by well status:'),
                dcc.RadioItems(
                    id='well_status_selector',
                    options=[
                        {'label': 'All ', 'value': 'all'},
                        {'label': 'Active only ', 'value': 'active'},
                        {'label': 'Customize ', 'value': 'custom'}
                    ],
                    value='active',
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Dropdown(
                    id='well_statuses',
                    options=well_status_options,
                    multi=True,
                    value=[],
                ),
            ],
            style={'width': '49%',
                   'display': 'inline-block', 'margin-bottom': '20'},
        ),
        html.Div(
            [
                html.P('Filter by well type:'),
                dcc.RadioItems(
                    id='well_type_selector',
                    options=[
                        {'label': 'All ', 'value': 'all'},
                        {'label': 'Productive only ', 'value': 'productive'},
                        {'label': 'Customize ', 'value': 'custom'}
                    ],
                    value='productive',
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Dropdown(
                    id='well_types',
                    options=well_type_options,
                    multi=True,
                    value=list(WELL_TYPES.keys()),
                ),
            ],
            style={'width': '49%', 'float': 'right',
                   'display': 'inline-block', 'margin-bottom': '20'}
        ),
        html.Div([
            html.Div(
                [
                    dcc.Graph(id='main_graph'),
                ],
                #className='six columns',
                style={'width': '67%', 'display': 'inline-block'}
            ),
            html.Div(
                [
                    dcc.Graph(id='individual_graph'),
                ],
                #className='six columns offset-by-one-half',
                style={'width': '33%', 'float': 'right', 'display': 'inline-block'}
            ),
        ]),
        html.Div([
            html.Div(
                [
                    dcc.Graph(id='count_graph'),
                ],
                #className='six columns',
                style={'width': '67%', 'display': 'inline-block'}
            ),
            html.Div(
                [
                    dcc.Graph(id='aggregate_graph'),
                    dcc.Checklist(
                        id='lock_selector',
                        options=[
                            {'label': 'Lock camera', 'value': 'locked'}
                        ],
                        values=[],
                        labelStyle={'margin-bottom': '-10'}
                    ),
                ],
                #className='six columns offset-by-one-half',
                style={'width': '33%', 'float': 'right', 'display': 'inline-block'}
            ),
        ]),
    ],
    className='ten columns offset-by-one',

)


# In[]:
# Create callbacks

# Radio -> multi
@app.callback(Output('well_statuses', 'value'),
              [Input('well_status_selector', 'value')])
def display_status(selector):

    if selector == 'all':
        return list(WELL_STATUSES.keys())
    elif selector == 'active':
        return ['AC']
    else:
        return []


# Radio -> multi
@app.callback(Output('well_types', 'value'),
              [Input('well_type_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(WELL_TYPES.keys())
    elif selector == 'productive':
        return ['GD', 'GE', 'GW', 'IG', 'IW', 'OD', 'OE', 'OW']
    else:
        return []


# # Multi -> radio
# @app.callback(Output('well_status_selector', 'value'),
#               [Input('well_statuses', 'value')])
# def display_status(statuses):
#     if statuses == list(WELL_STATUSES.keys()):
#         return 'all'
#     elif statuses == ['AC']:
#         return 'active'
#     else:
#         return 'custom'
#
#
# # Multi -> radio
# @app.callback(Output('well_type_selector', 'value'),
#               [Input('well_types', 'value')])
# def display_type(types):
#     if types == list(WELL_TYPES.keys()):
#         return 'all'
#     elif types == ['GD', 'GE', 'GW', 'IG', 'IW', 'OD', 'OE', 'OW']:
#         return 'productive'
#     else:
#         return 'custom'


# Selectors -> main graph
@app.callback(Output('main_graph', 'figure'),
              [Input('well_statuses', 'value'),
               Input('well_types', 'value'),
               Input('year_slider', 'value')],
              [State('lock_selector', 'values'),
               State('main_graph', 'relayoutData')])
def make_main_figure(well_statuses, well_types, year_slider,
                     selector, main_graph_layout):

    dff = df[df['Well_Status'].isin(well_statuses)
             & df['Well_Type'].isin(well_types)
             & (df['Date_Well_Completed'] > dt.datetime(year_slider[0], 1, 1))
             & (df['Date_Well_Completed'] < dt.datetime(year_slider[1], 1, 1))]

    traces = []
    for well, dfff in dff.groupby('Well_Type'):
        trace = dict(
            type='scattermapbox',
            lon=dfff['Surface_Longitude'],
            lat=dfff['Surface_latitude'],
            text=dfff['Well_Name'],
            customdata=dfff['API_WellNo'],
            name=WELL_TYPES[well],
            marker=dict(
                size=4,
                opacity=0.6,
            )
        )
        traces.append(trace)

    print(main_graph_layout)

    if (main_graph_layout is not None and 'locked' in selector):

        lon = float(main_graph_layout['mapbox']['center']['lon'])
        lat = float(main_graph_layout['mapbox']['center']['lat'])
        zoom = float(main_graph_layout['mapbox']['zoom'])
        print('Locking')
        print(lon, lat, zoom)
        layout['mapbox']['center']['lon'] = lon
        layout['mapbox']['center']['lat'] = lat
        layout['mapbox']['zoom'] = zoom
    else:
        lon = -77.16
        lat = 42.54
        zoom = 7


    figure = dict(data=traces, layout=layout)
    return figure


# Main graph -> individual graph
@app.callback(Output('individual_graph', 'figure'),
              [Input('main_graph', 'hoverData'),
               Input('main_graph', 'clickData')])
def make_side_figure(main_graph_hover, main_graph_click):

    layout_secondary = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {'points': [{'curveNumber': 4, 'pointNumber': 3244, 'customdata': 31101228740000}]}

    try:
        raise Exception()
        chosen = [point['customdata'] for point in main_graph_click['points']]
        print('Clicked')
        print(main_graph_click['points'])
        print(chosen)
    except:
        chosen = [point['customdata'] for point in main_graph_hover['points']]
        print('Hovered')
        print(main_graph_hover['points'])
        print(chosen)

    n = 0
    try:
        selected = points[chosen[0]]
        selected['Production'].sort_index(inplace=True)
        x = selected['Production'].index
        y = selected['Production']['Gas Produced, MCF']
    except:
        x = []
        y = []
        print("Not available 1")
        n += 1

    try:
        selected = points[chosen[0]]
        selected['Production'].sort_index(inplace=True)
        x2 = selected['Production'].index
        y2 = selected['Production']['Oil Produced, bbl']
    except:
        x2 = []
        y2 = []
        print("Not available 2")
        n += 1

    try:
        selected = points[chosen[0]]
        selected['Production'].sort_index(inplace=True)
        x3 = selected['Production'].index
        y3 = selected['Production']['Water Produced, bbl']
    except:
        x3 = []
        y3 = []
        print("Not available 3")
        n += 1

    if n == 3:
        annotation = dict(
            text='No data available',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_secondary['annotations'] = [annotation]
        data = []
    else:
        data = [
            dict(
                type='scatter',
                mode='lines',
                x=x,
                y=y,
                name='Gas Produced (mcf)',
                line=dict(
                    shape="spline",
                    smoothing="2",
                ),
            ),
            dict(
                type='scatter',
                mode='lines',
                x=x2,
                y=y2,
                name='Oil Produced (bbl)',
                line=dict(
                    shape="spline",
                    smoothing="2",
                ),
            ),
            dict(
                type='scatter',
                mode='lines',
                x=x3,
                y=y3,
                name='Water Produced (bbl)',
                line=dict(
                    shape="spline",
                    smoothing="2",
                ),
            )
        ]
        layout_secondary['title'] = 'Individual Production: ' + selected['Well_Name']

    figure = dict(data=data, layout=layout_secondary)
    return figure


# In[]:
# Main

if __name__ == '__main__':
    app.run_server(debug=True)
