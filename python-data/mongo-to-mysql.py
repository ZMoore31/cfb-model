from pymongo import MongoClient
import json
import sys
import time
import requests
import pandas as pd
import mysql.connector
# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy import create_engine


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

engine = create_engine('mysql+mysqlconnector://'+DATABASE_USER+':'+DATABASE_PASSWORD+'@127.0.0.1/CFB', echo=False)

client = MongoClient('mongodb://localhost:27017/')
db = client['CFB']
games = db.games
ratings = db.ratings
recruitings = db.recruitings

game_data =  pd.DataFrame(list(games.find({})))
game_data = game_data.drop('_id', axis=1)
rating_data =  pd.DataFrame(list(ratings.find({})))
rating_data = rating_data.drop('_id', axis=1)
recruiting_data =  pd.DataFrame(list(recruitings.find({})))
recruiting_data = recruiting_data.drop('_id', axis=1)


# game_data.to_sql('games', con=engine)
rating_data.to_sql('ratings', con=engine)
recruiting_data.to_sql('recruiting_rankings', con=engine)
