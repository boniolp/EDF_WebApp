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
from analysis import *

from observation import *
from interval import *
from tools import *
from constants import *




#app = dash.Dash()

app_layout = []

visualization_layout = [
    html.H1(children='EDF Visualization',
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

    html.Div(children='Work by Edouard Mehlman, Paul Boniol',
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

    html.H3(children='Choose mode', style={'textAlign':'center'}),
    html.Label(''),
    dcc.Dropdown( 
        id='display_mode',
        options=[{'label':'Visualization', 'value':0},
            {'label':'AnomalyAnalysis', 'value':1}
        ],
        value='Visualization',
        multi=False
    ),

    html.H3(children='Main visualization', style={'textAlign':'center'}),

    html.Label(''),
    dcc.Dropdown(
        id='feature_param',
        options=[{'label': x, 'value':x} for x in suffixes_deb],
        value=[suffixes[0]],
        multi=True
    ),


    #html.Div(
    #        [  
    #           dcc.RangeSlider(
    #                id='year_slider',
    #                min=2006,
    #                max=2016,
    #                value=[2006, 2016]
    #           ),
    #        ],
    #        style={'margin-top': '20'}
    #    ),


    dcc.Graph(
        id='main_graph',
        figure=dict(
            data=[go.Scatter(x=df1.index, y=df1.values, name= suffixes_deb[0])],
            layout=dict(
                #dragmode='select',
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

    html.Div(children=html.H3("Other paramters"), style={'text-align': 'center'}),


    html.Div([

        dcc.Dropdown(
            id='related_param_1',
            options=[{'label': x, 'value':x} for x in suffixes_param],
            value=[suffixes[0]],
            multi=False
        ),
            dcc.Graph(
                id='related_graph_1',
                figure=dict()
            )

    ], style={'width': '49%', 'float': 'left', 
        'display': 'inline-block','backgroundColor': 'rgb(250, 250, 250)'}),

    html.Div([

        dcc.Dropdown(
            id='related_param_2',
            options=[{'label': x, 'value':x} for x in suffixes_param],
            value=[suffixes[0]],
            multi=False
        ),

        dcc.Graph(
            id='related_graph_2',
            figure=dict()
        )

    ], style={'width': '49%', 'float': 'right', 
        'display': 'inline-block','backgroundColor': 'rgb(250, 250, 250)'}),

    html.Div([

        dcc.Dropdown(
            id='related_param_3',
            options=[{'label': x, 'value':x} for x in suffixes_param],
            value=[suffixes[0]],
            multi=False
        ),

        dcc.Graph(
            id='related_graph_3',
            figure=dict()
        )

    ], style={'width': '49%', 'float': 'left', 
        'display': 'inline-block', 'backgroundColor': 'rgb(250, 250, 250)'}),

    html.Div([

        dcc.Dropdown(
            id='related_param_4',
            options=[{'label': x, 'value':x} for x in suffixes_param],
            value=[suffixes[0]],
            multi=False
        ),

        dcc.Graph(
            id='related_graph_4',
            figure=dict()
        )

    ], style={'width': '49%', 'float': 'right', 
        'display': 'inline-block', 'backgroundColor': 'rgb(250, 250, 250)'})

]

app_layout.append(visualization_layout)
app_layout.append(analisys_layout)

app.layout = html.Div(id='main_layout', children=app_layout[0])




#############################################################################
############################## interactCode #################################
#############################################################################


def make_secondary_graph(related_param): #, main_graph, related_graph_1):
    data = []
    title = ""
    
    title = related_param
    df1 = df[related_param]
    df1 = resample(df1)
    data = [go.Scatter(x=df1.index, y=df1.values, name= related_param)]
    #print(main_graph)
    return dict( 
            data=data,
            layout=dict(
                paper_bgcolor='rgb(240, 240, 240)',
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
                        #main_graph,
                    type='date'
                )
            )
        )   



@app.callback(dash.dependencies.Output('main_layout', 'children'),
              [dash.dependencies.Input('display_mode', 'value')])
def change_mode(display_mode):
    return app_layout[display_mode]

@app.callback(dash.dependencies.Output('related_graph_1', 'figure'),
              [dash.dependencies.Input('related_param_1', 'value')]) #,
#              dash.dependencies.Input('main_graph', 'selectedData')],
#              [dash.dependencies.State('related_graph_1', 'figure')])
def make_secondary_graph_1(related_param): # ,main_graph, related_graph_1):
    return make_secondary_graph(related_param) #, main_graph, related_graph_1)

@app.callback(dash.dependencies.Output('related_graph_2', 'figure'),
              [dash.dependencies.Input('related_param_2', 'value')])
def make_secondary_graph_2(related_param):
    return make_secondary_graph(related_param)

@app.callback(dash.dependencies.Output('related_graph_3', 'figure'),
              [dash.dependencies.Input('related_param_3', 'value')])
def make_secondary_graph_3(related_param):
    return make_secondary_graph(related_param)

@app.callback(dash.dependencies.Output('related_graph_4', 'figure'),
              [dash.dependencies.Input('related_param_4', 'value')])
def make_secondary_graph_4(related_param):
    return make_secondary_graph(related_param)
        




#@app.callback(dash.dependencies.Output('year_slider', 'value'),
#              [dash.dependencies.Input('main_graph', 'selectedData')])
#def update_year_slider(count_graph_selected):
#
#    if count_graph_selected is None:
#        return [2006, 2016]
#    else:
#        nums = []
#        for point in count_graph_selected['points']:
#            nums.append(int(point['pointNumber']))
#
#        return [min(nums) + 2006, max(nums) + 2007]




#dropdown --> graph
@app.callback(dash.dependencies.Output('main_graph', 'figure'),
              [dash.dependencies.Input('feature_param', 'value')])
def make_main_figure(feature_param):
    data = []
    title=""
    for i in range(len(feature_param)):
        df1 = df[feature_param[i]]
        df1 = resample(df1)
        data.append(go.Scatter(x=df1.index, y=df1.values, name= feature_param[i]))
        title = title + "  " + feature_param[i]
    
    if (data == []):
        data = [go.Scatter(x=[], y=[])]    

    return dict( 
            data=data,
            layout=dict(
                #dragmode='select',
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






external_css = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
for css in external_css:
    app.css.append_css({ "external_url": css })


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)






