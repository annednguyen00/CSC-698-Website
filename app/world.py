from app import app
import requests
import io
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

c6 = requests.get('https://raw.githubusercontent.com/annednguyen00/CSC-698/main/3.%20Dashboard/data/new_countries_count.csv').content
new_countries_count = pd.read_csv(io.StringIO(c6.decode('utf-8')), index_col='Iso3_code')
c7 = requests.get('https://raw.githubusercontent.com/annednguyen00/CSC-698/main/3.%20Dashboard/data/new_countries_rate.csv').content
new_countries_rate = pd.read_csv(io.StringIO(c7.decode('utf-8')), index_col='Iso3_code')

# Navigation bar
navbar = dbc.Nav([dbc.NavLink('Home', href='/index', external_link=True), 
                  dbc.NavLink('U.S. Dashboard', href='/us/', external_link=True), 
                  dbc.NavLink('World Dashboard', href='/world/', external_link=True), 
                  dbc.NavLink('2023 Predictions Dashboard', href="/predictions/", external_link=True)], 
                  class_name='navigation')

# Creating the default world map
countries_count_fig = go.Figure(data=go.Choropleth(locations=new_countries_count.index,
                                                   z=new_countries_count['2017-2022'],
                                                   text=new_countries_count['country'], 
                                                   colorscale='Purples', 
                                                   colorbar_title='Number of Victims'))
countries_count_fig.update_layout(title_text='Number of Victims of Firearm Homicides by Country (2017-2022)')

# World dashboard
dash_app2 = Dash(__name__, server=app, routes_pathname_prefix='/world/')
dash_app2.layout = html.Div([
    html.H1('U.S. Mass Shootings from 2017 to 2022', className='header'), 
    navbar, 
    html.H2('World Dashboard', className='dash_heading'),
    html.Hr(), 
    html.Div([
        html.Div([
            html.H3('Figure Selection', className='dash_heading'), 
            dcc.Dropdown(['Number of Victims of Firearm Homicides by Country', 
                          'Victims of Firearm Homicides per 100,000 Population by Country'], 
                         'Number of Victims of Firearm Homicides by Country', 
                         id='graph_selection')], style={'width': '45%'}),
        html.Div([
            html.H3('Year', className='dash_heading'), 
            dcc.Dropdown(['2017-2022', '2022', '2021', '2020', '2019', '2018', '2017'], 
                         '2017-2022', id='year_selection')], style={'width': '45%', 'margin-left': '15px'})], 
        style=dict(display='flex')),
    html.Div([dcc.Graph(figure=countries_count_fig, id='graph')])])

@dash_app2.callback(
    Output('graph', 'figure'),
    Input('graph_selection', 'value'), 
    Input('year_selection', 'value'))

def update_graph(graph, year):
    if graph == 'Number of Victims of Firearm Homicides by Country':
        countries_count_fig = go.Figure(
            data=go.Choropleth(locations=new_countries_count.index,
                               z=new_countries_count[year],
                               text=new_countries_count['country'], 
                               colorscale='Purples', 
                               colorbar_title='Number of Victims'))
        countries_count_fig.update_layout(
            title_text='Number of Victims of Firearm Homicides by Country (' + year + ')')
        fig = countries_count_fig
    
    if graph == 'Victims of Firearm Homicides per 100,000 Population by Country':
        countries_rate_fig = go.Figure(
            data=go.Choropleth(locations=new_countries_rate.index,
                               z=new_countries_rate[year],
                               text=new_countries_rate['country'], 
                               colorscale='Purples', 
                               colorbar_title='Number of Victims'))
        countries_rate_fig.update_layout(
            title_text='Victims of Firearm Homicides per 100,000 Population by Country (' + year + ')')
        fig = countries_rate_fig
    return fig

if __name__ == '__main__':
    dash_app2.run(port=8051)