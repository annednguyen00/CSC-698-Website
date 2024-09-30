from app import app
import requests
import io
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

c8 = requests.get('https://raw.githubusercontent.com/annednguyen00/CSC-698/main/3.%20Dashboard/data/incidents_count_forecast.csv').content
incidents_count_forecast = pd.read_csv(io.StringIO(c8.decode('utf-8')), index_col='Unnamed: 0')
c9 = requests.get('https://raw.githubusercontent.com/annednguyen00/CSC-698/main/3.%20Dashboard/data/victims_killed_forecast.csv').content
victims_killed_forecast = pd.read_csv(io.StringIO(c9.decode('utf-8')), index_col='Unnamed: 0')
c10 = requests.get('https://raw.githubusercontent.com/annednguyen00/CSC-698/main/3.%20Dashboard/data/victims_injured_forecast.csv').content
victims_injured_forecast = pd.read_csv(io.StringIO(c10.decode('utf-8')), index_col='Unnamed: 0')

# Navigation bar
navbar = dbc.Nav([dbc.NavLink('Home', href='/index', external_link=True), 
                  dbc.NavLink('U.S. Dashboard', href='/us/', external_link=True), 
                  dbc.NavLink('World Dashboard', href='/world/', external_link=True), 
                  dbc.NavLink('2023 Predictions Dashboard', href="/predictions/", external_link=True)], 
                  class_name='navigation')

# Creating the default prediction graph
incidents_count_fig = px.line(incidents_count_forecast, 
                              x=incidents_count_forecast.index, 
                              y='Linear Regression', 
                              color='Legend', 
                              labels={'index': 'Date', 
                                      'Linear Regression': 'Number of U.S. Shooting Incidents'}, 
                              title='Forecasting Incidents with Linear Regression (2023 Prediction)')

# Predictions dashboard
dash_app3 = Dash(__name__, server=app, routes_pathname_prefix='/predictions/')
dash_app3.layout = html.Div([
    html.H1('U.S. Mass Shootings from 2017 to 2022', className='header'), 
    navbar, 
    html.H2('2023 Predictions Dashboard', className='dash_heading'),
    html.Hr(), 
    html.Div([
        html.Div([
            html.H3('Figure Selection', className='dash_heading'), 
            dcc.Dropdown(['U.S. Shooting Incidents', 
                          'U.S. Shooting Victims Killed', 
                          'U.S. Shooting Victims Injured'], 
                         'U.S. Shooting Incidents', id='graph_selection')], 
            style={'width': '45%'}),
        html.Div([
            html.H3('Forecasting Method', className='dash_heading'), 
            dcc.Dropdown(['Linear Regression', 'Polynomial Regression', 'ARIMA', 
                          'Simple Exponential Smoothing', 'Holt\'s Method'], 
                         'Linear Regression', id='forecast_selection')], 
            style={'width': '45%', 'margin-left': '15px'})], 
        style=dict(display='flex')), 
    html.Div([dcc.Graph(figure=incidents_count_fig, id='graph')])])

@dash_app3.callback(
    Output('graph', 'figure'),
    Input('graph_selection', 'value'), 
    Input('forecast_selection', 'value'))

def update_graph(graph, forecast):
    if graph == 'U.S. Shooting Incidents':
        incidents_count_fig = px.line(incidents_count_forecast, 
              x=incidents_count_forecast.index, 
              y=forecast, 
              color='Legend', 
              labels={'index': 'Date', 
                      forecast: 'Number of U.S. Shooting Incidents'}, 
              title='Forecasting Incidents with ' + forecast + ' (2023 Prediction)')
        fig = incidents_count_fig
    
    if graph == 'U.S. Shooting Victims Killed':
        victims_killed_fig = px.line(victims_killed_forecast, 
              x=victims_killed_forecast.index, 
              y=forecast, 
              color='Legend', 
              labels={'index': 'Date', 
                      forecast: 'Number of U.S. Shooting Victims'}, 
              title='Forecasting Victims Killed with ' + forecast + ' (2023 Prediction)')
        fig = victims_killed_fig
        
    if graph == 'U.S. Shooting Victims Injured':
        victims_injured_fig = px.line(victims_injured_forecast, 
              x=victims_injured_forecast.index, 
              y=forecast, 
              color='Legend', 
              labels={'index': 'Date', 
                      forecast: 'Number of U.S. Shooting Victims'}, 
              title='Forecasting Victims Injured with ' + forecast + ' (2023 Prediction)')
        fig = victims_injured_fig
    return fig

if __name__ == '__main__':
    dash_app3.run(port=8052)