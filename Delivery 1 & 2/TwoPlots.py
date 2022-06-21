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

#%% This is the Quick and dirty Part (I know)

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


#%%   Import csv in Pandas Dataframe

data_path='./COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
pd_raw=pd.read_csv(data_path)
pd_raw.head()


data_path_2='./owid-covid-data.csv'
vac=pd.read_csv(data_path_2)
vac.head()

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

#%%

#Different type of Dataset - Could not find Vaccination Rate in the given DataSet
#Used Dataset can be found in Git Repo
#Source of Data: https://ourworldindata.org/covid-vaccinations

df_vac_ger = vac.loc[vac['location'] == 'Germany']
df_vac_gre = vac.loc[vac['location'] == 'Greece']
df_vac_nor = vac.loc[vac['location'] == 'Norway']

df_vac_ger.index = df_vac_ger["date"]
df_vac_gre.index = df_vac_gre["date"] 
df_vac_nor.index = df_vac_nor["date"]

df_vac_ger = df_vac_ger["people_fully_vaccinated_per_hundred"]
df_vac_gre = df_vac_gre["people_fully_vaccinated_per_hundred"]
df_vac_nor = df_vac_nor["people_fully_vaccinated_per_hundred"]

df2 = pd.concat([df_vac_ger, df_vac_gre,df_vac_nor], axis=1)
df2.columns = ["Germany","Greece","Norway"]



#%%Plot Data in Plotly

import plotly.express as px

fig1 = px.line(df[["Germany","Greece","Norway"]], labels={"index":"time", 
                              "value":"Relative number of cases"},
                                  title="Covid Cases" , template="plotly_dark")

fig1.write_html("Covid_Ger_Gre_Nor.html")

fig2 = px.line(df2[["Germany","Greece","Norway"]], labels={"index":"time", 
                              "value":"Percantage of fully vaccinated People"},
                                  title="Vaccination Rate" , template="plotly_dark")

fig2.write_html("Vacc_Ger_Gre_Nor.html")