import requests

def getScoreboard(year, week, groups = 80, seasontype = 2):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}
    url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
    queryParams = {
        'dates': year,
        'week': week,
        'groups': groups,
        'seasontype': seasontype,
        'limit': 900}
    response = requests.get(url, params=queryParams, headers=headers)
    return response.json()

def getConferences():
    url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard/conferences'
    response = requests.get(url)
    return response.json()
