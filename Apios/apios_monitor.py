from dash import Dash, Input, Output, dash_table, html, dcc, State
import plotly.graph_objects as go
import pandas as pd
from pandas import DataFrame
import plotly.express as px
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import sqlalchemy as sql
import itertools
from sqlalchemy.orm import Session
import itertools
import time
from collections import OrderedDict, deque
import numpy as np
from datetime import datetime
import random



import collections
collections.Callable = collections.abc.Callable

import collections
collections.MutableSequence = collections.abc.MutableSequence



# DB details 
db_url = "mysql+pymysql://uwe:uweproject@localhost/sensor_data"
engine = sql.create_engine(db_url)


# Varibales in global level
critical_count=[]
# del critical_count [:]
warning_count =[]
# del warning_count [:]
info_count=[]
# del info_count [:]
count_device =[]
oil_count =[]
temp_count =[]


# Main Application
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# Crtical alert coun componenet
critical_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Critical Alert", className="text text-center"),
                html.H1(children=critical_count, id="critical_count", className="text text-center"),
                dcc.Interval(id='c-component', interval=10*1000, n_intervals=0)
            ]
        ),  
    ],
    style={
        "background-color": "#ff70a6"
    }, 
)

# Warning Alert count componnet 
warning_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Warning Alert", className="text text-center"),
                html.H1(children=warning_count, id="warning_count", className="text text-center"),
                dcc.Interval(id='w-component', interval=10*1000, n_intervals=0)
            ]
        ), 
    ],
    style={
        "background-color": "#ffD670"
    },
)

# Info Alert count componenet 
info_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Info Alert", className="text text-center"),
                html.H1(children=info_count, id="info_count", className="text text-center"),
                dcc.Interval(id='i-component', interval=10*1000, n_intervals=0)
            ]
        ), 
    ],
    style={
        "background-color": "#70d6ff"
    },
)

# Alert Per Hour Componenet
alert_per_hr = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Alert Per Hour", className="text text-center"),
                html.H1(children=count_device, id="aph_count", className="text text-center"),
                dcc.Interval(id='aph-component', interval=10*1000, n_intervals=0)
            ]
        ), 
    ],
    style={
        "background-color": "#9fe481"}
)

# Count of alert on OIL Level
oil_alerts = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("No. of Oil Level Alert", className="text text-center"),
                html.H1(children=oil_count, id="oil_count", className="text text-center"),
                dcc.Interval(id='oil-component', interval=10*1000, n_intervals=0)
            ]
        ), 
    ],
        style={
        "background-color": "#5ab0c4"}
)

# Count of Alert on Temperature Level

temp_alerts = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("No. of Temperature Alert", className="text text-center"),
                html.H1(children=temp_count, id="temp_count", className="text text-center"),
                dcc.Interval(id='temp-component', interval=10*1000, n_intervals=0)
            ]
        ), 
    ],
        style={
        "background-color": "#FBC56F"}
)

# Number of device sen the alerts
device_count = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Device Count", className="text text-center", style={"color": "white"}),
                html.H1(children=count_device, id="d_count", className="text text-center", style={"color": "white"}),
                dcc.Interval(id='d-component', interval=10*1000, n_intervals=0)
            ]
        ), 
    ],
        style={
        "background-color": "#165E98"}
)

# Componenet adding to the rows and column
row_1 =dbc.Row(
    [
        dbc.Col(dbc.Card(critical_card, color="danger", outline=True)),
        dbc.Col(dbc.Card(warning_card, color="warning", outline=True)),
        dbc.Col(dbc.Card(info_card, color="info", outline=True))
    ], className="mb-5"), dbc.Row(
    [
        dbc.Col(dbc.Card(alert_per_hr, color="green", outline=True)),
        dbc.Col(dbc.Card(oil_alerts, color="warning", outline=True)),
        dbc.Col(dbc.Card(temp_alerts, color="info", outline=True))
    ], className="mb-5"),dbc.Row(
    [
        dbc.Col(dbc.Card(device_count, color="green", outline=True)),
    ], className="mb-5"),dbc.Row(
    [
        dbc.Col(dcc.Graph(id='alert-pie')),
        dcc.Interval(id='pie-component', interval=10*1000, n_intervals=0),
        dbc.Col(dcc.Graph(id='alert-pie2')),
        dcc.Interval(id='pie2-component', interval=10*1000, n_intervals=0),
        # dbc.Col(dbc.Card(oil_alerts, color="warning", outline=True)),
        # dbc.Col(dbc.Card(temp_alerts, color="info", outline=True))
    ], className="mb-5"),
    # dbc.Row(
    #     [
    #     dbc.Col(dcc.Graph(id="barchart")),
    #     dcc.Interval(id='gp1-component', interval=10*1000, n_intervals=0),
    #     dbc.Col(dbc.Card(device_count, color="danger", outline=True))
    # ], className="mb-5"),dbc.Row(
    #     [
    #     dbc.Col(dbc.Table(id="graph3"), style={
    #             'background-color': '#ffffff',
    #             'textAlign' : 'center',
    #             'color' : '#ffffff',
    #             "margin": "0%"
    #         })
    # ],className="mb-5")

