# -*- coding: utf-8 -*-
"""
Created on Tue May 24 10:45:39 2022

@author: K579641
"""
import subprocess
import os

import pandas as pd

import requests
from bs4 import BeautifulSoup
import json

POP_GER =  83240000
POP_GRE =  10720000
POP_NOR =   5379000

def relative_GER (x):
    return x/POP_GER

def relative_GRE (x):
    return x/POP_GRE

def relative_NOR (x):
    return x/POP_NOR

#%%    Update Data
'''
git_pull = subprocess.Popen( "/usr/bin/git pull" , 
                     cwd = os.path.dirname( '../data/raw/COVID-19/' ), 
                     shell = True, 
                     stdout = subprocess.PIPE, 
                     stderr = subprocess.PIPE )
(out, error) = git_pull.communicate()


print("Error : " + str(error)) 
print("out : " + str(out))

'''
#%% Fixed Population data



#%%   Import csv in Pandas Dataframe

data_path='./COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
pd_raw=pd.read_csv(data_path)
pd_raw.head()

#%% Do some Data preprocessing
#I want to drop everything that is not 

df = pd_raw.drop(["Province/State","Lat","Long"], axis=1)
df = df.transpose()
df.columns = list(df.loc["Country/Region"])
df = df.drop(["Country/Region"], axis=0)

def calculate_relative_GER(row):
    return int(row) / POP_GER

df["Germany"] = df["Germany"].apply( calculate_relative_GER )

def calculate_relative_GRE(row):
    return int(row) / POP_GRE

df["Greece"] = df["Greece"].apply( calculate_relative_GRE )

def calculate_relative_NOR(row):
    return int(row) / POP_NOR

df["Norway"] = df["Norway"].apply( calculate_relative_NOR )


#%%Plot Data in Plotly

import plotly.express as px

fig = px.line(df[["Germany","Greece","Norway"]], labels={"index":"time", 
                              "value":"Relative number of cases"},
                                  title="Covid Cases" , template="plotly_dark")

fig.write_html("Covid_Ger_Gre_Nor.html")