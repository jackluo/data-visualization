# In[]:
# Import required libraries
# import pickle
import datetime as dt

# import numpy as np
import pandas as pd
# import plotly.plotly as py
# import plotly.offline as pyo

import dash
from dash.dependencies import Input, Output
import dash_core_components as core
import dash_html_components as html

# Multi-dropdown options
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES


# In[]:
# Create controls
app = dash.Dash("New York Oil and Gas")
app.css.append_css(
    {
        'external_url': (
            # http://tiny.cc/dashcss
            'https://rawgit.com/chriddyp/0247653a7c52feb4c48437e1c1837f75'
            '/raw/a68333b876edaf62df2efa7bac0e9b3613258851/dash.css'
        )
    }
)

county_options = [{'label': str(COUNTIES[county]), 'value': str(county)}
                  for county in COUNTIES]

well_status_options = [{'label': str(WELL_STATUSES[well_status]),
                        'value': str(well_status)}
                       for well_status in WELL_STATUSES]

well_type_options = [{'label': str(WELL_TYPES[well_type]),
                      'value': str(well_type)}
                     for well_type in WELL_TYPES]


# In[]:
# Create layout
app.layout = html.Div(
    [
        html.H2('New York Oil and Gas Dashboard'),
        html.Div(
            [
                html.Span(
                    core.Dropdown(
                        id='counties',
                        options=county_options,
                        multi=True,
                        value=COUNTIES.keys(),
                    ),
                    style={
                        'display': 'none',
                    },
                ),
                html.Span(
                    core.RadioItems(
                        id='selector',
                        options=[
                            {'label': 'All', 'value': 'all'},
                            {'label': 'Active only', 'value': 'active'},
                            {'label': 'Customize', 'value': 'custom'}
                        ],
                        value='active'
                    ),
                ),
                html.Span(
                    core.Dropdown(
                        id='well_statuses',
                        options=well_status_options,
                        multi=True,
                        value=[],
                    ),
                    id='well_statuses_span',
                    style={
                        'display': 'inline-block',
                    },
                ),
                html.Span(
                    core.Dropdown(
                        id='well_types',
                        options=well_type_options,
                        multi=True,
                        value=WELL_TYPES.keys(),
                    ),
                ),

            ]
        ),
        core.Graph(id='map'),
        html.Span(
            core.RangeSlider(
                id='year_slider',
                min=1900,
                max=2017,
                value=[1900, 2017],
            )
        ),
    ],
    # style={
    #     'width': '1200',
    #     'margin-left': 'auto',
    #     'margin-right': 'auto',
    #     'text-align': 'center',
    #     'font-family': 'overpass',
    #     'background-color': '#F3F3F3'
    # }
)


# In[]:
# Create callbacks
df = pd.read_csv('data/wellspublic.csv', low_memory=False)
df['Date_Well_Completed'] = pd.to_datetime(df['Date_Well_Completed'])


# Status hider
@app.callback(Output('well_statuses_span', 'style'),
              [Input('selector', 'value')])
def display_control(selector):
    if selector == 'custom':
        return {'display': 'inline-block'}
    else:
        return {'display': 'none'}


@app.callback(Output('well_statuses', 'value'),
              [Input('selector', 'value')])
def display_control(selector):
    if selector == 'all':
        return WELL_STATUSES.keys()
    elif selector == 'active':
        return ['AC']
    else:
        return WELL_STATUSES.keys()


@app.callback(Output('map', 'figure'), [Input('counties', 'value'),
                                        Input('well_statuses', 'value'),
                                        Input('well_types', 'value'),
                                        Input('year_slider', 'value'),])
def make_figure(counties, well_statuses, well_types, year_slider):

    dff = df[df['Cnty'].isin(counties)
             & df['Well_Status'].isin(well_statuses)
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
            name=WELL_TYPES[well],
            marker=dict(
                size=4,
                opacity=0.6,
            )
        )
        traces.append(trace)

    mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjaXhzYTB0bHcwOHNoMnFtOWZ3YWdreDB3In0.pjROwb9_CEuyKPE-x0lRUw'  # noqa: E501

    layout = dict(
        autosize=True,
        font=dict(
            family="Overpass",
            size=12,
            color='#CCCCCC',
        ),
        margin=dict(
            l=20,
            r=120,
            b=20,
            t=20
        ),
        hovermode="closest",
        plot_bgcolor="#191A1A",
        paper_bgcolor="#020202",
        legend=dict(
            font=dict(size=10),
        ),
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style="dark",
            center=dict(
                lon=-76.40,
                lat=42.70,
            ),
            zoom=5.5,
        ),
    )

    figure = dict(data=traces, layout=layout)
    return figure



@app.callback(
    Output('well_types', 'value'),
    [Input('map', 'clickData'),
     Input('map', 'hoverData')])
def filterScatterPlot(clickData, hoverData):
    print(clickData)
    return WELL_TYPES.keys()

# In[]:
# Main

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
