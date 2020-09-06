#!/usr/bin/env python

import os
import pandas as pd
import pprint
import sys
from datetime import datetime

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))
from nhldata.app import NHLApi

nhl_api = NHLApi()

start_date = datetime(2018, 8, 1)
end_date = datetime(2019, 7, 31)

sched_data = nhl_api.schedule(start_date, end_date)

game_pks = []
counter = 0
for sched in sched_data["dates"]:
    sched_date_name = "schedule_date:"
    sched_date = sched["date"]
    #pprint.pprint(sched.keys())
    for game in sched["games"]:
        game_date_name = "game_date:"
        game_date = game["gameDate"]

        game_pk_name = "game_pk:"
        game_pk = str(game["gamePk"])

        season_name = "season:"
        season = game["season"]

        print(f"----------{counter}----------")
        print(f"{sched_date_name:>15} {sched_date}")
        print(f"{game_date_name:>15} {game_date}")
        print(f"{game_pk_name:>15} {game_pk}")
        print(f"{season_name:>15} {season}")

        print("status:")
        pprint.pprint(game["status"])
        print()

        counter += 1
        game_season = game_pk[0:4]
        game_type = game_pk[4:6]
        game_number = game_pk[6:10]

        game_pks.append(
            {
                "pk": game_pk,
                "season": game_season,
                "type": game_type,
                "number": game_number,
            }
        )


print(counter)
sorted_game_pks = sorted(game_pks, key=lambda x: x['pk'])
for game in sorted_game_pks:
    g_season = game['season']
    g_type = game['type']
    g_number = game['number']
    print(f"{g_season} {g_type} {g_number}")

# NOTE there is a difference from schedule.dates.date and games.gameDate it
# seems like the former is schedule day date and the latter is game date
