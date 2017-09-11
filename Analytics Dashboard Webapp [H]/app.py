# In[]:
# Import required libraries
import os
import datetime as dt
import time

import numpy as np
import pandas as pd
import cufflinks as cf

import flask
import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dcce

from dash_parser import *


# In[]:
# Setup app
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')

app = dash.Dash(__name__, server=server, url_base_pathname='/dash/gallery/analytics-report/', csrf_protect=False)  # noqa: E501

# Load data
files = ['facebook.csv', 'gdn.csv', 'mailchimp.csv', 'search.csv', 'traffic.csv', 'twitter.csv']
db = {}
offset = 734550  # 2012/02/17

for f in files:
    df = pd.read_csv('data/' + f)
    del df['Unnamed: 0']
    df.index += offset
    df.index = df.index.map(dt.datetime.fromordinal)
    db[f.replace('.csv', '')] = df

data_selector_options = [{'label': source.title(), 'value': source} for source in db]
data_selector_keys = list(db.keys())


# In[]:
# Create app layout

app.layout =  html.Div([
    # Fixed nav
    html.Div([
        html.H6(
            'Analytics Report | Periodic',
            style={
                'color': '#FFFFFF',
                'text-align': 'left',
                'float': 'left',
                'min-width': '30%',
                'max-width': '100%',
                'padding-left': '10',
                'padding-right': '10',
            }
        ),
        html.H6(
            'Plotly',
            style={
                'color': '#FFFFFF',
                'background-color': '#29B2EE',
                'text-align': 'center',
                'float': 'right',
                'width': '10%',
                'margin-right': '12',
                'padding-left': '10',
                'padding-right': '10',
                'border-radius': '3'
            }
        ),
    ],
        className='row',
        style={
            'background-color': '#6184D8',
            'position': 'fixed',
            'width': '100%',
            'top': '0',
            'left': '-1',
            'zIndex': '10000'
        }
    ),
    # Scrolling content
    html.Div([
        # Top section
        html.Div([
            # Left top section
            html.Div([
                html.Div([
                    html.Img(
                        src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                        style={
                            'position': 'relative',
                            'height': '95%',
                            'width': '95%',
                            'object-fit': 'contain',
                        },
                    ),
                ],
                    className='three columns',
                    style={
                        'background-color': '#F9F9F9',
                        'width': '200',
                        'max-height': '85',
                        'margin-right': '20',
                        'border-radius': '3'
                    }
                ),
                html.Div([
                    dcc.Dropdown(
                        id='period_dropdown',
                        options=[
                            {'label': 'Custom period', 'value': 'custom'},
                            {'label': 'Last 7 days', 'value': 'last_7'},
                            {'label': 'Last 30 days', 'value': 'last_30'},
                            {'label': 'Last week', 'value': 'last_week'},
                            {'label': 'Last month', 'value': 'last_month'},
                            {'label': 'Last quarter', 'value': 'last_quarter'},
                            {'label': 'Last year', 'value': 'last_year'}
                        ],
                        value='last_year'
                    ),
                    html.Div([
                        dcc.DatePickerRange(
                            id='period_selector',
                            min_date_allowed=dt.datetime(2012, 2, 17),
                            max_date_allowed=dt.datetime(2017, 2, 14),
                            start_date_placeholder_text='Select date',
                            start_date=dt.datetime(2016, 8, 14),
                            end_date=dt.datetime(2017, 2, 14)
                        ),
                    ])
                ],
                    style={'display': 'inline-block', 'margin-right': '20'}
                ),
                html.Div([
                    dcc.RadioItems(
                        id='resolution_selector',
                        options=[
                            {'label': 'Day', 'value': 'D'},
                            {'label': 'Week', 'value': 'W'},
                            {'label': 'Month', 'value': 'M'},
                        ],
                        value='D'
                    ),
                ],
                    style={'display': 'inline-block'}
                ),
            ],
                className='nine columns',
            ),
            # Right top section
            html.Div([
                html.Button(
                    'Share',
                    id='share_button',
                    style={'background-color': '#FFFFFF', 'width': '120'}
                ),
                html.Button(
                    'Export',
                    id='export_button',
                    style={'background-color': '#FFFFFF', 'width': '120'}
                ),
            ],
                className='three columns',
                style={
                    'float': 'right',
                    'width': '100',
                    'margin-right': '40',
                }
            ),
        ],
            className='row',
            style={
                'background-color': '#F0F0F0',
                'margin-top': '80',
                'padding': '10',
                'border-radius': '5',
            }
        ),
        # Bottom section
        html.Div([
            # Bottom header selector
            html.Div([
                dcc.Dropdown(
                    id='data_selector',
                    options=data_selector_options,
                    multi=True,
                    value=data_selector_keys,
                ),
            ],
                className='row'
            ),
            # Upper graph selector
            html.Div([
                html.Div([
                    dcc.Dropdown(id='top-left-graph-selector-1', value='Views')
                ],
                    className='three columns'
                ),
                html.Div([
                    dcc.Dropdown(id='top-left-graph-selector-2', value='Visits')
                ],
                    className='three columns'
                ),
            ],
                className='row',
                style={'margin-top': '10'}
            ),
            # Upper graph row
            html.Div([
                html.Div([
                    dcc.Graph(id='top-left-graph')
                ],
                    className='six columns'
                ),
                html.Div([
                    dcce.DataTable(
                        id='top-right-table',
                        rows=pd.DataFrame().to_dict('records'),  # Bug, can't be empty for now
                    )
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
            # Middle graph selector
            html.Div([
                html.Div([
                    dcc.Dropdown(id='middle-left-graph-selector', value='Impressions')
                ],
                    className='three columns'
                ),
                html.Div([
                    dcc.Dropdown(id='middle-centerleft-graph-selector', value='Conversion Rate')
                ],
                    className='three columns'
                ),
                html.Div([
                    dcc.Dropdown(id='middle-centerright-graph-selector', value='Cost / Conversion')
                ],
                    className='three columns'
                ),
                html.Div([
                    dcc.Dropdown(id='middle-right-graph-selector', value='CPC')
                ],
                    className='three columns'
                ),
            ],
                className='row',
                style={'margin-top': '10'}
            ),
            # Middle graph row
            html.Div([
                html.Div([
                    dcc.Graph(id='middle-left-graph')
                ],
                    className='three columns'
                ),
                html.Div([
                    dcc.Graph(id='middle-centerleft-graph')
                ],
                    className='three columns'
                ),
                html.Div([
                    dcc.Graph(id='middle-centerright-graph')
                ],
                    className='three columns'
                ),
                html.Div([
                    dcc.Graph(id='middle-right-graph')
                ],
                    className='three columns'
                ),
            ],
                className='row'
            ),
            # Lower graph selector
            html.Div([
                html.Div([
                    dcc.Dropdown(id='lower-left-graph-selector', value='Deliveries')
                ],
                    className='three columns'
                ),
                html.Div([
                    dcc.Dropdown(id='lower-centerleft-graph-selector', value='Opens')
                ],
                    className='three columns'
                ),
                html.Div([
                    dcc.Dropdown(id='lower-right-graph-selector', value='Cost')
                ],
                    className='six columns'
                ),
            ],
                className='row',
                style={'margin-top': '10'}
            ),
            # Lower graph row
            html.Div([
                html.Div([
                    dcc.Graph(id='lower-left-graph')
                ],
                    className='three columns'
                ),
                html.Div([
                    dcc.Graph(id='lower-centerleft-graph')
                ],
                    className='three columns'
                ),
                html.Div([
                    dcc.Graph(id='lower-right-graph')
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
        ],
            style={
                'background-color': '#F0F0F0',
                'margin-top': '30',
                'padding': '10',
                'border-radius': '5',
            }
        ),
    ],
        style={
            'width': '85%',
            'max-width': '1440',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'font-family': 'overpass',
        },
    )
],
    style={'font-family': 'Roboto'}
)


# In[]:
# Other layouts

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'  # noqa: E501
    })

external_css = ["https://fonts.googleapis.com/css?family=Roboto:400,300,600",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/1564e52057ea20b6c23a4047d3d9261fc793f3af/dash-analytics-report.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a3401de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-sachs-report-js.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})


# In[]:
# Helper functions

resampler = {
    'CPC': 'mean',
    'CPM': 'mean',
    'CTR': 'mean',
    'Conversion Rate': 'mean',
    'Cost / Conversion': 'mean',
    'Delivery Rate': 'mean',
    'Open Rate': 'mean',
    'Pages / Visit': 'mean',
    'Send Rate': 'mean',
    'Clicks': 'sum',
    'Conversions': 'sum',
    'Cost': 'sum',
    'Deliveries': 'sum',
    'Impressions': 'sum',
    'Opens': 'sum',
    'Recipients': 'sum',
    'Sends': 'sum',
    'Views': 'sum',
    'Visits': 'sum'
}

colors = {
    'Facebook': '#4267B2',
    'Gdn': '#33A929',
    'Mailchimp': '#FFC413',
    'Search': '#20A474',
    'Traffic': '#FF3730',
    'Twitter': '#4AB3F4'
}


def filter_resample(df, start_date, end_date, resolution):
    columns = df.columns
    sub_resampler = {column: resampler[column] for column in columns}

    df = df[start_date:end_date]
    df = df.resample(resolution).agg(sub_resampler)
    return df


def plot(dfs, selected, variables, kind='area'):

    data = []

    for variable in variables:

        plot_df_list = []
        name_list = []
        for i, df in enumerate(dfs):
            try:
                plot_df_list.append(df[variable])
                name_list.append(selected[i].title())
            except:
                print('Variable not found in dataset')

        plot_df = pd.concat(plot_df_list, axis=1)

        # Stacked area for non-ratio variables
        fill = False
        if resampler[variable] == 'sum':
            plot_df = plot_df.T.fillna(0).cumsum().T
            if kind == 'area':
                fill = True

        # Plotting
        color_list = [colors[name] for name in name_list]
        color_list = iter(color_list)
        name_list = iter(name_list)

        for index, row in plot_df.T.iterrows():
            trace = dict(
                type='scatter',
                mode='lines',
                x=row.index,
                y=row,
                name=next(name_list),
                hoverinfo="x+y++name",
                line=dict(
                    width='2',
                    color=next(color_list),
                ),
            )
            if fill:
                trace['fill'] = 'tonexty'
            data.append(trace)

    # Global layout
    layout = dict(
        autosize=True,
        height=500,
        font=dict(family='Overpass'),
        titlefont=dict(color='#CCCCCC', size='14'),
        plot_bgcolor='#FAFAFA',
        margin=dict(
            l=40,
            r=40,
            b=40,
            t=40
        ),
        hovermode="closest",
        showlegend=True,
        legend=dict(font=dict(size=10), orientation='h'),
    )

    return dict(data=data, layout=layout)


def make_table(dfs, selected, variables):

    plot_df_list = []
    for variable in variables:

        name_list = []
        for i, df in enumerate(dfs):
            try:
                plot_df_list.append(df[variable])
                name_list.append(selected[i].title())
            except:
                print('Variable not found in dataset')

    plot_df = pd.concat(plot_df_list, axis=1)
    return plot_df.to_dict('records')


# In[]:
# Callbacks

# Exec variables
selector_variables = [
    'top-left-graph-selector-1',
    'top-left-graph-selector-2',
    'middle-left-graph-selector',
    'middle-centerleft-graph-selector',
    'middle-centerright-graph-selector',
    'middle-right-graph-selector',
    'lower-left-graph-selector',
    'lower-centerleft-graph-selector',
    'lower-right-graph-selector'
]

graph_variables = [
    'middle-left-graph',
    'middle-centerleft-graph',
    'middle-centerright-graph',
    'middle-right-graph',
    'lower-left-graph',
    'lower-centerleft-graph',
    'lower-right-graph'
]

# Selectors
for i, selector_variable in enumerate(selector_variables):

    string = """

@app.callback(Output('{}', 'options'),
              [Input('data_selector', 'value')])
def update_options_{}(selected):

    unique_metrics = set()
    for source in selected:
        for el in db[source].columns.tolist():
            unique_metrics.add(el)

    metric_selector_options = [dict(label=metric, value=metric) for metric in unique_metrics]
    return metric_selector_options

    """.format(selector_variable, i)

    exec(string)

# Graphs
for i, selector_variable in enumerate(selector_variables[2:]):

    string = """

@app.callback(Output('{}', 'figure'),
              [Input('data_selector', 'value'),
               Input('period_selector', 'start_date'),
               Input('period_selector', 'end_date'),
               Input('resolution_selector', 'value'),
               Input('{}', 'value')])
def update_options_{}(selected, start_date, end_date, resolution, variable):

    dfs = []
    for data_source in selected:
        df = db[data_source]
        df = filter_resample(df, start_date, end_date, resolution)
        dfs.append(df)

    figure = plot(dfs, selected, [variable])
    return figure

    """.format(graph_variables[i], selector_variable, i)

    exec(string)

# Main 2 variable chart
@app.callback(Output('top-left-graph', 'figure'),
              [Input('data_selector', 'value'),
               Input('period_selector', 'start_date'),
               Input('period_selector', 'end_date'),
               Input('resolution_selector', 'value'),
               Input('top-left-graph-selector-1', 'value'),
               Input('top-left-graph-selector-2', 'value')])
def update_options_main(selected, start_date, end_date, resolution,
                        variable1, variable2):

    dfs = []
    for data_source in selected:
        df = db[data_source]
        df = filter_resample(df, start_date, end_date, resolution)
        dfs.append(df)

    figure = plot(dfs, selected, [variable1, variable2])
    return figure


# Main 2 variable chart
@app.callback(Output('top-right-table', 'rows'),
              [Input('data_selector', 'value'),
               Input('period_selector', 'start_date'),
               Input('period_selector', 'end_date'),
               Input('resolution_selector', 'value'),
               Input('top-left-graph-selector-1', 'value'),
               Input('top-left-graph-selector-2', 'value')])
def update_options_main(selected, start_date, end_date, resolution,
                        variable1, variable2):

    dfs = []
    for data_source in selected:
        df = db[data_source]
        df = filter_resample(df, start_date, end_date, resolution)
        dfs.append(df)

    rows = make_table(dfs, selected, [variable1, variable2])
    return rows


# In[]:
# Main
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
