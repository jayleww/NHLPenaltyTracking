
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
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


app = dash.Dash(__name__)
server = app.server


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
                              #{'label': '2013/2014', 'value': '2014'},
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
    html.Div(id='outputteams'),
    
    html.Div([
        html.Label('Penalty'),
        dcc.Dropdown(id='penaltyselect',
                     options=[
                         {'label': 'Slashing', 'value': 'slashing'},
                         {'label': 'Hooking', 'value': 'hooking'},
                         {'label': 'Tripping', 'value': 'tripping'},
                         {'label': 'Highsticking', 'value': 'sticking'},
                         {'label': 'Interference', 'value': 'interference'},
                         {'label': 'Roughing', 'value': 'roughing'},
                         {'label': 'Fighting', 'value': 'fighting'}
                     ],
                    ),
    ],
            style={'width': '48%', 'display': 'inline-block'}
    ),
    
        html.Div([
        html.Label('Seasons'),
        dcc.Dropdown(id='penaltyyears',
                          options=[
                              #{'label': '2013/2014', 'value': '2014'},
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
    dcc.Graph(id='penaltygraph'),
    html.Div(id='outputpenalty'),
    
    
        
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

@app.callback(dash.dependencies.Output('penaltygraph', 'figure'),
              [dash.dependencies.Input('penaltyselect', 'value'),
               dash.dependencies.Input('penaltyyears', 'value')
              ])

def callback_penalties(penalty, yearlist):
    traces = []
    for year in yearlist:
        teams_data = pd.read_csv('team_penalties_'+year, header=[0,1])
        teams = sorted(list(teamAbvs.values()))
        plot_data = pd.DataFrame()
        plot_data['Team'] = teams
        plot_data['Penalty Total'] = plot_data['Team'].apply(lambda team: teams_data[team][penalty].sum())
        if len(yearlist) == 1:
            plot_data.sort_values(by='Penalty Total', ascending=False, inplace=True)
        plot_data = plot_data[plot_data['Penalty Total'] > 0]
        traces.append(go.Bar(x=plot_data['Team'], y=plot_data['Penalty Total'], name=year, text=''))
    
    return {
        'data' : traces,
        'layout' : go.Layout(barmode='group', title = penalty.capitalize()+' Calls per Team', 
                             yaxis = dict(title='Number of Calls', showgrid=True, linecolor='black', linewidth=2, mirror=True), 
                             xaxis = dict(title='Team', showgrid=True, linecolor='black', linewidth=2, mirror=True))
    }
    


# In[ ]:


if __name__ == '__main__':
    app.run_server(debug=True)

