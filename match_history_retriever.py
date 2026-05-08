'''
This code retrieves the game ids of the last 20 games of a player using their
puuid.  The API_KEY variable should be replaced with your own Riot API key every
time you get a new one, and the puuid variable should be replaced with the puuid
of the player you want to get match history for, but the rest of the code runs
without modification.
'''
import requests

#put new API key here
API_KEY = "PUT YOUR KEY HERE"
HEADERS = {"X-Riot-Token": API_KEY}

#put the puuid of the player you want to get match history for here
puuid = "PUT PUUID HERE"

# change if needed. 'europe', 'americas', 'asia'
routing_region = "PUT REGION HERE"  

url = f"https://{routing_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count=20"

response = requests.get(url, headers=HEADERS)

if response.status_code == 200:
    matches = response.json()
    print(matches)
else:
    print(response.status_code, response.text)