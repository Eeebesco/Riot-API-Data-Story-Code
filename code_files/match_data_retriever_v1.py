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
API_KEY = "RGAPI-c7e959de-6cca-45c1-aa4c-bab67fa69109"
HEADERS = {"X-Riot-Token": API_KEY}

#use the appropiate ids here, you can also get more than 20 results if you want.
match_ids = [
    'EUW1_7819677840', 'EUW1_7818677110', 'EUW1_7818600564', 'EUW1_7818218842', 'EUW1_7818164240', 'EUW1_7818124228', 'EUW1_7818089785', 'EUW1_7817606828', 'EUW1_7816908562', 'EUW1_7816450846', 'EUW1_7816412283', 'EUW1_7816361498', 'EUW1_7815511098', 'EUW1_7815470886', 'EUW1_7815405287', 'EUW1_7815305964', 'EUW1_7815275930', 'EUW1_7815219984', 'EUW1_7815083274', 'EUW1_7815038504'
     ]

# change if needed. 'europe', 'americas', 'asia'
routing_region = "europe"

rows = []

for match_id in match_ids:
    url = f"https://{routing_region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        continue

    data = response.json()

    # Match-level info
    game_info = data["info"]
    game_duration = game_info["gameDuration"]
    game_mode = game_info["gameMode"]

    # Loop through all 10 players in the match
    for player in game_info["participants"]:
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
            "all_in_pings" : player["allInPings"],
            "assist_me_pings" : player["assistMePings"],
            "command_pings" : player["commandPings"],
            "enemy_missing_pings" : player["enemyMissingPings"],
            "enemy_vision_pings" : player["enemyVisionPings"],
            "hold_pings" : player["holdPings"],
            "get_back_pings" : player["getBackPings"],
            "need_vision_pings" : player["needVisionPings"],
            "on_my_way_pings" : player["onMyWayPings"],
            "push_pings" : player["pushPings"],
            "sight_wards_bought" : player["sightWardsBoughtInGame"],
            "detector_wards_placed" : player["detectorWardsPlaced"],
            "vision_score" : player["visionScore"],
            "vision_cleared_pings" : player["visionClearedPings"],
            "vision_wards_bought_in_game" : player["visionWardsBoughtInGame"],
            "wards_placed" : player["wardsPlaced"],
            "wards_killed" : player["wardsKilled"]
        }
        rows.append(row)

    time.sleep(1.2)  # avoid rate limits


df = pd.DataFrame(rows)

# Save to CSV, change name as needed
df.to_csv("second_match_data.csv", index=False)

print("Saved to match_data.csv")
