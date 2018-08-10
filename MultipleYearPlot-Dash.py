# coding: utf-8
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from datetime import datetime

#Dictionary of team names and abbreviations. VEG is used instead of VGK.
teamAbvs = {'Anaheim Ducks':'ANA', 'Arizona/Phoenix Coyotes':'ARI', 'Boston Bruins': 'BOS', 'Buffalo Sabres':'BUF', 'Carolina Hurricanes':'CAR', 'Calgary Flames':'CGY', 'Chicago Blackhawks':'CHI', 'Columbus Blue Jackets':'CBJ', 'Colorado Avalanche':'COL', 'Dallas Stars':'DAL', 'Detroit Red Wings':'DET', 'Edmonton Oilers':'EDM', 'Florida Panthers':'FLA', 'Los Angeles Kings':'LAK','Minnesota Wild':'MIN', 'Montreal Canadiens':'MTL', 'Nashville Predators':'NSH', 'New Jersey Devils':'NJD','New York Islanders':'NYI', 'New York Rangers':'NYR', 'Ottawa Senators':'OTT', 'Philadelphia Flyers':'PHI','Pittsburgh Penguins':'PIT', 'San Jose Sharks':'SJS', 'St. Louis Blues':'STL', 'Tampa Bay Lightning':'TBL','Toronto Maple Leafs':'TOR','Vancouver Canucks':'VAN', 'Vegas Golden Knights':'VEG', 'Washington Capitals':'WSH', 'Winnipeg Jets/Atlanta Thrashers':'WPG',
           }

#Use this for drop down labels/values 
sortedteamAbvsKeys = sorted(list(teamAbvs.keys()))
sortedteamAbvsValues = [teamAbvs[value] for value in sortedteamAbvsKeys]

#Start the server.
app = dash.Dash(__name__)
server = app.server

#Enter text for the top of the dashboard.
markdown_text = '''
### NHL Penalty Tracking
Pick a team or a penalty to view and the seasons to be displayed. Choosing NHL will display the totals for the entire league.
'''

#Start of the layout.
app.layout = html.Div([
    #Markdown division.
    html.Div([
    dcc.Markdown(children=markdown_text),
                 ]),
    #Team selection dropdown.
    html.Div([
        html.Label('Team'),
        dcc.Dropdown(id='teams', 
                     options=[{'label': i, 'value': j} for i, j in zip(['NHL']+sortedteamAbvsKeys,['NHL']+sortedteamAbvsValues)],
                     placeholder='Choose a team',
                          ),
        ],
    style={'width': '48%', 'display': 'inline-block'}
            ),
    #Season selection dropdown.
    html.Div([
        html.Label('Seasons'),
        dcc.Dropdown(id='years',
                          options=[
                              {'label': '2007/2008', 'value': '2008'},
                              {'label': '2008/2009', 'value': '2009'},
                              {'label': '2009/2010', 'value': '2010'},
                              {'label': '2010/2011', 'value': '2011'},
                              {'label': '2011/2012', 'value': '2012'},
                              {'label': '2012/2013', 'value': '2013'},
                              {'label': '2013/2014', 'value': '2014'},
                              {'label': '2014/2015', 'value': '2015'},
                              {'label': '2015/2016', 'value': '2016'},
                              {'label': '2016/2017', 'value': '2017'},
                              {'label': '2017/2018', 'value': '2018'}
                              ],
                          multi=True, placeholder='Choose the season/seasons to display',
                          ),
        
    ],
    style={'width': '48%', 'display': 'inline-block'}
            ),
    #Location of penalty plot for individual teams or entire league.
    dcc.Graph(id='teamgraph',
             figure={
             'data' : [go.Bar(x=['slashing', 'hooking', 'tripping','interference', 'highsticking', 'roughing', 'fighting' ],
                             y=[0,0,0,0,0,0,0],
                             )
                      ],
                 'layout' : go.Layout(title = 'Penalty Calls per Team',
                                      yaxis = dict(title='Number of Calls', showgrid=True, linecolor='black', linewidth=2, mirror=True), 
                                      xaxis = dict(title='Penalty', showgrid=True, linecolor='black', linewidth=2, mirror=True))
             },
              config={'displayModeBar': False
                     }
             ),
    html.Div(id='outputteams'),
    #Penalty dropdown menu.
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
                     placeholder='Choose a penalty to display',
                    ),
    ],
            style={'width': '48%', 'display': 'inline-block'}
    ),
    #Season selection dropdown.
        html.Div([
        html.Label('Seasons'),
        dcc.Dropdown(id='penaltyyears',
                          options=[
                              {'label': '2007/2008', 'value': '2008'},
                              {'label': '2008/2009', 'value': '2009'},
                              {'label': '2009/2010', 'value': '2010'},
                              {'label': '2010/2011', 'value': '2011'},
                              {'label': '2011/2012', 'value': '2012'},
                              {'label': '2012/2013', 'value': '2013'},
                              {'label': '2013/2014', 'value': '2014'},
                              {'label': '2014/2015', 'value': '2015'},
                              {'label': '2015/2016', 'value': '2016'},
                              {'label': '2016/2017', 'value': '2017'},
                              {'label': '2017/2018', 'value': '2018'}
                              ],
                          multi=True, placeholder='Choose the season/seasons to display',
                          ),
        
    ],
    style={'width': '48%', 'display': 'inline-block'}
            ),
    #Team plots for each penalty and season chosen.
    dcc.Graph(id='penaltygraph',
             figure={
             'data' : [go.Bar(x=sorted(list(teamAbvs.values())),
                             y=np.zeros(len(teamAbvs))
                             )
                      ],
                 'layout' : go.Layout(title = 'Penalty Calls Each Season',
                                      yaxis = dict(title='Number of Calls', showgrid=True, linecolor='black', linewidth=2, mirror=True), 
                                      xaxis = dict(title='Team', showgrid=True, linecolor='black', linewidth=2, mirror=True))
             },
              config={'displayModeBar': False
                     }
             ),
    html.Div(id='outputpenalty'),
    
    
        
])

