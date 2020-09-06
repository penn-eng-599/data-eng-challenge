#!/usr/bin/env python

import os
import pandas as pd
import pprint
import sys
from datetime import datetime

sys.path.append(os.path.join(sys.path[0], "..", ".."))
from nhldata.app import NHLApi

nhl_api = NHLApi()

# Given game_pk we are getting information on all players
game_pk = "2019030055"
boxscore_data = nhl_api.boxscore(game_pk)

home_players = boxscore_data["teams"]["home"]["players"]
away_players = boxscore_data["teams"]["away"]["players"]

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1].lower()] = x

    flatten(y, "player_")
    return out

players = []
for side in ["home", "away"]:
    all_players = boxscore_data["teams"][side]["players"]
    for key, player_data in all_players.items():
        result = flatten_json(player_data)
        result["side"] = side
        players.append(result)

#pprint.pprint(players)
df = pd.DataFrame(players)
with pd.option_context(
    'display.max_rows', None,
    'display.max_columns', None
):
    #print(df)
    print(df.dtypes)
    #print(df["side"])
print(df.shape)

