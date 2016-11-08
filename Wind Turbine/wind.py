##################### HEAD #######################

import pandas as pd 
from sqlalchemy import create_engine

import plotly.plotly as py
from plotly.graph_objs import *

################### FUNCTIONS ####################




# 1st graph
def graph1(df):
    
    mapbox_access_token = 'pk.eyJ1IjoicGxvdGx5ZXhhbXBsZXMiLCJhIjoiY2l1azN6bGMxMDE2djJ6c2M0dmFob3pjdCJ9.iQcf9R_QqzfhgIliXixmFg'

    trace = Scattermapbox(
            lat=df['lat_DD'].values,
            lon=df['long_DD'].values,
            mode='markers',
            marker=Marker(
                size=5
            ),
        )

    data = Data([trace])

    layout = Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=42,
                lon=-95
            ),
            pitch=0,
            zoom=5
        ),
    )

    fig = Figure(data=data,layout=layout)
    plot_url = py.plot(fig, filename = "Mapbox 1", validate=False)




# 2nd graph
def graph2(df):

    mapbox_access_token = 'pk.eyJ1IjoicGxvdGx5ZXhhbXBsZXMiLCJhIjoiY2l1azN6bGMxMDE2djJ6c2M0dmFob3pjdCJ9.iQcf9R_QqzfhgIliXixmFg'

    trace = Scattermapbox(
            lat=df['lat_DD'].values,
            lon=df['long_DD'].values,
            mode='markers',
            marker=Marker(
                color="#FFFFFF",
                size=5
            ),
        )

    data = Data([trace])

    layout = Layout(
        annotations=Annotations([
            Annotation(
                x=0.00,
                y=1.07,
                showarrow=False,
                text="Map 1 : Visualization of wind turbine locations in the US",
                xref='paper',
                yref='paper'
            )
        ]),
        font=Font(family="Droid Sans", size=14, color="FFFFFF"),
        autosize=True,
        hovermode='closest',
        paper_bgcolor='rgb(40, 40, 40)',
        margin=Margin(
            t=60,
            l=20,
            b=20,
            r=20,
            pad=0
        ),
        title = "",
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=42,
                lon=-95
            ),
            pitch=0,
            zoom=5,
            style="dark"
        ),
    )

    fig = Figure(data=data,layout=layout)
    plot_url = py.plot(fig, filename = "Mapbox 1 styled", validate=False)




def graph3(df):

    mapbox_access_token = 'pk.eyJ1IjoicGxvdGx5ZXhhbXBsZXMiLCJhIjoiY2l1azN6bGMxMDE2djJ6c2M0dmFob3pjdCJ9.iQcf9R_QqzfhgIliXixmFg'

    trace = Scattermapbox(
        lat=df['lat_DD'].values,
        lon=df['long_DD'].values,
        mode='markers',
        marker=Marker(
            color=[max(float(i), 5) for i in df['blade_l'].values],
            colorscale=[[0, 'rgb(221,42,145)'], [0.35, 'rgb(177,77,236)'], [0.5, 'rgb(118,117,237)'], [0.6, 'rgb(46,142,191)'], [0.7, 'rgb(11,152,121)'], [1, 'rgb(19,152,99)']],
            reversescale=True,
            showscale=True,
            autocolorscale=False,
            colorbar=ColorBar(
                title='Turbine<br>blade<br>length (m)'
            ),
            size=[max(float(i)/5, 5) for i in df['blade_l'].values],
            opacity=0.8
          
        ),
    )
     
    data = Data([trace])

    layout = Layout(
        annotations=Annotations([
            Annotation(
                x=0.00,
                y=1.07,
                showarrow=False,
                text="Map 2 : Visualization of wind turbine locations and their size in the US",
                xref='paper',
                yref='paper'
            )
        ]),
        font=Font(family="Droid Sans", size=14, color="FFFFFF"),
        autosize=True,
        hovermode='closest',
        paper_bgcolor='rgb(40, 40, 40)',
        margin=Margin(
            t=60,
            l=20,
            b=20,
            r=20,
            pad=0
        ),
        title = "",
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=42,
                lon=-95
            ),
            pitch=0,
            zoom=5,
            style="dark"
        ),
    )

    fig = Figure(data=data,layout=layout)
    plot_url = py.plot(fig, filename = "Mapbox 2", validate=False)




##################### MAIN #######################

if __name__ == "__main__":

    disk_engine = create_engine("sqlite:///assets/turbine_locations.db")
    df = pd.read_sql_query("Select lat_DD, long_DD, count(*) from data group by lat_DD, long_DD ", disk_engine)

    graph1(df)
    graph2(df)

    df = pd.read_sql_query("Select lat_DD, long_DD, blade_l, count(*) from data group by lat_DD, long_DD, blade_l", disk_engine)

    graph3(df)

    print "Done!"