# Application layout
app.layout = html.Div([
    html.H1(children = 'Technical Dashboard',
            style={
                'background-color': '#000000',
                'textAlign' : 'center',
                'color' : '#ffffff',
                "margin": "0%"
            }
            ),
    html.H1(row_1, id="count_c")
    
    ])


# Callback function for crtitical alert count
@app.callback(
    [Output(component_id='critical_count', component_property='children')],
    [Input('c-component', 'n_intervals')])


def critical(interval):
    # Establish the connection to the MySQl DB
    connection = engine.connect()
    df = pd.read_sql_query('SELECT * FROM data_table', con=connection)

    # The sum of critial alert count
    n=np.sum(df["Status"]=="Critical")
    return [html.Span(n)]

# Callback function for Warning Alert count
@app.callback(
    [Output(component_id='warning_count', component_property='children')],
    [Input('w-component', 'n_intervals')])


def warning(interval):
    connection = engine.connect()
    df = pd.read_sql_query('SELECT * FROM data_table', con=connection)

    # Total warning alert count 
    n=np.sum(df["Status"]=="Warning")
    return [html.Span(n)]

# Callback function for info alert count
@app.callback(
    [Output(component_id='info_count', component_property='children')],
    [Input('i-component', 'n_intervals')])


def info(interval):
    connection = engine.connect()
    df = pd.read_sql_query('SELECT * FROM data_table', con=connection)

    # Total info alert count
    n=np.sum(df["Status"]=="Info")
    return [html.Span(n)]

# Callback function for Alert per hour
@app.callback(
    [Output(component_id='aph_count', component_property='children')],
    [Input('aph-component', 'n_intervals')])

def APH (n):
    #establish the connect to the DB
    connection = engine.connect()
    df = pd.read_sql_query('SELECT * FROM data_table', con=connection)
    df['timestamp'] = pd.to_datetime(df['Date'])

    # Set the 'timestamp' column as the index
    df.set_index('timestamp', inplace=True)

    # Resample the DataFrame by hour and get the count of rows
    df_hourly = df.resample('H').count()
    value = df_hourly['Date'].values[0]
    return [html.Span(value)]

# callback function to the device count componenet
@app.callback(
    [Output(component_id='d_count', component_property='children')],
    [Input('d-component', 'n_intervals')])

def device_cnt(n):
    connection = engine.connect()
    df = pd.read_sql_query('SELECT * FROM data_table', con=connection)

    # get the devuce count
    mid=df["MachineID"].nunique()
    return [html.Span(mid)]

@app.callback(
    [Output(component_id='oil_count', component_property='children')],
    [Input('oil-component', 'n_intervals')])

def oil_cnt(n):
    connection = engine.connect()
    df = pd.read_sql_query('SELECT * FROM data_table', con=connection)

    #total number of alert rgeraing oil level
    n=np.sum(df["Factor"]=="Oil")
    return [html.Span(n)]

@app.callback(
    [Output(component_id='temp_count', component_property='children')],
    [Input('temp-component', 'n_intervals')])

def oil_cnt(n):
    connection = engine.connect()
    df = pd.read_sql_query('SELECT * FROM data_table', con=connection)

    # total number of alert regarding Temperature level
    n=np.sum(df["Factor"]=="Temperature")
    return [html.Span(n)]

# callback function for first pie chart (Number of alert per device)
@app.callback(Output('alert-pie', 'figure'), [Input('pie-component', 'n_intervals')])
def update_pie(value):
    connection = engine.connect()
    df = pd.read_sql_query('SELECT * FROM data_table', con=connection)
    # Group the DataFrame by 'device' and get the count of 'alert'
    df_alerts = df.groupby('MachineID')['Status'].count()
    data = [
        {
            'values': df_alerts.values,
            'labels': df_alerts.index,
            'type': 'pie',
            'name': 'Number of Alerts',
        },
    ]
    return {'data': data, 'layout': {'title': 'Number of Alerts per Device'}}

# Callback function for second pie chart (Number of crtitcal count per device)
@app.callback(Output('alert-pie2', 'figure'), [Input('pie2-component', 'n_intervals')])
def update_pie2(value):
    connection = engine.connect()
    df = pd.read_sql_query('SELECT * FROM data_table', con=connection)
    df_critical = df[df['Status'] == 'Critical']
    df_count = df_critical.groupby('MachineID').size().reset_index(name='critical_alert_count')

    data = [{
        'values': df_count['critical_alert_count'].tolist(),
        'labels': df_count['MachineID'].tolist(),
        'type': 'pie',
        'name': 'Number of Alerts',
    }]
    layout = {'title': 'Number of Critical Alerts per Device'}
    return {'data': data, 'layout': {'title': 'Number of Critical Alerts per Device'}}


if __name__ == "__main__":
    app.run_server()
