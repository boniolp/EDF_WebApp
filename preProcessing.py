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
from observation import *
from interval import *
from tools import *
from constants import *


#############################################################################
############################## import the data ##############################
#############################################################################

app = dash.Dash()
app.config.supress_callback_exceptions=True
#We need to do that, because we want to define a multi page webapp using callback 
#related to a specific page with no influence in the others. In order to do that,
#we need to be able to define some callback before the final layout that is not 
#static but can be modify dinamicly

colors = {
    'background': '#111111',
    'text': '#000000'
}

reactor_site = "A1" #[site+tranche for site in ["A","B","C","D","E","F","G","H"] for tranche in ["1","2"]] + ["B3","B4","F3","F4"]

suffixes_deb = [
"DEB1-1","DEB1-2",#"DEB1-3","DEB1-4", # Débit de fuite au joint 1 (Gamme Large)
#"DEB2-1","DEB2-2",#"DEB2-3","DEB2-4", # Débit de fuite au joint 1 (Gamme Étroite)
#"DEB3-1","DEB3-2",#"DEB3-3","DEB3-4","DEB3-5", # Débit d'injection au joint
]

suffixes_param = [
"PUI-",  # Puissance thermique moyenne
"PRE-",  # Pression
"TEM1-", # Température ligne d'injection aux joints (en * Celsius) ### A rapprocher de DEB3
#"TEM2-", # Température fuites joint 1
#"TEM3-1",#"TEM3-2","TEM3-3","TEM3-4",# Température eau joint 1 - 051PO ### A rapprocher de DEB1 DEB2
"VIT-1",#"VIT-2","VIT-3","VIT-4"# Vitesse de rotation
]

suffixes = []
suffixes = suffixes_deb + suffixes_param

PATH = "../Data/"
obs = Observation(PATH,reactor_site,suffixes,verbose=0,ignore_keys=deb2)
df = obs.full_concatenated_df
df_full = df["DEB1-1"]

def resample(data):
    return data.resample('1D',label='right').median()[0:300000].copy()

df1 = resample(df_full)