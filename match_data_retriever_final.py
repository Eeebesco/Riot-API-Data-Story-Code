'''
This code retrieves specified data from the last 20 matches of a player.
The API_KEY variable should be replaced with your own Riot API key every
time you get a new one, and the match_ids variable should be replaced with the
match ids of the matches you want to get data for, but the rest of the code runs
without modification.  The data is saved to a CSV file called 
"[player-name]_match_data" which can be then accessed separately.
'''

import requests
import pandas as pd
import time

#put new API key here
API_KEY = "API KEY HERE"
HEADERS = {"X-Riot-Token": API_KEY}

#use the appropiate ids here, you can also get more than 20 results if you want.
match_ids = ['MATCH IDS HERE']

# change if needed. 'europe', 'americas', 'asia'
routing_region = "REGION HERE"

#Change per person
target_name = "PLAYER NAME HERE"

rows = []

for match_id in match_ids:
    url = f"https://{routing_region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        continue

    data = response.json()
    game_info = data["info"]

    player = next(
        (p for p in game_info["participants"] if p["riotIdGameName"] == target_name),
        None
    )

    if player is None:
        continue

    row = {
        "match_id": match_id,
        "puuid": player["puuid"],
        "name": player["riotIdGameName"],
        "champion": player["championName"],
        "kills": player["kills"],
        "deaths": player["deaths"],
        "assists": player["assists"],
        "lane": player["lane"],
        "win": player["win"],
        "gold": player["goldEarned"],
        "minions_killed": player["totalMinionsKilled"],
        "total_ally_jungle_minions_killed": player["totalAllyJungleMinionsKilled"],
        "total_enemy_jungle_minions_killed": player["totalEnemyJungleMinionsKilled"],
        "all_in_pings": player["allInPings"],
        "assist_me_pings": player["assistMePings"],
        "command_pings": player["commandPings"],
        "enemy_missing_pings": player["enemyMissingPings"],
        "enemy_vision_pings": player["enemyVisionPings"],
        "hold_pings": player["holdPings"],
        "get_back_pings": player["getBackPings"],
        "need_vision_pings": player["needVisionPings"],
        "on_my_way_pings": player["onMyWayPings"],
        "push_pings": player["pushPings"],
        "sight_wards_bought": player["sightWardsBoughtInGame"],
        "detector_wards_placed": player["detectorWardsPlaced"],
        "vision_score": player["visionScore"],
        "vision_cleared_pings": player["visionClearedPings"],
        "vision_wards_bought_in_game": player["visionWardsBoughtInGame"],
        "wards_placed": player["wardsPlaced"],
        "wards_killed": player["wardsKilled"]
    }

    rows.append(row)

    time.sleep(1.2)

df = pd.DataFrame(rows)
filename = f"{target_name}_match_data.csv"
df.to_csv(filename, index=False)

print(f"Saved to {filename}")