import requests

def getTeamInfo(id):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}
    url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/{id}'.format(id=id)

    response = requests.get(url, headers=headers)
    return response.json()
