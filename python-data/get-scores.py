from pymongo import MongoClient
import sys
import time
import requests

sys.path.append('./services')
from scoreboard import getScoreboard

client = MongoClient('mongodb://localhost:27017/')
db = client['CFB']
games = db.games

for year in range(2002, 2018):
    for week in range(1,17):
        output = getScoreboard(year, week)
        if(len(output['events']) > 0):
            for event in output['events']:
                team1 = {
                  'date' : event["date"],
                  'year' : event["season"]["year"],
                  'gameID' : event["id"],
                  'neutralSite' : event["competitions"][0]["neutralSite"],
                  'conferenceCompetition' : event["competitions"][0]["conferenceCompetition"],
                  'teamID' : event["competitions"][0]["competitors"][0]["id"],
                  'opposingTeamID' : event["competitions"][0]["competitors"][1]["id"],
                  'teamAbbr' : event["competitions"][0]["competitors"][0]["team"]["abbreviation"],
                  'homeAway' : event["competitions"][0]["competitors"][0]["homeAway"],
                  'pointsFor' : event["competitions"][0]["competitors"][0]["score"],
                  'pointsAgainst' : event["competitions"][0]["competitors"][1]["score"]
                }
                games.insert_one(team1).inserted_id

                team2 = {
                  'date' : event["date"],
                  'year' : event["season"]["year"],
                  'gameID' : event["id"],
                  'neutralSite' : event["competitions"][0]["neutralSite"],
                  'conferenceCompetition' : event["competitions"][0]["conferenceCompetition"],
                  'teamID' : event["competitions"][0]["competitors"][1]["id"],
                  'opposingTeamID' : event["competitions"][0]["competitors"][0]["id"],
                  'teamAbbr' : event["competitions"][0]["competitors"][1]["team"]["abbreviation"],
                  'homeAway' : event["competitions"][0]["competitors"][1]["homeAway"],
                  'pointsFor' : event["competitions"][0]["competitors"][1]["score"],
                  'pointsAgainst' : event["competitions"][0]["competitors"][0]["score"]
                }
                games.insert_one(team2).inserted_id
        time.sleep(2)
