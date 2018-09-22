from pymongo import MongoClient
import json
import sys
import time
import requests
import pandas as pd
import numpy as np

sys.path.append('./services')
from team import getTeamInfo

client = MongoClient('mongodb://localhost:27017/')
db = client['CFB']
ratings = db.ratings

df =  pd.DataFrame(list(ratings.find({})))
df = list(pd.unique(df['teamID']))
print(df)

def calc_massey(year):
    df =  pd.DataFrame(list(games.find({'year': year})))
    df['pointsDiff'] = pd.to_numeric(df['pointsFor']) - pd.to_numeric(df['pointsAgainst'])
    totalPointsDiff = df.groupby(['teamID']).sum()['pointsDiff']
    totalPointsDiff[-1] = 0
    gameCount = df.groupby(['teamID']).size()
    teamList = pd.unique(df['teamID'])
    numberTeams = len(teamList)
    identity = np.identity(numberTeams)
    T = gameCount.values * identity
    T = pd.DataFrame(T)
    T.columns = gameCount.index.values
    T.index = gameCount.index.values
    gameCombos = pd.concat([pd.DataFrame(list(df.groupby(['teamID','opposingTeamID']).size().index.values)),pd.DataFrame(df.groupby(['teamID','opposingTeamID']).size()).reset_index(drop=True)], axis=1)
    for game in gameCombos.values:
        T[game[0]][game[1]] = -game[2]
    T.iloc[-1] = 1
    ratings = pd.DataFrame(np.linalg.inv(T.values).dot(totalPointsDiff.values))
    ratings.index = gameCount.index.values
    ratings.columns = ['Rating']
    ratings['Year'] = year
    ratings['teamID'] = gameCount.index.values
    return ratings[['teamID','Year','Rating']]
