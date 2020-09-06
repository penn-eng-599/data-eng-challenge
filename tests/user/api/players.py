#!/usr/bin/env python

import os
import pandas as pd
import pprint
import sys
from datetime import datetime

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))
from nhldata.app import NHLApi

nhl_api = NHLApi()

# Given game_pk we are getting information on all players
game_pk = "2019030055"
boxscore_data = nhl_api.boxscore(game_pk)

home_players = boxscore_data["teams"]["home"]["players"]
away_players = boxscore_data["teams"]["away"]["players"]


for key, player_data in home_players.items():
    print(key)
    pprint.pprint(player_data)

print(len(home_players))
#pprint.pprint(home_players)
