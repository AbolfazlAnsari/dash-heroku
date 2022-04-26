#import dash
#import dash_core_components as dcc
#import dash_bootstrap_components as dbc
#import dash_html_components as html
#=========================================main=========================================================
# import
# essential imports
# essential imports
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input

import plotly.express as px
import math
from dash import no_update

import pandas as pd
import numpy as np
import json


# read data
df_country = pd.read_csv("https://raw.githubusercontent.com/smbillah/ist526/main/gapminder.csv")

fig_scatter = px.scatter(
  data_frame = df_country, 
  x="lifeExp",         # gdp per capita
  y="gdpPercap",           # life expectancy  
  #size="pop",            # population
  color="continent",     # group/label
  hover_name="country",
  log_x=True, 
  #size_max=55, 
  range_x=[25,75], 
  range_y=[100,100000],
  title= "Life Expectancy vs GDP Per Captia of Countries", 
  
  # animation control
  #animation_frame="year", 
  #animation_group="country",
)

df_sao=df_country[(df_country["country"] == "Sao Tome and Principe")]

fig_bar = px.bar(
  data_frame = df_sao, 
  x="year",        # continent
  y="lifeExp",              # population    
  #color="continent",    # group/label
    
  #range_y=[0, 8000000000],
  title= "Life Expectancy of Sao Tome and Principe in different year", 
  
  # animation control
  #animation_frame="year", 
  #animation_group="country",
)

# this css creates columns and row layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# this is new
available_indicators = ['lifeExp',	'pop',	'gdpPercap']

## Uncomment the following line for runnning in Google Colab
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

## Uncomment the following line for running in a webbrowser
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# layout


app.layout = html.Div([
  # first row: header
  html.H4('A Sample Interactive Dashboard'),

  # second row: two drop-downs and radio-boxes. Each dropdown will take 4-column width
  html.Div([
    html.Div([
      dcc.Dropdown(
        id='xaxis-column',
        options=[{'label': i, 'value': i} for i in available_indicators], #e.g., {label: 'pop', 'value':'pop'}
        value='lifeExp'
      ),
      dcc.RadioItems(
        id='xaxis-type',
        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
        value='Linear',
        labelStyle={'display': 'inline-block'}
      )
    ], className='seven columns'),

    html.Div([
      dcc.Dropdown(
        id='yaxis-column',
        options=[{'label': i, 'value': i} for i in available_indicators],
        value='gdpPercap'
      ),
      dcc.RadioItems(
        id='yaxis-type',
        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
        value='Linear',
        labelStyle={'display': 'inline-block'}
      )
    ], className='five columns')

  ], className='row'),

  # third row: <scratter-plot> <bar chart>  
  html.Div([
            
    # scratter plot                      
    html.Div([
              
      # add scatter plot
      dcc.Graph(
        id='scatter-graph',
        figure=fig_scatter # we'll create one inside update_figure function
      ),
      
      # add slider
      dcc.Slider(
        id='year-slider',
        min=df_country['year'].min(),
        max=df_country['year'].max(),
        value=df_country['year'].min(),
        marks={str(year): str(year) for year in df_country['year'].unique()},
        step=None
      ),
      html.H3('Debug'),
    ], className = 'seven columns'),   

    html.Div([
      dcc.Graph(
          id='bar-graph',
          figure=fig_bar
      )
    ], className = 'five columns')
  ], className = 'row')    
])

# second callback definition
@app.callback(
  Output('scatter-graph', 'figure'), # one output, multiple input
  Input('year-slider', 'value'),
  Input('xaxis-column', 'value'),
  Input('yaxis-column', 'value'),
  Input('xaxis-type', 'value'),
  Input('yaxis-type', 'value'),
)

# second callback function
def update_graph(selected_year, xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type):
  # print all input params
  debug_params ='Input: {0}, {1}, {2}, {3}, {4}'.format(selected_year, xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type)

  # filter data frame by year
  filtered_df = df_country[df_country.year == selected_year]

  fig_scatter = px.scatter(
    data_frame = filtered_df,
    x=str(xaxis_column_name),
    y=str(yaxis_column_name),
    hover_name="country",
    color="continent",
    #size = 'pop',
    size_max=55,
    title= "{0}  vs {1} of Countries".format(xaxis_column_name, yaxis_column_name)
  )

  fig_scatter.update_layout(transition_duration=500)

  fig_scatter.update_xaxes(
    title=xaxis_column_name,
    type='linear' if xaxis_type == 'Linear' else 'log'
  )

  fig_scatter.update_yaxes(
    title=yaxis_column_name,
    type='linear' if yaxis_type == 'Linear' else 'log'
  )
  # return
  return fig_scatter

# end update_

# run the code
# uncomment the following line to run in Google Colab
#app.run_server(mode='inline', port=2210)

# uncomment the following lines to run in Browser via command line/terminal
#if __name__ == '__main__':
#app.run_server(debug=True, host='127.0.0.1', port=8050)
# Run dash app
if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=8050)
 
