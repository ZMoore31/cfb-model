import json
import sys
import time
import requests
import pandas as pd
import numpy as np
import mysql.connector
import os
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy import create_engine

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

engine = create_engine('mysql+mysqlconnector://'+DATABASE_USER+':'+DATABASE_PASSWORD+'@127.0.0.1/CFB', echo=False)

sys.path.append('./services')
from team import getTeamInfo

team_list = list(pd.read_sql('Select distinct teamID from ratings', engine)['teamID'])

def store_team_info(id):
    info = getTeamInfo(id)
    return pd.DataFrame.from_dict({
        'teamID': [info['team']['id']],
        'schoolName': [info['team']['location']],
        'teamName': [info['team']['name']],
        'abbreviation': [info['team']['abbreviation']],
        'displayName': [info['team']['displayName']],
        'shortDisplayName': [info['team']['shortDisplayName']],
        'color': [info['team']['color']],
        'altColor': [info['team']['alternateColor']] if 'alternateColor' in info['team'] else [''] ,
        'logo': [info['team']['logos'][0]['href']] if 'logos' in info['team'] else [''] ,
    })

for team in team_list:
    print(team)
    store_team_info(team).to_sql('team_info', con=engine, if_exists='append')
    time.sleep(1)
