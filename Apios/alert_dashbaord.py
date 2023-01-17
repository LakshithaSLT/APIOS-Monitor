import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, Dash, dcc
import sqlalchemy as sql
import pandas as pd
import numpy as np
import datetime as dt

# Database connection details
db_url = "mysql+pymysql://uwe:uweproject@localhost/sensor_data"
engine = sql.create_engine(db_url)


MachineID = []
alert = []
t = []

#Application of the alert dasbaord
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Warning alert component
warning = dbc.Alert(
            [
                "Warning Alert from Mchine ",
                html.A(MachineID, href="#", className="alert-link"),
                " at ",
                html.Span(t)
            ],
            color="warning",
        )
# INFO alert component
info = dbc.Alert(
            [
                "Info Alert from Machine ",
                html.A(MachineID, href="#", className="alert-link"),
                " at ",
                html.Span(t)
            ],
            color="primary",
        )

# Critical Alert component
critical = dbc.Alert(
            [
                "Critical Alert from ",
                html.A(MachineID, href="#", className="alert-link"),
                " at ",
                html.Span(t)
            ],
            color="danger",
        )
# Add components into the row
row =dbc.Row([  html.H1(children=alert)
])


app.layout = html.Div(
    # Dasboard title
    [html.H1(children="Alert dashbaord", id ="alertdddoard",
            style={
                'background-color': '#000000',
                'textAlign' : 'center',
                'color' : '#ffffff',
                "margin": "0%"
            }, 
            ),
            html.H1(row, id="alertboard"),
            dcc.Interval(id='alert', interval=1000, n_intervals=0)
       
        
    ],
    
)

#callback function to search the updated alerts and trigger
@app.callback(
    [Output(component_id='alertboard', component_property='children')],
    [Input('alert', 'n_intervals')])


def foo(n):
    #establish the connection to DB
    connection = engine.connect()
    df = pd.read_sql_query('SELECT * FROM data_table', con=connection)

    # Captured the last row by the status
    last_row = df['Status'].tail(1).values[0]

    # Capture the last alert by the MachinID
    mid = df['MachineID'].tail(1).values[0]

    #capture the last alert Time
    tid = df['Time'].tail(1).values[0]
    # dt_time = dt.datetime.now()
    # now = dt_time.strftime("%H:%M:%S")
    if last_row== "Critical":
        del MachineID [:]
        del t [:]
        MachineID.append(mid)
        alert.append(critical)
        t.append(tid)
        return [html.Span(alert)]
    elif last_row=="Warning":
        del MachineID [:]
        del t [:]
        MachineID.append(mid)
        alert.append(warning)
        t.append(tid)
        return [html.Span(alert)]
    else:
        del MachineID [:]
        del t [:]
        MachineID.append(mid)
        alert.append(info)
        t.append(tid)
        return [html.Span(alert)]


if __name__ == "__main__":
    app.run_server()
