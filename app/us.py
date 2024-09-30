from app import app
import requests
import io
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

# Reading in the csv files
c1 = requests.get('https://raw.githubusercontent.com/annednguyen00/CSC-698/main/3.%20Dashboard/data/state_incidents.csv').content
state_incidents = pd.read_csv(io.StringIO(c1.decode('utf-8')), index_col='Unnamed: 0')
c2 = requests.get('https://raw.githubusercontent.com/annednguyen00/CSC-698/main/3.%20Dashboard/data/state_victims.csv').content
state_victims = pd.read_csv(io.StringIO(c2.decode('utf-8')), index_col='Unnamed: 0')
c3 = requests.get('https://raw.githubusercontent.com/annednguyen00/CSC-698/main/3.%20Dashboard/data/victims_killed.csv').content
victims_killed = pd.read_csv(io.StringIO(c3.decode('utf-8')), index_col='Unnamed: 0')
c4 = requests.get('https://raw.githubusercontent.com/annednguyen00/CSC-698/main/3.%20Dashboard/data/victims_injured.csv').content
victims_injured = pd.read_csv(io.StringIO(c4.decode('utf-8')), index_col='Unnamed: 0')
c5 = requests.get('https://raw.githubusercontent.com/annednguyen00/CSC-698/main/3.%20Dashboard/data/guns.csv').content
guns = pd.read_csv(io.StringIO(c5.decode('utf-8')), index_col='state')

# Navigation bar
navbar = dbc.Nav([dbc.NavLink('Home', href='/index', external_link=True), 
                  dbc.NavLink('U.S. Dashboard', href='/us/', external_link=True), 
                  dbc.NavLink('World Dashboard', href='/world/', external_link=True), 
                  dbc.NavLink('2023 Predictions Dashboard', href="/predictions/", external_link=True)], 
                  class_name='navigation')

# Creating the default U.S. map
state_incidents_fig = go.Figure(data=go.Choropleth(locations=state_incidents.index, 
                                                   z=state_incidents['2017-2022'], 
                                                   text=state_incidents['state'], 
                                                   locationmode='USA-states', 
                                                   colorscale='Reds',
                                                   colorbar_title='Number of Shootings'))
state_incidents_fig.update_layout(title_text='Number of Mass Shootings by State (2017-2022)', 
                                  geo_scope='usa')

# U.S. dashboard
dash_app1 = Dash(__name__, server=app, routes_pathname_prefix='/us/')
dash_app1.layout = html.Div([
    html.H1('U.S. Mass Shootings from 2017 to 2022', className='header'), 
    navbar, 
    html.H2('U.S. Dashboard', className='dash_heading'), 
    html.Hr(), 
    html.Div([
        html.Div([
            html.H3('Figure Selection', className='dash_heading'),
            dcc.Dropdown(['Number of Mass Shootings', 'Number of Shooting Victims', 
                          'Shooting Victims Killed', 'Shooting Victims Injured', 
                          'Number of Guns'], 
                          'Number of Mass Shootings', id='graph_selection')], style={'width': '45%'}), 
        html.Div([
            html.H3('Year', className='dash_heading'),
            dcc.Dropdown(['2017-2022', '2022', '2021', '2020', '2019', '2018', '2017'], 
                          '2017-2022', id='year_selection')], style={'width': '45%', 'margin-left': '15px'})], 
        style=dict(display='flex')),
    html.Div([dcc.Graph(figure=state_incidents_fig, id='graph')])])

@dash_app1.callback(
    Output('graph', 'figure'),
    Input('graph_selection', 'value'), 
    Input('year_selection', 'value'))

def update_graph(graph, year):
    if graph == 'Number of Mass Shootings':
        state_incidents_fig = go.Figure(
            data=go.Choropleth(locations=state_incidents.index, 
                               z=state_incidents[year], 
                               text=state_incidents['state'], 
                               locationmode='USA-states', 
                               colorscale='Reds',
                               colorbar_title='Number of Shootings'))
        state_incidents_fig.update_layout(title_text='Number of Mass Shootings by State (' + year + ')', 
                                          geo_scope='usa')
        fig = state_incidents_fig
    
    if graph == 'Number of Shooting Victims':
        state_victims_fig = go.Figure(
            data=go.Choropleth(locations=state_victims.index, 
                               z=state_victims[year], 
                               text=state_victims['state'], 
                               locationmode='USA-states', 
                               colorscale='Purples',
                               colorbar_title='Number of Victims'))
        state_victims_fig.update_layout(title_text='Number of Shooting Victims by State (' + year + ')', 
                                        geo_scope='usa')
        fig = state_victims_fig 
        
    if graph == 'Shooting Victims Killed':
        victims_killed_fig = go.Figure(
            data=go.Choropleth(locations=victims_killed.index, 
                               z=victims_killed[year], 
                               text=victims_killed['state'], 
                               locationmode='USA-states', 
                               colorscale='Purples',
                               colorbar_title='Number of Victims'))
        victims_killed_fig.update_layout(title_text='Shooting Victims Killed by State (' + year + ')', 
                                         geo_scope='usa')
        fig = victims_killed_fig
        
    if graph == 'Shooting Victims Injured':
        victims_injured_fig = go.Figure(
            data=go.Choropleth(locations=victims_injured.index, 
                               z=victims_injured[year], 
                               text=victims_injured['state'], 
                               locationmode='USA-states', 
                               colorscale='Purples',
                               colorbar_title='Number of Victims'))
        victims_injured_fig.update_layout(title_text='Shooting Victims Injured by State (' + year + ')', 
                                          geo_scope='usa')
        fig = victims_injured_fig
        
    if graph == 'Number of Guns':
        guns_fig = go.Figure(
            data=go.Choropleth(locations=guns.index, 
                               z=guns[year], 
                               text=guns['state.1'], 
                               locationmode='USA-states', 
                               colorscale='Blues',
                               colorbar_title='Number of Guns'))
        guns_fig.update_layout(title_text='Number of Guns by State (' + year + ')', 
                               geo_scope='usa')
        fig = guns_fig
    return fig

if __name__ == '__main__':
    dash_app1.run(port=8050) 