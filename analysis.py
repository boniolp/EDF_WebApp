import os
import sys
sys.path.insert(0, './src')

#import plotly.plotly as py
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from htmlTool import *
from preProcessing import *

from observation import *
from interval import *
from tools import *
from constants import *
from scale  import *
from score  import *
from rule  import *


#List of possible anomalies with a particular duration

anomalies = [
	("spike",MinutesScale(), Spike()),    # 1 day

	("osc_3h",MinutesScale(), Oscillation(3,18)),  # 3 hours
	("osc_6h",MinutesScale(20), Oscillation(18)), # 6 hours
	("osc_1d",HourScale(1), Oscillation(24)),    # 1 day

	("step_1d",HourScale(1), Step(24)),    # 1 day
	("step_5d",HourScale(4), Step(30)),    # 5 days
	("step_10d",HourScale(8), Step(30)),  # 10 days

	("trend_5d",HourScale(4), Trend(30)),   # 5 days
	("trend_15d",HourScale(12), Trend(30)), # 15 days
	("trend_30d",DayScale(1), Trend(30)),   # 30 days
	("trend_60d",DayScale(2), Trend(30))    # 60 days
]

#function related to score dataframe

def score_list_df(list_df, feature):
	list_score_df = []
	for df in list_df:
		list_score_df += [feature.score(df[deb1[0]])]
	return pd.concat(list_score_df, axis=0)
    
def list_subsampled(obs, scale_df):
    return obs.low_regime_intervals.split_between(
		scale_df.scale(obs.full_concatenated_df), time=timedelta(days=3))

def compute_score_df(obs,df):
	scores_df = []
	for name, scale, feature in anomalies:
		score_df = score_list_df(list_subsampled(obs,scale),feature)
		score_df = score_df[~score_df.isnull()]
		score_df.columns = [deb1[0]]
		scores_df += [score_df.to_frame(name)]

	scores_concat = pd.concat(scores_df, axis=1)  
	scores_concat.fillna(method='bfill',inplace=True)
	return scores_concat

#Stock of the Resutl

score_dataFrame = compute_score_df(obs,df_full)

analisys_layout = [
	html.H1(children='EDF Vizualisation',
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'backgroundColor': 'rgb(250, 250, 250)'
            }
        ),

    html.Div(children='Detection of anomalies in EDF sensors',
        style={
                'textAlign': 'center',
                'color': colors['text'],
                'backgroundColor': 'rgb(250, 250, 250)'
            }
    ),

    html.Div(children='Work by Edouard Melhman, Paul Boniol',
        style={
                'textAlign': 'center',
                'color': colors['text'],
                'backgroundColor': 'rgb(250, 250, 250)'
            }
    ),

    html.Div(children='Directed by Themis Palpanas',
        style={
                'textAlign': 'center',
                'color': colors['text'],
                'backgroundColor': 'rgb(250, 250, 250)',
                'borderBottom': 'thin lightgrey solid'
            }
    ),

    html.H3(children='Choose mode',style={'textAlign':'center'}),
    html.Label(''),
    dcc.Dropdown( 
        id='display_mode',
        options=[{'label':'Visualization', 'value':0},
                {'label':'AnomalyAnalysis', 'value':1}
            ],
        value='AnomalyAnalysis',
        multi=False
    ),


    html.H3(children='Main visualization',style={'textAlign':'center'}),

    html.Label(''),
    dcc.Dropdown(
        id='feature_param',
        options=[{'label': x, 'value':x} for x in suffixes_deb],
        value=[suffixes[0]],
        multi=True
    ),

    dcc.Graph(
        id='main_graph',
        figure=dict(
            data=[go.Scatter(x=df1.index, y=df1.values, name= suffixes_deb[0])],
            layout=dict(
                paper_bgcolor='rgb(250, 250, 250)',
                title='Deb1-1 sensor',
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1,
                                label='1m',
                                step='month',
                                stepmode='backward'),
                            dict(count=6,
                                label='6m',
                                step='month',
                                stepmode='backward'),
                            dict(count=1,
                                label='1y',
                                step='year',
                                stepmode='backward'),
                            dict(step='all')
                        ])
                    ),
                    rangeslider=dict(),
                    type='date'
                )
            )
        )
    ),

	html.H3(children='Anomaly type:',style={'textAlign':'center'}),

    html.Label(''),
    dcc.Dropdown(
        id='anomaly_type',
        options=[{'label': x[0], 'value':x[0]} for x in anomalies],
        value=[anomalies[0][0]],
        multi=True
    ),

    dcc.Graph(
        id='anomaly_graph',
    ),

    html.H4(children='Score for each anomaly categories', style={'textAlgin':'center'}),
    generate_table(score_dataFrame,50)

]


@app.callback(dash.dependencies.Output('anomaly_graph', 'figure'),
              [dash.dependencies.Input('anomaly_type', 'value')])
def make_anomaly_figure(anomaly_type):
    data = []
    title=""
    for i in range(len(anomaly_type)):
        df1 = score_dataFrame[anomaly_type[i]]
        df1 = resample(df1)
        data.append(go.Scatter(x=df1.index, y=df1.values, name= anomaly_type[i]))
        title = title + "  " + anomaly_type[i]
    
    if (data == []):
        data = [go.Scatter(x=[], y=[])]    

    return dict( 
            data=data,
            layout=dict(
                paper_bgcolor='rgb(250, 250, 250)',
                title=title,
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1,
                                label='1m',
                                step='month',
                                stepmode='backward'),
                            dict(count=6,
                                label='6m',
                                step='month',
                                stepmode='backward'),
                            dict(count=1,
                                label='1y',
                                step='year',
                                stepmode='backward'),
                            dict(step='all')
                        ])
                    ),
                    rangeslider=dict(),
                    type='date'
                )
            )
        )







