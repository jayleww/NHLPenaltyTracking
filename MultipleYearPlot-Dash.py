
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from datetime import datetime


# In[2]:


#Dictionary of team names and abbreviations. VEG is used instead of VGK.
teamAbvs = {'Anaheim Ducks':'ANA', 'Arizona Coyotes':'ARI', 'Boston Bruins': 'BOS', 'Buffalo Sabres':'BUF', 'Carolina Hurricanes':'CAR',
            'Calgary Flames':'CGY', 'Chicago Blackhawks':'CHI', 'Columbus Blue Jackets':'CBJ', 'Colorado Avalanche':'COL', 'Dallas Stars':'DAL',
           'Detroit Red Wings':'DET', 'Edmonton Oilers':'EDM', 'Florida Panthers':'FLA', 'Los Angeles Kings':'LAK',
           'Minnesota Wild':'MIN', 'Montreal Canadiens':'MTL', 'Nashville Predators':'NSH', 'New Jersey Devils':'NJD',
           'New York Islanders':'NYI', 'New York Rangers':'NYR', 'Ottawa Senators':'OTT', 'Phoenix Coyotes':'PHX', 'Philadelphia Flyers':'PHI',
           'Pittsburgh Penguins':'PIT', 'San Jose Sharks':'SJS', 'St. Louis Blues':'STL', 'Tampa Bay Lightning':'TBL',
           'Toronto Maple Leafs':'TOR','Vancouver Canucks':'VAN', 'Vegas Golden Knights':'VEG', 'Washington Capitals':'WSH', 'Winnipeg Jets':'WPG',
           }


# In[3]:


app = dash.Dash()


# In[5]:


app.layout = html.Div([
    
    html.Div([
        html.Label('Team'),
        dcc.Dropdown(id='teams', 
                     options=[{'label': i, 'value': i} for i in sorted(list(teamAbvs.values()))]
                          ),
        ],
    style={'width': '48%', 'display': 'inline-block'}
            ),
    
    html.Div([
        html.Label('Seasons'),
        dcc.Dropdown(id='years',
                          options=[
                              {'label': '2014/2015', 'value': '2015'},
                              {'label': '2015/2016', 'value': '2016'},
                              {'label': '2016/2017', 'value': '2017'},
                              {'label': '2017/2018', 'value': '2018'}
                              ],
                          multi=True
                          ),
        
    ],
    style={'width': '48%', 'display': 'inline-block'}
            ),
    
    dcc.Graph(id='teamgraph'),
    html.Div(id='outputteams')
])

@app.callback(dash.dependencies.Output('teamgraph', 'figure'), 
              [dash.dependencies.Input('teams', 'value'),
              dash.dependencies.Input('years', 'value')
              ])

def callback_teams(teamname, yearlist):
    traces = []
    for year in yearlist:
        team_data = pd.read_csv('team_penalties_'+year, header=[0,1])
        wanted_team = team_data[teamname]
        penalties = wanted_team.columns.drop('total')
        totals = []
        for penalty in penalties:
            totals.append(wanted_team[penalty].sum())
        penalties = [word.replace('sticking', 'highsticking') for word in penalties]
        traces.append(go.Bar(x=penalties, y=totals, name=year, text=totals, textposition='auto', hoverinfo='none'))
    
    
    return {
        'data' : traces,
        'layout' : go.Layout(barmode='group', title = 'Penalty Calls - '+teamname,
                        yaxis = dict(title='Number of Calls', showgrid=True, linecolor='black', linewidth=2, mirror=True), 
                        xaxis = dict(title='Penalty', showgrid=True, linecolor='black', linewidth=2, mirror=True))
    }



# In[ ]:


if __name__ == '__main__':
    app.run_server()