@app.callback(dash.dependencies.Output('teamgraph', 'figure'), 
              [dash.dependencies.Input('teams', 'value'),
              dash.dependencies.Input('years', 'value')
              ])

#Call back to create the teamplot
def callback_teams(teamname, yearlist):
    traces = []
    #Check if the entire NHL was chosen. 
    if teamname == 'NHL':
        penalty_data = pd.read_csv('yearly_penalty_totals')
        penalties = penalty_data.columns.drop('Year')
        #Replace 'sticking' with 'highsticking'. Issue with data collection.
        penalties = [word.replace('sticking', 'highsticking') for word in penalties]
        for year in sorted(yearlist):
            #Need custom trace name for lockout season
            if year == '2013':
                name = '2013 - Lockout'
            else:
                name = year 
            year = int(year)
            totals = list(penalty_data[penalty_data['Year']==year].drop('Year', axis=1).iloc[0]) 
            traces.append(go.Bar(x=penalties, y=totals, name=name, text=totals, textposition='auto', hoverinfo='none'))
    else:    
        for year in sorted(yearlist):
            team_data = pd.read_csv('team_penalties_'+year, header=[0,1])
            wanted_team = team_data[teamname]
            penalties = wanted_team.columns.drop('total')
            totals = []
            for penalty in penalties:
                totals.append(wanted_team[penalty].sum())
            penalties = [word.replace('sticking', 'highsticking') for word in penalties]
            if year == '2013':
                name = '2013 - Lockout'
            else:
                name = year
            traces.append(go.Bar(x=penalties, y=totals, name=name, text=totals, textposition='auto', hoverinfo='none'))
    
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
    for year in sorted(yearlist):
        teams_data = pd.read_csv('team_penalties_'+year, header=[0,1])
        teams = sorted(list(teamAbvs.values()))
        plot_data = pd.DataFrame()
        plot_data['Team'] = teams
        plot_data['Penalty Total'] = plot_data['Team'].apply(lambda team: teams_data[team][penalty].sum())
        if len(yearlist) == 1:
            plot_data.sort_values(by='Penalty Total', ascending=False, inplace=True)
        plot_data = plot_data[plot_data['Penalty Total'] > 0]
        if year == '2013':
            name = '2013 - Lockout'
        else:
            name = year 
        traces.append(go.Bar(x=plot_data['Team'], y=plot_data['Penalty Total'], name=name, text=''))
    
    return {
        'data' : traces,
        'layout' : go.Layout(barmode='group', title = penalty.capitalize()+' Calls per Team', 
                             yaxis = dict(title='Number of Calls', showgrid=True, linecolor='black', linewidth=2, mirror=True), 
                             xaxis = dict(title='Team', showgrid=True, linecolor='black', linewidth=2, mirror=True))
    }
    

if __name__ == '__main__':
    app.run_server(debug=True)

